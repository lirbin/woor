# -*- coding:utf-8 -*-

from selenium import webdriver
import unittest
import time


class MyTest(unittest.TestCase):
    dr = webdriver.Chrome()

    def setUp(self,driver= dr):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.baidu.com"
        self.verificationErrors = []
        self.accept_next_alert = True

    def tearDown(self):
        try:
            self.driver.refresh()
        except ConnectionRefusedError as e:
            print(e)
        finally:
            self.assertEqual([],self.verificationErrors)

    def testLoginBaidu(self):
        driver = self.driver
        driver.get(self.base_url)
        self.assertEqual(driver.title,"百度一下，你就知道")

    def testSearchSelenium(self):
        driver = self.driver
        driver.find_element_by_id("kw").send_keys("Selenium")
        driver.find_element_by_id("su").click()
        time.sleep(3)
        print('driver.title:', driver.title)
        self.assertEqual(driver.title, "Selenium_百度搜索")




if __name__ == '__main__':
    unittest.main()