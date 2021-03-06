import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest, time, Automate

class ThreadTest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.actions = ActionChains(self.driver)
        self.driver.get("https://chaosforum-20b27.firebaseapp.com")

    def tearDown(self):
        # pass
        self.driver.close()
    
    # Create thread succesfully
    def test_createThread(self):
        Automate.login(self.driver, False)
        # Click 'Create Thread'
        self.driver.find_element_by_class_name("card").find_element_by_class_name("form-control").click()
        # User input of thread fields
        # time.sleep(1)
        container = self.driver.find_element_by_class_name("card-body")
        titleField = container.find_element_by_name("thread_title")
        titleField.send_keys("test thread title")
        dropdowns = container.find_elements_by_class_name("css-1hwfws3")
        self.actions.move_to_element(dropdowns[0]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN)
        self.actions.move_to_element(dropdowns[1]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN)
        self.actions.move_to_element(dropdowns[2]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN).perform()
        commentField = container.find_element_by_name("comment")
        commentField.send_keys("test thread post")
        # Read user inputs
        school = dropdowns[1].text
        course = dropdowns[2].text
        title = titleField.text
        commentField.submit()
        thread = self.driver.find_element_by_class_name("thread-card.card")
        # Compare values with created thread
        self.assertEqual(school, thread.find_elements_by_class_name("data")[0].text)
        self.assertEqual(course, thread.find_elements_by_class_name("data")[1].text)
        self.assertEqual(title, thread.find_element_by_class_name("card-title").text)

    # Check for 'required' innerHTML for empty fields
    def test_emptyFields(self):
        Automate.login(self.driver, False)
        self.driver.find_element_by_class_name("card").find_element_by_class_name("form-control").click()
        container = self.driver.find_element_by_class_name("card-body")
        # time.sleep(1)
        titleField = container.find_element_by_name("thread_title")
        titleField.click()
        dropdowns = container.find_elements_by_class_name("css-1hwfws3")
        dropdowns[0].click()
        self.assertEqual(self.driver.find_elements_by_class_name("invalid-feedback")[0].text, "Required")
        dropdowns[1].click()
        self.assertEqual(self.driver.find_elements_by_class_name("invalid-feedback")[1].text, "Required")
        dropdowns[2].click()
        self.assertEqual(self.driver.find_elements_by_class_name("invalid-feedback")[2].text, "Required")
        self.driver.find_element_by_name("comment").click()
        self.driver.find_element_by_class_name("btn.btn-info").click()
        self.assertEqual(self.driver.find_elements_by_class_name("invalid-feedback")[3].text, "Required")
    
    def test_editOwnThread(self):
        username = Automate.login(self.driver, False)
        threads = self.driver.find_elements_by_class_name("thread-card.card")
        for threadIndex, thread in enumerate(threads):
            if thread.find_elements_by_class_name("data")[3].text == username:
                # Read thread details
                threadDetails = Automate.getThreadDetails(thread)
                # Click Thread Options -> Edit
                thread.find_element_by_class_name("thread-dropdown").click()
                thread.find_element_by_class_name("dropdown-item").click()
                break
        # update thread fields
        # time.sleep(1)
        container = self.driver.find_element_by_class_name("card-body")
        titleField = container.find_element_by_name("thread_title")
        titleField.clear()
        titleField.send_keys(threadDetails["title"] + " edited")
        dropdowns = container.find_elements_by_class_name("css-1hwfws3")
        dropdowns[0].click()
        collegeList = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div[2]/div[2]/div[1]/div").text.split("\n")

        for i in range(1, len(collegeList)):
            if collegeList[i] in collegeList[0]:
                break
            else:
                self.actions.send_keys(Keys.DOWN)
        self.actions.send_keys(Keys.DOWN).send_keys(Keys.RETURN)
        
        self.actions.move_to_element(dropdowns[1]).click().send_keys(Keys.RETURN)
        self.actions.move_to_element(dropdowns[2]).click().send_keys(Keys.RETURN).perform()
        school_new = dropdowns[1].text
        course_new = dropdowns[2].text
        title_new = titleField.text
        self.driver.find_element_by_class_name("btn.btn-info").click()
        # using threadIndex as page is refreshed -> DOM became stale
        threadDetails_displayed = Automate.getThreadDetails(self.driver.find_elements_by_class_name("thread-card.card")[threadIndex])
        # Check that thread details are updated correctly
        self.assertNotEqual(threadDetails_displayed["school"], threadDetails["school"])
        self.assertNotEqual(threadDetails_displayed["course"], threadDetails["course"])
        self.assertNotEqual(threadDetails_displayed["title"], threadDetails["title"])
        self.assertEqual(threadDetails_displayed["school"], school_new)
        self.assertEqual(threadDetails_displayed["course"], course_new)
        self.assertEqual(threadDetails_displayed["title"], title_new)

    def test_editAnyThread_mod(self):
        Automate.login(self.driver, True)
        threads = self.driver.find_elements_by_class_name("thread-card.card")
        for threadIndex, thread in enumerate(threads):
            # Read thread details
            threadDetails = Automate.getThreadDetails(thread)
            # Click Thread Options -> Edit
            thread.find_element_by_class_name("thread-dropdown").click()
            thread.find_element_by_class_name("dropdown-item").click()
            break

        container = self.driver.find_element_by_class_name("card-body")
        titleField = container.find_element_by_name("thread_title")
        titleField.clear()
        titleField.send_keys(threadDetails["title"] + " edited")
        dropdowns = container.find_elements_by_class_name("css-1hwfws3")
        dropdowns[0].click()
        collegeList = self.driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div[2]/div[2]/div[1]/div").text.split("\n")

        for i in range(1, len(collegeList)):
            if collegeList[i] in collegeList[0]:
                break
            else:
                self.actions.send_keys(Keys.DOWN)
        self.actions.send_keys(Keys.DOWN).send_keys(Keys.RETURN)

        self.actions.move_to_element(dropdowns[1]).click().send_keys(Keys.RETURN)
        self.actions.move_to_element(dropdowns[2]).click().send_keys(Keys.RETURN).perform()
        school_new = dropdowns[1].text
        course_new = dropdowns[2].text
        title_new = titleField.text
        self.driver.find_element_by_class_name("btn.btn-info").click()
        # using threadIndex as page is refreshed -> DOM became stale
        threadDetails_displayed = Automate.getThreadDetails(self.driver.find_elements_by_class_name("thread-card.card")[threadIndex])
        # Check that thread details are updated correctly
        self.assertNotEqual(threadDetails_displayed["school"], threadDetails["school"])
        self.assertNotEqual(threadDetails_displayed["course"], threadDetails["course"])
        self.assertNotEqual(threadDetails_displayed["title"], threadDetails["title"])
        self.assertEqual(threadDetails_displayed["school"], school_new)
        self.assertEqual(threadDetails_displayed["course"], course_new)
        self.assertEqual(threadDetails_displayed["title"], title_new)

    def test_editAnyThread_user(self):
        username = Automate.login(self.driver, False)
        threads = self.driver.find_elements_by_class_name("thread-card.card")
        for thread in threads:
            if thread.find_elements_by_class_name("data")[3].text != username:
                thread.find_element_by_class_name("thread-dropdown").click()
                options = thread.find_elements_by_class_name("dropdown-item")
                for option in options:
                    self.assertNotIn("Edit", option.text)
            break

    def test_deleteOwnThread(self):
        username = Automate.login(self.driver, False)
        threads = self.driver.find_elements_by_class_name("thread-card.card")
        threadCount = len(threads)
        for thread in threads:
            if thread.find_elements_by_class_name("data")[3].text == username:
                thread.find_element_by_class_name("thread-dropdown").click()
                thread.find_elements_by_class_name("dropdown-item")[1].click()
                self.driver.find_element_by_class_name("btn.btn-danger").click()
                break
        time.sleep(5)
        # Check that total threads decremented by 1
        newThreadCount = len(self.driver.find_elements_by_class_name("thread-card.card"))
        self.assertEqual(threadCount-1, newThreadCount)

    def test_deleteAnyThread_user(self):
        username = Automate.login(self.driver, False)
        threads = self.driver.find_elements_by_class_name("thread-card.card")
        for thread in threads:
            if thread.find_elements_by_class_name("data")[3].text != username:
                thread.find_element_by_class_name("thread-dropdown").click()
                options = thread.find_elements_by_class_name("dropdown-item")
                optionFound = False
                for option in options:
                    print("option:", option.text)
                    self.assertNotIn("Delete thread", option.text)
                    optionFound = True
                    break
                if optionFound:
                    break

    def test_deleteAnyThread_mod(self):
        Automate.login(self.driver, True)
        threads = self.driver.find_elements_by_class_name("thread-card.card")
        threadCount = len(threads)
        for thread in threads:
            thread.find_element_by_class_name("thread-dropdown").click()
            thread.find_elements_by_class_name("dropdown-item")[1].click()
            self.driver.find_element_by_class_name("btn.btn-danger").click()
            break
        time.sleep(5)
        newThreadCount = len(self.driver.find_elements_by_class_name("thread-card.card"))
        self.assertEqual(threadCount-1, newThreadCount)

    def test_reportThread(self):
        username = Automate.login(self.driver, False)
        for thread in self.driver.find_elements_by_class_name("thread-card.card"):
            optionFound = False
            if thread.find_elements_by_class_name("data")[3].text != username:
                # time.sleep(1)
                thread.find_element_by_class_name("thread-dropdown").click()
                try:
                    options = thread.find_element_by_class_name("dropdown-menu.show").find_elements_by_class_name("dropdown-item")
                    for option in options:
                        print(option.text)
                        if "Report thread" in option.text:
                            threadDetails = Automate.getThreadDetails(thread)
                            option.click()
                            optionFound = True
                            break
                except selenium.common.exceptions.NoSuchElementException:
                    continue
                
            if optionFound:
                break
        self.driver.find_element_by_class_name("custom-control-label").click()
        self.driver.find_element_by_class_name("btn.btn-danger").click()

        # view thread to get thread url
        time.sleep(3)
        thread.click()
        threadUrl = self.driver.current_url
        # Logout
        Automate.logout(self.driver)
        # Login with Moderator account to access Control Panel
        Automate.login(self.driver, True)
        self.driver.find_element_by_class_name("dropdown.nav-item").click()
        self.driver.find_element_by_class_name("dropdown-item").click()
        # Check that reported thread is recorded in Control Panel
        for report in self.driver.find_elements_by_class_name("report-card.card"):
            user_reported = report.find_element_by_class_name("data").text
            title_reported = report.find_element_by_class_name("card-title").text
            if user_reported == threadDetails["user"] and title_reported == threadDetails["title"]:
                report.click()
                break
        threadUrl_reported = self.driver.current_url
        self.assertEqual(threadUrl, threadUrl_reported)

    def test_upvoteThread(self):
        Automate.login(self.driver, False)
        for i, section in enumerate(self.driver.find_elements_by_class_name("votes-section")):
            upvote = section.find_elements_by_tag_name("div")[0]
            downvote = section.find_elements_by_tag_name("div")[1]
            # unvoted thread
            if upvote.get_attribute("class") == "vote-icon upvote-icon " and downvote.get_attribute("class") == "vote-icon downvote-icon ":
                voteCount = int(section.find_elements_by_tag_name("div")[2].text)
                upvote.click()
                break
        time.sleep(5)
        newVoteCount = int(self.driver.find_elements_by_class_name("votes-section")[i].find_elements_by_tag_name("div")[2].text)
        self.assertEqual(voteCount+1, newVoteCount)

    def test_downvoteThread(self):
        Automate.login(self.driver, False)
        for i, section in enumerate(self.driver.find_elements_by_class_name("votes-section")):
            upvote = section.find_elements_by_tag_name("div")[0]
            downvote = section.find_elements_by_tag_name("div")[1]
            # unvoted thread
            if upvote.get_attribute("class") == "vote-icon upvote-icon " and downvote.get_attribute("class") == "vote-icon downvote-icon ":
                voteCount = int(section.find_elements_by_tag_name("div")[2].text)
                downvote.click()
                break
        time.sleep(5)
        newVoteCount = int(self.driver.find_elements_by_class_name("votes-section")[i].find_elements_by_tag_name("div")[2].text)
        self.assertEqual(voteCount-1, newVoteCount)

    def test_voteOnce(self):
        Automate.login(self.driver, False)
        for i, section in enumerate(self.driver.find_elements_by_class_name("votes-section")):
            upvote = section.find_elements_by_tag_name("div")[0]
            downvote = section.find_elements_by_tag_name("div")[1]
            voteCount = int(section.find_elements_by_tag_name("div")[2].text)
            # if voted thread
            if upvote.get_attribute("class") == "vote-icon upvote-icon is-true":
                upvote.click()
                time.sleep(5)
                newVoteCount = int(self.driver.find_elements_by_class_name("votes-section")[i].find_elements_by_tag_name("div")[2].text)
                self.assertEqual(voteCount-1, newVoteCount)
            elif downvote.get_attribute("class") == "vote-icon downvote-icon is-true":
                downvote.click()
                time.sleep(5)
                newVoteCount = int(self.driver.find_elements_by_class_name("votes-section")[i].find_elements_by_tag_name("div")[2].text)
                self.assertEqual(voteCount+1, newVoteCount)
            else:
                continue
            break

    def test_searchThread(self):
        searchBar = self.driver.find_element_by_class_name("nav-search.form-control")
        keyword = "title"
        searchBar.send_keys(keyword)
        searchBar.send_keys(Keys.RETURN)
        for thread in self.driver.find_elements_by_class_name("thread-card.card"):
            title = thread.find_element_by_class_name("card-title").text
            print(title)
            self.assertIn(keyword, title)

    def test_filterThreads(self):
        container = self.driver.find_elements_by_class_name("nav")[1]
        dropdowns = container.find_elements_by_class_name("css-1hwfws3")
        time.sleep(5)
        self.actions.move_to_element(dropdowns[0]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN)
        self.actions.move_to_element(dropdowns[1]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN)
        self.actions.move_to_element(dropdowns[2]).click().send_keys(Keys.DOWN).send_keys(Keys.RETURN).perform()
        # self.actions.move_to_element(dropdowns[0]).click().send_keys("engineer").send_keys(Keys.RETURN)
        # self.actions.move_to_element(dropdowns[1]).click().send_keys("comp").send_keys(Keys.RETURN)
        # self.actions.move_to_element(dropdowns[2]).click().send_keys("org").send_keys(Keys.RETURN).perform()

        container.find_element_by_class_name("btn.btn-primary").click()
        school_filtered = dropdowns[1].text
        course_filtered = dropdowns[2].text
        for thread in self.driver.find_elements_by_class_name("thread-card.card"):
            school_result = thread.find_elements_by_class_name("data")[0].text
            course_result = thread.find_elements_by_class_name("data")[1].text
            print("new:", school_result, course_result)
            self.assertEqual(school_filtered, school_result)
            self.assertEqual(course_filtered, course_result)


if __name__ == "__main__":
    unittest.main(verbosity=2)