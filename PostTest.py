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

		# use the 1st post since it is the post we have just written
		firstPost = self.driver.find_elements_by_class_name("post-card.card")[0]
		# click post options then click the edit button on the latest post we created for this test
		postOptionButton = firstPost.find_element_by_class_name("post-dropdown")
		postOptionButton.click()
		# get a list of post options then search for the "Edit" option
		postOptionsList = firstPost.find_elements_by_class_name("dropdown-item")
		for i in range(len(postOptionsList)):
			if postOptionsList[i].text == "Edit":
				postOptionsList[i].click()
				break

		# write post content and click the post button to post
		newEditedPostContent = "Hello!"
		postEditTxtBox = firstPost.find_element_by_class_name("form-control")
		# clear post's content
		postEditTxtBox.clear()
		postEditTxtBox.send_keys(newEditedPostContent)
		# cause have 2 button of the same class name in the same page as one is for the create new post an another is save edited post
		postButton = firstPost.find_element_by_class_name("btn.btn-info")
		postButton.click()

		# delay 5 sec to let page update the new post's content before comparing the content
		time.sleep(5)
		# see if the post is successfully edited
		firstPostText = firstPost.find_element_by_class_name("card-text")
		self.assertEqual(firstPostText.text, newEditedPostContent)
		# see if the edited post reflect it has been edited
		firstPost.find_element_by_class_name("edited")


	###################################### Edit any post ######################################

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
			Automate.logout(self.driver)
			# login moderator account to test if it can edit other people's (for this case is the user's) post at the 1st thread
			Automate.login(self.driver, True)
		else:
			# moderator account have control panel as the 1st option of the list while logout button is 2nd option in the list
			Automate.logout(self.driver)
			# login user account to test if it can edit other people's (for this case is the mod's) post at the 1st thread
			Automate.login(self.driver, False)

		# navigate to first thread
		Automate.navigateToSelectiveThread(self.driver, 0)

		# use the 1st post since it is the post we have just written
		firstPost = self.driver.find_elements_by_class_name("post-card.card")[0]
		# click post options then click the edit button on the latest post we created for this test
		postOptionButton = firstPost.find_element_by_class_name("post-dropdown")
		postOptionButton.click()
		# get a list of post options then search for the "Edit" option
		postOptionsList = firstPost.find_elements_by_class_name("dropdown-item")

		if isMod:
			for i in range(len(postOptionsList)):
				if postOptionsList[i].text == "Edit":
					postOptionsList[i].click()
					break

			# write post content and click the post button to post
			newEditedPostContent = "Hello!"
			postEditTxtBox = firstPost.find_element_by_class_name("form-control")
			# clear post's content
			postEditTxtBox.clear()
			postEditTxtBox.send_keys(newEditedPostContent)
			# cause have 2 button of the same class name in the same page as one is for the create new post an another is save edited post
			postButton = firstPost.find_element_by_class_name("btn.btn-info")
			postButton.click()

			# delay 5 sec to let page update the new post's content before comparing the content
			time.sleep(5)
			# see if the post is successfully edited
			firstPostText = firstPost.find_element_by_class_name("card-text")
			self.assertEqual(firstPostText.text, newEditedPostContent)
			# see if the edited post reflect it has been edited
			firstPost.find_element_by_class_name("edited")

		else:
			# user cannot edit other people's post. If have means fail test case. So iterate the list of options to find if have "Edit"
			for i in range(len(postOptionsList)):
				self.assertNotEqual(postOptionsList, "Edit")

	###################################### Delete own post ######################################

	def test_deleteOwnPost_user(self):
		Automate.login(self.driver, False)
		self.deleteOwnPost()

	def test_deleteOwnPost_mod(self):
		Automate.login(self.driver, True)
		self.deleteOwnPost()

	def deleteOwnPost(self):
		Automate.navigateToSelectiveThread(self.driver, 0)
		Automate.writeAPost(self.driver, "Testing testing")

		# get the list of posts
		listOfPosts = self.driver.find_elements_by_class_name("post-card.card")

		# use the 1st post since it is the post we have just written
		firstPost = listOfPosts[0]
		# click post options
		postOptionButton = firstPost.find_element_by_class_name("post-dropdown")
		postOptionButton.click()
		# get a list of post options
		postOptionsList = firstPost.find_elements_by_class_name("dropdown-item")
		# there are many dropdown items with the same class name in the same page. So have to find the right one we wants to click
		# to delete the post we have just created
		for i in range(len(postOptionsList)):
				if "Delete post" in postOptionsList[i].text:
					postOptionsList[i].click()
					break

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

	def test_deleteAnyPost_user(self):
		self.deleteAnyPost(False)

	def test_deleteAnyPost_mod(self):
		self.deleteAnyPost(True)

	def deleteAnyPost(self, isMod):
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
			Automate.logout(self.driver)
			# login moderator account to test if it can edit other people's (for this case is the user's) post at the 1st thread
			Automate.login(self.driver, True)
		else:
			# moderator account have control panel as the 1st option of the list while logout button is 2nd option in the list
			Automate.logout(self.driver)
			# login user account to test if it can edit other people's (for this case is the mod's) post at the 1st thread
			Automate.login(self.driver, False)

		# navigate to first thread
		Automate.navigateToSelectiveThread(self.driver, 0)

		# get the list of posts
		listOfPosts = self.driver.find_elements_by_class_name("post-card.card")

		# use the 1st post since it is the post we have just written
		firstPost = listOfPosts[0]
		# click post options then click the edit button on the latest post we created for this test
		postOptionButton = firstPost.find_element_by_class_name("post-dropdown")
		postOptionButton.click()
		# get a list of post options then search for the "Edit" option
		postOptionsList = firstPost.find_elements_by_class_name("dropdown-item")

		if isMod:
			for i in range(len(postOptionsList)):
				if "Delete post" in postOptionsList[i].text:
					postOptionsList[i].click()
					break

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

		else:
			# user cannot edit other people's post. If have means fail test case. So iterate the list of options to find if have "Edit"
			for i in range(len(postOptionsList)):
				self.assertNotEqual(postOptionsList, "Delete post")

	###################################### Only upvote once per post ######################################

	def test_upvoteOnce_user(self):
		self.upvoteOnce(False)

	def test_upvoteOnce_mod(self):
		self.upvoteOnce(True)

	def upvoteOnce(self, isMod):
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
			Automate.logout(self.driver)
			# login moderator account to test if it can edit other people's (for this case is the user's) post at the 1st thread
			Automate.login(self.driver, True)
		else:
			# moderator account have control panel as the 1st option of the list while logout button is 2nd option in the list
			Automate.logout(self.driver)
			# login user account to test if it can edit other people's (for this case is the mod's) post at the 1st thread
			Automate.login(self.driver, False)

		# navigate to first thread
		Automate.navigateToSelectiveThread(self.driver, 0)

		# use the 1st post since it is the post we have just written
		firstPost = self.driver.find_elements_by_class_name("post-card.card")[0]

		# get the original number of votes
		voteSection = firstPost.find_element_by_class_name("votes-section")
		orignNumOfVotes = int(voteSection.text)
		# search for the upvote button and click on it
		upVoteButton = voteSection.find_element_by_class_name("vote-icon.upvote-icon")
		upVoteButton.click()
		# need time for the vote change to be reflected
		time.sleep(3)
		# check if the vote increases by one
		voteSection = firstPost.find_element_by_class_name("votes-section")
		self.assertEqual(orignNumOfVotes + 1, int(voteSection.text))
		upVoteButton.click()
		# need time for the vote change to be reflected
		time.sleep(3)
		voteSection = firstPost.find_element_by_class_name("votes-section")
		self.assertEqual(orignNumOfVotes, int(voteSection.text))

	###################################### Only upvote once per post ######################################

	def test_downvoteOnce_user(self):
		self.downvoteOnce(False)

	def test_downvoteOnce_mod(self):
		self.downvoteOnce(True)

	def downvoteOnce(self, isMod):
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
			Automate.logout(self.driver)
			# login moderator account to test if it can edit other people's (for this case is the user's) post at the 1st thread
			Automate.login(self.driver, True)
		else:
			# moderator account have control panel as the 1st option of the list while logout button is 2nd option in the list
			Automate.logout(self.driver)
			# login user account to test if it can edit other people's (for this case is the mod's) post at the 1st thread
			Automate.login(self.driver, False)

		# navigate to first thread
		Automate.navigateToSelectiveThread(self.driver, 0)

		# use the 1st post since it is the post we have just written
		firstPost = self.driver.find_elements_by_class_name("post-card.card")[0]

		# get the original number of votes
		voteSection = firstPost.find_element_by_class_name("votes-section")
		orignNumOfVotes = int(voteSection.text)
		# search for the upvote button and click on it
		upVoteButton = voteSection.find_element_by_class_name("vote-icon.downvote-icon")
		upVoteButton.click()
		# need time for the vote change to be reflected
		time.sleep(5)
		# check if the vote increases by one
		voteSection = firstPost.find_element_by_class_name("votes-section")
		self.assertEqual(orignNumOfVotes - 1, int(voteSection.text))
		upVoteButton.click()
		# need time for the vote change to be reflected
		time.sleep(5)
		voteSection = firstPost.find_element_by_class_name("votes-section")
		self.assertEqual(orignNumOfVotes, int(voteSection.text))

	###################################### Report thread ######################################

	def test_reportThread_user(self):
		self.reportThread(False)

	def test_reportThread_mod(self):
		self.reportThread(True)

	def reportThread(self, isMod):
		# content to write to a post
		contentToWrite = "AAA"

		if isMod:
			# log in mod account to post at the 1st thread
			Automate.login(self.driver, False)
		else:
			# log in mod account to post at the 1st thread
			Automate.login(self.driver, True)

		# navigate to first thread and create a post
		Automate.navigateToSelectiveThread(self.driver, 0)
		Automate.writeAPost(self.driver, contentToWrite)

		if isMod:
			# user account do not have control panel so logout button is 1st option in the list
			Automate.logout(self.driver)
			# login moderator account to test if it can report other people's (for this case is the user's) post at the 1st thread
			reporterUsername = Automate.login(self.driver, True)
		else:
			# moderator account have control panel as the 1st option of the list while logout button is 2nd option in the list
			Automate.logout(self.driver)
			# login user account to test if it can report other people's (for this case is the mod's) post at the 1st thread
			reporterUsername = Automate.login(self.driver, False)

		# navigate to first thread
		Automate.navigateToSelectiveThread(self.driver, 0)

		# use the 1st post since it is the post we have just written
		firstPost = self.driver.find_elements_by_class_name("post-card.card")[0]
		# click post options
		postOptionButton = firstPost.find_element_by_class_name("post-dropdown")
		postOptionButton.click()
		# get a list of post options
		postOptionsList = firstPost.find_elements_by_class_name("dropdown-item")
		# there are many dropdown items with the same class name in the same page. So have to find the right one we wants to click
		# to report the post we have just created
		for i in range(len(postOptionsList)):
				if "Report post" in postOptionsList[i].text:
					postOptionsList[i].click()
					break

		# to confirm reporting the post and reason for reporting
		self.driver.find_element_by_class_name("custom-control-label").click()
		self.driver.find_element_by_class_name  ("btn.btn-danger").click()

		# takes time for the page to load after reporting
		time.sleep(3)
		
		# get the URL for the thread the post is in
		threadUrl = self.driver.current_url

		# login moderator account if is user account testing if reporting works
		if not isMod:
			# Logout
			Automate.logout(self.driver)
			# Login with Moderator account to access Control Panel
			Automate.login(self.driver, True)

		accountMenuOptions = self.driver.find_element_by_class_name("dropdown.nav-item")
		accountMenuOptions.click()
		# get a list of options
		userOptionsList = accountMenuOptions.find_elements_by_class_name("dropdown-item")
		# iterate the list of options to find the Control Panel option and click on it to access it
		for i in range(len(userOptionsList)):
			if "Control Panel" in userOptionsList[i].text:
				userOptionsList[i].click()
				break

		time.sleep(1)
		# Check that reported thread is recorded in Control Panel
		# click on the "Reported posts" tab button
		reportedPostsTabButton = self.driver.find_elements_by_xpath("//a[@class='nav-link']")[0]
		reportedPostsTabButton.click()

		time.sleep(1)
		reportedPostsTab = self.driver.find_element_by_class_name("tab-pane.active")
		# get a list of reported posts
		reportedPostList = reportedPostsTab.find_elements_by_class_name("report-card.card")

		for i in range(len(reportedPostList)):
			user_reported = reportedPostList[i].find_element_by_class_name("data").text
			postContent = reportedPostList[i].find_element_by_class_name("card-title").text

			if user_reported == reporterUsername and postContent == contentToWrite:
				reportedPostList[i].click()
				time.sleep(3)
				
				try:
					# check if is the same post based on the thread the post is in cause can have the same user and post content but in different threads
					self.assertEqual(threadUrl, self.driver.current_url)
					return
				# driver with same name and title will be removed
				except AssertionError:
					self.driver.back()
					# click on the "Reported posts" tab button cause pressed back then it's default at "Reported threads" page and DOM will stale
					reportedPostsTabButton = self.driver.find_elements_by_xpath("//a[@class='nav-link']")[0]
					reportedPostsTabButton.click()
					# let it have time to load
					time.sleep(1)
					reportedPostsTab = self.driver.find_element_by_class_name("tab-pane.active")
					# get a list of reported posts since DOM will be stale so need get the new DOM object
					reportedPostList = reportedPostsTab.find_elements_by_class_name("report-card.card")


		# throws assertion exception since reported post not found in list of reported posts in the control panel
		raise AssertionError()


if __name__ == "__main__":
    unittest.main(verbosity=2)
