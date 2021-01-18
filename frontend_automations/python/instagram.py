import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

# replaces the need to manually provide chrome binary path
from instapy_chromedriver import binary_path


class InstagramSession:
    def __init__(self, username, password):
        """
        Initialise the session on instagram and try to
        login the user with the given credentials

        Parameters:
        username - username or email of the to be logged in user
        password - password of the to be logged in user
        """
        self.driver = webdriver.Chrome(executable_path=binary_path)
        ignored_exceptions = StaleElementReferenceException
        self.wait = WebDriverWait(self.driver, 5, ignored_exceptions=ignored_exceptions)

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
        self.driver.get("http://www.instagram.com")

        # wait for element to appear, then hover it
        print("Waiting for login elements to load")
        try:
            # wait for the elements to be visible
            username_input = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@name='username']")
                )
            )
            password_input = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@name='password']")
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
            notification_dialog = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//button[text()='Not Now']"))
            )
            ActionChains(self.driver).move_to_element(notification_dialog).click(
                notification_dialog
            ).perform()
            print("Logged in successfully")
            return True
        except TimeoutException as err:
            print(f"Element search timed out... {err}")
            return False
        except Exception as err:
            print(f"Page was not loaded correctly... {err}")
            return False

    def like_feed_posts(self, amount):
        """
        Likes the given amount of not yet liked posts
        on the feed page of the user

        Parameters:
        amount - amount of posts to be liked
        """
        # get the html main element for up down movement
        html = self.driver.find_element_by_tag_name("html")
        liked = 0

        while liked < amount:
            time.sleep(5)
            try:
                posts_like_buttons = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            "//span/button[*[local-name()='svg']/@aria-label='Like']",
                        )
                    )
                )

                # for each like button found, click the button
                for like_elem in posts_like_buttons:
                    ActionChains(self.driver).move_to_element(like_elem).click(
                        like_elem
                    ).perform()
                    liked += 1

                    print(f"Liked {liked} posts from feed.")
                    time.sleep(1)

                    # if we have enough posts liked, return
                    if liked == amount:
                        print(f"Liked all {amount} of the given amount of posts")
                        return

            except TimeoutException:
                # if not enough posts, load more posts
                html.send_keys(Keys.END)

            # load more posts
            html.send_keys(Keys.END)

    def close(self):
        """
        Closes the driver instance
        """
        print("Closing Browser instance")
        self.driver.close()


if __name__ == "__main__":
    username = "contacting.john.doe@gmail.com"
    password = "ThisIsJohnDoe!"

    # create a new instance of the Instagram session and like the posts
    session = InstagramSession(username, password)
    session.like_feed_posts(10)
    session.close()
