from selenium.webdriver.common.keys import Keys

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