"Stephon Kumar"
"Assignment 3"

import argparse
import csv
import urllib.request
from datetime import datetime

def fetch_log_content(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading the log file: {e}")
        return None

def parse_log_content(log_content):
    hits = []
    reader = csv.reader(log_content.splitlines())
    for row in reader:
        path, date_str, user_agent, _, _ = row
        hits.append({
            'path': path,
            'date': datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S'),
            'user_agent': user_agent,
        })
    return hits

def filter_image_hits(hits):
    image_hits = [hit for hit in hits if hit['path'].lower().endswith(('.jpg', '.gif', '.png'))]
    return image_hits

def find_most_used_browser(hits):
    browser_counts = {'Firefox': 0, 'Chrome': 0, 'Internet Explorer': 0, 'Safari': 0}
    for hit in hits:
        for browser in browser_counts:
            if browser.lower() in hit['user_agent'].lower():
                browser_counts[browser] += 1
                break
    most_used_browser = max(browser_counts, key=browser_counts.get)
    return most_used_browser

def display_hourly_hits(hits):
    hourly_hits = {}
    for hit in hits:
        hour = hit['date'].hour
        hourly_hits[hour] = hourly_hits.get(hour, 0) + 1

    sorted_hours = sorted(hourly_hits.items(), key=lambda x: x[1], reverse=True)
    for hour, count in sorted_hours:
        print(f"Hour {hour:02d} has {count} hits")

def display_extra_credit_hourly_hits(hits):
    hourly_hits = {}
    for hit in hits:
        hour = hit['date'].hour
        hourly_hits[hour] = hourly_hits.get(hour, 0) + 1

    sorted_hours = sorted(hourly_hits.items(), key=lambda x: x[0])
    for hour, count in sorted_hours:
        print(f"Hour {hour:02d} has {count} hits (Extra Credit)")

def main(url):
    """Main entry point for the program."""
    log_content = fetch_log_content(url)

    if log_content:
        hits = parse_log_content(log_content)

        image_hits = filter_image_hits(hits)
        image_percentage = (len(image_hits) / len(hits)) * 100
        print(f"Image requests account for {image_percentage:.1f}% of all requests")

        most_used_browser = find_most_used_browser(hits)
        print(f"The most used browser is: {most_used_browser}")

        display_hourly_hits(hits)

        display_extra_credit_hourly_hits(hits)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()

    main(args.url)
