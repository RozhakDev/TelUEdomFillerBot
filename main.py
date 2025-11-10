from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import setup_logger
from utils.webdriver_manager import get_driver
from pages.login_page import LoginPage
from pages.survey_list_page import SurveyListPage
from pages.survey_form_page import SurveyFormPage
import config

def main():
    """Main entry point for the Telkom University EDOM automation script.

    This function orchestrates the complete EDOM automation process:
      1. Initializes logging and WebDriver.
      2. Prompts the user to log in manually.
      3. Handles any unexpected post-login popups.
      4. Iterates through all survey pages and fills available questionnaires.
      5. Cleans up WebDriver resources after completion or interruption.

    Workflow:
        - LoginPage handles manual authentication.
        - SurveyListPage locates and opens each unfilled survey form.
        - SurveyFormPage selects answers, fills comments, and submits the form.

    Behavior:
        - The script pauses after each completed form for debugging purposes.
        - Logs all actions in detail (INFO level by default).
        - Handles unexpected alerts and browser interruptions gracefully.

    Raises:
        KeyboardInterrupt: When the user manually stops execution (Ctrl+C).
        Exception: For any unexpected runtime error (with traceback logging).
    """
    logger = setup_logger()
    driver = None # Initialize driver to None for safe cleanup

    try:
        driver = get_driver()

        login_page = LoginPage(driver, logger)
        survey_list = SurveyListPage(driver, logger)
        survey_form = SurveyFormPage(driver, logger)

        driver.get(config.BASE_URL)
        login_page.wait_for_login()

        logger.info("Login confirmed. Checking for post-login popup alert...")
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())

            alert = driver.switch_to.alert
            logger.warning(f"Dismissing unexpected alert with text: {alert.text}")
            alert.accept()
        except TimeoutException:
            logger.info("No popup alert found. Continuing normally.")

        for url in [config.SURVEY_URL, config.NEXT_SURVEY_URL]:
            survey_list.navigate_to_survey_page(url)

            for i, _ in enumerate(survey_list.click_next_survey_action()):
                logger.info(f"--- Starting survey form {i+1} on page {url} ---")

                survey_form.fill_answers(config.DEFAULT_COMMENT, config.RADIO_OPTION_INDEX)
                survey_form.click_save_or_submit()

                logger.info(f"--- Completed survey form {i+1} ---")

                # Pause for debugging...
                input(">>> Paused. Press Enter to continue to the next form...")
        
        logger.info("All survey pages processed.")
    except KeyboardInterrupt:
        logger.info("Script interrupted by user (Ctrl+C). Exiting gracefully.")
    except Exception as e:
        logger.error(f"An unexcepted error oncurred: {e}", exc_info=True)
    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver closed.")

if __name__ == "__main__":
    main()