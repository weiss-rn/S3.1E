import os

class fungsi:
    @staticmethod
    def create_directory(directory):
        os.makedirs(directory, exist_ok=True)