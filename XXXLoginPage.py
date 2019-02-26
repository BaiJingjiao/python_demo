import webium.settings
from selenium.webdriver import Chrome
webium.settings.driver_class = Chrome
import os
os.environ["webdriver.chrome.driver"] = "D:\\mytools\\auto_suite_python\\browser_drivers\\chromedriver.exe"

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from webium.controls.link import Link
from webium.driver import get_driver
from webium import BasePage, Find, Finds
import time

import sys
sys.path.append("D:\\mytools\\auto_suite_python")
from ecs.pages.change_password_page import *


class XXXLoginPage(BasePage):
    url = 'https://111.222.333.444:111111'

    username_input = Find(by=By.ID, value='username')
    password_input = Find(by=By.ID, value='password')
    login_btn = Find(by=By.ID, value='submitBtn')
    login_error_span = Find(by=By.ID, value='loginErrorMsg')

    def login_XXX(self, user='admin', pwd='dfdfsdfds'):
        self.open()
        self.username_input.send_keys(user)
        self.password_input.send_keys(pwd)
        self.login_btn.click()
        time.sleep(2)
        try:
            if self.login_error_span.is_displayed:
                #修改秘密
                self.password_input.clear()
                self.password_input.send_keys('dsfsfs')
                self.login_btn.click()
                change_pwd_page = ChangePasswordPage()
                change_pwd_page.change_password()
                #重新登录
                self.open()
                self.username_input.send_keys(user)
                self.password_input.send_keys(pwd)
                self.login_btn.click()
            else:
                return
        except:
            pass
