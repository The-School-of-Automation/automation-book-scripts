import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# replaces the need to manually provide chrome binary path
from instapy_chromedriver import binary_path


class TwitterRecommendationFollower:
    def __init__(self, username, password):
        """
        Initialise the session on twitter and try to
        login the user with the given credentials

        Parameters:
        username - username or email of the to be logged in user
        password - password of the to be logged in user
        """
        self.driver = webdriver.Chrome(executable_path=binary_path)
        ignored_exceptions = StaleElementReferenceException
        self.wait = WebDriverWait(
            self.driver, 10, ignored_exceptions=ignored_exceptions
        )

        is_logged_in = self.login(username, password)
        if not is_logged_in:
            raise Exception("Could not login with given credentials.")

    def login(self, username, password):
        """
        Login the user with the given username and password

        Parameters:
        username - username or email of the to be logged in user
        password - password of the to be logged in user

        Returns:
        bool - True if successful, false if not logged in
        """
        self.driver.get("http://twitter.com/login")

        # wait for element to appear, then hover it
        print("Waiting for login elements to load")
        try:
            # wait for the elements to be visible
            username_input = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@name='session[username_or_email]']")
                )
            )
            password_input = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@name='session[password]']")
                )
            )

            # using an action chain to write the username and password
            # into the two input fields on the login screen
            print("Sending username and password")
            action_chain = ActionChains(self.driver)
            action_chain.move_to_element(username_input).click()
            action_chain.send_keys(username)
            action_chain.move_to_element(password_input).click()
            action_chain.send_keys(password)
            action_chain.send_keys(Keys.ENTER)
            action_chain.perform()

            # waiting for and closing the notifications dialog
            time.sleep(5)
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Tweet']"))
            )
            print("Logged in successfully")
            return True
        except TimeoutException as err:
            print(f"Element search timed out... {err}")
            return False
        except Exception as err:
            print(f"Page was not loaded correctly... {err}")
            return False

    def follow_recommendations(self, amount):
        """
        Follows the given amount of accounts from the recommendations list
        of the logged in user.

        Parameters:
        amount - amount of accounts to follow from recommendations
        """
        self.driver.get("https://twitter.com/i/connect_people")
        time.sleep(5)

        print(f"Trying to follow {amount} accounts from recommendations")
        followed = 0

        while followed < amount:
            time.sleep(5)
            try:
                follow_buttons = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, "//span[text()='Follow']")
                    )
                )

                # for each follow button found, click the button
                for follow_elem in follow_buttons:
                    ActionChains(self.driver).move_to_element(follow_elem).click(
                        follow_elem
                    ).perform()
                    followed += 1

                    print(f"Followed {followed} accounts from recommendations.")
                    time.sleep(1)

                    # if we have enough posts liked, return
                    if followed == amount:
                        print(
                            f"Followed all {amount} of the given amount of recommendations"
                        )
                        return

            except TimeoutException:
                # if not enough posts, reload to show more recommendations
                self.driver.reload()
                time.sleep(5)

    def close(self):
        """
        Closes the driver instance
        """
        print("Closing Browser instance")
        self.driver.close()


if __name__ == "__main__":
    # export TWITTER_USERNAME="contacting.john.doe@gmail.com"
    # export TWITTER_PASSWORD="ThisIsJohnDoe\!"
    username = os.environ.get("TWITTER_USERNAME")
    password = os.environ.get("TWITTER_PASSWORD")

    # create a new instance of the Instagram session and like the posts
    session = TwitterRecommendationFollower(username, password)
    session.follow_recommendations(10)
    session.close()
