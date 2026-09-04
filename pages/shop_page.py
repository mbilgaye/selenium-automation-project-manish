from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage


def get_card_image_xpath(product):
    return By.XPATH, f"//img[@alt='{product}' and @class='card-img-top']"


def get_add_to_cart_xpath_for_product(product):
    return (By.XPATH,
            f"//div[@class='card']//img[@alt='{product}']/parent::div[@class='card']//button[contains(text(),'Add to Cart')]")


def get_quantity_xpath_for_product(product):
    return (By.XPATH,
            f"//div[@class='card']//img[@alt='{product}']/parent::div[@class='card']//input[@type='number' and @class='quantity']")


class ShopPage(BasePage):
    AGE_VERIFICATION_MODAL = (By.XPATH, "//div[@class='modal-content']")
    AGE_VERIFICATION_DOB = (
        By.XPATH, "//div[@class='modal-content']//input[@type='text' and @placeholder='DD-MM-YYYY']")
    AGE_VERIFICATION_CONFIRM_BUTTON = (By.XPATH, "//div[@class='modal-content']//button[text()='Confirm']")
    AGE_VERIFICATION_SUCCESS_MESSAGE = (By.XPATH, "//div[@role='status' and contains(text(), 'You are of age')]")
    AGE_VERIFICATION_FAILURE_MESSAGE = (By.XPATH, "//div[@role='status' and contains(text(), 'You are underage')]")
    ALCOHOL_CATEGORY = (By.XPATH, "//h4[text()='Category']/following-sibling::ul//a[text()='Alcohol']")

    PAGINATION_NEXT_BUTTON_NOT_DISABLED = (
    By.XPATH, "//button[@class='pagination-link' and not(@disabled) and text()='Next']")
    PAGE_NUMBERS = (By.XPATH, "//div[@class='page-numbers']//li")

    def enter_dob(self, dob):
        self.type_text(self.AGE_VERIFICATION_DOB, dob)
        return self

    def confirm_age_verification(self, dob):
        self.enter_dob(dob)
        self.click(self.AGE_VERIFICATION_CONFIRM_BUTTON)
        return self

    def is_age_verification_modal_visible(self):
        return self.is_visible(self.AGE_VERIFICATION_MODAL)

    def get_age_verification_message(self, verification_type):
        # messages = {
        #     "success": self.AGE_VERIFICATION_SUCCESS_MESSAGE,
        #     "fail": self.AGE_VERIFICATION_FAILURE_MESSAGE,
        # }
        # message_key = messages.get(verification_type.lower())
        # return self.get_text(message_key)
        if verification_type == "success":
            return self.get_text(self.AGE_VERIFICATION_SUCCESS_MESSAGE)
        if verification_type == "fail":
            return self.get_text(self.AGE_VERIFICATION_FAILURE_MESSAGE)

    def go_to_alcohol_category(self):
        self.click(self.ALCOHOL_CATEGORY)
        return self

    def wait_for_age_verification_modal_hidden(self, timeout=5):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(self.AGE_VERIFICATION_MODAL)
        )
        return self

    def find_product(self, product_name):
        product_locator = get_card_image_xpath(product_name)

        if self.is_visible(product_locator, timeout=5):
            return self.find(product_locator)

        number_of_pages = len(self.find_all(self.PAGE_NUMBERS))
        for _ in range(number_of_pages - 1):
            if not self.is_visible(self.PAGINATION_NEXT_BUTTON_NOT_DISABLED, timeout=1):
                break
            self.click(self.PAGINATION_NEXT_BUTTON_NOT_DISABLED)
            if self.is_visible(product_locator, timeout=1):
                return self.find(product_locator)

        raise TimeoutException(f"Product '{product_name}' was not found on any page.")

    def add_product_to_cart(self, product_name, quantity=1):
        self.find_product(product_name)

        product_add_to_cart_locator = get_add_to_cart_xpath_for_product(product_name)
        add_to_button = self.find(product_add_to_cart_locator)

        if quantity > 1:
            quantity_control_locator = get_quantity_xpath_for_product(product_name)
            self.type_text(quantity_control_locator, quantity)

        add_to_button.click()
        return self
