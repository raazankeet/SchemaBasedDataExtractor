import json
import argparse


def extract_data(data, schema, retain_empty_lists=True, retain_empty_objects=False):
    extracted_data = {}
    for key, value in schema.items():
        if isinstance(value, bool) and value:
            if key in data:
                extracted_data[key] = data[key]
        elif isinstance(value, dict):
            if key in data:
                extracted_data[key] = extract_data(
                    data[key], value, retain_empty_lists, retain_empty_objects)
        elif isinstance(value, list):
            if key in data and isinstance(data[key], list):
                if retain_empty_lists or len(data[key]) > 0:
                    extracted_data[key] = []
                    for item in data[key]:
                        if isinstance(item, dict):
                            extracted_item = extract_data(
                                item, value[0], retain_empty_lists, retain_empty_objects)
                            if retain_empty_objects or extracted_item:
                                extracted_data[key].append(extracted_item)
    return extracted_data


def main():
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(description="JSON Data Extractor")
    parser.add_argument("--input_main_file",
                        help="Path to the larger JSON file")
    parser.add_argument("--schema_to_extract",
                        help="Path to the schema JSON file")
    parser.add_argument("--retain_empty_lists", action="store_true",
                        help="Retain empty lists in the output")
    parser.add_argument("--retain_empty_objects", action="store_true",
                        help="Retain empty objects in the output")
    args = parser.parse_args()

    try:
        # Verify if the input file exists and is valid JSON
        with open(args.input_main_file, 'r') as file:
            larger_data = json.load(file)

        # Verify if the schema file exists and is valid JSON
        with open(args.schema_to_extract, 'r') as file:
            schema_data = json.load(file)

        # Extract the data based on the schema and command-line arguments
        extracted_data = extract_data(
            larger_data,
            schema_data,
            args.retain_empty_lists,
            args.retain_empty_objects
        )

        # Print the extracted data
        print("Extracted Data:")
        print(json.dumps(extracted_data, indent=2))

    # Handle file-related errors
    except FileNotFoundError as e:
        print("Error: File not found.")
    except json.JSONDecodeError as e:
        print("Error: Invalid JSON format.")

    # Handle other exceptions
    except Exception as e:
        print("Error:", str(e))


if __name__ == '__main__':
    main()
