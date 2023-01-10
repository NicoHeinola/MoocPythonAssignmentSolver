import os.path

import requests
import zipfile


class DriverManager:
    @staticmethod
    def driver_exists() -> bool:
        """
        Checks if geckodriver exists
        :return: if driver exists
        """

        return os.path.exists("./geckodriver.exe")

    @staticmethod
    def download_driver():
        """
        Downloads geckodriver
        """

        # Downloads geckodriver
        r = requests.get(r"https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-win64.zip")
        with open("geckodriver.zip", "wb") as file:
            file.write(r.content)

        # Unzips geckodriver
        with zipfile.ZipFile("geckodriver.zip", "r") as zip:
            zip.extractall()

        # Deletes geckodriver.zip
        os.remove("./geckodriver.zip")
