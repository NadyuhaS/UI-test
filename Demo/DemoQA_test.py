from BasePage import CheckBoxPage, ElementsPage, MainPage
import pytest
import config


class TestDemoQA:
    @pytest.fixture(scope='class', autouse=True)
    def prepare(self, request, browser):
        self = request.cls
        self.browser = browser
        self.main_page = MainPage(self.browser)
        self.element_page = ElementsPage(self.browser)
        self.checkbox_page = CheckBoxPage(self.browser)

    def test_main_page(self):
        self.main_page.open(config.demo_qa_main_page)
        self.browser.set_page_load_timeout(30)
        assert self.browser.current_url == config.demo_qa_main_page, 'Incorrect  browser link'
        self.main_page.click_card('Elements')
        self.browser.set_page_load_timeout(30)
        assert self.browser.current_url == config.demo_qa_elements_page

    def test_elements_page(self):
        # self.element_page.open(config.demo_qa_elements_page)
        group = self.element_page.show_element_list('Elements')
        assert self.element_page.is_element_list_shown('Elements')
        self.element_page.click_menu_element('Check Box')
        self.browser.set_page_load_timeout(30)
        assert self.browser.current_url == config.demo_qa_checkbox_page

    def test_checkbox_page(self):
        # self.checkbox_page.open(config.demo_qa_checkbox_page)
        assert self.checkbox_page.expand_tree('Home') is not None, f'No tree was opened'
        assert self.checkbox_page.expand_tree('Downloads') is not None, f'No tree was opened'

        self.checkbox_page.select_checkbox('Word File.doc')
        assert self.checkbox_page.get_text_result() == 'You have selected :wordFile'



