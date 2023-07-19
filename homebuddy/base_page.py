import datetime
import time

from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators import StoriesCount, AuthoriziedQuestion, UserInfo, ConfirmPhoneNumber
from locators import ZipCodePage, StepBody, ChooseWorkType, LeavePage, MaterialSelection, InputSquare


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def open(self, url):
        self.browser.get(url)

    def click(self, element):
        try:
            element.click()
        except WebDriverException:
            assert False, 'Element is not clickable'

    def get_parent(self, element):
        try:
            return element.find_element(By.XPATH, '..')
        except WebDriverException:
            return None

    def find_element_by_text(self, text, element_how, element_what, text_how, text_what, element=None,
                             time=10):
        for element in self.find_elements(element_how, element_what, element=element, time=time):
            if element.find_element(text_how, text_what).text == text:
                return element

    def find_element(self, how, what, element=None, time=10):
        if element:
            return WebDriverWait(element, time).until(lambda browser: element.find_element(how, what))
        return WebDriverWait(self.browser, time).until(lambda browser: self.browser.find_element(how, what))

    def find_elements(self, how, what, element=None, time=10):
        if element:
            return WebDriverWait(element, time).until(lambda browser: element.find_elements(how, what))
        return WebDriverWait(self.browser, time).until(lambda browser: self.browser.find_elements(how, what))

    def scroll_to_element(self, how=None, what=None, element=None):
        try:
            if how and not (element):
                element = self.find_element(how, what)
            element.scrollIntoView()
        except WebDriverException:
            assert False, f'Can\'t scroll to element'

    def is_element(self, how, what, element=None, time=10):
        if not element:
            element = self.browser
        try:
            WebDriverWait(element, time).until(EC.presence_of_element_located((how, what)))
        except NoSuchElementException:
            return False
        return True


class InputZipCodePage(BasePage):
    def input_value(self, value):
        input_element = self.find_element(*ZipCodePage.INPUT_ZIPPCODE_MAIN)
        input_element.clear()
        input_element.send_keys(value)

    def get_validation_result(self, element):
        validation_sign = self.find_element(*ZipCodePage.VALIDATOR_ICON, element=element)
        if validation_sign.is_displayed():
            return True
        return False

    def check_validation_result(self):
        input_body = self.get_parent(self.find_element(*ZipCodePage.INPUT_ZIPPCODE_MAIN))
        return self.get_validation_result(input_body)

    def click_button(self):
        input_group = self.get_parent(self.get_parent(self.find_element(*ZipCodePage.INPUT_ZIPPCODE_MAIN)))
        button = self.find_element(*ZipCodePage.GET_ESTIMATE_BUTTON, element=input_group)
        self.click(button)

    def get_error_message(self, element):
        message = self.find_element(*ZipCodePage.ERROR_MESSAGE, element=element)
        return message.text

    def check_correct_action(self):
        input_part = self.get_parent(
            self.get_parent(self.get_parent(self.find_element(*ZipCodePage.INPUT_ZIPPCODE_MAIN))))
        if self.is_element(*ZipCodePage.ERROR_MESSAGE, element=input_part):
            assert self.get_error_message(input_part) == 'Unknown ZIP Code', f'Uncorrect error message ' \
                                                                             f'{self.get_error_message(input_part)} ' \
                                                                             f'!= \'Unknown ZIP Code\''


class StepBodyFunctional(BasePage):
    def check_title(self, title, start=None):
        step_body = self.find_element(*StepBody.STEP_BODY)
        assert step_body
        title_text = ''
        while (datetime.datetime.utcnow() - start).seconds <= 120:
            title_text = self.find_element(*StepBody.TITLE, element=step_body, time=200).text
            if title_text == title:
                break
            time.sleep(1)
        assert title_text == title, f'Title is uncorrect {title_text} != {title}'

    def choose_item(self, how, what, item_name):
        step_body = self.find_element(*StepBody.STEP_BODY)
        items = self.find_elements(how, what, element=step_body)
        item = list(filter(lambda item: self.find_element(*StepBody.ITEM_NAME, element=item).text.strip().replace('\n',
                                                                                                                  ' ') == item_name,
                           items))
        self.click(item[0])

    def click_button(self, button_name=None):
        step_body = self.find_element(*StepBody.STEP_BODY)
        buttons = self.find_elements(*StepBody.BUTTON, element=step_body)
        if len(buttons) > 1:
            button = list(filter(lambda button: button.text == button_name, buttons))[0]
        else:
            button = buttons[0]
        assert button.is_enabled()
        self.click(button)

    def get_progress_bar_value(self):
        return int(self.find_element(*StepBody.PROGRESS_BAR).get_attribute('value'))

    def check_progress_bar(self, previous_progress_value):
        start = datetime.datetime.utcnow()
        while (datetime.datetime.utcnow() - start).seconds <= 120:
            if self.get_progress_bar_value() - previous_progress_value >= 14:
                break
        assert self.get_progress_bar_value() - previous_progress_value >= 14, f'Progress bar new value ' \
                                                                              f'{self.get_progress_bar_value()} ' \
                                                                              f'and previous {previous_progress_value}'


