# Tool to extract endpoints, secrets and paths from a given JS file,URL or a webpage

# Import libraries
import httpx
import json
import re
import sys
from urllib.parse import urljoin
from enum import Enum

# Declare TYPE enum
class TYPES(Enum):

    WEBPAGE = 1
    JS_URL = 2
    JS_FILE = 3

# Declare patterns pathes
ENDPOINT_PATTERNS = "patterns/endpoint.json"
PATH_PATTERNS = "patterns/path.json"
SECRET_PATTERNS = "patterns/secret.json"

# Function to find the extraction type based on the input
def find_type() -> Enum | str:

    if sys.argv[1]:
        TARGET = sys.argv[1]

        if TARGET.startswith("https://") or TARGET.startswith("http://"):

            if TARGET.endswith(".js"):
                TYPE = TYPES.JS_URL
            
            else:
                TYPE = TYPES.WEBPAGE
        
        else:

            TYPE = TYPES.JS_FILE

    else:
        print("[-] No Target Found!...")
        sys.exit(1)
    
    return TYPE, TARGET

# Extract JS file URLs from a webpage
def extract_js_files(content: str, base_url: str = "") -> list:
    pattern = r'''(?:src=["']|href=["'])([^"']+\.js(?:\?[^"']*)?)["']'''
    
    matches = re.findall(pattern, content, re.IGNORECASE)

    # Convert relative URLs to absolute if base_url is provided
    js_files = [
        urljoin(base_url, url) if base_url else url
        for url in matches
    ]

    # Remove duplicates while keeping order
    return list(dict.fromkeys(js_files))

# Function to extract based on the given pattern
def extract(pattern: str, text: str) -> set:

    # Load patterns
    with open(pattern) as f:
        patterns = json.load(f)
        
    # Extract
    extracted = set()

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
                extracted.add(match)

    return extracted

# Get the type and the target
TYPE, TARGET = find_type()

# Extract based on the TYPE
if TYPE == TYPES.WEBPAGE:

    # Get JS files from the webpage
    response = httpx.get(url=TARGET, follow_redirects=True).text
    js_list = extract_js_files(content=response, base_url=TARGET)

    # Find everything from the extracted JS files
    for JSFile in js_list:

        js_response = httpx.get(url=JSFile).text
        endpoints = extract(pattern=ENDPOINT_PATTERNS, text=js_response)
        secrets = extract(pattern=SECRET_PATTERNS, text=js_response)
        pathes = extract(pattern=PATH_PATTERNS, text=js_response)

        print("**************************************************")
        print(f'[+] Findings For {JSFile}:\n')

        print("************************")
        print("[+] Found Endpoints:")
        for endpoint in endpoints:
            print(endpoint)
        
        print("************************")
        print("[+] Found Secrets:")
        for secret in secrets:
            print(secret)
        
        print("************************")
        print("[+] Found Pathes:")
        for path in pathes:
            print(path)
        print("**************************************************")

if TYPE == TYPES.JS_URL:

    # Fetch the JS file
    js_response = httpx.get(url=TARGET).text

    # Extract everything
    endpoints = extract(pattern=ENDPOINT_PATTERNS, text=js_response)
    secrets = extract(pattern=SECRET_PATTERNS, text=js_response)
    pathes = extract(pattern=PATH_PATTERNS, text=js_response)

    print("**************************************************")
    print(f'[+] Findings For {TARGET}:\n')

    print("************************")
    print("[+] Found Endpoints:")
    for endpoint in endpoints:
        print(endpoint)

    print("************************")    
    print("[+] Found Secrets:")
    for secret in secrets:
        print(secret)
        
    print("************************")
    print("[+] Found Pathes:")
    for path in pathes:
        print(path)
    print("**************************************************")

if TYPE == TYPES.JS_FILE:

    # Open the file
    with open(TARGET, 'r') as f:
        content = f.read()
    
    # Extract everything
    endpoints = extract(pattern=ENDPOINT_PATTERNS, text=content)
    secrets = extract(pattern=SECRET_PATTERNS, text=content)
    pathes = extract(pattern=PATH_PATTERNS, text=content)

    print("**************************************************")
    print(f'[+] Findings For {TARGET}:\n')

    print("************************")
    print("[+] Found Endpoints:")
    for endpoint in endpoints:
        print(endpoint)
    
    print("************************")
    print("[+] Found Secrets:")
    for secret in secrets:
        print(secret)
    
    print("************************")
    print("[+] Found Pathes:")
    for path in pathes:
        print(path)
    print("**************************************************")