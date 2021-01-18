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


class SpotifyListenerBot:
    def __init__(self, username, password):
        """
        Initialise the session on spotify and try to
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
        self.driver.get("https://accounts.spotify.com/en/login")

        # wait for element to appear, then hover it
        print("Waiting for login elements to load")
        try:
            # wait for the elements to be visible
            username_input = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@ng-model='form.username']")
                )
            )
            password_input = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[@ng-model='form.password']")
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
                EC.presence_of_element_located((By.XPATH, "//a[text()='Web Player']"))
            )
            print("Logged in successfully")
            return True
        except TimeoutException as err:
            print(f"Element search timed out... {err}")
            return False
        except Exception as err:
            print(f"Page was not loaded correctly... {err}")
            return False

    def listen_to_playlist(self, playlist_url, duration):
        """
        Opens and listens to the given playlist url for a given amount of time.

        Parameters:
        playlist_url - url of the to be played playlist
        duration - amount of seconds the playlist is listened to
        """
        self.driver.get(playlist_url)
        time.sleep(5)

        print(f"Trying to start playing playlist {playlist_url}")
        try:
            play_buttons = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[@aria-label='Play']")
                )
            )

            # invisible play button on top of page, actual play button [1]
            # print(f"Found {len(play_buttons)} play buttons")
            ActionChains(self.driver).move_to_element(play_buttons[1]).click(
                play_buttons[1]
            ).perform()

            # give the playlist time to start
            time.sleep(10)

            # wait till the playlist is started and the pause element visible
            self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//button[@title='Pause']")
                )
            )

            print(f"Started listening to playlist {playlist_url}")
            time.sleep(duration)

            print(f"Played playlist {playlist_url} for {duration} seconds")
        except TimeoutException:
            print(f"Playlist {playlist_url} could not be played... moving on")

    def close(self):
        """
        Closes the driver instance
        """
        print("Closing Browser instance")
        self.driver.close()


if __name__ == "__main__":
    # export SPOTIFY_USERNAME="contacting.john.doe@gmail.com"
    # export SPOTIFY_PASSWORD="ThisIsJohnDoe\!"
    username = os.environ.get("SPOTIFY_USERNAME")
    password = os.environ.get("SPOTIFY_PASSWORD")

    # create a new instance of the Instagram session and like the posts
    session = SpotifyListenerBot(username, password)
    session.listen_to_playlist(
        "https://open.spotify.com/show/1VXcH8QHkjRcTCEd88U3ti", 10
    )
    session.close()
