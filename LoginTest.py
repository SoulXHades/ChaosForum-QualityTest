from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest, time

class LoginTest(unittest.TestCase):
    invalidEmail = "abc@not.NTU.email.com"
    unregisteredEmail = "unregistered@e.ntu.edu.sg"
    registeredEmail = "limj0202@e.ntu.edu.sg"
    correctPw = "123456"
    wrongPw = "123"

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.get("https://chaosforum-20b27.firebaseapp.com")

    def tearDown(self):
        self.driver.close()

    def test_invalidEmail(self):
        self.driver.find_element_by_link_text("Login").click()
        self.driver.find_element_by_name("email").send_keys(LoginTest.invalidEmail)
        self.driver.find_element_by_id("root").click()
        self.assertEqual(self.driver.find_element_by_class_name("invalid-feedback").text, "Please use your NTU email")

    def test_unregisteredEmail(self):
        self.driver.find_element_by_link_text("Login").click()
        self.driver.find_element_by_name("email").send_keys(LoginTest.unregisteredEmail)
        password = self.driver.find_element_by_name("password")
        password.send_keys(LoginTest.correctPw)
        password.send_keys(Keys.RETURN)
        self.assertEqual(self.driver.find_element_by_class_name("toast.toast-error ").text, "Email not found.")

    def test_correctLogin(self):
        self.driver.find_element_by_link_text("Login").click()
        self.driver.find_element_by_name("email").send_keys(LoginTest.registeredEmail)
        password = self.driver.find_element_by_name("password")
        password.send_keys(LoginTest.correctPw)
        password.send_keys(Keys.RETURN)
        self.assertEqual(self.driver.find_element_by_class_name("toast.toast-success ").text, "Login Success! You will be redirected shortly")

    def test_wrongPassword(self):
        self.driver.find_element_by_link_text("Login").click()
        self.driver.find_element_by_name("email").send_keys(LoginTest.registeredEmail)
        password = self.driver.find_element_by_name("password")
        password.send_keys(LoginTest.wrongPw)
        password.send_keys(Keys.RETURN)
        # self.assertEqual(self.driver.find_element_by_class_name("toast.toast-error ").text, "Wrong password.")
        self.assertEqual(self.driver.find_element_by_class_name("toast.toast-error ").get_attribute("innerHTML"), "Wrong password.")

    def test_voteWithoutLogin(self):
        # upvote 1st thread without login
        voteCount = int(self.driver.find_element_by_class_name("votes-section").get_attribute("div")[2].text())
        self.driver.find_element_by_class_name("vote-icon.upvote-icon ").click()
        time.sleep(5)
        newVoteCount = int(self.driver.find_element_by_class_name("votes-section").get_attribute("div")[2].text())
        self.assertEqual(self.driver.find_element_by_class_name("toast.toast-info ").text, "Log in to vote for this thread!")
        self.assertEqual(voteCount, newVoteCount)

if __name__ == "__main__":
    unittest.main()