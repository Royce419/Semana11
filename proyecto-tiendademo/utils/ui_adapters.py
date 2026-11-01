import sys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class SeleniumUI:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    def click(self, selector):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector))).click()
    def fill(self, selector, value):
        element = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        if element.get_attribute("type") == "number":
            element.send_keys(Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL, "a")
            element.send_keys(value)
        else:
            element.clear()
            element.send_keys(value)
    def text(self, selector):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).text
    def visible(self, selector):
        return any(e.is_displayed() for e in self.driver.find_elements(By.CSS_SELECTOR, selector))
    def value(self, selector):
        return self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector))).get_attribute("value")
    def screenshot(self, path):
        self.driver.save_screenshot(str(path))

class PlaywrightUI:
    def __init__(self, page):
        self.page = page
    def click(self, selector):
        self.page.locator(selector).click()
    def fill(self, selector, value):
        self.page.locator(selector).fill(value)
    def text(self, selector):
        self.page.locator(selector).wait_for(state="visible")
        return self.page.locator(selector).inner_text()
    def visible(self, selector):
        return self.page.locator(selector).is_visible()
    def value(self, selector):
        return self.page.locator(selector).input_value()
    def screenshot(self, path):
        self.page.screenshot(path=str(path), full_page=True)
