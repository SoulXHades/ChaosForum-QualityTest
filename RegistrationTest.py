from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, time
from selenium.webdriver.common.action_chains import ActionChains
import random
import string

class RegistrationTest(unittest.TestCase):
	displayName = "limj020221"
	
	
	validEmailDomain= "e.ntu.edu.sg"
	invalidEmailDomain = "not.NTU.email.com"
	password = "abcde"
	
	number = '1'
	lowercaseAlpha = "a"
	uppercaseAlpha = "A"
	specialChar = "#"
	
	def setUp(self):
		self.driver = webdriver.Firefox()
		self.actions = ActionChains(self.driver)
		self.driver.implicitly_wait(10)
		self.driver.get("https://chaosforum-20b27.firebaseapp.com/#/signup")

	def tearDown(self):
		self.driver.close()

	def test_invalidPassword(self):
		self.driver.find_element_by_name("password").send_keys(self.password)
		self.driver.find_element_by_name("password").send_keys(Keys.TAB)
		time.sleep(1)

		invalid_feedback_arr = ["Password must be at least 8 characters long.","Password must have at least 1 special character","Password must have at least 1 uppercase character","Password must have at least 1 numeric character","Required"]
		inputs = ["fgh",self.specialChar,self.uppercaseAlpha,self.number,""]

		for i in range(0,len(invalid_feedback_arr)):
			invalid_feedback = self.driver.find_element_by_class_name("invalid-feedback").text
			self.assertEqual(invalid_feedback,invalid_feedback_arr[i])
			self.driver.find_element_by_name("password").send_keys(inputs[i])
			self.driver.find_element_by_name("password").send_keys(Keys.TAB)
			time.sleep(0.5)

	def test_matchDifferentPassword(self):
		password1 = self.password + self.uppercaseAlpha + self.lowercaseAlpha + self.number + self.specialChar
		password2 = self.password + self.uppercaseAlpha + self.lowercaseAlpha  + self.specialChar + self.number
		self.driver.find_element_by_name("password").send_keys(password1)
		self.driver.find_element_by_name("password2").send_keys(password2)
		invalid_feedback = self.driver.find_element_by_class_name("invalid-feedback").text
		self.assertEqual(invalid_feedback,"Password and Confirm password doesn't match")


	def test_invalidEmail(self):
		self.driver.find_element_by_name("email").send_keys(self.displayName+"@"+self.invalidEmailDomain)
		self.driver.find_element_by_name("email").send_keys(Keys.TAB)
		time.sleep(1)
		invalid_feedback = self.driver.find_element_by_class_name("invalid-feedback").text

		self.assertEqual(invalid_feedback,"Please use your NTU email")


	def test_existingUser(self):
		self.driver.find_element_by_name("displayName").send_keys(self.displayName)
		self.driver.find_element_by_name("email").send_keys(self.displayName+"@"+self.validEmailDomain)
		password = self.password +self.number + self.lowercaseAlpha + self.uppercaseAlpha + self.specialChar
		self.driver.find_element_by_name("password").send_keys(password)
		self.driver.find_element_by_name("password2").send_keys(password)
		
		container = self.driver.find_elements_by_class_name("form-group")[2]
		dropdowns = container.find_elements_by_class_name("css-1hwfws3")
		time.sleep(3)
		self.actions.move_to_element(dropdowns[0]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN)
		self.actions.move_to_element(dropdowns[1]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN).perform()
		time.sleep(2)
		self.driver.find_element_by_class_name("signup-button.btn.btn-primary").click()
		time.sleep(2)
		self.assertEqual(self.driver.find_element_by_class_name("toast.toast-error").text, "User already exist!")




	def test_correctRegistration(self):
		displayName = self.randomString(7)
		self.driver.find_element_by_name("displayName").send_keys(displayName)
		self.driver.find_element_by_name("email").send_keys(displayName+"@"+self.validEmailDomain)
		password = self.password +self.number + self.lowercaseAlpha + self.uppercaseAlpha + self.specialChar
		self.driver.find_element_by_name("password").send_keys(password)
		self.driver.find_element_by_name("password2").send_keys(password)
		
		container = self.driver.find_elements_by_class_name("form-group")[2]
		dropdowns = container.find_elements_by_class_name("css-1hwfws3")
		time.sleep(3)
		self.actions.move_to_element(dropdowns[0]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN)
		self.actions.move_to_element(dropdowns[1]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN).perform()
		time.sleep(2)
		self.driver.find_element_by_class_name("signup-button.btn.btn-primary").click()
		time.sleep(2)
		self.assertEqual(self.driver.find_element_by_class_name("toast.toast-success ").text, "Signup Success! Please check your email for verification.")

	def randomString(self,stringLength=10):
		"""Generate a random string of fixed length """
		letters = string.ascii_lowercase
		return ''.join(random.choice(letters) for i in range(stringLength))
	
# The password must be at least 8 characters long.
# The password must contain at least 1 numeric character.
# The password must contain at least 1 special character.
# The password must contain at least 1 lowercase character.
# The password must contain at least 1 uppercase character.

if __name__ == "__main__":
    unittest.main(verbosity=2)