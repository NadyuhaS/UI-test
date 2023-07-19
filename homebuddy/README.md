# Siren Group AG
## Test assignment for Middle QA Automation Engineer

### Testing task

Develop several (at least 3) UI autotests for [HomeBuddy](https://hb-eta.stage.sirenltd.dev/siding)

>**Use scenario**:
>- zip code 09090
>- answer the questions on the form
>- enter the first and last name
>- enter an email
>- enter the phone number
>- (if necessary) confirm the phone number
>- get a "thank you" page.

Feel free to choose the checks yourself.
Use "py test" + "selenium"

### Test structure

The project consists from 6 files:

- *config.py* - contains main web url
- *conftest.py* - contains environment settings
- *locators.py* - contains test locators
- *base_page.py* - contains main functional
- *test_homebuddy.py* - contains test scenarios
- *requirements.txt* - contains list of necessary libraries

### Test cases

***test_homebuddy.py*** contains 92 tests.
There are 4 major test scenarios:
1. - Choose work type == *'Repair section(s) of siding'*
   - Answer ***'No'*** for question: *'Some contractors will only repair/replace siding for a minimum of 
one full side of a house. Would you like to continue?'* 
   - Go to [home page](https://hb-eta.stage.sirenltd.dev/)


2. - Choose work type == *'Repair section(s) of siding'*
   - Answer ***'Yes'*** for question: *'Some contractors will only repair/replace siding for a minimum of 
one full side of a house. Would you like to continue?'* 
   - Choose any material type
   - Input any square, ex 12
   - Choose any stories count
   - Choose answer ***'No'*** for question: *'Are you the homeowner or authorized to make property changes?'*
   - Answer ***'No'*** for question: *'Our contractors require the homeowner or someone authorized to make property 
changes be present during the estimate. Would you like to continue?'* 
   - Go to [home page](https://hb-eta.stage.sirenltd.dev/)


3. - Choose any work type except *'Repair section(s) of siding'*
   - Choose any material
   - Input any square, ex 12
   - Choose any stories count
   - Choose answer ***'No'*** for question: *'Are you the homeowner or authorized to make property changes?'*
   - Answer ***'Yes'*** for question: *'Our contractors require the homeowner or someone authorized to make property 
changes be present during the estimate. Would you like to continue?'*
   - Input full name
   - Input email
   - Input phone number
   - If same user email and phone number have already been in dataBase:
     - input random phone number
     - input random created email
   - Press **Phone number is correct**
   - Go to ["Thank you" page](https://hb-eta.stage.sirenltd.dev/thank-you)


4. - Choose any work type except *'Repair section(s) of siding'*
   - Choose any material
   - Input any square, ex 12
   - Choose any stories count
   - Choose answer ***'No'*** for question: *'Are you the homeowner or authorized to make property changes?'*
   - Answer ***'Yes'*** for question: *'Our contractors require the homeowner or someone authorized to make property 
changes be present during the estimate. Would you like to continue?'*
   - Input full name
   - Input email
   - Input phone number
   - If same user email and phone number have already been in dataBase:
     - input random phone number
     - input random created email
   - Press **Edit phone number**
   - Input changed phone number
   - Press **Phone number is correct**
   - Go to ["Thank you" page](https://hb-eta.stage.sirenltd.dev/thank-you)

Also there are some tests which check validation of input value and possible error text.

### Launch

For test launching you need to open *terminal*/*command line* and input:
```commandline
pytest -v homebuddy/test_homebuddy.py
```
The test process are going in background mode with Mozila FireFox webdriver.

If you are interesting in viewing you will input next value to *terminal*/*command line*:
```commandline
pytest -v --browser_name chrome homebuddy/test_homebuddy.py 
```

s