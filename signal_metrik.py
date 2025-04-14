import yaml
import numpy as np
import time
import h5py
import hdf5plugin  # Needed for HDF5 compression plugins
import matplotlib.pyplot as plt
import sys
import csv
import argparse
import copy

# ----------------------------- Argument Parsing -----------------------------

def parse_arguments():
    """
    Parse command-line arguments for signal-to-noise calculation.
    """
    parser = argparse.ArgumentParser(description="Signal-to-noise calculation.")
    parser.add_argument('-roi_file', default="rois.yaml", help="Path to ROI file.")
    parser.add_argument('-output_file', default="metric_dump.csv", help="Output CSV for metrics.")
    parser.add_argument('-event_file', type=str, help="Event file (.raw or .h5).")
    parser.add_argument('-process', type=int, default=-1, help="Process index for logging.")
    args = parser.parse_args()
    return args.roi_file, args.event_file, args.output_file, args.process

# ----------------------------- ROI Loading ----------------------------------

def load_rois(roi_file):
    """Load ROI definitions from YAML file."""
    with open(roi_file, "r") as file:
        return yaml.safe_load(file)

# ----------------------------- Event Matrix Loading -------------------------

def load_event_matrix(event_file):
    """Load event matrix depending on file extension."""
    if event_file.endswith(".raw"):
        print("Raw file detected")
        return load_raw_event_matrix(event_file).T
    else:
        print("HDF5 file detected")
        return load_hdf5_event_matrix(event_file).T

def load_hdf5_event_matrix(event_file):
    with h5py.File(event_file, "r") as file:
        width, height = file.attrs["width"], file.attrs["height"]
        event_matrix = np.zeros((width, height), dtype=np.int32)
        
        max_index = min(len(file["ms_to_idx"]) - 1, 4000)
        x = file["events"]["x"][:file["ms_to_idx"][max_index]]
        y = file["events"]["y"][:file["ms_to_idx"][max_index]]
        scale = max(4000 / len(file["ms_to_idx"]), 1)
        
        np.add.at(event_matrix, (x, y), scale)
        
    return event_matrix

def load_raw_event_matrix(event_file):
    """
    Placeholder for RAW file reading using RawReader.
    """
    # Uncomment if using RawReader from Metavision SDK
    # from metavision_core.event_io.raw_reader import RawReader
    # raw_stream = RawReader(event_file)
    # event_matrix = np.zeros((raw_stream.width, raw_stream.height), dtype=np.int32)
    # while not raw_stream.is_done():
    #     events = raw_stream.load_n_events(1000000)
    #     np.add.at(event_matrix, (events["x"], events["y"]), 1)
    # return event_matrix
    raise NotImplementedError("RAW file reading not implemented in this example.")

# ----------------------------- Hot Pixel Logic ------------------------------

def get_hot_pixel_matrix(size):
    """Return mask matrix with known hot pixels removed."""
    bad_pixels = [[1, 115], [3, 624], [9, 768], ...]  # abbreviated for clarity
    mask = np.ones(size, dtype=bool)
    for x, y in bad_pixels:
        mask[x, y] = False
    return mask

# ----------------------------- Main Metric Calculation ----------------------

def calculate_signal_to_noise(roi_file, event_file, process):
    print(f"Processing: {event_file}")
    t_start = time.time()

    # Load data
    rois = load_rois(roi_file)
    event_matrix = load_event_matrix(event_file)
    hot_pixel_mask = get_hot_pixel_matrix(event_matrix.shape)

    roi_positions = assign_grid_positions(rois)
    event_counts = np.zeros(len(rois) + 1)  # Last index for background

    # ROI and noise masking
    y_idx, x_idx = np.meshgrid(np.arange(event_matrix.shape[0]), np.arange(event_matrix.shape[1]), indexing='ij')
    background_mask = np.ones_like(event_matrix, dtype=bool)

    for i, (x, y, r_sig, r_noise, _) in enumerate(rois):
        roi_mask = (x_idx - x)**2 + (y_idx - y)**2 <= r_sig**2
        noise_mask = (x_idx - x)**2 + (y_idx - y)**2 <= r_noise**2
        event_counts[i] = np.sum(event_matrix[roi_mask & hot_pixel_mask])
        background_mask[noise_mask & hot_pixel_mask] = False

    # Background estimation
    event_counts[-1] = np.sum(event_matrix[background_mask & hot_pixel_mask])
    noise_area = event_matrix.size - sum(np.pi * roi[3]**2 for roi in rois)

    # Normalize by area
    signal_areas = [np.pi * roi[2]**2 for roi in rois]
    event_counts[:-1] /= signal_areas
    event_counts[-1] /= noise_area

    # Final signal-to-noise computation
    signal_to_noise = np.maximum(event_counts[:-1] - event_counts[-1], 0) / max(1, event_counts[-1])
    signal_to_noise /= [roi[4] for roi in rois]

    print(f"Process {process}: SNR -> {[round(val, 2) for val in signal_to_noise]}")
    return [signal_to_noise[i] for i in roi_positions]

# ----------------------------- Helper Functions -----------------------------

def assign_grid_positions(rois):
    """Assign ROIs to 4x4 grid positions based on proximity."""
    x_vals, y_vals = [], []
    for x, y, *_ in rois:
        if not any(abs(x - xv) < 100 for xv in x_vals):
            x_vals.append(x)
        if not any(abs(y - yv) < 100 for yv in y_vals):
            y_vals.append(y)
    x_vals.sort()
    y_vals.sort()
    return [next(i for i, xv in enumerate(x_vals) if abs(x - xv) < 100) +
            next(j for j, yv in enumerate(y_vals) if abs(y - yv) < 100) * 4 for x, y, *_ in rois]

def save_results(output_file, signal_to_noise, _):
    """Save SNR list to CSV."""
    with open(output_file, "w", newline='') as file:
        csv.writer(file).writerow(signal_to_noise)

# ----------------------------- Main Execution -------------------------------

def main():
    roi_file, event_file, output_file, process = parse_arguments()
    snr_values = calculate_signal_to_noise(roi_file, event_file, process)
    save_results(output_file, snr_values, event_file)

if __name__ == "__main__":
    main()
