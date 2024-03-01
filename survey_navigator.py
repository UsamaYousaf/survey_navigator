
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time


def navigate_survey_and_save_results(url, chosen_responses):
    """
    Navigates through an online survey, selects responses based on input,
    and saves the questions along with the selected responses to a CSV file.
    """
    chrome_service = webdriver.ChromeService(
        executable_path='/usr/local/bin/chromedriver')
    browser = webdriver.Chrome(service=chrome_service)
    browser.get(url)
    start_button = WebDriverWait(browser, 4).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'button--big'))
    )
    start_button.click()

    survey_data = []

    for response in chosen_responses:

        WebDriverWait(browser, 4).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'theses__text'))
        )
        question = browser.find_element(By.CLASS_NAME, 'theses__text').text
        print(question)

        if response == "stimme zu":
            answer_button = WebDriverWait(browser, 4).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button.theses-btn[data-choice="1"]'))
            )
        elif response == "neutral":
            answer_button = WebDriverWait(browser, 4).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button.theses-btn[data-choice="0"]'))
            )
        else:
            answer_button = WebDriverWait(browser, 4).until(
                EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, 'button.theses-btn[data-choice="-1"]'))
            )

        answer_button.click()

        survey_data.append((question, response))

        time.sleep(1)

    with open('/path/to/save/survey_results.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Selected Response'])
        writer.writerows(survey_data)

    browser.quit()


responses = ["stimme zu", "neutral", "stimme nicht zu"]

navigate_survey_and_save_results(
    'https://www.wahl-o-mat.de/bundestagswahl2021/app/main_app.html', responses)
