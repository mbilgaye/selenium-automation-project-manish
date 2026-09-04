import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login_page import LoginPage
from pages.cart_page import CartPage
from tests.test_data.age_verification_test_data import OVER_18_DOB
from tests.test_data.authentication_test_data import AUTHENTICATION_TEST_DATA


def setup_cart_with_product(driver, product_name, quantity):
    # 1. Login
    login_page = LoginPage(driver).open(LoginPage.URL)
    homepage = login_page.login(
        AUTHENTICATION_TEST_DATA["valid_username"],
        AUTHENTICATION_TEST_DATA["valid_password"]
    )

    # 2. Go to shop and confirm age verification if visible
    shop_page = homepage.go_to_shop()
    if shop_page.is_age_verification_modal_visible():
        shop_page.confirm_age_verification(OVER_18_DOB)
        shop_page.wait_for_age_verification_modal_hidden()

    # 3. Clear cart to start fresh
    cart_page = CartPage(driver).clear_cart()

    # 4. Add product to cart
    shop_page.open("https://grocerymate.masterschool.com/store")
    shop_page.add_product_to_cart(product_name, quantity)

    # 5. Navigate to checkout
    cart_page.open(CartPage.URL)
    return cart_page


def test_shipping_cost_below_threshold(driver):
    """
    SC-001 — Below threshold applies shipping fee
    Preconditions: Cart total < 20.00
    Expected: Shipping fee 5.00 applied, Total = subtotal + shipping
    """
    cart_page = setup_cart_with_product(driver, "Kale", 19)

    subtotal = cart_page.get_subtotal()
    shipping = cart_page.get_shipping_cost()
    total = cart_page.get_total()
    msg = cart_page.get_free_shipping_message()

    assert subtotal == 19.00, f"Expected subtotal to be 19.00, but got {subtotal}"
    assert shipping == 5.00, f"Expected shipping fee to be 5.00, but got {shipping}"
    assert total == 24.00, f"Expected total to be 24.00, but got {total}"
    assert "20" in msg, f"Expected free shipping message to mention threshold 20, but got '{msg}'"


def test_shipping_cost_exactly_threshold(driver):
    """
    SC-002 — Exactly threshold behavior
    Preconditions: Cart total equals exactly 20.00
    Expected: Shipping is free (inclusive rule)
    """
    cart_page = setup_cart_with_product(driver, "Kale", 20)

    subtotal = cart_page.get_subtotal()
    shipping = cart_page.get_shipping_cost()
    total = cart_page.get_total()

    assert subtotal == 20.00, f"Expected subtotal to be 20.00, but got {subtotal}"
    assert shipping == 0.00, f"Expected shipping to be free (0.00), but got {shipping}"
    assert total == 20.00, f"Expected total to be 20.00, but got {total}"


def test_shipping_cost_above_threshold(driver):
    """
    SC-003 — Above threshold grants free shipping
    Preconditions: Cart total > 20.00
    Expected: Shipping cost = 0, Total = subtotal
    """
    cart_page = setup_cart_with_product(driver, "Kale", 21)

    subtotal = cart_page.get_subtotal()
    shipping = cart_page.get_shipping_cost()
    total = cart_page.get_total()

    assert subtotal == 21.00, f"Expected subtotal to be 21.00, but got {subtotal}"
    assert shipping == 0.00, f"Expected shipping to be free (0.00), but got {shipping}"
    assert total == 21.00, f"Expected total to be 21.00, but got {total}"


def test_shipping_cost_dynamic_recalculation(driver):
    """
    SC-004 — Dynamic recalculation when quantity changes
    Preconditions: Cart near threshold
    Steps: Increase quantity to cross threshold -> Decrease quantity below threshold
    Expected: Shipping recalculates immediately and correctly without refresh
    """
    cart_page = setup_cart_with_product(driver, "Kale", 19)

    assert cart_page.get_subtotal() == 19.00
    assert cart_page.get_shipping_cost() == 5.00
    assert cart_page.get_total() == 24.00

    # Increase quantity to 20 to cross threshold
    cart_page.update_item_quantity(20)

    # Wait for dynamic update
    WebDriverWait(driver, 10).until(
        lambda d: print(
            f"Polling subtotal (target 20.00): {cart_page.get_subtotal()}") or cart_page.get_subtotal() == 20.00
    )

    assert cart_page.get_shipping_cost() == 0.00
    assert cart_page.get_total() == 20.00

    # Decrease quantity back to 19 to go below threshold
    cart_page.update_item_quantity(19)

    # Wait for dynamic update
    WebDriverWait(driver, 10).until(
        lambda d: print(
            f"Polling subtotal (target 19.00): {cart_page.get_subtotal()}") or cart_page.get_subtotal() == 19.00
    )

    assert cart_page.get_shipping_cost() == 5.00
    assert cart_page.get_total() == 24.00
