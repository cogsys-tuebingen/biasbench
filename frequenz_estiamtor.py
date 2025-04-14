import os
import csv
import yaml
import time
import h5py
import random
import hdf5plugin
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

from tqdm import tqdm
from scipy.optimize import curve_fit
from hdf5plugin import Blosc  # Ensures compression support
from argparse import ArgumentParser


# ─────────────────────────────────────────────────────────────
#                         Data Loaders
# ─────────────────────────────────────────────────────────────

def load_hdf5_data(file_path):
    with h5py.File(file_path, 'r') as f:
        t = np.array(f['events/t'])
        p = np.array(f['events/p'])
        x = np.array(f['events/x'])
        y = np.array(f['events/y'])
        ms_to_idx = np.array(f['ms_to_idx'])
    return t, p, x, y, ms_to_idx


def load_rois_from_yaml(roi_file):
    with open(roi_file, "r") as file:
        return yaml.safe_load(file)


# ─────────────────────────────────────────────────────────────
#                    Signal Processing Utils
# ─────────────────────────────────────────────────────────────

def cos_func(x, A, B, C, D, E):
    return A * np.cos(B * (x + C)) + D * x + E


def extract_frequency(rois, file_path, periods=10, slices=10):
    t, p, x, y, ms_to_idx = load_hdf5_data(file_path)
    total_events = len(p)
    pos_events = np.sum(p)
    neg_events = total_events - pos_events
    total_time_sec = t[-1] / 1_000_000

    frequencies = []
    freq_errors = []

    for roi in rois:
        x0, y0, r_signal, r_noise, freq_guess = roi

        # Time window
        start_idx = min(1000, len(ms_to_idx) // 2)
        time_span = min(len(ms_to_idx) - start_idx - 1,
                        max(1, int(1000 / freq_guess * periods)))
        dt = time_span / (slices * periods)
        t_min = ms_to_idx[start_idx]
        t_max = ms_to_idx[start_idx + time_span]

        x_roi = x[t_min:t_max]
        y_roi = y[t_min:t_max]
        p_roi = p[t_min:t_max]
        t_roi = t[t_min:t_max]

        # Apply circular ROI mask
        mask = (x_roi - x0) ** 2 + (y_roi - y0) ** 2 <= r_signal ** 2
        if np.sum(mask) <= 5:
            frequencies.append(0)
            freq_errors.append(0)
            continue

        p_filtered = p_roi[mask]
        t_filtered = t_roi[mask]

        # Bin and compute signal
        signal_times = [t_filtered[0]]
        signal_values = [0]

        for i in range(len(p_filtered)):
            if t_filtered[i] > signal_times[-1] + dt * 1000:
                signal_times.append(t_filtered[i])
                signal_values.append(0)
            signal_values[-1] += 2 * p_filtered[i] - 1

        x_fit = np.asarray(signal_times) / 1_000_000
        y_fit = np.asarray(signal_values)

        try:
            p0 = [np.max(y_fit), freq_guess * 2 * np.pi, x_fit[np.argmax(y_fit)], 0, np.mean(y_fit)]
            params, cov = curve_fit(cos_func, x_fit, y_fit, p0=p0)
            frequencies.append(params[1] / (2 * np.pi))
            freq_errors.append(np.sqrt(cov[1][1]) if cov.shape == (5, 5) else 0)
        except Exception:
            frequencies.append(0)
            freq_errors.append(0)

    return frequencies, freq_errors, pos_events, neg_events, total_time_sec


def prepare_row(freqs, freq_errors, pos, neg, time_sec, file_path):
    meta = file_path.split("/")[-1].split(".")[0].split("_")
    meta += [pos, neg, time_sec]

    for f, fe in zip(freqs, freq_errors):
        meta.append(f)
        meta.append(fe)

    return meta


# ─────────────────────────────────────────────────────────────
#                        Parallel Workers
# ─────────────────────────────────────────────────────────────

def split_into_chunks(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def process_file_batch(file_list, rois, proc_id):
    data = []
    for idx, file_path in enumerate(tqdm(file_list, desc=f"Process {proc_id}", position=proc_id)):
        result = extract_frequency(rois, file_path)
        row = prepare_row(*result, file_path)
        data.append(row)

        if len(data) % 10 == 0:
            with open(f"tmp_save{proc_id}.tmp.csv", "a") as tmp_file:
                writer = csv.writer(tmp_file)
                writer.writerows(data[-10:])

    return data


# ─────────────────────────────────────────────────────────────
#                        Main Routine
# ─────────────────────────────────────────────────────────────

def generate_readme(rois, output_csv_path):
    readme_path = os.path.join(os.path.dirname(output_csv_path), "readme.txt")
    with open(readme_path, "w") as f:
        f.write(f"CSV File: {os.path.basename(output_csv_path)}\n\n")
        f.write("Format:\n")
        f.write("bias_diff_on, bias_diff_off, bias_hpf, bias_fo, bias_refr, pos_events, neg_events, total_time, f1, f1_err, ..., f16, f16_err\n\n")
        f.write("ROI Descriptions:\n")
        for i, roi in enumerate(rois):
            f.write(f"ROI {i}: x={roi[0]}, y={roi[1]}, r_signal={roi[2]}, r_noise={roi[3]}, norm={roi[4]}\n")


def load_completed_files():
    completed = set()
    for i in range(8):
        try:
            with open(f"tmp_save{i}.tmp.csv", "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) > 5:
                        base = str(row[0])
                        for j in range(4):
                            base += "_" + str(row[j + 1])
                        completed.add(base + ".h5")
        except FileNotFoundError:
            continue
    return completed


def run_analysis(input_folder, output_csv, roi_file):
    rois = load_rois_from_yaml(roi_file)
    completed_files = load_completed_files()

    all_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder)
                 if f.endswith(".h5") and f not in completed_files and f.find("tmp")==-1]

    print(f"Found {len(all_files)} files to process (skipping {len(completed_files)} already processed).")

    num_workers = min(8, mp.cpu_count() - 1)
    chunks = split_into_chunks(all_files, num_workers)

    with mp.Pool(num_workers) as pool, open(output_csv, "a", newline='') as f:
        writer = csv.writer(f)
        tasks = [pool.apply_async(process_file_batch, args=(chunk, rois, i)) for i, chunk in enumerate(chunks)]

        for result in tasks:
            for row in result.get():
                writer.writerow(row)

    generate_readme(rois, output_csv)


# ─────────────────────────────────────────────────────────────
#                         Entry Point
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = ArgumentParser(description="Frequency extraction from HDF5 event data.")
    parser.add_argument("--input_folder", help="Path to the folder containing .h5 files.")
    parser.add_argument("--output_csv", help="Path to the output CSV file.")
    parser.add_argument("--roi_file", help="YAML file containing ROI definitions.")

    args = parser.parse_args()
    run_analysis(args.input_folder, args.output_csv, args.roi_file)
