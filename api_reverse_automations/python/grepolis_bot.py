import logging
import re
import urllib
import json

import requests


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def get_cookie_string(cookies):
    """
    Create a cookie string from the given cookie dictionary

    Parameters:
    cookies - dictionary of cookie values

    Returns:
    string - cookies concatenated into cookie header string
    """
    cookie_string = ""
    for cookie in cookies:
        cookie_string += f"{cookie}={cookies[cookie]}; "

    return cookie_string.strip()


def set_cookie(cookie_dict, cookie_header):
    """
    Updates the given cookie_dict parameter with the new cookies

    Parameters:
    cookie_dict - dictionary of cookie pairs to be updated
    cookie_header - requests cookie header to be used for updating
    """
    # update cookie dict with the new values
    cookie_dict.update(cookie_header.get_dict())


def main():
    """
    Main logic for grepolis login, session handling, and
    game world opening.
    """

    # create a session to keep the session information
    session = requests.Session()
    session.withCredentials = True

    # make sure to set the content type (show request as curl to check)
    session.headers = {
        "User-Agent": "Chrome/51.0.2704.63",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    # request main page and set the cookies for session
    base_url = "https://en.grepolis.com/"
    res = session.get(base_url)
    cookie_dict = res.cookies.get_dict()
    session.headers["cookie"] = get_cookie_string(cookie_dict)

    # required information extracted from the request in dev tools
    session.headers["X-Requested-With"] = "XMLHttpRequest"
    session.headers["X-XSRF-TOKEN"] = cookie_dict["XSRF-TOKEN"]

    # credentials
    username = "scriptworld"
    password = "udemy123"

    # copy paste from dev tools
    # be careful! for complex passwords you need to urlencode them
    login_url = "https://en.grepolis.com/glps/login_check"
    data = f"login%5Buserid%5D={username}&login%5Bpassword%5D={password}&login%5Bremember_me%5D=true"
    check = session.post(login_url, data=data)
    login_data = check.json()

    if not login_data["success"]:
        logger.error(f"Invalid Credentials... {check.status_code} - {login_data}")
        return

    # set the new cookie for the logged in session
    set_cookie(cookie_dict, check.cookies)
    session.headers["cookie"] = get_cookie_string(cookie_dict)

    #
    lobby = session.get(base_url, allow_redirects=False)
    set_cookie(cookie_dict, lobby.cookies)
    session.headers["cookie"] = get_cookie_string(cookie_dict)
    redirect_url = lobby.headers["Location"]

    jobOffer = session.get(redirect_url, allow_redirects=False)
    set_cookie(cookie_dict, jobOffer.cookies)
    session.headers["cookie"] = get_cookie_string(cookie_dict)

    lobby_url = "https://en0.grepolis.com/start/index"
    lobby = session.get(lobby_url)

    # get the CSRF token using regex
    lobby_data = lobby.text
    csrf_pattern = r"CSRF\.token = '(\w+)';"
    csrf_token_search = re.search(csrf_pattern, lobby_data)
    csrf_token = csrf_token_search[1]

    # use the csrf token to login to game world
    gameworld_login_url = "https://en0.grepolis.com/start?action=login_to_game_world"
    gameworld = "en126"
    gameworld_data = f"world={gameworld}&facebook_session=&facebook_login=&token={csrf_token}&portal_sid=&name={username}&password="

    # session_id is in this header in the location
    temp = session.post(gameworld_login_url, gameworld_data, allow_redirects=False)
    set_cookie(cookie_dict, temp.cookies)
    session.headers["cookie"] = get_cookie_string(cookie_dict)
    trash = temp.headers["Location"]

    temp1 = session.get(trash, allow_redirects=False)
    set_cookie(cookie_dict, temp1.cookies)
    session.headers["cookie"] = get_cookie_string(cookie_dict)
    url_path = temp1.headers["Location"]

    # define the game world to be played in
    gameworld_url = f"https://{gameworld}.grepolis.com"
    game = session.get(gameworld_url + url_path)
    set_cookie(cookie_dict, game.cookies)
    session.headers["cookie"] = get_cookie_string(cookie_dict)

    # token is hidden in window.game object this time
    game_data = game.text
    game_csrf_token_pattern = r'csrfToken":"(\w+)"'
    game_csrf_token_search = re.search(game_csrf_token_pattern, game_data)
    game_csrf_token = game_csrf_token_search[1]

    # get the information for the town with the given id
    town_id = "10947"
    data_url_data = "json=" + urllib.parse.quote_plus(
        '{"types":[{"type":"easterIngredients"},{"type":"map","param":{"x":9,"y":3} },{"type":"bar"},{"type":"backbone"}],"town_id":10947,"nl_init":false}'
    )
    data_url = f"https://{gameworld}.grepolis.com/game/data?town_id={town_id}&action=get&h={game_csrf_token}"
    lastResponse = session.post(data_url, data_url_data)

    # display the game state of the current town
    logger.info(json.dumps(lastResponse.json(), indent=4))


if __name__ == "__main__":
    main()
