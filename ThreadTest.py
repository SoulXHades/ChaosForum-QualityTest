from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import unittest, Automate

import time

class ThreadTest(unittest.TestCase):
    title = "test thread title"
    college = "engineering"
    school = "computer science"
    course = "data structure"
    username = "JingQiang"

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.actions = ActionChains(self.driver)
        self.driver.get("https://chaosforum-20b27.firebaseapp.com")
        Automate.login(self.driver, True)

    def tearDown(self):
        time.sleep(2)
        # self.driver.close()
    
    # def test_createThread(self):
    #     self.driver.find_element_by_xpath("//input[@placeholder='Create thread...']").click()
    #     self.driver.find_element_by_name("thread_title").send_keys(ThreadTest.title)
    #     dropdowns = self.driver.find_elements_by_class_name("css-1hwfws3")
    #     self.actions.move_to_element(dropdowns[0]).click().send_keys(ThreadTest.college).send_keys(Keys.RETURN)
    #     self.actions.move_to_element(dropdowns[1]).click().send_keys(ThreadTest.school).send_keys(Keys.RETURN)
    #     self.actions.move_to_element(dropdowns[2]).click().send_keys(ThreadTest.course).send_keys(Keys.RETURN).perform()
    #     self.driver.find_element_by_name("comment").send_keys("test thread post")
    #     # self.driver.find_element_by_class_name("btn.btn-info").click()
    
    # def test_emptyFields(self):
    #     self.driver.find_element_by_xpath("//input[@placeholder='Create thread...']").click()
    #     dropdowns = self.driver.find_elements_by_class_name("css-1hwfws3")
    #     self.driver.find_element_by_name("thread_title").click()
    #     dropdowns[0].click()
    #     self.assertEqual(self.driver.find_elements_by_class_name("invalid-feedback")[0].text, "Required")
    #     dropdowns[1].click()
    #     self.assertEqual(self.driver.find_elements_by_class_name("invalid-feedback")[1].text, "Required")
    #     dropdowns[2].click()
    #     self.assertEqual(self.driver.find_elements_by_class_name("invalid-feedback")[2].text, "Required")
    #     self.driver.find_element_by_name("comment").click()
    #     self.driver.find_element_by_class_name("btn.btn-info").click()
    #     self.assertEqual(self.driver.find_elements_by_class_name("invalid-feedback")[3].text, "Required")

    # def test_editOwnThread(self):
    #     threads = self.driver.find_elements_by_class_name("thread-card.card")
    #     for thread in threads:
    #         if thread.find_elements_by_class_name("data")[3].text == ThreadTest.username:
    #             thread.find_element_by_class_name("thread-dropdown").click()
    #             thread.find_element_by_class_name("dropdown-item").click()
    #             break
    
    # def test_deleteOwnThread(self):
    #     for thread in self.driver.find_elements_by_class_name("thread-card.card"):
    #         if thread.find_elements_by_class_name("data")[3].text == ThreadTest.username:
    #             thread.find_element_by_class_name("thread-dropdown").click()
    #             thread.find_elements_by_class_name("dropdown-item")[1].click()
    #             # self.driver.find_element_by_class_name("btn.btn-danger").click()
    #             break

    # def test_reportThread(self):
    #     for thread in self.driver.find_elements_by_class_name("thread-card.card"):
    #         if thread.find_elements_by_class_name("data")[3].text != ThreadTest.username:
    #             thread.find_element_by_class_name("thread-dropdown").click()
    #             # report thread. element index might change due to account access rights
    #             thread.find_elements_by_class_name("dropdown-item")[2].click()
    #             self.driver.find_element_by_class_name("custom-control-label").click()
    #             # self.driver.find_element_by_class_name("btn.btn-danger").click()
    #             break

    # def test_upVoteThread(self):
    #     for section in self.driver.find_elements_by_class_name("votes-section"):
    #         upvote = section.find_elements_by_tag_name("div")[0]
    #         downvote = section.find_elements_by_tag_name("div")[1]
    #         # unvoted thread
    #         if upvote.get_attribute("class") == "vote-icon upvote-icon " and downvote.get_attribute("class") == "vote-icon downvote-icon ":
    #             voteCount = int(section.find_elements_by_tag_name("div")[2].text)
    #             upvote.click()
    #             votedSection = section
    #             break
    #     time.sleep(5)
    #     newVoteCount = int(votedSection.find_elements_by_tag_name("div")[2].text)
    #     self.assertEqual(voteCount+1, newVoteCount)

    # def test_downVoteThread(self):
    #     for section in self.driver.find_elements_by_class_name("votes-section"):
    #         upvote = section.find_elements_by_tag_name("div")[0]
    #         downvote = section.find_elements_by_tag_name("div")[1]
    #         # unvoted thread
    #         if upvote.get_attribute("class") == "vote-icon upvote-icon " and downvote.get_attribute("class") == "vote-icon downvote-icon ":
    #             voteCount = int(section.find_elements_by_tag_name("div")[2].text)
    #             downvote.click()
    #             votedSection = section
    #             break
    #     time.sleep(5)
    #     newVoteCount = int(votedSection.find_elements_by_tag_name("div")[2].text)
    #     self.assertEqual(voteCount-1, newVoteCount)

    def test_voteOnce(self):
        for section in self.driver.find_elements_by_class_name("votes-section"):
            upvote = section.find_elements_by_tag_name("div")[0]
            downvote = section.find_elements_by_tag_name("div")[1]
            # voted thread
            if upvote.get_attribute("class") == "vote-icon upvote-icon is-true" or downvote.get_attribute("class") == "vote-icon downvote-icon is-true":
                voteCount = int(section.find_elements_by_tag_name("div")[2].text)
                upvote.click()
                # downvote.click()
                votedSection = section
                break
            time.sleep(5)
            newVoteCount = int(votedSection.find_elements_by_tag_name("div")[2].text)
            self.assertEqual(voteCount, newVoteCount)

    
            


if __name__ == "__main__":
    unittest.main()