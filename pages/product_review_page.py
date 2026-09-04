from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProductReviewPage(BasePage):

    REVIEW_SECTION = (
        By.CSS_SELECTOR,
        "section.new-review-section"
    )

    COMMENT_TEXTAREA = (
        By.CSS_SELECTOR,
        "textarea.new-review-form-control"
    )

    REVIEW_RESTRICTION_MESSAGE = (
        By.XPATH,
        "//div[@class='reviewRestriction']//p"
    )

    SEND_BUTTON = (
        By.XPATH,
        "//button[@class='new-review-btn new-review-btn-send']"
    )

    CANCEL_BUTTON = (
        By.CSS_SELECTOR,
        "button.new-review-btn-cancel"
    )

    CHARACTER_COUNTER = (
        By.CSS_SELECTOR,
        ".new-review-char-counter span"
    )

    def star(self, rating):
        return (
            By.XPATH,
            f"(//div[contains(@class,'interactive-rating')]//span[contains(@class,'star')])[{rating}]"
        )

    def select_rating(self, rating):
        self.click(self.star(rating))
        return self

    def enter_comment(self, comment):
        self.type_text(self.COMMENT_TEXTAREA, comment)
        return self

    def submit_review(self):
        self.click(self.SEND_BUTTON)
        return self

    def cancel_review(self):
        self.click(self.CANCEL_BUTTON)
        return self

    def get_character_counter(self):
        return self.get_text(self.CHARACTER_COUNTER)

    def submit_product_review(self, rating, comment=""):
        self.select_rating(rating)

        if comment:
            self.enter_comment(comment)

        self.submit_review()
        return self

    def get_review_restriction_message(self):
        return self.get_text(self.REVIEW_RESTRICTION_MESSAGE)

    def is_review_restriction_visible(self):
        return self.is_visible(self.REVIEW_RESTRICTION_MESSAGE, timeout=5)
