class LoginPage:
    """Handles manual login flow for iGracias using Selenium.

    This class is used to pause script execution and wait for the user
    to manually log into the iGracias portal using the browser window
    that Selenium has opened.
    """
    def __init__(self, driver, logger):
        """Initializes the LoginPage object.

        Args:
            driver (selenium.webdriver): The Selenium WebDriver instance controlling the browser.
            logger (logging.Logger): Logger instance for logging status messages.
        """
        self.driver = driver
        self.logger = logger

    def wait_for_login(self):
        """Pauses the script and waits for the user to complete manual login.

        This method logs a message instructing the user to log in manually
        in the browser. The script will resume only after the user confirms
        the login by pressing Enter in the console.
        """
        self.logger.info("Please log in manually in the browser window.")
        input("After you have successfully logged in, press Enter in this console to continue...")
        self.logger.info("Login confirmed by user. Continuing script.")