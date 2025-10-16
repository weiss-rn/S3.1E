import requests
import P4_1 as fungsi
import os

class fungsi:
    @staticmethod
    def create_directory(directory):
        os.makedirs(directory, exist_ok=True)

def main_source(url, directory):
    fungsi.create_directory(directory)
    req = requests.get(url)
    source_code = req.text
    print(source_code)

main_source("https://www.google.com/", "test")