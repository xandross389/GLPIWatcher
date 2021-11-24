import json
import os

DEFAULT_CONFIG_FILENAME = './config.json'


class ConfigurationException(Exception):
    pass


class CredentialsDictException(ConfigurationException):
    pass


class Configuration:
    def __init__(self, password="", username="", chrome_executable_path="./chromedriver/chromedriver.exe",
                 headless_browsing=True, page_loading_timeout=60, monitor_enable=False,
                 login_page="https://informacionti.etecsa.cu/", tickets_page="https://informacionti.etecsa.cu/ticket.php",
                 close_tickets_retry_times=5, allow_opened_tickets_begin_time="08:00",
                 allow_opened_tickets_end_time="17:30"):
        self._password = password
        self._username = username
        self._chrome_executable_path = chrome_executable_path
        self._headless_browsing = headless_browsing
        self._page_loading_timeout = page_loading_timeout
        self._monitor_enable = monitor_enable
        self._login_page = login_page
        self._tickets_page = tickets_page
        self._close_tickets_retry_times = close_tickets_retry_times
        self._allow_opened_tickets_begin_time = allow_opened_tickets_begin_time
        self._allow_opened_tickets_end_time = allow_opened_tickets_end_time

    # getters
    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username

    @property
    def chrome_executable_path(self):
        return self._chrome_executable_path

    @property
    def headless_browsing(self):
        return self._headless_browsing

    @property
    def page_loading_timeout(self):
        return self._page_loading_timeout

    @property
    def monitor_enable(self):
        return self._monitor_enable

    @property
    def login_page(self):
        return self._login_page

    @property
    def tickets_page(self):
        return self._tickets_page

    @property
    def close_tickets_retry_times(self):
        return self._close_tickets_retry_times

    @property
    def allow_opened_tickets_begin_time(self):
        return self._allow_opened_tickets_begin_time

    @property
    def allow_opened_tickets_end_time(self):
        return self._allow_opened_tickets_end_time

    # setters
    @password.setter
    def password(self, value):
        self._password = value

    @username.setter
    def username(self, value):
        self._username = value

    @chrome_executable_path.setter
    def chrome_executable_path(self, value):
        self._chrome_executable_path = value

    @headless_browsing.setter
    def headless_browsing(self, value):
        self._headless_browsing = value

    @page_loading_timeout.setter
    def page_loading_timeout(self, value):
        self._page_loading_timeout = value

    @monitor_enable.setter
    def monitor_enable(self, value):
        self._monitor_enable = value

    @login_page.setter
    def login_page(self, value):
        self._login_page = value

    @tickets_page.setter
    def tickets_page(self, value):
        self._tickets_page = value

    @close_tickets_retry_times.setter
    def close_tickets_retry_times(self, value):
        self._close_tickets_retry_times = value

    @allow_opened_tickets_begin_time.setter
    def allow_opened_tickets_begin_time(self, value):
        self._allow_opened_tickets_begin_time = value

    @allow_opened_tickets_end_time.setter
    def allow_opened_tickets_end_time(self, value):
        self._allow_opened_tickets_end_time = value


class ConfigurationManager:
    def __init__(self, config_file=DEFAULT_CONFIG_FILENAME):
        self._config_file = config_file
        self._config = Configuration()

    @property
    def config(self):
        return self._config

    def create_default_configuration_file(self):
        config = {
            'username': self.config.username,
            'password': self.config.password,
            'chrome_executable_path': self.config.chrome_executable_path,
            'headless_browsing': self.config.headless_browsing,
            'page_loading_timeout': self.config.page_loading_timeout,
            'monitor_enable': self.config.monitor_enable,
            'login_page': self.config.login_page,
            'tickets_page': self.config.tickets_page,
            'close_tickets_retry_times': self.config.close_tickets_retry_times,
            'allow_opened_tickets_begin_time': self.config.allow_opened_tickets_begin_time,
            'allow_opened_tickets_end_time': self.config.allow_opened_tickets_end_time
        }

        with open(self._config_file, 'w') as outfile:
            json.dump(config, outfile, sort_keys=True, indent=4)

    def load_configuration(self):
        if not os.path.isfile(self._config_file):
            self.create_default_configuration_file()

        try:
            with open(self._config_file, "r") as read_file:
                config_string = json.load(read_file)

                try:
                    self.config.username = config_string['username']
                    self.config.password = config_string['password']
                    self.config.chrome_executable_path = config_string['chrome_executable_path']
                    self.config.headless_browsing = config_string['headless_browsing']
                    self.config.page_loading_timeout = config_string['page_loading_timeout']
                    self.config.monitor_enable = config_string['monitor_enable']
                    self.config.login_page = config_string['login_page']
                    self.config.tickets_page = config_string['tickets_page']
                    self.config.close_tickets_retry_times = config_string['close_tickets_retry_times']
                    self.config.allow_opened_tickets_begin_time = config_string['allow_opened_tickets_begin_time']
                    self.config.allow_opened_tickets_end_time = config_string['allow_opened_tickets_end_time']
                except Exception as assign_error:
                    print('Error assigning json field - ' + str(assign_error))
        except Exception as file_err:
            print('Err loading json from file - ' + str(file_err))
        finally:
            read_file.close()
            return self._config

    def get_config(self, config_file=DEFAULT_CONFIG_FILENAME):
        self._config_file = config_file

        return self.load_configuration()


