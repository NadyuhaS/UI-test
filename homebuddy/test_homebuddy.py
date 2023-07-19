import datetime
import random
import string

import pytest

import config
from base_page import InputZipCodePage, ChooseWorkTypePage, MaterialSelectionPage, InputSquarePage
from base_page import StoriesCountPage, AuthoriziedQuestionPage, LeavingPage, UserInfoPage, ConfirmPhoneNumberPage


class TestHomeBuddy:
    @pytest.fixture(scope='class', autouse=True,
                    params=[
                        {
                            'work_type': {'name': 'Repair section(s) of siding', 'button': 'No'},
                            'material': 'Vinyl',
                            'authorizied': None,
                            'confirm': None
                        },
                        {
                            'work_type': {'name': 'Repair section(s) of siding', 'button': 'Yes'},
                            'material': 'Fiber cement',
                            'authorizied': {'item_name': 'No', 'button': 'No'},
                            'confirm': None
                        },
                        {
                            'work_type': {'name': 'Not sure'},
                            'material': 'Wood',
                            'authorizied': {'item_name': 'No', 'button': 'Yes'},
                            'confirm': 'Phone number is correct'
                        },
                        {
                            'work_type': {'name': 'Replace existing siding'},
                            'material': 'Not sure',
                            'authorizied': {'item_name': 'Yes'},
                            'confirm': 'Edit phone number'
                        },
                    ])
    def prepare(self, request, browser):
        self = request.cls
        self.work_type = request.param['work_type']
        self.material = request.param['material']
        self.authorizied = request.param['authorizied']
        self.confirm = request.param['confirm']
        self.browser = browser
        self.browser.get(config.website_url)

    '''
    Check validation of input zip code
    '''
    @pytest.mark.parametrize("zip_code, validation_result", [
        ('00', False),
        ('090909', False),
        ('09090', True)
    ])
    def test_input_zip_code(self, zip_code, validation_result):
        zip_code_page = InputZipCodePage(self.browser)
        zip_code_page.input_value(zip_code)
        validation = zip_code_page.check_validation_result()
        assert validation == validation_result, f'Validation {validation} != Expected {validation_result}'
        zip_code_page.click_button()
        if not (validation):
            zip_code_page.check_correct_action()

    '''
    Check work type choice
    '''
    def test_work_type_choice(self):
        choose_work_type_page = ChooseWorkTypePage(self.browser)
        leave_page = LeavingPage(self.browser)
        progress_value = choose_work_type_page.get_progress_bar_value()
        choose_work_type_page.check_title(title='What type of project is this?',
                                          start=datetime.datetime.utcnow())
        choose_work_type_page.choose_work_type(self.work_type['name'])
        button = self.work_type['button'] if 'button' in self.work_type.keys() else None
        choose_work_type_page.click_button(button_name=button)
        if button:
            if button == 'No':
                leave_page.check_leave_page()
        if not (button) or button == 'Yes':
            choose_work_type_page.check_progress_bar(previous_progress_value=progress_value)

    '''
    Check material choice
     '''
    def test_material_choice(self):
        if self.browser.current_url == config.website_url:
            material_selection_page = MaterialSelectionPage(self.browser)
            progress_value = material_selection_page.get_progress_bar_value()
            material_selection_page.check_title(title='What kind of siding do you want?',
                                                start=datetime.datetime.utcnow())
            material_selection_page.choose_material(material_name=self.material)
            material_selection_page.click_button()
            material_selection_page.check_progress_bar(previous_progress_value=progress_value)
        else:
            assert 'button' in self.work_type.keys()
            assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'

    '''
    Check checkbox "Not sure"
    '''
    def test_checkbox_input_square(self):
        if self.browser.current_url == config.website_url:
            square_page = InputSquarePage(self.browser)
            square_page.check_title(title='Approximately how many square feet will be covered with new siding?',
                                    start=datetime.datetime.utcnow())
            square_page.click_checkbox()
            assert square_page.check_enable_button()
            square_page.click_checkbox()
            assert not (square_page.check_enable_button())
        else:
            assert 'button' in self.work_type.keys()
            assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'

    '''
    Check validation of  input square
    '''
    @pytest.mark.parametrize("input_value, error_message", [
        ('000', 'Number can’t start with 0'),
        ('abscd', 'Please use numbers only'),
        ('-15', 'Please use numbers only'),
        ('15.3', 'Please use numbers only'),
        ('14,2', 'Please use numbers only'),
    ])
    def test_input_value_square(self, input_value, error_message):
        if self.browser.current_url == config.website_url:
            square_page = InputSquarePage(self.browser)
            square_page.check_title(title='Approximately how many square feet will be covered with new siding?',
                                    start=datetime.datetime.utcnow())
            square_page.input_value(value=input_value)
            square_page.check_error_message(error_text=error_message)
        else:
            assert 'button' in self.work_type.keys()
            assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'

    '''
    Check input correct square
    '''
    def test_input_square(self):
        if self.browser.current_url == config.website_url:
            square_page = InputSquarePage(self.browser)
            progress_value = square_page.get_progress_bar_value()
            square_page.check_title(title='Approximately how many square feet will be covered with new siding?',
                                    start=datetime.datetime.utcnow())
            square_page.input_value(value='10')
            square_page.click_button()
            square_page.check_progress_bar(previous_progress_value=progress_value)
        else:
            assert 'button' in self.work_type.keys()
            assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'

    '''
    Check stories count choice
    '''
    def test_stories_count_choice(self):
        if self.browser.current_url == config.website_url:
            stories_count_page = StoriesCountPage(self.browser)
            progress_value = stories_count_page.get_progress_bar_value()
            stories_count_page.check_title(title='How many stories is your house?',
                                           start=datetime.datetime.utcnow())
            stories_count_page.choose_stories_count(item_name='2 stories')
            stories_count_page.click_button()
            stories_count_page.check_progress_bar(previous_progress_value=progress_value)
        else:
            assert 'button' in self.work_type.keys()
            assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'

    '''
    Check answer for authorizied question
    '''
    def test_authorizied_question(self):
        if self.browser.current_url == config.website_url:
            auth_question_page = AuthoriziedQuestionPage(self.browser)
            leave_page = LeavingPage(self.browser)
            progress_value = auth_question_page.get_progress_bar_value()
            auth_question_page.check_title(title='Are you the homeowner or authorized to make property changes?',
                                           start=datetime.datetime.utcnow())
            auth_question_page.choose_answer(item_name=self.authorizied['item_name'])
            button = self.authorizied['button'] if 'button' in self.authorizied.keys() else None
            auth_question_page.click_button(button_name=button)
            if button and button == 'No':
                leave_page.check_leave_page()
            if not (button) or button == 'Yes':
                auth_question_page.check_progress_bar(previous_progress_value=progress_value)
        else:
            assert 'button' in self.work_type.keys()
            assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'

    '''
    Check validation of input different value email and full name
    '''
    @pytest.mark.parametrize("full_name, name_error, email, email_error", [
        ('', 'Enter your full name', '', 'Enter your email address'),
        ('111111', 'Full name can consist only of latin letters and dashes', '', 'Enter your email address'),
        ('huh', 'Your full name should contain both first and last name', '', 'Enter your email address'),
        ('huh ', None, '', 'Enter your email address'),
        ('Nn N', None, '1233', 'Wrong email'),
        ('Nn N', None, '1@2.ru', None)
    ])
    def test_user_info(self, full_name, name_error, email, email_error):
        if self.browser.current_url == config.website_url:
            user_info_page = UserInfoPage(self.browser)
            progress_value = user_info_page.get_progress_bar_value()
            user_info_page.check_title(title='Who should I prepare this estimate for?',
                                       start=datetime.datetime.utcnow())
            user_info_page.input_full_name(full_name=full_name)
            user_info_page.input_email(email=email)
            user_info_page.click_button()
            user_info_page.check_full_name_error(error_message=name_error)
            user_info_page.check_email_error(error_message=email_error)
            if not (name_error or email_error):
                user_info_page.check_progress_bar(previous_progress_value=progress_value)
        else:
            if not (self.authorizied):
                assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'
            else:
                assert self.work_type['button'] == 'No' or self.authorizied[
                    'button'] == 'No', f'Work type button {self.work_type["button"]} or' \
                                       f'Authorizied button {self.authorizied["button"]} == True'

    '''
    Check validation of input phone number
    '''
    @pytest.mark.parametrize("phone_number, error_message", [
        ('+1(000)', 'Invalid Phone number'),
        ('+1(000)000-0000', None)
    ])
    def test_input_phone_number(self, phone_number, error_message):
        if self.browser.current_url == config.website_url:
            phone_number_page = UserInfoPage(self.browser)
            phone_number_page.check_title(title='What is your phone number?',
                                          start=datetime.datetime.utcnow())
            phone_number_page.input_phone_number(phone_number=phone_number)
            phone_number_page.click_button()
            phone_number_page.check_phone_number_error(error_message=error_message)
            if phone_number_page.get_title(
                    previous_value='What is your phone number?') == 'This phone number and email already exist in our database.':
                phone_number = f'+1(0{"".join(random.choice(string.digits) for i in range(2))})' \
                               f'{"".join(random.choice(string.digits) for i in range(3))}' \
                               f'-{"".join(random.choice(string.digits) for i in range(4))}'
                email = f'{"".join(random.choice(string.ascii_letters) for i in range(random.randint(1, 15)))}' \
                        f'@{"".join(random.choice(string.ascii_letters) for i in range(random.randint(1, 15)))}.com'
                phone_number_page.input_phone_number(phone_number=phone_number)
                phone_number_page.input_email(email=email)
                phone_number_page.click_button()
        else:
            if not (self.authorizied):
                assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'
            else:
                assert self.work_type['button'] == 'No' or self.authorizied[
                    'button'] == 'No', f'Work type button {self.work_type["button"]} or' \
                                       f'Authorizied button {self.authorizied["button"]} == True'

    '''
    Check confirm phone number
    '''
    def test_confirm_phone_number(self):
        if self.browser.current_url == config.website_url:
            confirm_phone_number_page = ConfirmPhoneNumberPage(self.browser)
            confirm_phone_number_page.check_title(title='Please confirm your phone number.',
                                                  start=datetime.datetime.utcnow())
            number = confirm_phone_number_page.get_number()
            confirm_phone_number_page.click_button(button_name=self.confirm)
            if self.confirm == 'Edit phone number':
                confirm_phone_number_page.check_title(title='Please confirm your phone number.',
                                                      start=datetime.datetime.utcnow())
                confirm_phone_number_page.input_phone_number(phone_number=number)
                confirm_phone_number_page.click_button(button_name='Phone number is correct')
            confirm_phone_number_page.check_final_page()
        else:
            if not (self.authorizied):
                assert self.work_type['button'] == 'No', f'Work type button must be "No", {self.work_type["button"]}'
            else:
                assert self.work_type['button'] == 'No' or self.authorizied[
                    'button'] == 'No', f'Work type button {self.work_type["button"]} or' \
                                       f'Authorizied button {self.authorizied["button"]} == True'