class ChooseWorkTypePage(StepBodyFunctional):
    def check_work_type_count(self, count):
        step_body = self.find_element(*StepBody.STEP_BODY)
        work_types = self.find_elements(*ChooseWorkType.ITEM, element=step_body)
        assert len(work_types) > 0, f'No elements {ChooseWorkType.ITEM} was found'
        assert len(work_types) == count, f'Uncorrect length, {len(work_types)} != {count}'

    def choose_work_type(self, work_type_name):
        self.choose_item(*ChooseWorkType.ITEM, work_type_name)
        if work_type_name == 'Repair section(s) of siding':
            step_body = self.find_element(*StepBody.STEP_BODY)
            text_warning = self.find_element(*ChooseWorkType.ITEM_WARNING, element=step_body).text.strip().replace('\n',
                                                                                                                   ' ')
            assert text_warning == 'Some contractors will only repair/replace siding for a minimum of one full ' \
                                   'side of a house. Would you like to continue?', f'Warning text {text_warning}'


class LeavingPage(StepBodyFunctional):
    def check_leave_page(self):
        step_body = self.find_element(*StepBody.STEP_BODY)
        assert self.find_element(*LeavePage.INFORMATION_MESSAGE, step_body).text == 'Sorry to see you go!'
        assert self.find_element(*StepBody.BUTTON, step_body).is_enabled()
        self.click(self.find_element(*StepBody.BUTTON, step_body))
        assert self.browser.current_url == 'https://hb-eta.stage.sirenltd.dev/', f'{self.browser.current_url} ' \
                                                                                 f'!= https://hb-eta.stage.sirenltd.dev/'


class MaterialSelectionPage(StepBodyFunctional):
    def choose_material(self, material_name):
        self.choose_item(*MaterialSelection.ITEM, item_name=material_name)


class InputSquarePage(StepBodyFunctional):
    def input_value(self, value):
        input_field = self.find_element(*InputSquare.INPUT_FIELD, element=self.find_element(*StepBody.STEP_BODY))
        input_field.clear()
        input_field.send_keys(value)

    def click_checkbox(self):
        checkbox = self.find_element(*InputSquare.CHECKBOX, element=self.find_element(*StepBody.STEP_BODY))
        checkbox_group = self.get_parent(checkbox)
        label = self.find_element(*InputSquare.CHECKBOX_LABEL, element=checkbox_group)
        label.click()

    def check_enable_button(self):
        step_body = self.find_element(*StepBody.STEP_BODY)
        button = self.find_element(*StepBody.BUTTON, element=step_body)
        return button.is_enabled()

    def check_error_message(self, error_text):
        is_visible = True if error_text else False
        step_body = self.find_element(*StepBody.STEP_BODY)
        error_message = self.find_element(*InputSquare.ERROR_MESSAGE, element=step_body)
        assert error_message.is_displayed() == is_visible, 'Error message unshown'
        assert (error_text and error_message.text == error_text) or (
                not (error_text) and error_message.text != error_text), f'Getting {error_message.text}, expected {error_text}'


class StoriesCountPage(StepBodyFunctional):
    def choose_item(self, how, what, item_name):
        step_body = self.find_element(*StepBody.STEP_BODY)
        items = self.find_elements(how, what, element=step_body)
        for item in items:
            icon = self.get_parent(item)
            icon_label = self.find_element(*StepBody.LABEL, element=icon)
            if self.find_element(*StepBody.ITEM_NAME, element=icon_label).text == item_name:
                icon_label.click()
                break

    def choose_stories_count(self, item_name):
        self.choose_item(*StoriesCount.ITEM, item_name)


