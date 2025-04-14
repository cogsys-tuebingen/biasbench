import os
import sys
import gc
import subprocess
import time
from metavision_core.event_io.raw_reader import RawReader
import argparse
import yaml
import multiprocessing as mp
from tqdm import tqdm

def parse_arguments():
    """
    Parses command-line arguments for sensor type, biases, and input-output folder pairs.
    Ensures that the number of input-output folder pairs is even.
    """
    parser = argparse.ArgumentParser(description="Process sensor type and paired arguments.")
    
    # Optional arguments
    parser.add_argument("--sensor_type", type=str, help="Specify the sensor type", default="IMX636")
    parser.add_argument("--default_bias", type=str, help="Default bias used when no bias was detected", default="[0,0,0,0,0]")
    parser.add_argument("--bias_file_name", type=str, help="File containing biases", default="biases.yaml")
    parser.add_argument("--bias_from_name", type=bool, help="is the bias in the name", default=False)
    parser.add_argument("--processes", type=int, help="How many parralell processes to use", default=5)
    
    # Positional arguments: Accepts an arbitrary number of values as input-output pairs
    parser.add_argument("pairs", nargs="*", help="Pairs of values (input and output folder paths)")
    
    args = parser.parse_args()
    
    # Ensure pairs are valid (if an odd number is given, assume default output folder "hdf5" in last input folder)
    if len(args.pairs) % 2 != 0:
        args.pairs.append(os.path.join(args.pairs[-1], "hdf5"))
    
    # Convert the list into (input, output) pairs
    paired_values = list(zip(args.pairs[::2], args.pairs[1::2]))


    #creating default bias file:
    bias_files=[]
    for i in paired_values:
        bias_files.append(os.path.join(i[0],args.bias_file_name))
    return args.sensor_type, paired_values, args.default_bias,bias_files,args.bias_from_name,args.processes

def load_biases(file_path):
    """
    Load bias values from a text file.

    Args:
        file_path (str): Path to the biases file.

    Returns:
        list: A list of bias configurations.
    """
    """Load bias values from a YAML file."""
    with open(file_path, "r") as f:
        biases = yaml.safe_load(f)
    return_bias={}
    for entry in biases:
        return_bias.update({entry[0]:entry[1:]})
    return return_bias

def get_all_event_files(directory):
    """
    Retrieve all valid event files (.raw or .h5) from the given directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        list: List of filenames without extensions.
    """
    files = os.listdir(directory)
    return [
        file.split(".raw")[0].split(".h5")[0]
        for file in files
        if (".raw" in file or ".h5" in file) and "tmp" not in file
    ]

def create_data_format_file(path):
    """
    Creates a 'Data_format.txt' file in the specified directory if it doesn't already exist.
    The file describes the structure and contents of the HDF5 files generated.

    Args:
        path (str): Directory where the 'Data_format.txt' file will be created.
    """
    if "Data_format.txt" not in os.listdir(path):
        data_format_content = """HDF5 File
├── /events
│   ├── /p  (array of polarities)
│   ├── /t  (array of timestamps in microseconds)
│   ├── /x  (array of x-coordinates)
│   ├── /y  (array of y-coordinates)
├── /t_offset  (scalar value)
├── /ms_to_idx (array mapping ms to event indices)
├── /bias  (array of used biases)
├── /height (scalar, camera height)
├── /width (scalar, camera width)
├── /sensor (string, e.g., IMX636)""".split("\n")
        
        with open(os.path.join(path, "Data_format.txt"), "w") as file:
            file.writelines([line + "\n" for line in data_format_content])
        
        print("Data_format File created")

def convert_files(files, input_folder, output_folder, biases, sensor_type,proces):
    """
    Convert raw event files to HDF5 format using an external converter script.

    Args:
        files (list): List of file names to convert.
        input_folder (str): Path to the folder containing input files.
        output_folder (str): Path to the folder to save converted files.
        biases (list): List of bias configurations.
        sensor_type (str): Sensor type used for data taking.
    """
    create_data_format_file(output_folder)
    counter = 0
    start_time = time.time()
    if proces==0:
        pool = mp.Pool(processes=mp.cpu_count()-1)
    else:
        pool = mp.Pool(processes=proces)

    results=[]
    index=0
    for i, file in enumerate(files):
        print(f"Queuing {file}...")
        bias = biases[i] if i < len(biases) else biases[-1]
        results.append(pool.apply_async(run_supprocess, (
            "python3", "raw_to_hdf5.py",
            os.path.join(input_folder, file + ".raw"),
            os.path.join(output_folder, file + ".h5"),
            str(bias),
            sensor_type,
            str(i+1)
        )))
    for res in tqdm(results, desc="Converting files", unit="file"):
        res.get() 
    
    pool.close()
    pool.join()

    
    print(f"File conversion complete. Total time: {int(time.time() - start_time)} seconds")

def run_supprocess(*args):
    t0=time.time()
    command=[]
    for value in args:
        command.append(value)
    subprocess.run(command)
    #print(f"Finished converting {command[1]} in {round(time.time() - t0, 2)} seconds.\n")



def main():
    """
    Main function that handles batch conversion of raw event files to HDF5.
    Parses command-line arguments and iterates through all input-output folder pairs.
    """
    if len(sys.argv) < 2:
        print("Usage: python3 batch_raw_to_hdf5_converter.py [--sensor sensor_type] input_path [output_path]")
        sys.exit(1)
    
    sensor_type, destinations, default_bias,bias_files,bias_from_file ,processes = parse_arguments()
    
    counter=0
    for input_folder, output_folder in destinations:
        print(f"Sensor Type: {sensor_type}")
        print(f"Input folder: {input_folder}")
        print(f"Output folder: {output_folder}")
        
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        
        input_files = get_all_event_files(input_folder)
        input_files.sort()
        output_files = get_all_event_files(output_folder)
        files_to_convert = [file for file in input_files if file not in output_files]
        
        print(f"Starting conversion of {len(files_to_convert)} files...\n")
        if bias_from_file:
            biases=[]
            for filename in files_to_convert:
                if len(filename.split("_") )!=5:
                    biases.append([int(k) for k in default_bias.strip("[]").split(",")])
                else:
                    biases.append([int(k) for k in filename.split("_") ])
            print(biases)
        else:
            try:
                biases_dict = load_biases(bias_files[counter])
                biases=[]
                for filename in files_to_convert:
                    if filename in biases_dict:
                        biases.append(biases_dict[filename])
                    else:
                        biases.append([int(k) for k in default_bias.strip("[]").split(",")])

            except FileNotFoundError:
                biases = [[int(k) for k in default_bias.strip("[]").split(",")] for _ in range(len(files_to_convert))]
        counter+=1


        convert_files(files_to_convert, input_folder, output_folder, biases, sensor_type,processes)

if __name__ == "__main__":
    main()
