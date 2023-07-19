from selenium.webdriver.common.by import By


class HomePageLocators:
    HOME_CONTENT = (By.CSS_SELECTOR, 'div.home-content')
    HOME_BODY = (By.CSS_SELECTOR, 'div.home-body')
    CATEGORY_CARDS = (By.CSS_SELECTOR, 'div.category-cards')
    CARD = (By.CSS_SELECTOR, 'div.card.mt-4.top-card')
    CARD_HEADER = (By.CSS_SELECTOR, 'h5')


class ElementsPageLocators:
    ACCORDION = (By.CSS_SELECTOR, 'div.accordion')
    ELEMENT_GROUP = (By.CSS_SELECTOR, 'div.element-group')
    ELEMENT_GROUP_HEADER = (By.CSS_SELECTOR, 'div.header-text')
    ELEMENT_LIST_MENU_COLLAPSE = (By.CSS_SELECTOR, 'div.element-list.collapse')
    ELEMENT_LIST_SHOWN_SIGN = (By.CSS_SELECTOR, 'div.element-list.collapse.show')
    MENU_LIST_BTN = (By.CSS_SELECTOR, 'li.btn.btn-light')
    MENU_LIST_BTN_HEADER = (By.CSS_SELECTOR, 'span.text')


class CheckBoxLocators:
    TREE = (By.CSS_SELECTOR, 'div#tree-node')
    TREE_BUTTON = (By.CSS_SELECTOR, 'button.rct-collapse-btn')
    TREE_ELEMENT = (By.CSS_SELECTOR, 'li.rct-node')
    TREE_ELEMENT_HEADER = (By.CSS_SELECTOR, 'span.rct-title')
    EXPANDED_SIGN = (By.CSS_SELECTOR, 'li.rct-node-expanded')
    CHECKBOX = (By.CSS_SELECTOR, 'span.rct-checkbox')
    RESULT = (By.CSS_SELECTOR, 'div.display-result span')