class AuthoriziedQuestionPage(StoriesCountPage):
    def choose_answer(self, item_name):
        self.choose_item(*AuthoriziedQuestion.ITEM, item_name)
        if item_name == 'No':
            warning = self.find_element(*AuthoriziedQuestion.WARRNING_MESSAGE,
                                        element=self.find_element(*StepBody.STEP_BODY))
            assert warning and warning.text == 'Our contractors require the homeowner or someone authorized ' \
                                               'to make property changes be present during the estimate. ' \
                                               'Would you like to continue?', f'Getting warning {warning.text}'

    def click_button(self, button_name=None):
        step_body = self.find_element(*StepBody.STEP_BODY)
        buttons = self.find_elements(*StepBody.BUTTON, element=step_body)
        if len(buttons) > 1:
            button = list(filter(lambda button: button.text == button_name, buttons))[0]
        else:
            button = buttons[0]
        assert button.is_enabled(), f'Button is not enabble'
        self.click(button)


class UserInfoPage(StepBodyFunctional):
    def input_full_name(self, full_name):
        step_body = self.find_element(*StepBody.STEP_BODY)
        input_full_name_field = self.find_element(*UserInfo.FULL_NAME, element=step_body)
        input_full_name_field.clear()
        input_full_name_field.send_keys(full_name)

    def input_email(self, email):
        step_body = self.find_element(*StepBody.STEP_BODY)
        input_email_field = self.find_element(*UserInfo.EMAIL, element=step_body)
        input_email_field.clear()
        input_email_field.send_keys(email)

    def input_phone_number(self, phone_number):
        step_body = self.find_element(*StepBody.STEP_BODY)
        input_full_name_field = self.find_element(*UserInfo.PHONE_NUMBER, element=step_body)
        input_full_name_field.clear()
        input_full_name_field.send_keys(phone_number)

    def check_error(self, how, what, error_message):
        input_field = self.find_element(how, what, element=self.find_element(*StepBody.STEP_BODY))
        name_group = self.get_parent(self.get_parent(self.get_parent(self.get_parent(input_field))))
        error = self.find_element(*UserInfo.ERROR, element=name_group)
        assert error.is_displayed() == (error_message is not None), f'Error is displayed {error.is_displayed()},' \
                                                                    f'Must be {error_message is not None}'
        if not (error_message): error_message = ''
        assert error.text == error_message, f'Text error {error.text} expected {error_message}'

    def check_full_name_error(self, error_message):
        self.check_error(*UserInfo.FULL_NAME, error_message=error_message)

    def check_email_error(self, error_message):
        self.check_error(*UserInfo.EMAIL, error_message=error_message)

    def check_phone_number_error(self, error_message):
        self.check_error(*UserInfo.PHONE_NUMBER, error_message=error_message)

    def get_title(self, previous_value):
        start = datetime.datetime.utcnow()
        step_body = self.find_element(*StepBody.STEP_BODY)
        while(datetime.datetime.utcnow() - start).seconds <= 120:
            tr = self.find_element(*StepBody.TITLE, element=step_body).text
            if self.find_element(*StepBody.TITLE, element=step_body).text != previous_value:
                break
            time.sleep(1)
        return self.find_element(*StepBody.TITLE, element=step_body).text


class ConfirmPhoneNumberPage(UserInfoPage):
    def click_button(self, button_name):
        step_body = self.find_element(*StepBody.STEP_BODY)
        buttons = self.find_elements(*ConfirmPhoneNumber.BUTTON, element=step_body)
        for button in buttons:
            label = self.find_element(*ConfirmPhoneNumber.BUTTON_TEXT, element=button)
            if label.text == button_name:
                button.click()
                break

    def check_final_page(self):
        start = datetime.datetime.utcnow()
        while (datetime.datetime.utcnow() - start).seconds <= 120:
            if self.browser.current_url == 'https://hb-eta.stage.sirenltd.dev/thank-you':
                break
            time.sleep(1)
        assert self.browser.current_url == 'https://hb-eta.stage.sirenltd.dev/thank-you', f'Link {self.browser.current_url},' \
                                                                                          f'expected https://hb-eta.stage.sirenltd.dev/thank-you'
        self.check_title(title='Thank you Nn, your contractor QA Customer will call soon!',
                         start=datetime.datetime.utcnow())

    def get_number(self):
        return self.find_element(*UserInfo.PHONE_NUMBER).get_attribute('value')
