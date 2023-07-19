from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException, \
    ElementClickInterceptedException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from locators import HomePageLocators, ElementsPageLocators, CheckBoxLocators


class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def open(self, url):
        self.browser.get(url)

    def is_visible(self, how, what, time=10) -> bool:
        try:
            WebDriverWait(self.browser, time).until(EC.visibility_of_element_located((how, what)))
        except WebDriverException:
            return False
        return True

    def is_element(self, how, what, element=None, time=10) -> bool:
        if not element:
            element = self.browser
        try:
            WebDriverWait(element, time).until(EC.presence_of_element_located((how, what)))
        except NoSuchElementException:
            return False
        return True

    def is_elements(self, how, what,element=None, time=10) -> bool:
        if not element:
            element = self.browser
        try:
            WebDriverWait(element, time).until(EC.presence_of_all_elements_located((how, what)))
        except NoSuchElementException:
            return False
        return True

    def is_clickable(self, how, what, time=10) -> bool:
        try:
            WebDriverWait(self.browser, time).until(EC.element_to_be_clickable((how, what)))
        except ElementClickInterceptedException:
            return False
        return True

    def find_element_by_text(self, text, element_how, element_what, text_how, text_what, element=None,
                             time=10) -> object:
        for element in self.find_elements(element_how, element_what, element=element, time=time):
            if element.find_element(text_how, text_what).text == text:
                return element

    def find_element(self, how, what, element=None, time=10) -> object:
        if element:
            return WebDriverWait(element, time).until(lambda browser: element.find_element(how, what))
        return WebDriverWait(self.browser, time).until(lambda browser: self.browser.find_element(how, what))

    def find_elements(self, how, what, element=None, time=10) -> list:
        if element:
            return WebDriverWait(element, time).until(lambda browser: element.find_elements(how, what))
        return WebDriverWait(self.browser, time).until(lambda browser: self.browser.find_elements(how, what))

    def click(self, element):
        try:
            element.click()
        except WebDriverException:
            assert False, 'Element is not clickable'

    def scroll_to_element(self, how=None, what=None, element=None):
        try:
            if how and not (element):
                element = self.find_element(how, what)
            element.scrollIntoView()
        except WebDriverException:
            assert False, f'Can\'t scroll to element'


class MainPage(BasePage):
    def __find_cards(self, name) -> object:
        return self.find_element_by_text(name, *HomePageLocators.CARD, *HomePageLocators.CARD_HEADER)

    def click_card(self, name):
        assert self.is_elements(*HomePageLocators.CATEGORY_CARDS), 'No card is on page'
        self.click(self.__find_cards(name))


class ElementsPage(BasePage):
    def __find_group(self, name) -> object:
        return self.find_element_by_text(name, *ElementsPageLocators.ELEMENT_GROUP,
                                         *ElementsPageLocators.ELEMENT_GROUP_HEADER)

    def show_element_list(self, name) -> object:
        assert self.is_visible(*ElementsPageLocators.ACCORDION)
        group = self.__find_group(name)
        assert group is not None, f'No group element has name = {name}'
        if not self.is_element(*ElementsPageLocators.ELEMENT_LIST_SHOWN_SIGN, element=group):
            self.click(group)
        return group

    def is_element_list_shown(self, name) -> bool:
        group = self.__find_group(name)
        return self.is_element(*ElementsPageLocators.ELEMENT_LIST_SHOWN_SIGN,
                               element=group)

    def click_menu_element(self, name, group=None):
        if not group:
            for element in self.find_elements(*ElementsPageLocators.ELEMENT_LIST_SHOWN_SIGN):
                self.click(self.find_element_by_text(name, *ElementsPageLocators.MENU_LIST_BTN,
                                                     *ElementsPageLocators.MENU_LIST_BTN_HEADER, element=element))
        else:
            self.click(self.find_element_by_text(name, *ElementsPageLocators.MENU_LIST_BTN,
                                                 *ElementsPageLocators.MENU_LIST_BTN_HEADER, element=group))



class CheckBoxPage(BasePage):
    def __find_tree_element(self, name) -> object:
        return self.find_element_by_text(name, *CheckBoxLocators.TREE_ELEMENT,
                                         *CheckBoxLocators.TREE_ELEMENT_HEADER)

    def expand_tree(self, name) -> object:
        assert self.is_element(*CheckBoxLocators.TREE), f'There is No tree element on page {self.browser.curent_url}'
        tree_element = self.__find_tree_element(name)
        assert tree_element is not None, f'Can\'t find any tree element with name = {name}'
        self.click(self.find_element(*CheckBoxLocators.TREE_BUTTON, element=tree_element))
        return self.find_element_by_text(name, *CheckBoxLocators.EXPANDED_SIGN,
                                         *CheckBoxLocators.TREE_ELEMENT_HEADER)

    def get_text_result(self) -> str:
        return ''.join([element.text for element in self.find_elements(*CheckBoxLocators.RESULT)])

    def select_checkbox(self, name) -> object:
        tree_element = self.__find_tree_element(name)
        assert tree_element is not None, f'Can\'t find any tree element with name = {name}'
        self.click(self.find_element(*CheckBoxLocators.CHECKBOX, element=tree_element))
        return tree_element
