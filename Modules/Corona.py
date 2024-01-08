import json
import time
import threading
import requests

API_KEY = "your key"
PROJECT_TOKEN = "your token"


class Data:
    def __init__(self, api_key, project_key):
        self.api_key = api_key
        self.project_key = project_key
        self.params = {
            "api_key": self.api_key
        }
        self.data = self.get_data()

    def get_data(self):
        res = requests.get(
            f'https://www.parsehub.com/api/v2/projects/{self.project_key}/last_ready_run/data', params=self.params)
        data = json.loads(res.text)
        return data

    def get_total_cases(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Coronavirus Cases:":
                return content['value']

    def get_total_death(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Deaths:":
                return content['value']

    def get_total_recovered(self):
        data = self.data['total']

        for content in data:
            if content['name'] == "Recovered:":
                return content['value']

        return "0"

    def get_county_data(self, country):
        data = self.data['country']

        for content in data:
            if content['name'].lower() == country.lower():
                return content

        return "0"

    def get_list_of_countries(self):
        countries = []
        for country in self.data['country']:
            countries.append(country['name'].lower())

        return countries

    def update_data(self):
        requests.post(
            f'https://www.parsehub.com/api/v2/projects/{self.project_key}/run', params=self.params)
        old_data = self.data
        while True:
            new_data = self.get_data()
            if new_data != old_data:
                self.data = new_data
                print("Data is updated")
                break
