from selenium import webdriver
import unittest

class RegistrationTest(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(10)
		self.driver.get("https://chaosforum-20b27.firebaseapp.com")

	def tearDown(self):
		self.driver.close()

	def testing1(self):
		self.assertIn("Chaos Forum", self.driver.title)
