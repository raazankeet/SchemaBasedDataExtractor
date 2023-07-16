import json
import argparse
import csv


def extract_data(data, schema, retain_empty_lists=True, retain_empty_objects=False):
    """
    Recursively extracts data from JSON based on a schema.
    Args:
        data (dict): JSON data to extract from.
        schema (dict): Schema specifying the desired structure.
        retain_empty_lists (bool): Flag to retain empty lists in the output.
        retain_empty_objects (bool): Flag to retain empty objects in the output.
    Returns:
        dict: Extracted data based on the schema.
    """
    extracted_data = {}

    # Iterate over the schema keys and values
    for key, value in schema.items():
        # If the value is a boolean and True, extract the corresponding key from the data
        if isinstance(value, bool) and value:
            if key in data:
                extracted_data[key] = data[key]

        # If the value is a dictionary, recursively extract data for the key from the nested data
        elif isinstance(value, dict):
            if key in data:
                extracted_item = extract_data(
                    data[key], value, retain_empty_lists, retain_empty_objects)
                if extracted_item or retain_empty_objects:
                    extracted_data[key] = extracted_item

        # If the value is a list, extract data for each item in the list
        elif isinstance(value, list):
            if key in data and isinstance(data[key], list):
                extracted_items = []
                for item in data[key]:
                    if isinstance(item, dict):
                        extracted_item = extract_data(
                            item, value[0], retain_empty_lists, retain_empty_objects)
                        if extracted_item or retain_empty_objects:
                            extracted_items.append(extracted_item)
                if extracted_items or retain_empty_lists:
                    extracted_data[key] = extracted_items

    # If retain_empty_objects is False and no data was extracted, return None
    if not retain_empty_objects and not extracted_data:
        return None

    return extracted_data


def convert_json_to_csv(data, output_file):
    # Flatten the JSON data
    flattened_data = []
    for item in data:
        flattened_data.append(flatten_dict(item))

    # Extract the headers from the flattened data
    headers = sorted(
        set(key for item in flattened_data for key in item.keys()))

    # Open the CSV file for writing
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(
            file, fieldnames=headers, quoting=csv.QUOTE_ALL)

        # Write the headers to the CSV file
        writer.writeheader()

        # Write each flattened data item as a row in the CSV file
        writer.writerows(flattened_data)


def flatten_dict(dictionary, parent_key='', sep='.'):
    """
    Flattens a nested dictionary into a single-level dictionary.
    Args:
        dictionary (dict): The nested dictionary.
        parent_key (str): The parent key for nested dictionaries.
        sep (str): The separator to use between nested keys.
    Returns:
        dict: The flattened dictionary.
    """
    flattened_dict = {}
    for key, value in dictionary.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            flattened_dict.update(flatten_dict(value, new_key, sep=sep))
        elif isinstance(value, list):
            if all(isinstance(item, dict) for item in value):
                for i, item in enumerate(value):
                    flattened_item = flatten_dict(
                        item, parent_key=f"{new_key}[{i}]", sep=sep)
                    flattened_dict.update(flattened_item)
            else:
                flattened_dict[new_key] = json.dumps(value).replace('"', '""')
        else:
            flattened_dict[new_key] = value
    return flattened_dict


def main():
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="JSON Data Extractor")
    parser.add_argument(
        "--input_file", help="Path to the input JSON file", required=True)
    parser.add_argument(
        "--schema_file", help="Path to the schema JSON file", required=True)
    parser.add_argument("--output_file", help="Path to the output file")
    parser.add_argument("--format", choices=["json", "csv"], default="json",
                        help="Output format (json or csv)")
    parser.add_argument("--retain_empty_lists", action="store_true",
                        help="Retain empty lists in the output")
    parser.add_argument("--retain_empty_objects", action="store_true",
                        help="Retain empty objects in the output")
    args = parser.parse_args()

    try:
        # Read the input JSON file
        with open(args.input_file, 'r') as file:
            input_data = json.load(file)

        # Read the schema JSON file
        with open(args.schema_file, 'r') as file:
            schema_data = json.load(file)

        # Extract the data based on the schema and command-line arguments
        extracted_data = extract_data(
            input_data, schema_data, args.retain_empty_lists, args.retain_empty_objects)

        # Determine the output format
        if args.format == "json":
            output_data = extracted_data
            output_extension = "json"
        else:
            output_data = extracted_data["users"] if "users" in extracted_data else [
            ]
            output_extension = "csv"

        # Save the extracted data to the output file
        if args.output_file:
            output_file = args.output_file
        else:
            output_file = f"output.{output_extension}"

        if output_extension == "json":
            with open(output_file, 'w') as file:
                json.dump(output_data, file, indent=2)
            print(f"Data extracted successfully and saved to '{output_file}'.")
        elif output_extension == "csv":
            convert_json_to_csv(output_data, output_file)
            print(f"Data extracted successfully and saved to '{output_file}'.")
        else:
            print(f"Invalid output format: {args.format}")

    # Handle file-related errors and other exceptions
    except FileNotFoundError as e:
        if str(e).startswith("[Errno 2]"):
            if args.input_file in str(e):
                print(f"Error: Input JSON file '{args.input_file}' not found.")
            elif args.schema_file in str(e):
                print(
                    f"Error: Schema JSON file '{args.schema_file}' not found.")
        else:
            print("Error:", str(e))
    except json.JSONDecodeError as e:
        if args.input_file in str(e):
            print(
                f"Error: Invalid JSON format in input JSON file '{args.input_file}': {str(e)}.")
        elif args.schema_file in str(e):
            print(
                f"Error: Invalid JSON format in schema JSON file '{args.schema_file}': {str(e)}.")
        else:
            print(
                f"Error: Invalid JSON format in file '{args.schema_file}': {str(e)}.")
    except Exception as e:
        print("Error:", str(e))


if __name__ == '__main__':
    main()
