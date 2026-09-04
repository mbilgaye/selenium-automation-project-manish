from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://grocerymate.masterschool.com/auth"

    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    # (By.XPATH, "//input[@type='email']
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BTN = (By.XPATH, "//button[@type='submit' and text()='Sign In']")

    def enter_email(self, email):
        self.type_text(self.EMAIL_INPUT, email)
        return self

    def enter_password(self, password):
        self.type_text(self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        self.click(self.LOGIN_BTN)
        from pages.home_page import HomePage
        return HomePage(self.driver)

    def login(self, email, password):
        return(
            self.enter_email(email)
            .enter_password(password)
            .click_login()
        )