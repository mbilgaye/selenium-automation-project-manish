from selenium.webdriver.common.by import By

from pages.base_page import BasePage


def plus_button(self, product_name):
    return (
        By.XPATH,
        f"//h5[normalize-space()='{product_name}']/parent::div//button[@class='plus']"
    )


def minus_button(self, product_name):
    return (
        By.XPATH,
        f"//h5[normalize-space()='{product_name}']/parent::div//button[@class='minus']"
    )


class CartPage(BasePage):
    URL = "https://grocerymate.masterschool.com/checkout"

    REMOVE_ITEM_LINK = (By.CSS_SELECTOR, "a.remove-icon")
    CART_ITEM = (By.CSS_SELECTOR, ".checkout-card-item-container")
    SHIPPING_COST = (By.CSS_SELECTOR, ".shipment-container h5:last-child")
    SUBTOTAL = (By.CSS_SELECTOR, ".product-total-container h5:last-child")
    TOTAL = (By.CSS_SELECTOR, ".total-container h5:last-child")
    FREE_SHIPPING_MESSAGE = (By.CSS_SELECTOR, ".free-shipment-message")
    QUANTITY_INPUT = (By.CSS_SELECTOR, "input.quantity-input")

    def clear_cart(self):
        """Remove all products from the cart. Safe to call when the cart is already empty."""
        if "/checkout" not in self.get_url():
            self.open(self.URL)

        while self.is_visible(self.REMOVE_ITEM_LINK, timeout=1):
            self.click(self.REMOVE_ITEM_LINK)

        return self

    def get_cart_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEM))

    def get_shipping_cost(self):
        text = self.get_text(self.SHIPPING_COST)
        return self._parse_price(text)

    def get_subtotal(self):
        # Wait until subtotal parsed price is greater than 0.0
        self.wait.until(
            lambda d: self._parse_price(d.find_element(*self.SUBTOTAL).text) > 0.0
        )
        text = self.get_text(self.SUBTOTAL)
        return self._parse_price(text)

    def get_total(self):
        text = self.get_text(self.TOTAL)
        return self._parse_price(text)

    def get_free_shipping_message(self):
        if self.is_visible(self.FREE_SHIPPING_MESSAGE, timeout=2):
            return self.get_text(self.FREE_SHIPPING_MESSAGE)
        return ""

    def update_item_quantity(self, quantity):

        return self

    def _parse_price(self, text):
        import re
        match = re.search(r"([\d]+(?:[.,]\d+)?)", text.replace(",", "."))
        return float(match.group(1)) if match else 0.0
