import subprocess
import argparse
import json
import requests
import os
from datetime import datetime

def run_semgrep(config_path, target_path):
    try:
        # Construct the semgrep command
        command = [
            "semgrep",
            "--config", config_path,
            "--json",  # Add the --json flag to get JSON output
            target_path
        ]
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Semgrep scan encountered an error.")
            print(result.stderr)
            return

        # Print the raw JSON output
        print("Raw Semgrep output:")
        print(result.stdout)

        # Parse the JSON output
        json_output = json.loads(result.stdout)
        
        # Extract the `path` value from the JSON output and assign to `target_url`
        target_url = None
        for result in json_output.get('results', []):
            path_value = result.get('path', '')
            if path_value:
                # Splice the path to get only the filename
                target_url = os.path.basename(path_value)
                print(f"Found target URL: {target_url}")
                break  # Assuming you only want the first occurrence

        if target_url:
            print(f"Example target URL: {target_url}")

            # Send a simple HTTP request using the requests library
            full_url = f"http://localhost:8080/{target_url}?search=asdf"python
            response = requests.get(full_url)
            print(f"HTTP request to {full_url} returned status code {response.status_code} with body: {response.text}")
        else:
            print("No target URLs found.")
        
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
    except Exception as e:
        print(f"An error occurred while running Semgrep: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Semgrep with a specified config file and target directory.')
    parser.add_argument('--config', type=str, required=True, help='Path to the Semgrep config file.')
    parser.add_argument('--target', type=str, required=True, help='Path to the target directory to scan.')

    args = parser.parse_args()

    run_semgrep(args.config, args.target)
