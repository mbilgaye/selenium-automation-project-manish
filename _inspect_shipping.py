import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.shop_page import ShopPage
from tests.test_data.age_verification_test_data import OVER_18_DOB
from tests.test_data.authentication_test_data import AUTHENTICATION_TEST_DATA


def parse_price(text):
    match = re.search(r"([\d]+(?:[.,]\d+)?)", text.replace(",", "."))
    return float(match.group(1)) if match else None


def get_texts(driver):
    shipment = driver.find_element(By.CSS_SELECTOR, ".shipment-container h5:last-child").text
    subtotal = driver.find_element(By.CSS_SELECTOR, ".product-total-container h5:last-child").text
    total = driver.find_element(By.CSS_SELECTOR, ".total-container h5:last-child").text
    msg = driver.find_element(By.CSS_SELECTOR, ".free-shipment-message").text
    return shipment, subtotal, total, msg


def setup(driver):
    homepage = LoginPage(driver).open(LoginPage.URL).login(
        AUTHENTICATION_TEST_DATA["valid_username"],
        AUTHENTICATION_TEST_DATA["valid_password"],
    )
    shop_page = homepage.go_to_shop()
    if shop_page.is_age_verification_modal_visible():
        shop_page.confirm_age_verification(OVER_18_DOB)
        time.sleep(3)
    CartPage(driver).clear_cart()
    return shop_page


driver = webdriver.Chrome()
try:
    shop = setup(driver)
    for label, product, qty in [
        ("below", "Celery", 1),
        ("exact", "Kale", 20),
        ("above", "Kale", 21),
    ]:
        CartPage(driver).clear_cart()
        shop = ShopPage(driver)
        shop.open("https://grocerymate.masterschool.com/store")
        shop.add_product_to_cart(product, qty)
        driver.get("https://grocerymate.masterschool.com/checkout")
        time.sleep(1)
        s, sub, tot, msg = get_texts(driver)
        print(label, "raw:", s, sub, tot, msg)
        print(label, "parsed:", parse_price(s), parse_price(sub), parse_price(tot))
finally:
    driver.quit()
