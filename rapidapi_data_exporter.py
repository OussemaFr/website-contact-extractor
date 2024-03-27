import csv
import requests

class RapidAPIDataExporter:
    def __init__(self, rapid_api_key, output_file):
        """
        Initialize the exporter with a RapidAPI key and an output file path.

        Args:
        - rapid_api_key (str): The RapidAPI key.
        - output_file (str): The path to the output CSV file.
        """
        self.rapid_api_key = rapid_api_key
        self.output_file = output_file
        self.fieldnames = [
            "link", "domain", "depth", "original_start_url", "emails", "phones",
            "descriptions", "linkedins", "twitters", "instagrams", "facebooks",
            "youtubes", "tiktoks", "telegrams", "status_code", "page_type"
        ]

        # Create or append to the output file
        with open(self.output_file, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            # Write header only if file is empty
            if file.tell() == 0:
                writer.writeheader()

    def append_data(self, websites):
        """
        Append data for each website in the list to the CSV file.

        Args:
        - websites (list): A list of website URLs.
        """
        for website in websites:
            payload = {
                "start_url": website,
                "max_requests": 2
            }
            data = self.get_data(payload)
            with open(self.output_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.fieldnames)
                writer.writerow(data)

    def get_data(self, payload):
        """
        Get data from the RapidAPI endpoint.

        Args:
        - payload (dict): The payload to send to the endpoint.

        Returns:
        - dict: The response JSON from the endpoint.
        """
        url = "https://contact-details-scraper.p.rapidapi.com/get_contact_details"
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": self.rapid_api_key,
            "X-RapidAPI-Host": "contact-details-scraper.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)
        return response.json()

# Example usage
rapid_api_key = "YOUR_RAPIDAPI_KEY"
output_file = "output.csv"
websites = ["https://example.com/", "https://example.org/"]

# Initialize the exporter
exporter = RapidAPIDataExporter(rapid_api_key, output_file)

# Append data for each website to the CSV file
exporter.append_data(websites)
