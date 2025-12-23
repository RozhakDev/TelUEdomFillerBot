import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class SurveyListPage:
    """Handles navigation and discovery of pending EDOM survey entries.

    This class focuses on the survey list page — the one displaying all available
    or pending questionnaires with their 'Start' buttons.

    Responsibilities:
      - Navigating to a survey listing page.
      - Iterating through and clicking each available 'Start' button sequentially.
      - Providing a generator-based workflow for handling multiple forms.
    
    Attributes:
        driver (webdriver.Chrome): Active Selenium WebDriver instance.
        logger (logging.Logger): Logger instance for consistent structured logging.
    """

    def __init__(self, driver, logger):
        """Initializes the SurveyListPage instance.

        Args:
            driver (webdriver.Chrome): The Selenium WebDriver instance controlling the browser.
            logger (logging.Logger): Logger for outputting debug and info messages.
        """
        self.driver = driver
        self.logger = logger

    def navigate_to_survey_page(self, url):
        """Navigates the driver to a specific EDOM survey list page.

        Args:
            url (str): The full URL of the survey page to visit.
        """
        self.logger.info(f"Navigating to survey page: {url}")
        self.driver.get(url)

    def click_next_survey_action(self):
        """
        Iterates through all 'Start' buttons using a robust clicking mechanism.

        This generator finds each 'start' link, scrolls it into view, and uses
        a JavaScript click to avoid interception errors. If a click is
        intercepted, it logs a warning and skips, as commanded.
        """
        start_link_xpath = "//a[.//img[contains(@src, 'kue_blmisi.png')]]"

        while True:
            try:
                self.logger.info("Searching for the next 'Start' link...")
                wait = WebDriverWait(self.driver, 15)
                start_link = wait.until(
                    EC.presence_of_element_located((By.XPATH, start_link_xpath))
                )

                self.logger.info("Found a 'Start' link. Preparing to click.")

                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", start_link)
                time.sleep(1)

                self.driver.execute_script("arguments[0].click();", start_link)
                self.logger.info("Successfully clicked 'Start' link.")
                
                yield

                self.logger.info("Resuming search for the next survey.")
            
            except ElementClickInterceptedException:
                self.logger.warning("Click intercepted. Forcing continuation to form filling as commanded.")
                yield
            except TimeoutException:
                self.logger.info("No more 'Start' links found on this page.")
                break
            except Exception as e:
                self.logger.error(f"An unexpected error occurred during click, but forcing continuation as commanded: {e}")
                yield