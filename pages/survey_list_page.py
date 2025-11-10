from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
            url (str): The full URL of the survey page to visit (e.g.,
                `https://igracias.telkomuniversity.ac.id/survey/?pageid=1661`).

        Behavior:
            - Logs navigation activity.
            - Performs a direct GET request to the specified URL via Selenium.

        Raises:
            Exception: If the driver fails to load the page (e.g., due to network errors).
        """
        self.logger.info(f"Navigating to survey page: {url}")
        self.driver.get(url)

    def click_next_survey_action(self):
        """Iterates through all 'Start' buttons and yields control for each form to be filled.

        This method searches for survey entries that display the *“Belum Mengisi”*
        icon (`kue_blmisi.png`) and clicks them one at a time.  
        After each click, it yields control to the caller, allowing form processing
        before resuming the search for the next available survey.

        Yields:
            None: After each 'Start' button click, the method pauses for form handling.

        Behavior:
            - Continuously searches for the next available 'Start' link.
            - Clicks and yields after each found instance.
            - Stops gracefully when no more pending surveys exist.

        Logs:
            - Discovery of new surveys and each click action.
            - Informational message when all surveys have been processed.

        Raises:
            TimeoutException: If no 'Start' button is found within 5 seconds of search.
        """
        start_link_xpath = "//a[.//img[contains(@src, 'kue_blmisi.png')]]"

        while True:
            try:
                start_link = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, start_link_xpath))
                )

                self.logger.info("Found a 'Start' link. Clicking it.")

                start_link.click()
                yield

                self.logger.info("Resuming search for the next 'Start' link.")
            except TimeoutException:
                self.logger.info("No more 'Start' links found on this page. Moving on.")
                break