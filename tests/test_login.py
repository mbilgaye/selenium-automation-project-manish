from pages.login_page import LoginPage


def test_login(driver):
    login_page = LoginPage(driver).open(LoginPage.URL)
    homepage = login_page.login("johndoe@example.com", "admin123")
    assert homepage.is_visible(homepage.LOGOUT_LINK)