from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Ticket:
    """
    Tickets locators
    """
    XPATH_BUTTON_SAVE = "/html/body/main/div[2]/div[2]/div[2]/form/div/div[2]/input[1]" # '//*[@id="tabsbody"]/div[2]/input[1]'
    XPATH_STATUS_COMBO = "/html/body/main/div[2]/div[2]/div[2]/form/div/table[2]/tbody/tr[2]/td[1]/span/span[1]/span"
                         # '//*[@id="select2-dropdown_criteria_0__value_98844551-container"]'
    """
    Tickets URLs
    """
    URL_TICKETS = "https://informacionti.etecsa.cu/front/ticket.php"

    def __init__(self, url="", ticket_id=0, xpath_locator="", assigned_user="", status=""):
        self.url = url
        self.ticket_id = ticket_id
        self.xpath_locator = xpath_locator
        self.assigned_user = assigned_user
        self.status = status

    def set_state(self, status, web_driver=None):
        web_driver.get(self.url)
        "/html/body/main/div[2]/div[2]/div[2]/form/div/table[2]/tbody/tr[2]/td[1]/select"
        "/html/body/main/div[2]/div[2]/div[2]/form/div/table[2]/tbody/tr[2]/td[1]/select/option[1]"
        try:
            status_combo = WebDriverWait(web_driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, self.XPATH_STATUS_COMBO))
            ).click()
            status_combo.select_by_visible_text(Status.EN_ESPERA)

            # You can also use
            # status_combo.select_by_value(Status.EN_ESPERA)
            # details_period.select_by_visible_text()
            # details_period.select_by_index()

        except TimeoutException:
            print(' button not found')


class Status(object):
    """
    Set of tickets status.
    """

    NUEVO = "New"
    NUEVO_ID = 30
    EN_CURSO = "Processing"
    EN_CURSO_ASIGNADA = "Processing (assigned)"
    EN_CURSO_PLANIFICADA = "Processing (planned)"
    EN_CURSO_PLANIFICADA_ID = 31
    EN_ESPERA = "Pending"
    EN_ESPERA_ID = 32
    RESUELTO = "Solved"
    RESUELTO_ID = 33
    CARRADO = "Closed"
    CARRADO_ID = 34
