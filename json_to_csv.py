import json
import csv


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


def convert_json_to_csv(input_file, output_file):
    # Read the JSON data
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Flatten the JSON data
    flattened_data = []
    for user in data['users']:
        flattened_user = flatten_dict(user)
        flattened_data.append(flattened_user)

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


# Usage example
input_file = 'Output/Opt.json'
output_file = 'Output/output.csv'
convert_json_to_csv(input_file, output_file)
