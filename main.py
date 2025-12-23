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

    This function orchestrates the entire automation process, handling login,
    navigation, and the multi-step completion of survey forms.

    The script follows a complex sequence for each survey:
    1.  Navigates to a survey list page.
    2.  Clicks the initial 'start' link for an available survey.
    3.  On an intermediate page, clicks a second 'start' link to enter the form.
    4.  Fills out 'Part 1' of the questionnaire.
    5.  Clicks a 'Save' button to navigate to 'Part 2'.
    6.  Fills out 'Part 2' of the questionnaire.
    7.  Clicks 'Save' again, then clicks the final 'Submit' button.

    The script pauses after each fully completed survey to allow for manual
    verification before proceeding to the next one. It is designed to handle
    unexpected browser alerts and provides detailed logging for all actions.

    Raises:
        KeyboardInterrupt: If the user presses Ctrl+C to stop the script.
        Exception: For any unhandled runtime errors during execution.
    """
    logger = setup_logger()
    driver = None

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

                if not survey_form.click_intermediate_link():
                    logger.error("Failed to enter form, skipping to next.")
                    continue

                logger.info("Attempting to fill Part 1...")
                survey_form.fill_all_visible_answers(config.DEFAULT_COMMENT, config.RADIO_OPTION_INDEX)

                logger.info("Submitting Part 1 to proceed to Part 2...")
                survey_form.click_save_or_submit()
                
                logger.info("Attempting to fill Part 2...")
                survey_form.fill_all_visible_answers(config.DEFAULT_COMMENT, config.RADIO_OPTION_INDEX)

                logger.info("Clicking 'Save' on Part 2...")
                survey_form.click_save_or_submit()

                logger.info("Clicking final 'Submit' button...")
                survey_form.click_save_or_submit()

                logger.info(f"--- Completed survey form {i+1} ---")

                # Pause for debugging...
                # input(">>> Paused. Press Enter to continue to the next form...")
        
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