#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class BugSquash:
    def __init__(self, url: str) -> None:
        s = Service("./chromedriver")

        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.url = url
        self.driver.get(url)

    def get_web_vitals(self):
        with open("./web_vitals.js") as f:
            script = f.read()

        self.driver.execute_script(script)

        result_lcp = WebDriverWait(self.driver, timeout=5).until(
            lambda driver: driver.execute_script("return window.__selenium_lcp;")
        )

        result_cls = WebDriverWait(self.driver, timeout=5).until(
            lambda driver: driver.execute_script("return window.__selenium_cls;")
        )

        result_ttfb = WebDriverWait(self.driver, timeout=5).until(
            lambda driver: driver.execute_script("return window.__selenium_ttfb;")
        )

        span = self.driver.find_element(By.ID, "__selenium_span")
        ac = ActionChains(self.driver)
        ac.move_to_element(span).click().perform()

        result_fid = WebDriverWait(self.driver, timeout=5).until(
            lambda driver: driver.execute_script("return window.__selenium_fid;")
        )

        # performance = self.driver.execute_script(
        #     "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
        # )
        # ttfb = self.driver.execute_script(
        #     "return window.performance.timing.responseStart - window.performance.timing.fetchStart"
        # )

        self.driver.implicitly_wait(3)

        return {
            "ttfb": result_ttfb["responseStart"],
            "lcp": result_lcp["renderTime"],
            "cls": result_cls["value"],
            "fid": result_fid,
        }

    def fill_input_by_id(self, _id, _text):
        element = self.driver.find_element(By.ID, _id)
        element.send_keys(_text)

    def click_by_id(self, _id):
        element = self.driver.find_element(By.ID, _id)
        element.click()

    def check_url(self, url):
        return self.driver.current_url == url

    def get_first_form(self):
        return self.driver.find_element(By.TAG_NAME, "form")

    def exit(self):
        self.driver.quit()


if __name__ == "__main__":
    bug_squash = BugSquash("https://hackathon.bz.it/secure/login")

    print(bug_squash.get_web_vitals())

    bug_squash.fill_input_by_id("_username", "YOUR_USERNAME_HERE")
    bug_squash.fill_input_by_id("_password", "YOUR_PASSWORD_HERE")
    bug_squash.click_by_id("_submit")
    bug_squash.get_first_form().submit()
    print(bug_squash.check_url("https://hackathon.bz.it/secure/user"))

    bug_squash.exit()