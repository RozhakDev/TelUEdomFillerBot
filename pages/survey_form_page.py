from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class SurveyFormPage:
    """Handles the automation logic for filling and submitting EDOM survey forms.

    This class is responsible for:
      - Switching to the correct iframe (if present).
      - Selecting answers for each question (via radio buttons).
      - Filling the comment box.
      - Clicking Save or Submit buttons as needed.

    Attributes:
        driver (webdriver.Chrome): The Selenium WebDriver instance used to interact with the browser.
        logger (logging.Logger): Logger instance for structured output.
        switched_to_iframe (bool): Tracks whether the driver has switched into an iframe context.
    """

    def __init__(self, driver, logger):
        """Initializes the SurveyFormPage object.

        Args:
            driver (webdriver.Chrome): Active Selenium WebDriver instance.
            logger (logging.Logger): Logger for outputting status and debug information.
        """
        self.driver = driver
        self.logger = logger
        self.switched_to_iframe = False

    def _switch_to_survey_iframe(self):
        """Switches WebDriver context to the iframe containing the survey form.

        Tries to locate an `<iframe>` tag within 10 seconds.  
        If found, the driver switches into it and logs success.  
        If not found, assumes that the form is already on the main page.

        Raises:
            TimeoutException: If no iframe is found within the timeout period.
        """
        try:
            wait = WebDriverWait(self.driver, 10)
            iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.iframe(iframe)
            self.switched_to_iframe = True
            self.logger.info("Switched to survey iframe.")
        except TimeoutException:
            self.logger.warning("Could not find an iframe. Assuming form is on the main page.")
            self.switched_to_iframe = False

    def fill_answers(self, comment, radio_index):
        """Fills out all radio questions and comment box on the EDOM form.

        Args:
            comment (str): Text to input into the comment box (e.g., appreciation message).
            radio_index (int): Index of the radio button to select per question.  
                Use `-1` to always select the last (typically 'Sangat Puas') option.

        Behavior:
            1. Switches to the iframe (if exists).
            2. Locates all radio questions.
            3. Selects the specified radio option for each question group.
            4. Fills the comment textarea with the provided message.

        Logs:
            - Information for each question successfully answered.
            - Warnings or errors if elements are missing.
        """
        self._switch_to_survey_iframe()

        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='radio']")))
            comment_box = wait.until(EC.presence_of_element_located((By.NAME, "Answer7")))

            radio_questions = self.driver.find_elements(By.CSS_SELECTOR, "input[type='radio']")

            processed_questions = set()
            for question in radio_questions:
                q_name = question.get_attribute('name')
                if q_name and q_name not in processed_questions:
                    options = self.driver.find_elements(By.NAME, q_name)
                    if options:
                        target_option = None
                        if radio_index == -1:
                            target_option = options[-1]
                        else:
                            target_option = options[min(radio_index, len(options)-1)]

                        self.driver.execute_script("arguments[0].click();", target_option)

                        self.logger.info(f"Selected option for question '{q_name}'")
                        processed_questions.add(q_name)

            comment_box.send_keys(comment)
            self.logger.info("Filled comment box.")
        except TimeoutException:
            self.logger.error("Form elements (radio buttons or comment box) not found. Aborting this form.")
            if self.switched_to_iframe:
                self.driver.switch_to.default_content()

    def click_save_or_submit(self):
        """Clicks the 'Save' and/or 'Submit' buttons on the survey form.

        The method:
            1. Attempts to click the Save button first (if found).
            2. Then attempts to click the Submit button.
            3. If either button is not found, logs a warning instead of throwing.

        After submission, if previously inside an iframe, the driver switches back
        to the default content.

        Raises:
            TimeoutException: When buttons are not interactable within 10 seconds.
        """
        wait = WebDriverWait(self.driver, 10)
        try:
            save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@src, 'btn_save2')]")))
            save_btn.click()
            self.logger.info("Clicked Save button.")
        except TimeoutException:
            self.logger.warning("Save button was not found or clickable.")

        try:
            submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@src, 'btn_submit')]")))
            submit_btn.click()
            self.logger.info("Clicked Submit button.")
        except TimeoutException:
            self.logger.warning("Submit button was not found or clickable.")
        finally:
            if self.switched_to_iframe:
                self.driver.switch_to.default_content()
                self.logger.info("Switched back to default content.")