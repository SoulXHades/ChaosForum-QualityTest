from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import time
import unittest
import Automate

class PostTest(unittest.TestCase):
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)

	# 	self.driver = webdriver.Firefox()
	# 	self.driver.get("https://chaosforum-20b27.firebaseapp.com/#/home")

	# # need set longer delay else test scripts execute without page fully loaded yet, causing elements not found errors
	# # def setUp(self):
	# # 	self.driver.implicitly_wait(5)

	# def __del__(self):
	# 	self.driver.close();

	def setUp(self):
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(10)
		self.driver.get("https://chaosforum-20b27.firebaseapp.com")

	def tearDown(self):
		self.driver.close()

	###################################### Test Cases ######################################

	# check if page will not allow user to post and there will be an element prompting to login/signup first
	def test_PostWithoutLogin(self):
		try:
			# to check the status of the login button see if it is not login before proceeding
			loginButtonStatus = self.driver.find_element_by_class_name("dropdown-toggle.nav-link")
		except selenium.common.exceptions.NoSuchElementException as e:
			# no need logout cause not login
			pass
		else:
			# to logout since is login as can find the dropdown toggle button which only login then appear
			# have a few elements with the same class name. The button to logout is the first element with that class name
			logoutButton = self.driver.find_elements_by_class_name("dropdown-item")[0]
			# click to logout
			logoutButton.click()

		self.navigateToSelectiveThread(0)

		# delay 5 sec to let page load
		#self.driver.implicitly_wait(5)
		# if cannot find then throw exception means fail test case
		promptLogin = self.driver.find_element_by_class_name("login-prompt-text")

	def test_ableToWriteOrUploadPicInPost(self):
		Automate.login(self.driver, False)
		# thread selected should not be too close to thread 0 (top thread as new post bump threads to the top.
		# May cause different test case function to race condition the posts in the same thread
		self.navigateToSelectiveThread(4)

		# write post content and click the post button to post
		testMsg = "Testing 123"
		self.writeAPost(testMsg)

		# delay 5 sec to let page update to show the new post before comparing the content
		time.sleep(5)
		# see if the test post is successfully created
		latestPost = self.driver.find_elements_by_class_name("card-text")[0]
		self.assertEqual(latestPost.text, testMsg)

	def test_postWithoutContent(self):
		Automate.login(self.driver, False)
		# navigate to first thread on the homepage
		self.navigateToSelectiveThread(0)

		# if can find button with class name "btn.btn-info.disabled", means the button is disabled since we didn't write any content
		self.postButton = self.driver.find_element_by_class_name("btn.btn-info.disabled")

		# write content to post's textbox again and see if the button will be disabled once there is no content
		postTxtBox = self.driver.find_element_by_class_name("form-control")
		postTxtBox.send_keys("AAA")
		# check if the post button is toggled to enable to post
		postButton = self.driver.find_element_by_class_name("btn.btn-info")
		postTxtBox.clear()
		# see if the post button is toggled backed to disabled now that the content is empty
		self.postButton = self.driver.find_element_by_class_name("btn.btn-info.disabled")

	def test_editOwnPost(self):
		Automate.login(self.driver, False)
		# thread selected should not be too close to thread 0 (top thread as new post bump threads to the top.
		# May cause different test case function to race condition the posts in the same thread
		self.navigateToSelectiveThread(4)
		self.writeAPost("Testing testing")

		# delay 5 sec to let page update to load the new post into the page
		time.sleep(5)
		# click post options then click the edit button on the latest post we created for this test
		postOptionButton = self.driver.find_elements_by_class_name("post-dropdown")[0]
		postOptionButton.click()
		# there are many dropdown items with the same class name in the same page. So have to find the right one we wants to click
		postEditButton = self.driver.find_elements_by_class_name("dropdown-item")[1]
		postEditButton.click()

		# write post content and click the post button to post
		newEditedPostContent = "Hello!"
		postEditTxtBox = self.driver.find_elements_by_class_name("form-control")[1]
		# clear post's content
		postEditTxtBox.clear()
		postEditTxtBox.send_keys(newEditedPostContent)
		# cause have 2 button of the same class name in the same page as one is for the create new post an another is save edited post
		postButton = self.driver.find_elements_by_class_name("btn.btn-info")[1]
		postButton.click()

		# delay 5 sec to let page update the new post's content before comparing the content
		time.sleep(5)
		# see if the test post is successfully created
		latestPost = self.driver.find_elements_by_class_name("card-text")[0]
		self.assertEqual(latestPost.text, newEditedPostContent)


	###################################### Own Functions ######################################
	# login into the forum
	def login(self):
		try:
			# to check the status of the login button see if it is not login before proceeding
			loginButtonStatus = self.driver.find_element_by_class_name("dropdown-toggle.nav-link")
		except selenium.common.exceptions.NoSuchElementException as e:
			# if enters exception block means never
			# search for login button then click it to navigate to the login page
			loginButton = self.driver.find_element_by_class_name("btn.btn-outline-info")
			loginButton.click()

			# delay 5 sec to let page load
			self.driver.implicitly_wait(5)
			# input username and password before logging in via pressing the ENTER button
			usernameTxtBox = self.driver.find_elements_by_class_name("form-control")[0]
			usernameTxtBox.send_keys("C170095@e.ntu.edu.sg")
			passwdTxtBox = self.driver.find_elements_by_class_name("form-control")[1]
			passwdTxtBox.send_keys("C170095@e.ntu.edu.sg")
			passwdTxtBox.send_keys(Keys.ENTER)

	# navigate into the top thread from the list of threads on the home page
	def navigateToSelectiveThread(self, threadIndex):
		# delay 5 sec to let page load
		self.driver.implicitly_wait(7)
		# to enter the first thread on the list of threads in the home page
		thread = self.driver.find_elements_by_class_name("thread-card.card")[threadIndex]
		thread.click()

	# to post a content on a thread
	def writeAPost(self, postContent):
		# write post content and click the post button to post
		postTxtBox = self.driver.find_element_by_class_name("form-control")
		postTxtBox.send_keys(postContent)
		postButton = self.driver.find_element_by_class_name("btn.btn-info")
		postButton.click()
