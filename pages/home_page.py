from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):

    LOGOUT_LINK = (By.XPATH, "//a[@href='/auth' and text()='Log Out']")
    SHOP_LINK = (By.XPATH, "//ul[@class='anim-nav']//a[@href='/store']")

    def go_to_shop(self):
        self.click(self.SHOP_LINK)
        from pages.shop_page import ShopPage
        return ShopPage(self.driver)
