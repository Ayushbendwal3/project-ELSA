import requests
import json

URL = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles="


def get_wiki(text):
    try:
        article = URL+text
        result = requests.get(article)
        data = result.json()
        output = data["query"]["pages"]
        final = output[list(output.keys())[0]]
        final = final['extract']
        return final

    except:
        print("data not found")
