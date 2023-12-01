import time
from credentials import username, pwd
from selenium import webdriver

GAMES_PER_ROUND = 5


def collect_data_from_round(driver: webdriver, game_url: str):
    """
    given driver and game_url, runs collect_data_once GAMES_PER_ROUND times
    """
    for i in range(GAMES_PER_ROUND):
        time.sleep(1)
        __collect_data_once(driver, game_url)


def __collect_data_once(driver: webdriver, game_url: str):
    """
    given driver and game_url, creates a screenshot of the game canvas, logins, takes a random guess,
    collects results, and stores results as a label
    """
    driver.get(game_url)
    image_path = __create_screenshot(driver, 'screenshots')
    driver.get(game_url)
    __enable_cookies(driver)
    __place_marker(driver)
    lat, lon = __find_actual_location(driver)
    __store_coordinates('coordinates.txt', lat, lon, image_path)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    driver.find_element(webdriver.common.by.By.XPATH, '//*[@id="__next"]/div[2]/div[3]/main/div[2]/div/div[2]/div/div[2]/div[2]/div').click()
    

def __store_coordinates(textfile: str, lat: float, lon: float, image_path: str):
    """
    given args, store them as a string label
    """
    with open(textfile, 'a') as f:
        to_write = str(lat) + ', ' + str(lon) + ', ' + image_path + '\n'
        f.write(to_write)


def __find_actual_location(driver: webdriver): 
    """
    given driver, find the marker for the actual location, click on it (which will derive a google maps tab),
    and gather latitude & longitude data from google maps url
    """
    time.sleep(2)
    driver.find_element(webdriver.common.by.By.XPATH, '//*[@id="__next"]/div[2]/div[3]/main/div[2]/div/div[1]/div[1]/div/div/div/div[2]/div[2]/div/div[3]/div[3]/div').click()
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(6) # required for url to update
    google_maps_url = driver.current_url
    coordinates = google_maps_url.split('@')[-1].split(',')[:2]
    parent = driver.window_handles[0]
    chld = driver.window_handles[1]
    driver.switch_to.window(chld)    
    driver.close() # to close the google maps tab
    return float(coordinates[0]), float(coordinates[1])


def __place_marker(driver: webdriver):
    """
    given driver, place a (currently, random) marker on a geographical map in a game of geoguessr
    """
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(driver.find_element(webdriver.common.by.By.TAG_NAME, 'canvas'), 320, 150).click().perform()
    time.sleep(1)
    action.move_to_element_with_offset(driver.find_element(webdriver.common.by.By.TAG_NAME, 'canvas'), 320, 280).click().perform()


def geoguessr_login(driver: webdriver):
    """
    given driver, logs into geoguessr.com with username and pwd in crendentials.py
    """
    driver.get('https://www.geoguessr.com/signin')
    __enable_cookies(driver)
    
    action = webdriver.common.action_chains.ActionChains(driver)
    driver.find_element(webdriver.common.by.By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/main/div/div/form/div/div[1]/div[2]/input').send_keys(username)
    driver.find_element(webdriver.common.by.By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/main/div/div/form/div/div[2]/div[2]/input').send_keys(pwd)
    time.sleep(1)
    driver.find_element(webdriver.common.by.By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/main/div/div/form/div/div[3]/div[1]/div/button').click()
    time.sleep(3)


def __enable_cookies(driver: webdriver):
    """
    given driver, gets rid of 'enable cookies?' pop-up for current tab
    """
    time.sleep(2)
    driver.execute_script("""
        var l = document.getElementsByClassName("onetrust-pc-dark-filter ot-fade-in")[0];
        l.parentNode.removeChild(l);
        var l = document.getElementsByClassName("ot-sdk-container")[0];
        l.parentNode.removeChild(l);
    """)


def __create_screenshot(driver: webdriver, folder: str):
    """
    given driver and folder, takes a screenshot of the streetview canvas and saves it in folder
    """
    image_path = f'{folder}/canvas_{int(time.time())}.png'
    f = open(image_path, 'xb')
    __enable_cookies(driver)
    gui_classes = ['game_guessMap__MTlQ_', 'game_status__q_b7N game_statusWithCompassTop__F_unm', 'game_topHud__tAKJD', 'game_controls___pIfC',
                   'gmnoprint SLHIdE-sv-links-control', 'gmnoprint', 'gmnoprint', 'gmnoprint gm-style-cc', 'gm-style-cc']
    for class_id in gui_classes:
        try:
            driver.execute_script("""
               var l = document.getElementsByClassName("{}")[0];
                l.parentNode.removeChild(l);
            """.format(class_id))
        except:
            pass

    canvas = driver.find_element(webdriver.common.by.By.TAG_NAME, 'canvas')
    time.sleep(1)
    f.write(canvas.screenshot_as_png)
    return image_path
