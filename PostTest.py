from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium
import time
import unittest
import Automate

class PostTest(unittest.TestCase):
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

		Automate.navigateToSelectiveThread(self.driver, 0)

		# delay 5 sec to let page load
		#self.driver.implicitly_wait(5)
		# if cannot find then throw exception means fail test case
		promptLogin = self.driver.find_element_by_class_name("login-prompt-text")


	###################################### Able to write/upload picture in post ######################################

	def test_ableToWriteOrUploadPicInPost_user(self):
		Automate.login(self.driver, False)
		self.ableToWriteOrUploadPicInPost()


	def test_ableToWriteOrUploadPicInPost_mod(self):
		Automate.login(self.driver, True)
		self.ableToWriteOrUploadPicInPost()

	def ableToWriteOrUploadPicInPost(self):
		Automate.navigateToSelectiveThread(self.driver, 4)

		# write post content and click the post button to post
		testMsg = "Testing 123"
		Automate.writeAPost(self.driver, testMsg)

		# delay 5 sec to let page update to show the new post before comparing the content
		time.sleep(5)
		# see if the test post is successfully created
		latestPost = self.driver.find_elements_by_class_name("card-text")[0]
		self.assertEqual(latestPost.text, testMsg)

	###################################### Post without content ######################################

	def test_postWithoutContent_user(self):
		Automate.login(self.driver, False)
		self.postWithoutContent()

	def test_postWithoutContent_mod(self):
		Automate.login(self.driver, True)
		self.postWithoutContent()

	def postWithoutContent(self):
		# navigate to first thread on the homepage
		Automate.navigateToSelectiveThread(self.driver, 0)

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

	###################################### Edit own post ######################################

	def test_editOwnPost_user(self):
		Automate.login(self.driver, False)
		self.editOwnPost()

	def test_editOwnPost_mod(self):
		Automate.login(self.driver, True)
		self.editOwnPost()

	def editOwnPost(self):
		Automate.navigateToSelectiveThread(self.driver, 4)
		Automate.writeAPost(self.driver, "Testing testing")

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
		# see if the post is successfully edited
		latestPost = self.driver.find_elements_by_class_name("card-text")[0]
		self.assertEqual(latestPost.text, newEditedPostContent)
		# see if the edited post reflect it has been edited
		self.driver.find_elements_by_class_name("edited")[0]

	###################################### Delete own post ######################################

	'''def test_deleteOwnPost_user(self):
		Automate.login(self.driver, False)
		self.deleteOwnPost(False)

	def test_deleteOwnPost_mod(self):
		Automate.login(self.driver, True)
		self.deleteOwnPost(True)

	def deleteOwnPost(self, isMod):
		Automate.navigateToSelectiveThread(self.driver, 0)
		Automate.writeAPost(self.driver, "Testing testing")

		# delay 5 sec to let page update to load the new post into the page
		time.sleep(5)

		# get the list of posts
		listOfPosts = self.driver.find_elements_by_class_name("post-card.card")

		# click post options then click the edit button on the latest post we created for this test
		postOptionButton = self.driver.find_elements_by_class_name("post-dropdown")[0]
		postOptionButton.click()
		# there are many dropdown items with the same class name in the same page. So have to find the right one we wants to click
		# to delete the post we have just created
		if isMod:
			postDeleteButton = self.driver.find_elements_by_class_name("dropdown-item")[3]
		else:
			postDeleteButton = self.driver.find_elements_by_class_name("dropdown-item")[2]
		postDeleteButton.click()

		# to click the confirm delete button when being prompted before delete
		self.driver.implicitly_wait(7)
		confirmDeleteButton = self.driver.find_element_by_class_name("btn.btn-danger")
		confirmDeleteButton.click()

		# delay 5 sec to let page update to load the new post into the page
		time.sleep(3)
		# get the list of posts after deleting a post
		newListOfPosts = self.driver.find_elements_by_class_name("post-card.card")
		# check if the number of posts in the thread should be reduced by 1 means successfully deleted that post
		self.assertEqual(len(listOfPosts)-1, len(newListOfPosts))


	###################################### Edit any post ######################################

	def test_editAnyPost_user(self):
		Automate.login(self.driver, False)
		self.editAnyPost()

	def test_editAnyPost_mod(self):
		Automate.login(self.driver, True)
		self.editAnyPost()

	def editAnyPost(self):
		pass'''


if __name__ == "__main__":
    unittest.main(verbosity=2)
