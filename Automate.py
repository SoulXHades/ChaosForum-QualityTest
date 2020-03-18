from selenium.webdriver.common.keys import Keys
import time

moderator = "limj0202@e.ntu.edu.sg"
moderator_pw = "123456"
user = "C170095@e.ntu.edu.sg"
user_pw = "C170095@e.ntu.edu.sg"

def login(driver, isMod):
    driver.find_element_by_link_text("Login").click()
    if isMod:
        driver.find_element_by_name("email").send_keys(moderator)
        pw = moderator_pw
    else:
        driver.find_element_by_name("email").send_keys(user)
        pw = user_pw

    password = driver.find_element_by_name("password")
    password.send_keys(pw)
    password.send_keys(Keys.RETURN)

def logout(driver, logoutBtnPos):
	accountMenuOptions = driver.find_element_by_class_name("dropdown.nav-item")
	accountMenuOptions.click()
	logoutButton = driver.find_elements_by_class_name("dropdown-item")[logoutBtnPos]
	# click to logout
	logoutButton.click()


###################################### Post Related ######################################

# navigate into the top thread from the list of threads on the home page
def navigateToSelectiveThread(driver, threadIndex):
	# delay 5 sec to let page load
	#time.sleep(3)
	# to enter the first thread on the list of threads in the home page
	thread = driver.find_elements_by_class_name("thread-card.card")[threadIndex]
	thread.click()

# to post a content on a thread
def writeAPost(driver, postContent):
	# write post content and click the post button to post
	newPost = driver.find_element_by_class_name("main-thread-card.card")
	postTxtBox = newPost.find_element_by_class_name("form-control")
	postTxtBox.send_keys(postContent)
	postButton = newPost.find_element_by_class_name("btn.btn-info")
	postButton.click()

	# delay 5 sec to let page update to show the new post before comparing the content
	time.sleep(5)