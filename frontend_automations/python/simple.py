import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# replaces the need to manually provide chrome binary path
from instapy_chromedriver import binary_path


def main():
    # define the options of our chrome instance
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    print("Starting Chrome Browser...")

    # get an instance of the chrome browser and open google.com
    driver = webdriver.Chrome(executable_path=binary_path, options=chrome_options)
    # driver = webdriver.Firefox() <= requires geckodriver binary
    driver.get("http://www.google.com")

    # find the search field and send the text before submitting using Enter
    search_term = "i love automation"
    print(f"Searching for {search_term}")

    lucky_button = driver.find_element_by_css_selector("[name='q']")
    lucky_button.send_keys(search_term)
    lucky_button.send_keys(Keys.ENTER)

    # capture the, at that moment, current screen and wait 3 sec before exit
    print("Capturing Screenshot")
    driver.get_screenshot_as_file("result.png")
    time.sleep(3)

    print("Closing Chrome instance")
    driver.close()


if __name__ == "__main__":
    main()
