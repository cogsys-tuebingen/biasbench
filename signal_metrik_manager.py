import os
import subprocess
import multiprocessing as mp
import argparse
import sys
import time
import h5py
import hdf5plugin
import numpy as np
import csv


def parse_arguments():
    """
    Parses command-line arguments for sensor type, biases, and input-output folder pairs.
    Ensures that the number of input-output folder pairs is even.

    Returns:
        argparse.Namespace: Parsed arguments including roi_file, input_folder, and output_folder.
    """
    parser = argparse.ArgumentParser(description="Process sensor type and paired arguments.")
    parser.add_argument("-roi_file", type=str, help="File with ROIs", default="rois.yaml")
    parser.add_argument("-input_folder", type=str, help="Input folder with files", default="./")
    parser.add_argument("-output_folder", type=str, help="Output folder with files", default="./signal_metric/")
    return parser.parse_args()


def get_all_event_files(directory):
    """
    Retrieve all valid event files (.raw or .h5) from the given directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        list: List of base filenames without extensions.
    """
    files = os.listdir(directory)
    return [
        file.split(".raw")[0].split(".h5")[0]
        for file in files
        if (".h5" in file or ".raw" in file) and "tmp" not in file
    ]


def convert_files(files, input_folder, output_folder, args):
    """
    Convert raw event files to signal metrics using an external script via multiprocessing.

    Args:
        files (list): List of base filenames to convert.
        input_folder (str): Path to folder containing input files.
        output_folder (str): Path to save processed output.
        args (Namespace): Parsed command-line arguments.
    """
    counter = 0
    start_time = time.time()
    pool = mp.Pool(processes=mp.cpu_count() - 1)
    results = []

    for file in files:
        print(f"Looking at {file}...")
        if not os.path.exists(os.path.join(output_folder, file + ".csv")):
            results.append(pool.apply_async(run_supprocess, (
                "python3", "signal_metrik.py",
                "-roi_file", args.roi_file,
                "-output_file", os.path.join(output_folder, file + ".csv"),
                "-process", str(counter),
                "-event_file", os.path.join(input_folder, file + ".h5")
            )))
        else:
            print(f"Skipping file {file} (already exists).")
        counter += 1

    for res in results:
        res.get()

    pool.close()
    pool.join()

    print(f"Signal metric generation complete. Total time: {int(time.time() - start_time)} seconds")


def run_supprocess(*args):
    """
    Runs a subprocess with the given arguments and measures execution time.

    Args:
        *args: Command-line arguments to pass to subprocess.
    """
    t0 = time.time()
    command = list(args)
    subprocess.run(command)
    print(f"Finished metric calculation for {command[1]} in {round(time.time() - t0, 2)} seconds.\n")


def combine(folder):
    """
    Combines all generated CSV files into one summary CSV file.

    Args:
        folder (str): Folder containing individual signal CSVs.
    """
    files = [
        f for f in os.listdir(folder)
        if f.endswith(".csv") and "tmp" not in f and "total_signals" not in f
    ]
    counter = 0
    start_time = time.time()

    with open(os.path.join(folder, "total_signals.csv"), mode='w', newline='') as file:
        writer = csv.writer(file)
        for csfile in files:
            if counter % 100 == 0:
                print(f"Merged {counter} files in {round(time.time() - start_time, 2)} seconds.")
            with open(os.path.join(folder, csfile), mode='r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:
                        for part in csfile.split(".")[0].split("_"):
                            row.append(int(part))
                        writer.writerow(row)
            counter += 1

    print(f"Finished merging {len(files)} files.")


def main():
    """
    Main function to manage the full pipeline:
    - Parse command-line arguments
    - Identify and convert event files
    - Merge all outputs into one CSV
    """
    if len(sys.argv) < 2:
        print("Usage: python3 signal_metric_manager.py -roi_file rois.yaml -input_folder ./events")
        sys.exit(1)

    args = parse_arguments()

    print(f"Input folder: {args.input_folder}")
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder, exist_ok=True)

    input_files = get_all_event_files(args.input_folder)
    convert_files(input_files, args.input_folder, args.output_folder, args)

    print("Finished calculating metrics. Now combining...")
    combine(args.output_folder)


if __name__ == "__main__":
    main()