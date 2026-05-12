# Module to crawl a web page to extract all JS files

"""
Input: Webpage
Workflow: Parse the page, extract all JS files
Output: JS files URLs
"""

# Import necessary libraries
import httpx

# Main class for the crawler
class Crawler:

    # Initialize the class
    def __init__(self, url: str):
        self.url = url
    
    # Get the page's source code
    def request(self):
        response = httpx.get(self.url, follow_redirects=True)

        return response