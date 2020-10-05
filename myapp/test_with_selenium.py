import time
import myapp.views
import myapp.config
from flask_testing import LiveServerTestCase
from selenium import webdriver
import selenium.webdriver.support.ui as ui


class TestUserInterface(LiveServerTestCase):

    def create_app(self):
        return myapp.views.app

    def setUp(self):
        """
        Setting up selenium server
        """
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:5000")
        self.wait = ui.WebDriverWait(self.driver, 1000)

    def tearDown(self):
        """
        Closing the server
        """
        self.driver.quit()

    def test_input_stuff(self):
        """
        The proper test with selenium is here.
        We try an input then a click on submit button and we check if the
        google map is displayed
        """
        new_input = self.driver.find_element_by_css_selector("#note")
        new_input.send_keys("Openclassrooms")
        assert new_input.get_attribute("value") == "Openclassrooms"
        button = self.driver.find_element_by_css_selector("#submit_button")
        button.click()
        time.sleep(6)
        assert self.driver.find_element_by_css_selector("#imggoogle").is_displayed()
