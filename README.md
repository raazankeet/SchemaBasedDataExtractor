# JSON Data Extractor

The JSON Data Extractor is a command-line tool that allows you to extract specific data from a larger JSON file based on a provided schema.

## Features

- Extracts data from a larger JSON file based on a schema
- Retains or drops empty lists and objects based on command-line arguments
- Command-line argument support for input and schema file paths
- Error handling for file-related issues and invalid JSON format

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/json-data-extractor.git

   ```

2. Change to the project directory:

   ```shell
   cd json-data-extractor

   ```

3. Install the required dependencies:

   pip install -r requirements.txt

## Usage

Run the JSON Data Extractor using the following command-line arguments:

    python JSONextractor.py --input_main_file=<path_to_input_file> --schema_to_extract=<path_to_schema_file> [--retain_empty_lists] [--retain_empty_objects]

Replace `<path_to_input_file>` with the path to your larger JSON file, and `<path_to_schema_file>` with the path to your schema JSON file. The optional arguments `--retain_empty_lists` and `--retain_empty_objects` determine whether to retain empty lists and empty objects in the extracted data.

The tool will extract the data based on the provided schema and print the extracted data in JSON format.

## Example

Suppose you have the following files:

**larger_file.json**

```json
{
  "users": [
    {
      "id": 1,
      "name": "John",
      "age": 25,
      "address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "country": "USA"
      },
      "projects": [
        {
          "id": 1,
          "name": "Project A"
        }
      ]
    },
    {
      "id": 2,
      "name": "Alice",
      "age": 30,
      "address": {
        "street": "456 Elm St",
        "city": "San Francisco",
        "state": "CA",
        "country": "USA"
      },
      "projects": [
        {
          "id": 2,
          "name": "Project B"
        }
      ]
    }
  ]
}
```

**schema.json**

```
{
  "users": [
    {
      "name": true,
      "address": {
        "state": true,
        "country": true
      },
      "projects": [
        {
          "id": true

        }
      ]
    }
  ]
}

```

You can run the JSON Data Extractor with the following command:

```
python JSONextractor.py --input_main_file=larger_file.json --schema_to_extract=schema.json --retain_empty_lists --retain_empty_objects
```

The tool will extract the desired data based on the schema and print the extracted data in JSON format:

```
{
  "users": [
    {
      "name": "John",
      "address": {
        "state": "NY",
        "country": "USA"
      },
      "projects": [
        {
          "id": 1
        }
      ]
    },
    {
      "name": "Alice",
      "address": {
        "state": "CA",
        "country": "USA"
      },
      "projects": [
        {
          "id": 2
        }
      ]
    }
  ]
}
```
