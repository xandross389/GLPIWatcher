from abc import ABC, abstractmethod
from src.ticket import Ticket
import hashlib
from datetime import datetime
from pathlib import Path
from random import uniform
# Abstract class declaration for Ad base class
import json
import os
from time import sleep
import pyperclip
# import pyautogui
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.ticket import Status


class Glpi():
    # URLs
    # URL_LOGIN = "http://informacionti.etecsa.cu"
    URL_LOGOUT = "/front/logout.php?noAUTO=1"
    URL_TICKETS = "/front/ticket.php"
    # locators
    XPATH_LOGIN_USERNAME = "/html/body/div[1]/div[2]/form/p[1]/input"
                          # "/html/body/div[1]/div[3]/form/p[1]/input"  # //*[@id="login_name"]
    XPATH_LOGIN_PASSWORD = "/html/body/div[1]/div[2]/form/p[2]/input"
                        # "/html/body/div[1]/div[3]/form/p[2]/input"  # //*[@id="login_password"]
    XPATH_LOGIN_BUTTON = "/html/body/div[1]/div[2]/form/p[5]/input"
                        # "/html/body/div[1]/div[3]/form/p[4]/input"  # //*[@id="boxlogin"]/form/p[4]/input
    XPATH_LOGOUT_BUTTON = "/html/body/div[1]/header/div[2]/ul/li[1]/a"
    XPATH_MENU_BUTTON = "/html/body/div[1]/div[1]/a/i"
    XPATH_TICKETS_BUTTON = "/html/body/div[3]/div[2]/dl[2]/dd[1]/a"
    # Defaults constants
    DEFAULT_RAND_MIN = 1
    DEFAULT_RAND_MAX = 3
    # TODO: Move these parameter to a json configuration file
    # Constants
    TXT_ERR_LOADING_PAGE = 'Error loading page'
    TXT_ERR_INTERACTING_WITH_ELEMENT = 'Error interacting with element'
    TXT_ERR_UPLOADING_IMAGES = 'Error uploading image(s)'
    TXT_WAITING_FOR_AD_INSERT_FINISHES = 'Waiting for ad insert finishes...'
    TXT_AD_INSERTED = 'Ad inserted!!! Go ahead...'
    TXT_TIMED_OUT_WAITING_FOR_AD_INSERT_TRYING_AGAIN = 'Timed out waiting for ad insert. Trying again'
    TXT_GO_TO_PROCESS_NEXT_AD_OR_FINISH = 'Go to process next ad or finish'
    TXT_TIMED_OUT_WAITING_SELECTOR = ''

    def __init__(self, web_driver=None):
        self._web_driver = web_driver

    @property
    def web_driver(self):
        return self._web_driver

    def login(self, login_page="", username="", password=""):
        assert username != "" and password != ""

        if username != "" and password != "":
            self.web_driver.get(login_page)

            try:
                WebDriverWait(self.web_driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, self.XPATH_LOGIN_USERNAME))).send_keys(username)
            except TimeoutException:
                print('username box not found')

            try:
                WebDriverWait(self.web_driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, self.XPATH_LOGIN_PASSWORD))).send_keys(password)
            except TimeoutException:
                print('password box not found')

            try:
                WebDriverWait(self.web_driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, self.XPATH_LOGIN_BUTTON))).click()
            except TimeoutException:
                print('login button not found')

        return self.is_logged_in()

    def is_logged_in(self):
        try:
            print('Waiting for login process finishes...')
            WebDriverWait(self.web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_LOGOUT_BUTTON))
            )
            print('User is logged in')
            return True
        except TimeoutException:
            print('User is not logged in')
            return False

    def logout(self):
        try:
            print('Waiting for logout process finishes...')
            WebDriverWait(self.web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_LOGOUT_BUTTON))
            ).click()
            print('User is logged out')
            return True
        except TimeoutException:
            print('User is not logged out')
            return False

    def get_opened_tickets(self, limit_count=100):
        opened_tickets = []

        try:
            print('Waiting for main menu button...')
            WebDriverWait(self.web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_MENU_BUTTON))
            ).click()
        except TimeoutException:
            print('main menu not found')
            return False

        try:
            print('Waiting for tickets button')
            WebDriverWait(self.web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_TICKETS_BUTTON))
            ).click()
            # return True
        except TimeoutException:
            print('tickets button not found')
            return False

        self.set_display_number_elements(limit_count)
        self.set_filter_tickets_by_status(status=Status.EN_CURSO)

        for i in range(limit_count):
            id_locator = f"/html/body/main/div/form[2]/div/table/tbody/tr[{i + 1}]/td[2]"
            url_locator = f"/html/body/main/div/form[2]/div/table/tbody/tr[{i + 1}]/td[3]/a"
            status_locator = f"/html/body/main/div/form[2]/div/table/tbody/tr[{i + 1}]/td[5]"
            assigned_user_locator = f"/html/body/main/div/form[2]/div/table/tbody/tr[{i + 1}]/td[10]"

            element_id = WebDriverWait(self.web_driver, 60).until(
                EC.presence_of_element_located((By.XPATH, id_locator))
            )
            ticket_id = element_id.text

            element_url = WebDriverWait(self.web_driver, 60).until(
                EC.presence_of_element_located((By.XPATH, url_locator))
            )
            ticket_url = element_url.text

            element_status = WebDriverWait(self.web_driver, 60).until(
                EC.presence_of_element_located((By.XPATH, status_locator))
            )
            ticket_status = element_status.text

            element_user = WebDriverWait(self.web_driver, 60).until(
                EC.presence_of_element_located((By.XPATH, assigned_user_locator))
            )
            ticket_assigned_user = element_user.text

            # print(f"Ticket: {ticket_url}, {ticket_id}, {ticket_assigned_user}, {ticket_status}")

            opened_tickets.append(Ticket(
                url=ticket_url,
                ticket_id=ticket_id,
                assigned_user=ticket_assigned_user,
                status=ticket_status
            ))

        return opened_tickets

    def set_waiting_ticket_by_url(self, url):
        pass  # TODO: Set to on waiting given url ticket if opened

    def set_waiting_ticket_by_id(self, id):
        pass  # TODO: Set to on waiting given id ticket if opened

    def set_waiting_ticket_by_xpath_locator(self, xpath_locator):
        pass  # TODO: Set to on waiting given xpath_locator ticket if opened

    def apply_search_filter(self, criteria="", operand="", value=""):
        pass

    def set_filter_tickets_by_status(self, status=Status.EN_CURSO_ASIGNADA):
        xpath_criteria_combo = "/html/body/main/div/form[1]/div/ul/li[1]/span[2]/span[1]/span"
        xpath_criteria_combo_input = "/html/body/span[2]/span/span[1]/input"
        xpath_status_combo = "/html/body/main/div/form[1]/div/ul/li[1]/span[3]/span[2]/span/span[1]/span"
        xpath_status_combo_input = "/html/body/span[2]/span/span[1]/input"
        xpath_search_button = "/html/body/main/div/form[1]/div/div/input"

        # set criteria to status
        try:
            WebDriverWait(self.web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, xpath_criteria_combo))
            ).click()

            element = WebDriverWait(self.web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, xpath_criteria_combo_input))
            )
            element.send_keys("Status")
            element.send_keys(Keys.ENTER)

            # set status
            try:
                WebDriverWait(self.web_driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_status_combo))
                ).click()

                element = WebDriverWait(self.web_driver, 60).until(
                    EC.element_to_be_clickable((By.XPATH, xpath_status_combo_input))
                )
                element.send_keys(status)
                element.send_keys(Keys.ENTER)

                self.web_driver.find_element_by_xpath(xpath_search_button).click()

            except TimeoutException:
                print('status locator not found')

        except TimeoutException:
            print('criteria locator not found')

    def set_display_number_elements(self, count=100):
        xpath_display_combo = "/html/body/main/div/div[1]/table/tbody/tr/td[1]/form/span[2]"
        xpath_display_combo_input = "/html/body/span[2]/span/span[1]/input"

        try:
            WebDriverWait(self.web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, xpath_display_combo))
            ).click()

            element = WebDriverWait(self.web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, xpath_display_combo_input))
            )
            element.send_keys(count)
            element.send_keys(Keys.ENTER)
        except TimeoutException:
            print(' button not found')


