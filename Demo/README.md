# Test with Selenium

## Description

It is the UI test of [DemoQA web site](https://demoqa.com/), which was created 
with using Python and Selenium.

## Test Cases

### Prepare to testing

> Install webdriver Chrome or FireFox, [conftest.py](https://github.com/NadyuhaS/Technical-Interview/blob/main/07.03.2023/conftest.py).

> Elaborate basic functions, which are used in testing all pages,
> [BasePages.py](https://github.com/NadyuhaS/Technical-Interview/blob/main/07.03.2023/BasePage.py).

> Create a file [locators.py](https://github.com/NadyuhaS/Technical-Interview/blob/main/07.03.2023/locators.py) with all important CSS locators. 

> Develop file with main links, [config.py]().

### Test case № 1 MainPage

> **I.** Open [DemoQA web site](https://demoqa.com/).
> > **Result** : Website is opened correctly.

> **II.** Click card *"Elements"*.
> > **Result** : [Elements page](https://demoqa.com/elements) is opened.

### Test case № 2 ElementsPage

> **I.** Click *"Elements"* accordian element.
> > **Result** : *"Check Box"* menu element is shown.

> **II.** Click *"Check Box"* menu element.
> > **Result** : [Checkbox page](https://demoqa.com/checkbox) is opened.

### Test case № 3 CheckBoxPage

> **I.** Open *"Home"* tree.
> > **Result** : *"Home"* tree is expanded.

> **II.** Open *"Downloads"* tree.
> > **Result** : *"Downloads"* tree is expanded.

> **III.** Choose *"Word File.doc"*
> > **Result** : Success message is shown with text "You have selected :wordFile"

## Launch

### Launnch in Chrome
```
pytest -v DemoQA_test.py
or
pytest -v --browser_name chrome DemoQA_test.py
```
### Launch in FireFox
```
pytest -v --browser_name firefox DemoQA_test.py
```

## Result

All tests are passed. Average run length of test is 15 seconds with using Chrome,
the longest action is installing WebDriver nearly 6-10 seconds.
The length of test is 10 seconds with using Firefox.
