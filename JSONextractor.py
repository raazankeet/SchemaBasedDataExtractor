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
                extracted_item = extract_data(
                    data[key], value, retain_empty_lists, retain_empty_objects)
                if extracted_item or retain_empty_objects:
                    extracted_data[key] = extracted_item
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
    if not retain_empty_objects and not extracted_data:
        return None
    return extracted_data


def main():
    parser = argparse.ArgumentParser(description="JSON Data Extractor")
    parser.add_argument("--retain_empty_lists", action="store_true",
                        help="Retain empty lists in the output")
    parser.add_argument("--retain_empty_objects", action="store_true",
                        help="Retain empty objects in the output")
    args = parser.parse_args()

    try:
        # Read the larger JSON file
        with open('Inputs/larger_file.json', 'r') as file:
            larger_data = json.load(file)

        # Read the schema JSON file
        with open('Schema/Schema.json', 'r') as file:
            schema_data = json.load(file)

        # Extract the data
        extracted_data = extract_data(
            larger_data, schema_data, args.retain_empty_lists, args.retain_empty_objects)

        # Print the extracted data
        print("Extracted Data:")
        print(json.dumps(extracted_data, indent=2))
    except FileNotFoundError as e:
        print("Error: File not found.")
    except json.JSONDecodeError as e:
        print("Error: Invalid JSON format.")
    except Exception as e:
        print("Error:", str(e))


if __name__ == '__main__':
    main()
