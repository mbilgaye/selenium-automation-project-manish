from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    """
        Parent class for all page objects.

        Provides shared browser interaction helpers so individual
        page objects can focus purely on page-specific behvaior.
    """

    DEFAULT_TIMEOUT = 5

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def open(self, url):
        self.driver.get(url)
        return self

    def get_title(self):
        return self.driver.title

    def get_url(self):
        return self.driver.current_url

    def find(self, locator):
        """Wait for and return single element"""
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    def find_all(self, locator):
        """Wait and return all matching elements"""
        self.wait.until(
            EC.presence_of_all_elements_located(locator)
        )
        return self.driver.find_elements(*locator)

    def is_visible(self, locator, timeout=5):
        """Return True if element is visible within timeout"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def click(self, locator):
        """Wait for element to be clickable, then clicks it"""
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def type_text(self, locator, text):
        """Clear the field and type text"""
        element = self.wait.until(
            EC.visibility_of_element_located(locator)
        )
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Return visible text of an element"""
        return self.find(locator).text.strip()

    def get_attribute(self, locator, attr):
        return self.find(locator).get_attribute(attr)

    def wait_for_url(self, partial_url, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(partial_url)
        )

    def refresh(self):
        self.driver.refresh()
        return self

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def clear_cookies_and_session_storage(self):
        self.driver.delete_all_cookies()
        self.execute_script("window.sessionStorage.clear();")
        return self