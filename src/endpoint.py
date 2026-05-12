# Module to extract endpoints from a JS file

# Import libraries
import json
import re

# Get all regex patterns from the json file
with open('patterns/endpoint.json', encoding='utf-8') as f:
    patterns = json.load(f)

# Function to extract the endpoints based on the regex patterns
def extract_endpoints(text: str) -> set:

    all_endpoints = set()

    for pattern in patterns:

        try:
            matches = re.finditer(
                pattern['regex'],
                text,
                re.IGNORECASE | re.MULTILINE | re.DOTALL
            )

            for match in matches:

                groups = [g for g in match.groups() if g]

                if groups:
                    for g in groups:
                        all_endpoints.add(g.strip())

                else:
                    all_endpoints.add(match.group(0).strip())

        except re.error as e:
            pass

    return all_endpoints