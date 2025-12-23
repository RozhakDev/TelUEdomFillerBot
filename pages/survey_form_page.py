import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SurveyFormPage:
    """Handles automation for the multi-part EDOM survey form.

    This class provides discrete methods to handle the workflow of a multi-page
    questionnaire. It is designed to be controlled by an external orchestrator
    (e.g., main.py) which calls its methods in the correct sequence.

    Attributes:
        driver (webdriver.Chrome): The active Selenium WebDriver instance.
        logger (logging.Logger): The logger instance for status reporting.
    """

    def __init__(self, driver, logger):
        """Initializes the SurveyFormPage object.

        Args:
            driver (webdriver.Chrome): The Selenium WebDriver instance.
            logger (logging.Logger): The logger for outputting status messages.
        """
        self.driver = driver
        self.logger = logger

    def click_intermediate_link(self):
        """Attempts to click the 'start' link on an intermediate page.

        This function handles an inconsistent workflow where the first survey
        may require a second click on an intermediate page, while subsequent
        surveys may not. It attempts to find the link; if found, it is
        clicked. If not found (TimeoutException), it assumes the driver is
        already on the correct form page and returns True to allow the main
        process to continue.

        Returns:
            bool: True if the process should continue (i.e., click succeeded
                  or was gracefully skipped). False for any other unexpected error.
        """
        try:
            self.logger.info("Searching for a potential intermediate 'start' link...")
            link_xpath = "//a[.//img[contains(@src, 'kue_blmisi.png')]]"
            wait = WebDriverWait(self.driver, 10)
            
            start_link = wait.until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
            
            self.logger.info("Found and clicked the intermediate 'start' link.")
            self.driver.execute_script("arguments[0].click();", start_link)
            return True
        except TimeoutException:
            self.logger.warning("Intermediate 'start' link not found. Assuming we are already on the form page and proceeding.")
            return True
        except Exception as e:
            self.logger.error(f"An unexpected error occurred trying to click intermediate link: {e}")
            return False

    def fill_all_visible_answers(self, comment, radio_index):
        """Fills all radio buttons and the comment box on the current page.

        This method first scrolls the page to ensure all questions are loaded
        and visible. It then iterates through all radio buttons, selecting the
        specified answer for each unique question group. It is designed to be
        called for each part of a multi-page form.

        Args:
            comment (str): The text to input into the comment textarea.
            radio_index (int): The 0-based index for the radio button to select.
                -1 selects the last option.

        Returns:
            bool: True if answers were filled, False if no radio buttons were found.
        """
        try:
            self.logger.info("Scrolling page to find all questions...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio']")))

            radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")
            
            processed_questions = set()
            for radio in radio_buttons:
                q_name = radio.get_attribute('name')
                if q_name and q_name not in processed_questions:
                    options = self.driver.find_elements(By.NAME, q_name)
                    if options:
                        target_option = options[radio_index] if radio_index != -1 else options[-1]
                        self.driver.execute_script("arguments[0].click();", target_option)
                        processed_questions.add(q_name)
            
            self.logger.info(f"Completed filling {len(processed_questions)} unique questions on this page.")

            try:
                comment_box = self.driver.find_element(By.TAG_NAME, "textarea")
                comment_box.clear()
                comment_box.send_keys(comment)
                self.logger.info("Filled comment box.")
            except NoSuchElementException:
                self.logger.info("No comment box found on this page part. Skipping.")
            
            return True
        except TimeoutException:
            self.logger.error("No radio buttons found on this page part.")
            return False
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while filling answers: {e}")
            return False

    def click_save_or_submit(self):
        """Finds and clicks a 'Save' or 'Submit' button.

        This method prioritizes clicking a 'Save' button first, which is often
        used to navigate to the next part of a form. If a 'Save' button is not
        found, it then searches for a 'Submit' button to finalize the form.
        """
        wait = WebDriverWait(self.driver, 10)
        
        try:
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@src, 'btn_save2')]")))
            save_btn.click()
            self.logger.info("Clicked 'Save' (or 'Next') button.")
            return
        except TimeoutException:
            self.logger.info("'Save' button not found, looking for 'Submit'.")

        try:
            submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@src, 'btn_submit')]")))
            submit_btn.click()
            self.logger.info("Clicked 'Submit' button.")
            return
        except TimeoutException:
            self.logger.warning("No 'Save' or 'Submit' button was found or clickable.")