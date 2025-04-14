import yaml
import numpy as np
import h5py
import hdf5plugin
from metavision_core.event_io.raw_reader import RawReader
import matplotlib.pyplot as plt
import sys
import argparse
import tkinter as tk
from tkinter import simpledialog

def get_event_matrix(event_file):
    """
    Determines the file type and loads the corresponding event matrix.

    Args:
        event_file (str): Path to the event file (.raw or .hdf5).

    Returns:
        np.ndarray: Transposed event matrix.
    """
    if event_file.endswith(".raw"):
        print("RAW file detected")
        return load_raw_event_matrix(event_file).T
    else:
        print("HDF5 file detected")
        return load_hdf5_event_matrix(event_file).T
    
def load_hdf5_event_matrix(event_file):
    """
    Loads an event matrix from an HDF5 file.

    Args:
        event_file (str): Path to the HDF5 file.

    Returns:
        np.ndarray: Event matrix.
    """
    with h5py.File(event_file, "r") as file:
        width, height = file.attrs["width"], file.attrs["height"]
        event_matrix = np.zeros((width, height), dtype=np.int32)
        
        # Efficiently accumulate event counts
        np.add.at(event_matrix, (file["events"]["x"][:], file["events"]["y"][:]), 1)
    
    return event_matrix

def load_raw_event_matrix(event_file):
    """
    Loads an event matrix from a RAW file.

    Args:
        event_file (str): Path to the RAW file.

    Returns:
        np.ndarray: Event matrix.
    """
    raw_stream = RawReader(event_file)
    event_matrix = np.zeros((raw_stream.width, raw_stream.height), dtype=np.int32)

    while not raw_stream.is_done():
        events = raw_stream.load_n_events(1000000)
        
        # Extract x and y coordinates
        x_coords = events["x"]
        y_coords = events["y"]

        # Efficiently accumulate event counts
        np.add.at(event_matrix, (x_coords, y_coords), 1)
        
    return event_matrix


def select_roi_centers(image, num_points=16):
    """
    Allows the user to interactively select ROI centers from the event image.

    Args:
        image (np.ndarray): The event image to display.
        num_points (int): Number of ROI centers to select.

    Returns:
        tuple: (Selected points, ROI centers list)
    """
    fig, ax = plt.subplots()
    plt.imshow(image, cmap='gray')
    plt.title("Select ROI Centers (Click)")

    selected_points = [np.empty((0, 2)) for _ in range(num_points)]
    rois = []
    counter = 0

    def onclick(event):
        nonlocal counter
        if event.xdata is None or event.ydata is None:
            return  # Ignore invalid clicks
        
        if event.key == ' ':
            # Add new point to current selection
            new_point = np.array([[event.xdata, event.ydata]])
            selected_points[counter] = np.vstack([selected_points[counter], new_point])
            plt.scatter(event.xdata, event.ydata, color='red', marker='x')
            plt.draw()

        elif event.key == 'z' and len(selected_points[counter]) > 0:
            # Remove last added point
            selected_points[counter] = selected_points[counter][:-1]
            plt.cla()  # Clear the plot
            plt.imshow(image, cmap='gray')
            for i in range(counter):
                for pt in selected_points[i]:
                    plt.scatter(pt[0], pt[1], color='green', marker='x')
            for pt in selected_points[counter]:
                    plt.scatter(pt[0], pt[1], color='red', marker='x')
            for roi in rois:
                circle = plt.Circle((roi[0], roi[1]), np.sqrt(roi[2]), color='green', alpha=0.5, fill=True, linewidth=2)
                ax.add_patch(circle)

            plt.draw()

        elif event.key == 'enter' and len(selected_points[counter]) >= 3:
            # Define circle ROI from selected points
            x, y, r = define_circle(selected_points[counter])
            
            # Ask user for frequency input
            root = tk.Tk()
            root.withdraw()  # Hide the main Tkinter window
            freq = simpledialog.askfloat("Input", "Enter frequency (float):")

            # Store ROI parameters
            rois.append([x, y, r, r+5, freq])
            print(f"ROI {counter + 1}: Center=({x}, {y}), Radius={r}")

            # Visualize selected ROI
            plt.scatter(x, y, color='green', marker='x')
            for pt in selected_points[counter]:
                plt.scatter(pt[0],pt[1], color='green', marker='x')
            circle = plt.Circle((x, y), r, color='green', alpha=0.5, fill=True, linewidth=2)
            ax.add_patch(circle)
            plt.draw()

            counter += 1
            if counter >= num_points:
                plt.close()  # Close the selection window once all points are selected

    plt.gcf().canvas.mpl_connect('key_press_event', onclick)
    plt.show()
    
    return selected_points, rois


def define_circle(points):
    """
    Computes the best-fit circle from a set of selected points.

    Args:
        points (np.ndarray): Selected points forming a circle.

    Returns:
        tuple: (center_x, center_y, radius)
    """
    x = np.asarray([pt[0] for pt in points])
    y = np.asarray([pt[1] for pt in points])

    # Solve linear system to fit a circle
    A = np.column_stack([x, y, np.ones_like(x)])
    B = x**2 + y**2
    C, _, _, _ = np.linalg.lstsq(A, B, rcond=None)

    # Compute center and radius
    a, b = C[0] / 2, C[1] / 2
    r = np.sqrt(C[2] + a**2 + b**2)

    return a, b, r


def save_rois(output_file, roi_centers):
    """
    Saves the selected ROI centers to a YAML file.

    Args:
        output_file (str): Path to the output YAML file.
        roi_centers (list): List of ROI parameters.
    """
    with open(output_file, "w") as file:
        yaml.dump([[float(value) for value in roi] for roi in roi_centers], file)


def main():
    """
    Main function to load event data, allow ROI selection, and save the selected ROIs.
    """
    if len(sys.argv) < 2:
        print("Usage: python script.py <event_file> [output_rois.yaml]")
        sys.exit(1)

    event_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) >= 3 else "rois.yaml"

    print(f"Processing file: {event_file}")
    image = get_event_matrix(event_file)
    
    # Normalize image for better visibility
    image = np.log10(image + 1)  # Avoid log(0)
    image = (image * 255 / np.max(image)).astype(np.uint8)

    # Select ROI centers interactively
    _, roi_centers = select_roi_centers(image)

    # Save selected ROIs
    save_rois(output_file, roi_centers)


if __name__ == "__main__":
    main()
