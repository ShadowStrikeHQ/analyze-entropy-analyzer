import argparse
import logging
import math
import os
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_entropy(data):
    """
    Calculates the Shannon entropy of a byte string.

    Args:
        data (bytes): The byte string to analyze.

    Returns:
        float: The Shannon entropy in bits per byte.
    """
    if not data:
        return 0  # Empty data has zero entropy

    entropy = 0
    data_length = len(data)
    frequency_map = {}

    # Calculate frequency of each byte
    for byte in data:
        if byte in frequency_map:
            frequency_map[byte] += 1
        else:
            frequency_map[byte] = 1

    # Calculate entropy based on byte frequencies
    for byte in frequency_map:
        probability = frequency_map[byte] / data_length
        entropy -= probability * math.log2(probability)

    return entropy


def analyze_file(filepath):
    """
    Analyzes the entropy of a file.

    Args:
        filepath (str): The path to the file to analyze.

    Returns:
        float: The Shannon entropy of the file's contents, or None if an error occurs.
    """
    try:
        with open(filepath, 'rb') as f:
            file_data = f.read()  # Read the entire file as bytes
        return calculate_entropy(file_data)
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        return None
    except IOError as e:
        logging.error(f"Error reading file {filepath}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while processing {filepath}: {e}")
        return None


def setup_argparse():
    """
    Sets up the argument parser for the command-line interface.

    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Calculate and visualize the Shannon entropy of files to identify potential obfuscation or encryption."
    )
    parser.add_argument("filepath", help="The path to the file to analyze.")
    parser.add_argument(
        "-o", "--output", help="Optional: Specify an output file to store the entropy value.", metavar="output_file"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging (DEBUG level)."
    )
    return parser


def main():
    """
    Main function to parse arguments, analyze the file, and output the results.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose logging enabled.")

    filepath = args.filepath

    # Input validation: Check if the file exists
    if not os.path.isfile(filepath):
        logging.error(f"Error: File '{filepath}' does not exist.")
        return

    entropy_value = analyze_file(filepath)

    if entropy_value is not None:
        print(f"Shannon entropy of {filepath}: {entropy_value:.4f} bits per byte")

        if args.output:
            try:
                with open(args.output, "w") as outfile:
                    outfile.write(str(entropy_value))  # Store entropy as string
                logging.info(f"Entropy value written to {args.output}")
            except IOError as e:
                logging.error(f"Error writing to output file {args.output}: {e}")


if __name__ == "__main__":
    # Example usage:
    # python main.py test.txt
    # python main.py encrypted.dat -o entropy_output.txt
    # python main.py suspicious_file.bin -v
    main()