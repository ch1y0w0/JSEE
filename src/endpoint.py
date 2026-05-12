# Module to extract endpoints from a JS file

# Import libraries
import json
import re

# Get all regex patterns from the json file
with open('endpoint_patterns.json') as f:
    patterns = json.load(f)

# Function to extract the endpoints based on the regex patterns
def extract_endpoints(text: str) -> set:

    all_endpoints = set()

    for pattern in patterns:
        matches = re.findall(
            pattern['regex'], 
            text, 
            re.IGNORECASE | re.MULTILINE | re.DOTALL
        )
        for match in matches:
            if isinstance(match, tuple):
                match = next((m for m in match if m), None)
            if match:
                all_endpoints.add(match)

    return all_endpoints