import time

import pytest

from pages.login_page import LoginPage
from pages.product_review_page import ProductReviewPage
from tests.test_data.age_verification_test_data import OVER_18_DOB
from tests.test_data.authentication_test_data import AUTHENTICATION_TEST_DATA
from tests.test_data.product_review_test_data import PRODUCT_REVIEW_TEST_DATA


@pytest.mark.parametrize(
    "case_label,product, rating, comment",
    PRODUCT_REVIEW_TEST_DATA,
    ids=[case[0] for case in PRODUCT_REVIEW_TEST_DATA]
)
def test_submit_product_review(
        driver,
        case_label,
        product,
        rating,
        comment
):
    login_page = LoginPage(driver).open(LoginPage.URL)

    home_page = login_page.login(
        AUTHENTICATION_TEST_DATA["valid_username"],
        AUTHENTICATION_TEST_DATA["valid_password"]
    )

    shop_page = home_page.go_to_shop()
    if shop_page.is_age_verification_modal_visible():
        shop_page.confirm_age_verification(OVER_18_DOB)
        shop_page.wait_for_age_verification_modal_hidden()
    product = shop_page.find_product(product_name=product)

    product.click()

    review_page = ProductReviewPage(driver)

    if review_page.is_review_restriction_visible():
        assert (
                review_page.get_review_restriction_message()
                == "You have already reviewed this product."
        )
        return

    review_page.submit_product_review(
        rating=rating,
        comment=comment,
    )

    assert review_page.is_review_restriction_visible()
    assert (
            review_page.get_review_restriction_message()
            == "You have already reviewed this product."
    )
