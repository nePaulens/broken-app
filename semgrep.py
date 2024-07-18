import sys
import subprocess
import argparse
import os
import requests
import json

def run_semgrep(config_file, target_directory):
    try:
        # Construct the semgrep command
        command = [
            "semgrep",
            "--config", config_file,
            "--json",  # Add the --json flag to get JSON output
            target_directory
        ]
        # Execute the command
        result = subprocess.run(command, capture_output=True, text=True)
        
        
        output_filename = f"scan.json"
        
        # Ensure the logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Full path to the output file
        output_filepath = os.path.join('logs', output_filename)

        # Print or save the output
        if result.returncode == 0:
            print("Semgrep scan completed successfully.")
            with open(output_filepath, 'w') as file:
                json_output = json.loads(result.stdout)
                for obj in json_output.get('results', []):
                    file.write(json.dumps(obj) + '\n')
            print(f"Output written to {output_filepath}")
        else:
            print("Semgrep scan encountered an error.")
            print(result.stderr)
    except Exception as e:
        print(f"An error occurred while running Semgrep: {e}")


def run_requests():

	# Read the JSON file
	file_path = '/home/kali/Desktop/semgrep_work/logs/scan.json'
	with open(file_path, 'r') as file:
		data_list = json.load(file)

	# Iterate through each JSON object in the file
	for data in data_list:
		# Extract the path value
		path_value = data.get('extra', {}).get('dataflow_trace', {}).get('intermediate_vars', [{}])[0].get('location', {}).get('path', '')

	if path_value:
		# Transform the path into a URL
		base_url = "http://localhost:8080"
		url = base_url + path_value.replace("/home/kali/Desktop/cvwa/CVWA/site", "")

	# Send an HTTP GET request with ?search=$VAL
	val = "test_value"
	request_url = f"{url}?search={val}"
	response = requests.get(request_url)

		# Compare the header with the sent value
	if response.headers.get('search') == val:
		print(f'XSS found in {path_value}')





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Semgrep with a specified config file and target directory.')
    parser.add_argument('--config', type=str, required=True, help='Path to the Semgrep config file.')
    parser.add_argument('--target', type=str, required=True, help='Path to the target directory to scan.')
    parser.add_argument('--scan-target', type=str, help='URL to send the JSON object from scan.txt.')

    args = parser.parse_args()

    run_semgrep(args.config, args.target)
    run_requests()
