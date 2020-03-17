from selenium import webdriver
import unittest

class RegistrationTest(unittest.TestCase):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.driver = webdriver.Firefox()
		self.driver.get("https://chaosforum-20b27.firebaseapp.com/#/home")

	def testing1(self):
		self.assertIn("Chaos Forum", self.driver.title)

	def __del__(self):
		self.driver.close();
