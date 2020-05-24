# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestRegister():
  def setup_method(self, method):
    self.driver = webdriver.Firefox()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_register(self):
    self.driver.get("http://127.0.0.1:5000/login?next=%2F")
    self.driver.set_window_size(550, 680)
    self.driver.find_element(By.LINK_TEXT, "Sign Up Here!").click()
    self.driver.find_element(By.LINK_TEXT, "Home").click()
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.LINK_TEXT, "Sign Up Here!").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("susan")
    self.driver.find_element(By.ID, "email").send_keys("susan@example.com")
    self.driver.find_element(By.ID, "password").send_keys("cat")
    self.driver.find_element(By.ID, "password_2").send_keys("cat")
    self.driver.find_element(By.ID, "administrator").click()
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").click()
    element = self.driver.find_element(By.ID, "email")
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("cat")
    self.driver.find_element(By.ID, "password_2").send_keys("cat")
    self.driver.find_element(By.CSS_SELECTOR, "p:nth-child(6)").click()
    self.driver.find_element(By.ID, "administrator").click()
    self.driver.find_element(By.ID, "submit").click()
    self.driver.find_element(By.ID, "username").click()
    self.driver.find_element(By.ID, "username").send_keys("luke")
    self.driver.find_element(By.ID, "email").send_keys("luke@example.com")
    self.driver.find_element(By.ID, "password").send_keys("loop")
    self.driver.find_element(By.ID, "password_2").send_keys("loop")
    self.driver.find_element(By.ID, "administrator").click()
    self.driver.find_element(By.ID, "submit").click()
    self.driver.close()
  
