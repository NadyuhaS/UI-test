from selenium.webdriver.common.by import By


class ZipCodePage:
    INPUT_ZIPPCODE_MAIN = (By.CSS_SELECTOR, 'input#zipCode')
    INPUT_ZIPPCODE = (By.CSS_SELECTOR, 'input#zip_footer1')
    VALIDATOR_ICON = (By.CSS_SELECTOR, 'div.rightIcon')
    GET_ESTIMATE_BUTTON = (By.CSS_SELECTOR, 'button')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.zip--caption')


class StepBody:
    STEP_BODY = (By.CSS_SELECTOR, 'div#StepBodyId')
    TITLE = (By.CSS_SELECTOR, 'h4')
    ITEM_NAME = (By.CSS_SELECTOR, 'div.h5')
    BUTTON = (By.CSS_SELECTOR, 'button')
    PROGRESS_BAR = (By.CSS_SELECTOR, 'progress')
    LABEL = (By.CSS_SELECTOR, 'label')


class ChooseWorkType:
    ITEM = (By.CSS_SELECTOR, 'div.typeOfProject__item')
    ITEM_WARNING = (By.CSS_SELECTOR, 'div.h4')


class LeavePage:
    INFORMATION_MESSAGE = (By.CSS_SELECTOR, 'h3')


class MaterialSelection:
    ITEM = (By.CSS_SELECTOR, 'div.kindOfSiding__item')


class InputSquare:
    INPUT_FIELD = (By.CSS_SELECTOR, 'div.customInput__group input')
    CHECKBOX = (By.CSS_SELECTOR, "input[type='checkbox']")
    CHECKBOX_LABEL = (By.CSS_SELECTOR, 'label')
    ERROR_MESSAGE = (By.CSS_SELECTOR, 'div.customInput__message')


class StoriesCount:
    ITEM = (By.CSS_SELECTOR, "input[name='sdStories']")
    ITEM_LABEL = (By.CSS_SELECTOR, 'label')


class AuthoriziedQuestion:
    ITEM = (By.CSS_SELECTOR, 'input[name=\'internalOwner\']')
    WARRNING_MESSAGE = (By.CSS_SELECTOR, 'div.text-orangeDeep100')


class UserInfo:
    FULL_NAME = (By.CSS_SELECTOR, 'input[name=\'fullName\']')
    EMAIL = (By.CSS_SELECTOR, 'input[name=\'email\']')
    ERROR = (By.CSS_SELECTOR, 'div.customInput__message')
    PHONE_NUMBER = (By.CSS_SELECTOR, 'input#phoneNumber')


class ConfirmPhoneNumber:
    BUTTON = (By.CSS_SELECTOR, 'button.customButton')
    BUTTON_TEXT = (By.CSS_SELECTOR, 'span.customButton__text')
