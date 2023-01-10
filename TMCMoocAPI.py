import time
from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains


class TMCMoocAPI:

    class URLS:
        LOGIN = "https://tmc.mooc.fi/login"
        LOGOUT = "https://tmc.mooc.fi/signout"
        PYTHON_ASSIGNMENTS = "https://tmc.mooc.fi/org/mooc/courses/950"

    def __init__(self):
        self._driver: webdriver.Firefox = webdriver.Firefox()
        self._logged_in: bool = False

    def _wait_for_url(self, url: str, timeout: int = 5) -> bool:
        """
        Waits until url has changed
        :param url: Desired url
        :param timeout: How long it will wait
        :return: If successful
        """
        try:
            WebDriverWait(self._driver, timeout).until(
                lambda e: self._driver.current_url == url)
            return True
        except TimeoutException:
            return False

    def _wait_for_element_present(self, search_term: tuple, timeout: int = 5) -> bool:
        """
        Waits until it finds correct element
        :param search_term: Such as (By.ID, "<id>")
        :param timeout: How long will it search
        :return: If successful
        """
        try:
            element_present = EC.presence_of_element_located(search_term)
            WebDriverWait(self._driver, timeout).until(element_present)
            return True
        except TimeoutException:
            return False

    def is_logged_in(self) -> bool:
        """
        Returns if you are logged into MOOC
        :return: True of False
        """
        return self._logged_in

    def get_answers(self) -> bool:
        return True