from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import click

class element_to_be_clickable(object):
    def __init__(self, element):
        self.element = element

    def __call__(self, driver):
        if self.element.is_displayed() and self.element.is_enabled():
           return self.element
        return False

def wait(driver, timeout, method):
    return WebDriverWait(driver, timeout).until(method)

def login(driver, user, pw):
    user_input = driver.find_element_by_id('lemail').send_keys(user)
    pass_input = driver.find_element_by_id('lpassword').send_keys(pw)
    # click log in button
    # login_button = driver.find_element_by_xpath("//button[text()='Log In']")
    wait(driver, 10, EC.invisibility_of_element_located((By.CLASS_NAME, "preloader")))
    # wait(driver, 10, EC.presence_of_element_located((By.XPATH, "//button[text()='Log In']"))).click()
    driver.find_element_by_xpath("//button[text()='Log In']").click()

def switch_to_demo(driver):
    # click side menu button
    wait(driver, 10, EC.element_to_be_clickable((By.CLASS_NAME, "m-page-header__left-button"))).click()
    demo_switch = wait(driver, 10, EC.element_to_be_clickable((By.CLASS_NAME, "switch__switch")))
    # if not demo_switch.is_selected:
    demo_switch.click()
    # deselect side menu
    # driver.find_element_by_xpath("//html").click()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def cleanup_text(text):
    text = text.split("\n")[0]
    return text.replace(" ", "")

def get_change(text):
    return float(cleanup_text(text).replace("%", ""))


def close_by_profit(driver, pair, want_change_percent):
    try:
        bot_row_es = wait(driver, 10, EC.presence_of_all_elements_located((By.CLASS_NAME, "m-bots-rows__panel-root")))
    except:
        raise Exception('no bots defined')
    for bot_row_e in bot_row_es:
        # check pair value
        if cleanup_text(bot_row_e.find_element_by_class_name("m-bots-rows__centered-block").text) == pair:
            # check change value
            if get_change(bot_row_e.find_element_by_class_name("value-change__percents").text) >= want_change_percent:
                # click bot row for details
                wait(driver, 10, EC.invisibility_of_element_located((By.CLASS_NAME, "MuiBackdrop-root")))
                bot_row_e.click()
                # click close button
                wait(driver, 10, element_to_be_clickable(bot_row_e.find_element_by_class_name("m-bots-rows__button_color_red"))).click()
                # click close method dropdown
                driver.find_element_by_class_name("dropdown-input__button").click()
                # click 'sell at market price'
                driver.find_element_by_xpath("//div[contains(text(), 'Sell at the market price')]/..").click()
                # click 'close bot' button
                driver.find_element_by_xpath("//span[contains(text(), 'Close bot')]/..").click()

@click.group()
def cli():
    pass

@cli.command('take-profit')
@click.option('--username', required=True)
@click.option('--password', required=True)
@click.option('--is_demo', type=bool, default=False, required=False)
@click.option('--pair', required=True)
@click.option('--change', type=float, required=True)
def take_profit(username, password, is_demo, pair, change):
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('window-size=800x600')
    # driver = webdriver.Chrome(options=options)

    options = webdriver.FirefoxOptions()
    options.headless = True
    options.add_argument("-width=800")
    options.add_argument("-height=600")
    driver = webdriver.Firefox(options=options)

    driver.get("https://app.bitsgap.com/bot")

    login(driver, username, password)
    if is_demo:
        switch_to_demo(driver)
    close_by_profit(driver, pair, change)

if __name__ == '__main__':
    cli()
