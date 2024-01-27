import json
import os
import glob
import autopep8
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

def load_or_create_config():
    """
    Loads the configuration from a JSON file, or creates a new configuration file 
    if it does not exist, based on user input.
    """
    config_path = 'config.json'
    if not os.path.exists(config_path):
        # Configuration is missing; prompt the user for required information
        print("Configuration missing. Please enter the required information.")
        project_name = input("Enter the project name: ")
        output_file = input("Enter the output file name (with .pyp extension): ")
        config = {
            "project_name": project_name,
            "output_file": output_file
        }
        # Save the new configuration to a file
        with open(config_path, 'w') as file:
            json.dump(config, file)
    else:
        # Load existing configuration
        with open(config_path, 'r') as file:
            config = json.load(file)
    return config

def clean_and_concatenate_files(input_dir, output_file):
    """
    Concatenates all Python files found in the input directory, cleans them using
    autopep8, and saves to the specified output file.
    """
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Identify internal modules to handle imports correctly
    internal_modules = set()
    for filename in glob.glob(input_dir + '/**/*.py', recursive=True):
        module_name = os.path.basename(filename)[:-3]
        internal_modules.add(module_name)

    # Read and concatenate code from each file
    concatenated_code = []
    for filename in glob.glob(input_dir + '/*.py'):
        with open(filename, 'r') as file:
            code = file.read()
            concatenated_code.append(code)

    # Clean concatenated code using autopep8
    concatenated_code = '\n\n'.join(concatenated_code)
    concatenated_code = autopep8.fix_code(concatenated_code)

    # Process and clean up imports
    final_lines = []
    for line in concatenated_code.split('\n'):
        stripped_line = line.strip()
        if stripped_line.startswith('import ') or stripped_line.startswith('from '):
            parts = stripped_line.split()
            if parts[1].split('.')[0] not in internal_modules:
                final_lines.append(line)
        else:
            final_lines.append(line)

    # Write the final cleaned code to the output file
    final_code = '\n'.join(final_lines).lstrip()
    with open(output_file, 'w') as outfile:
        outfile.write(final_code)

class Handler(FileSystemEventHandler):
    """
    Event handler for Watchdog observer. This gets triggered when a file modification
    event occurs in the watched directory.
    """
    def on_modified(self, event):
        print("File Modified - Running Build Script @" + time.strftime("%H:%M:%S", time.localtime()))
        config = load_or_create_config()
        clean_and_concatenate_files(f'./dev/{config["project_name"]}', f'./build/{config["project_name"]}/{config["output_file"]}')

if __name__ == "__main__":
    # Main execution logic
    config = load_or_create_config()
    project_path = f'./dev/{config["project_name"]}'
    
    # Create the project directory if it does not exist
    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print(f"Created project directory at {project_path}")

    # Setting up and starting a filesystem observer
    event_handler = Handler()
    observer = Observer()
    observer.schedule(event_handler, project_path, recursive=True)
    observer.start()
    
    # Keep the script running or exit on keyboard interrupt (Ctrl+C)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