# class RevolicoAd(Ad):
#     '''
#     Revolico Categories
#     value: 31 - Compra / Venta -> Celulares/Líneas/Accesorios
#
#
#     Revolico Provinces
#     value: 4 - Pinar del Río
#
#     '''
#     # LOCATORS
#     URL_ROOT_PAGE = 'https://www.revolico.com'
#     URL_INSERT_AD = 'https://www.revolico.com/insertar-anuncio.html'
#     # XPATH selectors
#     XPATH_RECAPTCHA_CHECKBOX_LOCATOR = '//*[@id="recaptcha-accessible-status"]'
#     XPATH_RECAPTCHA_ANCHOR_CONTENT_LOCATOR = '//*[@id="rc-anchor-container"]/div[3]'
#     XPATH_PRICE_SELECTOR = '//*[@id="ad-price"]'
#     XPATH_CURRENCY_SELECTOR = '//*[@id="currency-select"]'
#     XPATH_CATEGORY_SELECTOR = '//*[@id="subcategory-select"]'
#     XPATH_PROVINCE_SELECTOR = '//*[@id="province-select"]'
#     XPATH_MUNICIPALITY_SELECTOR = '//*[@id="municipality-select"]'
#     XPATH_TITLE_SELECTOR = '//*[@id="ad-title"]'
#     XPATH_DESCRIPTION_SELECTOR = '//*[@id="ad-description"]'
#     XPATH_MAIL_SELECTOR = '//*[@id="ad-email"]'
#     XPATH_NAME_SELECTOR = '//*[@id="ad-name"]'
#     XPATH_PHONE_SELECTOR = '//*[@id="ad-phone"]'
#     XPATH_IMAGE_UPLOAD_BUTTON_LOCATOR = '//*[@id="__next"]/div/main/div/div/form/div[1]/section[3]/div/div/div/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[1]/button'
#     XPATH_IMAGE_UPLOAD_BUTTON_2_LOCATOR = '//*[@id="__next"]/div/main/div/div/form/div[1]/section[3]/div/div/div/div[1]/div/div/div/div/div[2]/div/span[1]/div/div[2]/div[1]/div/button'
#     XPATH_IMAGE_UPLOAD_MORE_BUTTON_LOCATOR = '//*[@id="__next"]/div/main/div/div/form/div[1]/section[3]/div/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/button[2]'
#     XPATH_GO_BACK_AFTER_IMAGE_UPLOAD_MORE_BUTTON_LOCATOR = '//*[@id="__next"]/div/main/div/div/form/div[1]/section[3]/div/div/div/div[1]/div/div/div/div/div[2]/div/span[1]/div/div[1]/button'
#     XPATH_RETRY_UPLOAD_IMAGES_LOCATOR = '//*[@id="__next"]/div/main/div/div/form/div[1]/section[3]/div/div/div/div[1]/div/div/div/div/div[2]/div/div[3]/div[1]/div[3]/button[1]'
#     XPATH_IMAGES_UPLOAD_STATUS_LOCATOR = '/html/body/div[1]/div/main/div/div/form/div[1]/section[3]/div/div/div/div[1]/div/div/div/div/div[2]/div/div[2]/div[2]'
#     XPATH_DELETE_INSERTED_AD_LOCATOR = '/html/body/div[1]/div/main/div/div/div/div/ul/li[3]/a'
#     XPATH_SUBMIT_AD_BUTTON_LOCATOR = '//*[@id="__next"]/div/main/div/div/form/div[2]/fieldset/button'
#     XPATH_CANCEL_AD_BUTTON_LOCATOR = '//*[@id="__next"]/div/main/div/div/form/div[2]/fieldset/button'
#     # CSS selectors
#     XPATH_NO_PUBLIC_EMAIL_CSS_SELECTOR = '#radio2'
#     XPATH_PUBLIC_EMAIL_CSS_SELECTOR = '#radio1'
#     # texts
#     TXT_IMAGES_UPLOAD_COMPLETED = 'Completado'
#
#     def __init__(self, web_driver=None, auto_click_im_not_bot=False):
#         super().__init__(web_driver, auto_click_im_not_bot)
#         self._currency = ''
#         self._use_public_mail = False
#         self._image_1_filename = ''
#         self._image_2_filename = ''
#         self._image_3_filename = ''
#
#     @staticmethod
#     def get_inserted_ad_id_from_inserted_url(url=''):
#         assert url != ''
#         var_adid_subcad = 'adid='
#         var_adid_start_index = url.index(var_adid_subcad)
#         after_id_sub_cad = '&token='
#         id_end_index = url.index(after_id_sub_cad)
#         id_start_index = var_adid_start_index + len(var_adid_subcad)
#         return url[id_start_index:id_end_index]
#
#     @staticmethod
#     def get_insert_ad_xpath_locator_from_id(ad_id=''):
#         return f'//*[@id="ad-{ad_id}"]/ul/li[4]/a'
#
#     def logout_from_ad_site(self, logout_url=None, xpath_logout_btn_locator=None,
#                             xpath_logged_out_element_locator=None,
#                             delayed=False, rand_min=0, rand_max=1):
#         pass
#
#     def load_from_json(self, json_filename):
#         try:
#             with open(json_filename, "r") as read_file:
#                 ads_string = json.load(read_file)
#                 try:
#                     self._obfuscate = ads_string['obfuscate']
#                     self._title_obf_level = ads_string['title_obf_level']
#                     self._desc_obf_level = ads_string['desc_obf_level']
#                     self._enabled = ads_string['enabled']
#                     self._schedule = ads_string['schedule']
#                     self._price = ads_string['price']
#                     self._currency = ads_string['currency']
#                     self._category = ads_string['category']
#                     self._province = ads_string['province']
#                     self._municipality = ads_string['municipality']
#                     self._title = ads_string['title']
#                     self._description = ads_string['description']
#                     self._mail = ads_string['mail']
#                     self._name = ads_string['name']
#                     self._phone = ads_string['phone']
#                     self._use_public_mail = ads_string['use_public_mail'] == 'true'
#                     self._image_1_filename = ads_string['image_1_filename']
#                     self._image_2_filename = ads_string['image_2_filename']
#                     self._image_3_filename = ads_string['image_3_filename']
#                 except Exception as asign_error:
#                     print(f"Error asigning json field - {asign_error}")
#         except Exception as file_err:
#             print(f"Err loading json from file  - {file_err}")
#         finally:
#             read_file.close()
#
#     # getters
#     def obfuscate(self):
#         return self._obfuscate
#
#     def enabled(self):
#         return self._enabled
#
#     def get_schedule(self):
#         return self._schedule
#
#     def get_price(self):
#         return self._price
#
#     def get_category(self):
#         return self._category
#
#     def get_province(self):
#         return self._province
#
#     def get_municipality(self):
#         return self._municipality
#
#     def get_title(self):
#         return self._title
#
#     def get_description(self):
#         return self._description
#
#     def get_mail(self):
#         return self._mail
#
#     def get_use_public_mail(self):
#         return self._use_public_mail
#
#     def get_name(self):
#         return self._name
#
#     def get_phone(self):
#         return self._phone
#
#     def get_currency(self):
#         return self._currency
#
#     def get_image_1_filename(self):
#         return self._image_1_filename
#
#     def get_image_2_filename(self):
#         return self._image_2_filename
#
#     def get_image_3_filename(self):
#         return self._image_3_filename
#
#     def publish_ad(self, delayed=True, rand_min=12, rand_max=15):
#         print('Ad: ' + self.get_title())
#
#         try:
#             AdUtils.wait_between(rand_min, rand_max) if delayed else None
#             # self.web_driver.get(self.URL_INSERT_AD)
#             # if not self.web_driver.current_url == self.URL_ROOT_PAGE:
#             print('curr url ')
#             curr_url = self.web_driver.current_url
#             print('curr url ' + curr_url)
#             if 'insertado' in curr_url:
#                 last_inserted_id = RevolicoAd.get_inserted_ad_id_from_inserted_url(curr_url)
#                 new_ad_xpath_locator = RevolicoAd.get_insert_ad_xpath_locator_from_id(last_inserted_id)
#                 self.web_driver.find_element_by_xpath(new_ad_xpath_locator).click()
#                 self.web_driver.get(RevolicoAd.get_inserted_ad_id_from_inserted_url())
#             elif curr_url == self.URL_ROOT_PAGE or curr_url == self.URL_ROOT_PAGE + '/':
#                 self.web_driver.find_element_by_xpath('//*[@id="new_ad"]').click()
#             else:
#                 self.web_driver.get(self.URL_ROOT_PAGE)
#                 sleep(10)
#                 self.web_driver.find_element_by_xpath('//*[@id="new_ad"]').click()
#
#         except Exception as err:
#             print(f"{self.TXT_ERR_LOADING_PAGE} ({self.URL_INSERT_AD}) {err}")
#
#         recaptcha_loaded = False
#         recaptcha_loaded_retry_counts = 0
#         while not recaptcha_loaded or recaptcha_loaded_retry_counts <= 5:
#             try:
#                 print('Waiting for ReCaptcha loads...')
#                 WebDriverWait(self.web_driver, 45).until(EC.frame_to_be_available_and_switch_to_it(
#                     (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
#                 WebDriverWait(self.web_driver, 45).until(
#                     EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']")))
#                 recaptcha_loaded = True
#             except TimeoutException:
#                 print("Timed out waiting for ReCaptcha to load. Trying again")
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.refresh()
#             finally:
#                 # change back to default iframe
#                 print('ReCaptcha loaded!!! Go ahead')
#                 self.web_driver.switch_to.default_content()
#
#             recaptcha_loaded_retry_counts += 1
#
#         if recaptcha_loaded:
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.find_element_by_xpath(self.XPATH_PRICE_SELECTOR).send_keys(self.get_price())
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} price - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.find_element_by_xpath(self.XPATH_CURRENCY_SELECTOR).send_keys(
#                     self.get_currency())
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} currency - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.find_element_by_xpath(self.XPATH_CATEGORY_SELECTOR).send_keys(
#                     self.get_category())
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} category - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.find_element_by_xpath(self.XPATH_PROVINCE_SELECTOR).send_keys(
#                     self.get_province())
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} province - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.find_element_by_xpath(self.XPATH_MUNICIPALITY_SELECTOR).send_keys(
#                     self.get_municipality())
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} municipality - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#
#                 if self.obfuscate():
#                     title = self.get_obfuscated_title()
#                 else:
#                     title = self.get_title()
#
#                 # pyperclip.copy('')
#                 # pyperclip.copy(title)
#                 # self.web_driver.find_element_by_xpath(self.XPATH_TITLE_SELECTOR).send_keys(Keys.CONTROL + "v")
#                 self.web_driver.find_element_by_xpath(self.XPATH_TITLE_SELECTOR).send_keys(title)
#                 # pyperclip.copy('')
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} title - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#
#                 if self.obfuscate():
#                     body = self.get_obf_description()
#                 else:
#                     body = self.get_description()
#
#                 pyperclip.copy('')
#                 pyperclip.copy(body)
#                 self.web_driver.find_element_by_xpath(self.XPATH_DESCRIPTION_SELECTOR).send_keys(Keys.CONTROL + "v")
#                 pyperclip.copy('')
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} description - {err}")
#
#             if not self.get_use_public_mail():
#                 try:
#                     AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                     self.web_driver.find_element_by_css_selector(self.XPATH_NO_PUBLIC_EMAIL_CSS_SELECTOR).click()
#                 except Exception as err:
#                     print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} public email - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.find_element_by_xpath(self.XPATH_MAIL_SELECTOR).send_keys(self.get_mail())
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} mail - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.find_element_by_xpath(self.XPATH_NAME_SELECTOR).send_keys(self.get_name())
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} name - {err}")
#
#             try:
#                 AdUtils.wait_between(rand_min, rand_max) if delayed else None
#                 self.web_driver.find_element_by_xpath(self.XPATH_PHONE_SELECTOR).send_keys(self.get_phone())
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} phone - {err}")
#
#             # Images uploading
#             try:
#                 self.upload_ad_images(delayed=delayed, rand_min=rand_min, rand_max=rand_max)
#             except Exception as err:
#                 print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} image - {err}")
#
#             if self.auto_click_im_not_bot:
#                 # click i am not a robot
#                 try:
#                     print("Trying click i am not robot button")
#                     WebDriverWait(self.web_driver, 120).until(EC.frame_to_be_available_and_switch_to_it(
#                         (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
#                     AdUtils.wait_between(rand_min=5, rand_max=8)
#                     WebDriverWait(self.web_driver, 120).until(
#                         EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
#                     print('ReCaptcha clicked')
#                 except TimeoutException:
#                     print("Timed out waiting for ReCaptcha to click captcha")
#                     self.web_driver.refresh()
#                 finally:
#                     # change back to default iframe
#                     self.web_driver.switch_to.default_content()
#
#             # check if catcha is solved
#             try:
#                 print("Waiting for captcha solves to submit button")
#                 WebDriverWait(self.web_driver, 180).until(EC.frame_to_be_available_and_switch_to_it(
#                     (By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
#                 WebDriverWait(self.web_driver, 180).until(
#                     EC.presence_of_element_located((By.XPATH, "//span[@aria-checked='true']")))
#                 print('ReCaptcha solved')
#                 # change back to default iframe
#                 self.web_driver.switch_to.default_content()
#                 # submit button click
#                 try:
#                     self.web_driver.find_element_by_xpath(self.XPATH_SUBMIT_AD_BUTTON_LOCATOR).click()
#                     print("Submit button clicked")
#                 except Exception as err:
#                     print(f"{self.TXT_ERR_INTERACTING_WITH_ELEMENT} submit button  - {err}")
#
#             except TimeoutException:
#                 print("Timed out waiting for ReCaptcha solves to click submit button")
#                 self.web_driver.refresh()
#             finally:
#                 # change back to default iframe
#                 self.web_driver.switch_to.default_content()
#
#             ad_created = False
#             ad_created_retry_counts = 0
#             # current_url = self.web_driver.current_url
#             while not ad_created or ad_created_retry_counts <= 3:
#                 try:
#                     print('Waiting for ad insert finishes (captcha solves)...')
#                     WebDriverWait(self.web_driver, 240).until(
#                         EC.presence_of_element_located((By.XPATH, self.XPATH_DELETE_INSERTED_AD_LOCATOR))
#                     )
#                     ad_created = True
#                     print('Ad inserted!!! Go ahead...')
#                 except TimeoutException:
#                     print("Timed out waiting for ad insert. Trying again")
#                 finally:
#                     print('Go to process next ad or finish')
#
#                 ad_created_retry_counts += 1
#                 print(f"Remaining times {ad_created_retry_counts}")
#         else:
#             print('Failed ReCaptcha loading :-( |==> Ad publication skipped !!!')
#
#     def upload_ad_images(self, delayed=True, rand_min=0.2, rand_max=0.5):
#         filenames_str = ''
#
#         if not self.get_image_1_filename() == '':
#             image_1_abs_path = os.path.abspath(os.path.join(
#                 os.getcwd() + '/' + self.IMAGES_SUB_FOLDER + self.get_image_1_filename()))
#             if os.path.exists(image_1_abs_path):
#                 filenames_str += image_1_abs_path
#             else:
#                 print('File (' + image_1_abs_path + ') not exists')
#
#         if not self.get_image_2_filename() == '':
#             image_2_abs_path = os.path.abspath(os.path.join(
#                 os.getcwd() + '/' + self.IMAGES_SUB_FOLDER + self.get_image_2_filename()))
#             if os.path.exists(image_2_abs_path):
#                 if filenames_str == '':
#                     filenames_str += image_2_abs_path
#                 else:
#                     filenames_str += '" "' + image_2_abs_path
#             else:
#                 print('File (' + image_2_abs_path + ') not exists')
#
#         if not self.get_image_3_filename() == '':
#             image_3_abs_path = os.path.abspath(os.path.join(
#                 os.getcwd() + '/' + self.IMAGES_SUB_FOLDER + self.get_image_3_filename()))
#             if os.path.exists(image_3_abs_path):
#                 if filenames_str == '':
#                     filenames_str += image_3_abs_path
#                 else:
#                     filenames_str += '" "' + image_3_abs_path
#             else:
#                 print('File (' + image_3_abs_path + ') not exists')
#
#         # if not filenames_str == '':
#         #     AdUtils.wait_between(rand_min=rand_min, rand_max=rand_max) if delayed else None
#         #     try:
#         #         print('Submiting upload image button...')
#         #         self.web_driver.find_element_by_xpath(self.XPATH_IMAGE_UPLOAD_BUTTON_LOCATOR).click()
#         #         sleep(2)
#         #         try:
#         #             pyautogui.write('"' + filenames_str + '"')
#         #             AdUtils.wait_between(rand_min=rand_min, rand_max=rand_max) if delayed else None
#         #             print('Sending images tu server...')
#         #             pyautogui.press('enter')
#         #         except Exception as err:
#         #             print(f"Error uploading images - {err}")
#         #
#         #     except Exception as err:
#         #         print(f"Error clicking upload images button - {err}")
#         # return
