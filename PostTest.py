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
	'''def test_PostWithoutLogin(self):
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
		self.postButton = self.driver.find_element_by_class_name("btn.btn-info.disabled")'''

	###################################### Edit own post ######################################

	def test_editOwnPost_user(self):
		Automate.login(self.driver, False)
		self.editOwnPost(False)

	def test_editOwnPost_mod(self):
		Automate.login(self.driver, True)
		self.editOwnPost(True)

	def editOwnPost(self, isMod):
		Automate.navigateToSelectiveThread(self.driver, 4)
		Automate.writeAPost(self.driver, "Testing testing")

		firstPost = self.driver.find_elements_by_class_name("post-card.card")[0]
		# click post options then click the edit button on the latest post we created for this test
		postOptionButton = firstPost.find_element_by_class_name("post-dropdown")
		postOptionButton.click()
		postOptionsList = firstPost.find_elements_by_class_name("dropdown-item")
		for i in range(len(postOptionsList)):
			if postOptionsList[0].text == "edit":
				postOptionsList[0].click()
			# postEditButton = firstPost.find_elements_by_class_name("dropdown-item")[0]
			# postEditButton.click()

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


	###################################### Edit any post ######################################

	'''def test_editAnyPost_user(self):
		self.editAnyPost(False)

	def test_editAnyPost_mod(self):
		self.editAnyPost(True)

	def editAnyPost(self, isMod):
		if isMod:
			# log in mod account to post at the 1st thread
			Automate.login(self.driver, False)
		else:
			# log in mod account to post at the 1st thread
			Automate.login(self.driver, True)

		# navigate to first thread and create a post
		Automate.navigateToSelectiveThread(self.driver, 0)
		Automate.writeAPost(self.driver, "AAA")

		if isMod:
			# user account do not have control panel so logout button is 1st option in the list
			Automate.logout(self.driver, 0)
			# login moderator account to test if it can edit other people's (for this case is the user's) post at the 1st thread
			Automate.login(self.driver, True)
		else:
			# moderator account have control panel as the 1st option of the list while logout button is 2nd option in the list
			Automate.logout(self.driver, 1)
			# login user account to test if it can edit other people's (for this case is the mod's) post at the 1st thread
			Automate.login(self.driver, False)

		# navigate to first thread
		Automate.navigateToSelectiveThread(self.driver, 0)

		# click post options then click the edit button on the latest post we created for this test
		postOptionButton = self.driver.find_elements_by_class_name("post-dropdown")[0]
		postOptionButton.click()

		if isMod:
			# get first item in the post option list
			dropDownFirstItem = self.driver.find_elements_by_class_name("dropdown-item")[2]
			# only moderator account can edit other people's post hence the 1st option should be "Edit"
			self.assertEqual(dropDownFirstItem.text, "Edit")
			# click on the edit button and write content to it
			dropDownFirstItem.click()
		else:
			# get first item in the post option list
			dropDownFirstItem = self.driver.find_elements_by_class_name("dropdown-item")[1]
			# user cannot edit other people's post. Hence the 1st option should be "Report post"
			self.assertEqual(dropDownFirstItem.text, "Report post")

	###################################### Delete own post ######################################

	def test_deleteOwnPost_user(self):
		Automate.login(self.driver, False)
		self.deleteOwnPost(False)

	def test_deleteOwnPost_mod(self):
		Automate.login(self.driver, True)
		self.deleteOwnPost(True)

	def deleteOwnPost(self, isMod):
		Automate.navigateToSelectiveThread(self.driver, 0)
		Automate.writeAPost(self.driver, "Testing testing")

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


	###################################### Delete any post ######################################

	def test_editAnyPost_user(self):
		self.editAnyPost(False)

	def test_editAnyPost_mod(self):
		self.editAnyPost(True)

	def editAnyPost(self, isMod):
		if isMod:
			# log in mod account to post at the 1st thread
			Automate.login(self.driver, False)
		else:
			# log in mod account to post at the 1st thread
			Automate.login(self.driver, True)

		# navigate to first thread and create a post
		Automate.navigateToSelectiveThread(self.driver, 0)
		Automate.writeAPost(self.driver, "AAA")

		if isMod:
			# user account do not have control panel so logout button is 1st option in the list
			Automate.logout(self.driver, 0)
			# login moderator account to test if it can edit other people's (for this case is the user's) post at the 1st thread
			Automate.login(self.driver, True)
		else:
			# moderator account have control panel as the 1st option of the list while logout button is 2nd option in the list
			Automate.logout(self.driver, 1)
			# login user account to test if it can edit other people's (for this case is the mod's) post at the 1st thread
			Automate.login(self.driver, False)

		# navigate to first thread
		Automate.navigateToSelectiveThread(self.driver, 0)

		# click post options then click the edit button on the latest post we created for this test
		postOptionButton = self.driver.find_elements_by_class_name("post-dropdown")[0]
		postOptionButton.click()

		if isMod:
			# get first item in the post option list
			dropDownFirstItem = self.driver.find_elements_by_class_name("dropdown-item")[2]
			# only moderator account can edit other people's post hence the 1st option should be "Edit"
			self.assertEqual(dropDownFirstItem.text, "Edit")
		else:
			# get first item in the post option list
			dropDownFirstItem = self.driver.find_elements_by_class_name("dropdown-item")[1]
			# user cannot edit other people's post. Hence the 1st option should be "Report post"
			self.assertEqual(dropDownFirstItem.text, "Report post")'''


if __name__ == "__main__":
    unittest.main(verbosity=2)
