This is a project, which aims to use semgrep python library to scan source code for vulnerabilities, based on rules and then verifies it by sending a http request to the scanned target and analyzes the response.
Currently, it is focused on discovering and verifying reflected XSS vulnerabilities.

Usage:
python3 semgrep.py --target {PATH_TO_SOURCE_CODE} --config {PATH_TO_RULES}

How it works:
Using semgrep, it scans a file (or multiple, it can scan the whole directory) and looks for vulnerabilities that are defined in rules.yaml file, then it saves the scan output to /logs/scan.json, then depending on what was found, it will generate a HTTP request and sends it to the target, then analyzes its response, in order to validate existence of found vulnerability.

As a test bench, CVWA is included.

In case CVWA is not there, run this
git clone https://github.com/convisolabs/CVWA

Usage:
docker build -t cvwa .
docker container run -ti -p 8080:80 cvwa

This will allow you to access self-hosted CVWA application through a web browser
http://localhost:8080
