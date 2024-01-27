# PyC4DAssembler
### Cinema 4D Python Plugin Development Tool

This script is a development tool designed specifically for creating Cinema 4D Python plugins. It allows developers to work on Cinema 4D plugins by writing code in multiple `.py` files, enhancing code readability and making it easier to write unit tests. The script monitors changes in the development files and automatically concatenates them into a single `.pyp` file. This approach streamlines the plugin development process, especially for complex plugins that benefit from modular coding.

## Key Features

- **Multi-File Development:** Enables writing Cinema 4D Python plugins in multiple `.py` files for better organization and readability.
- **Automatic Concatenation:** Watches for file changes and automatically concatenates multiple `.py` files into a single `.pyp` file.
- **Code Cleanup:** Uses `autopep8` to format the concatenated code, ensuring adherence to Python coding standards.

## Installation

Ensure Python is installed on your system along with the `watchdog` and `autopep8` packages. Install these dependencies using:

```bash
pip install watchdog autopep8
```


## Configuration
On the first run, you'll be prompted to enter:

- The name of your project.
- The desired name for the output plugin .pyp file.

These details will be saved in a config.json file for future runs.

## Usage
Run the script in your terminal:

```bash
python build.py
```

The script monitors a specified directory for changes. When modifications are detected, it concatenates all .py files in the directory into a single .pyp file.

## Limitations
Currently, the script concatenates files in alphabetical order. You might need to name your files accordingly to ensure correct order.
Post-concatenation, some manual code cleanup may be required, such as refining imports or other minor adjustments.

## Contributions
Feel free to contribute to this project. Ensure that your contributions follow the coding standards and include appropriate unit tests.


## Contact
safina3d
