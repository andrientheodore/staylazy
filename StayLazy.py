from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re
import logging

class StayLazyCheckIn(unittest.TestCase):
    def setUp(self):
        print("[+] Initializing firefox driver..")
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(executable_path="FULL_PATH_TO_GECKODRIVER", options=self.options)
        print("[+] Initializing firefox addons..")
        self.driver.install_addon("FULL_PATH_TO_FIREFOX_ADD_ON", temporary=True)
        self.driver.maximize_window()
        self.base_url = "https://www.google.com/"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_untitled_test_case(self):
        logging.basicConfig(format="%(asctime)s %(message)s", filename="StaySafe.log", level=logging.INFO)
        driver = self.driver
        print("[+] Loading StaySafe Web..")
        driver.get("https://apps.powerapps.com/play/b07d6180-7878-4b00-8a10-86a968dd27b1")
        print("[+] Sleep for 15 seconds to allow the website to load..")
        time.sleep(15)
        driver.switch_to.frame(0)
        try:
            print("[+] Check Login..")
            if self.driver.find_element_by_xpath("//body/div/div[2]/div[2]/div/button").is_displayed():
                print("[+] Logging in..")
                self.driver.find_element_by_xpath("//body/div/div[2]/div[2]/div/button").click()
        except NoSuchElementException:
            print("[+] No login required..")

        print("[+] Check if you already declare staysafe for today..")        
        try: 
            if driver.find_element_by_xpath("//div[@id='publishedCanvas']/div/div[3]/div/div/div[19]/div/div/div/div/button/div").is_displayed():
                print("[+] You already declare staysafe..")
                print("[+] Terminating..")
                logging.info("Already declare staysafe..")
                return True
        except NoSuchElementException: 
            print("[+] Declaring staysafe..") 
            driver.find_element_by_xpath("//div[@id='publishedCanvas']/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[12]/div/div/div/div/div[2]/div[3]").click()
            driver.find_element_by_xpath("//div[@id='publishedCanvas']/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[6]/div/div/div/div[8]/div/div/div/div/div[2]/div[2]").click()
            driver.find_element_by_xpath("(//input[contains(@tabindex,'120')])").click()
            driver.find_element_by_xpath("(//input[contains(@tabindex,'96')])").click()
            driver.find_element_by_xpath("(//input[contains(@value,'No')])[2]").click()
            driver.find_element_by_xpath("(//*[@id='publishedCanvas']/div/div[2]/div/div/div[19]/div/div/div/div/button/div)").click()
            time.sleep(5)
            print("[+] Declared succesfully..")
            logging.info("StaySafe declared succesfully")
            return True

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
