#Stephon Kumar
#Assignment 3

import argparse
import requests
import csv
from datetime import datetime

# Function to download the file from a given URL
def download_file(url):
    try:
        # Make an HTTP GET request to the specified URL
        response = requests.get(url)
        # Raise an exception for bad HTTP status codes (e.g., 404, 500)
        response.raise_for_status()
        # Return the text content of the response (the CSV data)
        return response.text
    except requests.exceptions.RequestException as e:
        # Print error message if the download fails
        print(f"Failed to download the file: {e}")
        return None

# Function to process the CSV data into a list of lists
def process_log_data(data):
    log_entries = []
    # Split the input data into lines and read each line as a row
    for row in csv.reader(data.splitlines()):
        log_entries.append(row)
    return log_entries

# Function to count how many requests are for image files
def find_image_requests(log_entries):
    # Define tuple of image file extensions
    image_extensions = ('.jpg', '.gif', '.png')
    image_hits = 0
    # Iterate through each log entry
    for entry in log_entries:
        # Check if the file path ends with a known image extension
        if entry[0].endswith(image_extensions):
            image_hits += 1
    # Calculate the total number of hits
    total_hits = len(log_entries)
    # Calculate the percentage of image hits
    image_percentage = (image_hits / total_hits * 100) if total_hits > 0 else 0
    return image_hits, image_percentage

# Function to determine the most popular browser used
def find_popular_browser(log_entries):
    # Dictionary to count hits per browser
    browsers = {"Firefox": 0, "Chrome": 0, "Internet Explorer": 0, "Safari": 0}
    # Iterate through each log entry
    for entry in log_entries:
        # Increment count for the browser found in the entry
        if "Firefox" in entry[2]:
            browsers["Firefox"] += 1
        elif "Chrome" in entry[2]:
            browsers["Chrome"] += 1
        elif "MSIE" in entry[2] or "Trident" in entry[2]:  # Includes older and newer IE identifiers
            browsers["Internet Explorer"] += 1
        elif "Safari" in entry[2]:
            browsers["Safari"] += 1
    # Find the browser with the maximum count
    popular_browser = max(browsers, key=browsers.get)
    return popular_browser

# Function to analyze and print hits per hour
def analyze_hits_by_hour(log_entries):
    # Initialize a dictionary with an entry for each hour, 0 through 23
    hour_hits = {str(hour): 0 for hour in range(24)}
    # Iterate through each log entry
    for entry in log_entries:
        # Extract the hour from the datetime string
        hour = datetime.strptime(entry[1], "%m/%d/%Y %H:%M:%S").hour
        # Increment the count for the extracted hour
        hour_hits[str(hour)] += 1
    # Print the count of hits for each hour
    for hour, count in sorted(hour_hits.items(), key=lambda x: int(x[0])):
        print(f"Hour {hour} has {count} hits")

if __name__ == "__main__":
    # Setup command line argument parsing
    parser = argparse.ArgumentParser(description="Process web log files.")
    parser.add_argument("--url", required=True, help="URL of the log file")
    args = parser.parse_args()

    # Download the data from the provided URL
    data = download_file(args.url)
    if data:
        # Process the CSV data into a usable format
        log_entries = process_log_data(data)
        # Calculate image request stats
        image_hits, image_percent = find_image_requests(log_entries)
        # Determine the most popular browser
        popular_browser = find_popular_browser(log_entries)

        # Print the results
        print(f"Image requests account for {image_percent:.2f}% of all requests.")
        print(f"The most popular browser is {popular_browser}.")
        # Extra: Analyze and print the distribution of hits by hour
        analyze_hits_by_hour(log_entries)
    else:
        print("No data to process.")
