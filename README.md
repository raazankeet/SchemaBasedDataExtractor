# JSON Data Extractor

The JSON Data Extractor is a command-line tool that allows you to extract specific data from a larger JSON file based on a provided schema.

## Features

- Extracts data from a larger JSON file based on a schema
- Retains or drops empty lists and objects based on command-line arguments
- Command-line argument support for input and schema file paths
- Error handling for file-related issues and invalid JSON format

## Usage

To use the JSON Data Extractor, follow these steps:

1. Ensure you have Python installed on your system. (Preferrably 3.x )

2. Download or clone this repository.

   ```shell
   git clone https://github.com/raazankeet/SchemaBasedDataExtractor.git

   ```

3. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt

   ```

4. Prepare your input files:

- Create an input JSON file containing the data you want to extract.
- Create a schema JSON file specifying the desired structure of the extracted data.

5. Run the JSON Data Extractor using the following command:
   ```
   python JSONextractor.py --input_file <input_file_path> --schema_file <schema_file_path> [--output_file <output_file_path>] [--retain_empty_lists] [--retain_empty_objects]
   ```

- Replace `<input_file_path>` with the path to your input JSON file.
- Replace `<schema_file_path>` with the path to your schema JSON file.
- Replace `<output_file_path>` (optional) with the path where you want to save the extracted data as a JSON file. If not provided, the extracted data will be printed on the console.
- Use the `--retain_empty_lists` flag to retain empty lists in the output (optional).
- Use the `--retain_empty_objects` flag to retain empty objects in the output (optional).

6. The extracted data will be saved to the output file or displayed on the console, depending on your command-line arguments.

## Examples

- Extract data from `input.json` using `schema.json` and save the output to `output.json`:

```
python JSONextractor.py --input_file input.json --schema_file schema.json --output_file output.json
```

- Extract data from `input.json` using `schema.json`, retain empty lists, and save the output to `output.json`:

```
python JSONextractor.py --input_file input.json --schema_file schema.json --output_file output.json --retain_empty_lists

```

- Extract data from `input.json` using `schema.json`, retain empty objects, and display the output on the console:

```
python JSONextractor.py --input_file input.json --schema_file schema.json --retain_empty_objects
```

## Example

Suppose you have the following files:

**input.json**

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

```json
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

```json
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

## License

This project is licensed under the [MIT License](LICENSE).
