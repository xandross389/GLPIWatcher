from time import sleep

# internal constants
from selenium import webdriver

from src.configuration_manager import ConfigurationManager
from src.glpi import Glpi
from src.ticket import Status

config_manager = ConfigurationManager()
config = config_manager.get_config()

sleep(30)

# Global variabless
RAND_MIN = 1
RAND_MAX = 2
JSON_EXTENSION = '.json'
# Enable or Disable site ads publication
PORLALIVRE_ENABLED = True


def get_web_driver(headless=False):
    # # OBFUSCATE SELENIUM CLIENT
    options = webdriver.ChromeOptions()
    # # Removes navigator.webdriver flag
    # # For older ChromeDriver under version 79.0.3945.16
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    # # For ChromeDriver version 79.0.3945.16 or over
    # options.add_argument("--disable-blink-features")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    # # Change Browser Options
    # # option.add_argument("window-size=1355,760")
    # options.add_argument("start-maximized")
    # options.add_argument(
    #     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    #     "Chrome/74.0.3729.169 Safari/537.36")
    # # option.add_argument('--no-sandbox')
    options.headless = headless
    # # For ChromeDriver version 79.0.3945.16 or over
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    #
    # # Open Browser
    driver = webdriver.Chrome(executable_path=config.chrome_executable_path, options=options)
    # driver.set_page_load_timeout(PAGE_LOADING_TIMEOUT)
    # # driver.implicitly_wait(0.5)
    # driver = uc.Chrome(options=load_chrome_profile(PROFILE_FOLDER, headless=headless),
    #                    version_main=94, executable_path=CHROME_EXECUTABLE_PATH)
    return driver


def is_working_time():
    # TODO
    return True


if __name__ == '__main__':
    if is_working_time():
        print()
        with get_web_driver(headless=config.headless_browsing) as web_driver:
            if config.monitor_enable:

                glpi = Glpi(web_driver)

                if glpi.login(config.login_page, config.username, config.password):
                    opened_tickets = glpi.get_opened_tickets()

                    for opened_ticket in opened_tickets:
                        # opened_ticket.set_state("EN ESPERA")
                        print(f"closing ticket {opened_ticket.id}")
                        opened_ticket.set_state(web_driver=web_driver, state=Status.EN_ESPERA)

                    print("logged in")
                    sleep(30)
                    if glpi.logout():
                        print("logged out")
                else:
                    print(f"No se pudo iniciar sesion con el usuario {config.username}")
            # sleep(60)



