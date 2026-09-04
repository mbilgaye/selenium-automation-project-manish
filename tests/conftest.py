import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    options.add_argument("--disable-features=PasswordManagerEnabled,PasswordLeakDetection")
    options.add_experimental_option("prefs", prefs)
    web_driver = webdriver.Chrome(options=options)
    web_driver.delete_all_cookies()
    yield web_driver
    web_driver.quit()
