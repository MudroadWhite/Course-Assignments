"""Functional Tests for Flask Application
   RUN main.py before running this module"""

import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from database import email_info_in_db, delete_row, delete_event_row, get_request_id, delete_request_row,\
    commit, delete_pledge_by_amount


# Example from https://www.geeksforgeeks.org/writing-tests-using-selenium-python/
# inherit TestCase Class and create a new test class
# Test that the DAMS server works
class InitialTest(unittest.TestCase):
    """Test that the DAMS homepage loads"""

    # initialization of webdriver
    def setUp(self):
        """Opens a web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    def test_check_page_loads(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')
        print("Web element = {}".format(elem.text))

        assert "Welcome to" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


# Test that the DAMS server works
class NavSignInTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_signin_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Go back to home page
        button = driver.find_element_by_class_name("logo")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful return
        assert "Welcome to" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


class NavSignUpTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_signup_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign up page
        button = driver.find_element_by_id("button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation -- SHOULD CURRENTLY FAIL
        assert "Sign Up" in elem.text

        # Go back to home page
        button = driver.find_element_by_class_name("logo")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful return
        assert "Welcome to" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


class NewRegisterTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign up page
        button = driver.find_element_by_id("button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign Up" in elem.text

        # Find the form fields
        fn = driver.find_element_by_id('fn')
        ln = driver.find_element_by_id('ln')
        email = driver.find_element_by_id('email')
        conf_email = driver.find_element_by_id('conf_email')
        psw = driver.find_element_by_id('psw')
        conf_psw = driver.find_element_by_id('conf_psw')
        zipcode = driver.find_element_by_id('zip')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        fn.send_keys("John")
        ln.send_keys("Doe")
        email.send_keys("newEmail@web.com")
        conf_email.send_keys("newEmail@web.com")
        psw.send_keys("myPass1234")
        conf_psw.send_keys("myPass1234")
        zipcode.send_keys("12345")
        submit.click()

        # Assert that we were redirected to the home page
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to" in elem.text

        # Check that the database was updated correctly
        assert email_info_in_db("newEmail@web.com", "myPass1234", "recipient", "12345") is True

        # Delete the info from the database
        delete_row("newEmail@web.com")

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


class ExistingRegisterTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign up page
        button = driver.find_element_by_id("button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign Up" in elem.text

        # Find the form fields
        fn = driver.find_element_by_id('fn')
        ln = driver.find_element_by_id('ln')
        email = driver.find_element_by_id('email')
        conf_email = driver.find_element_by_id('conf_email')
        psw = driver.find_element_by_id('psw')
        conf_psw = driver.find_element_by_id('conf_psw')
        zipcode = driver.find_element_by_id('zip')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        fn.send_keys("John")
        ln.send_keys("Doe")
        email.send_keys("myMail@web.com")
        conf_email.send_keys("myMail@web.com")
        psw.send_keys("myPass1234")
        conf_psw.send_keys("myPass1234")
        zipcode.send_keys("12345")
        submit.click()

        # Assert that we were redirected to the sign up page with error
        elem = driver.find_element_by_css_selector('p')
        assert "Entered Email already has an account" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


class MismatchEmailRegisterTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign up page
        button = driver.find_element_by_id("button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign Up" in elem.text

        # Find the form fields
        fn = driver.find_element_by_id('fn')
        ln = driver.find_element_by_id('ln')
        email = driver.find_element_by_id('email')
        conf_email = driver.find_element_by_id('conf_email')
        psw = driver.find_element_by_id('psw')
        conf_psw = driver.find_element_by_id('conf_psw')
        zipcode = driver.find_element_by_id('zip')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        fn.send_keys("John")
        ln.send_keys("Doe")
        email.send_keys("myMail@web.com")
        conf_email.send_keys("Mail@web.com")
        psw.send_keys("myPass1234")
        conf_psw.send_keys("myPass1234")
        zipcode.send_keys("12345")
        submit.click()

        # Assert that we were redirected to the sign up page with error
        elem = driver.find_element_by_css_selector('p')
        assert "Entered Emails do not match" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


class MismatchPSWRegisterTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign up page
        button = driver.find_element_by_id("button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign Up" in elem.text

        # Find the form fields
        fn = driver.find_element_by_id('fn')
        ln = driver.find_element_by_id('ln')
        email = driver.find_element_by_id('email')
        conf_email = driver.find_element_by_id('conf_email')
        psw = driver.find_element_by_id('psw')
        conf_psw = driver.find_element_by_id('conf_psw')
        zipcode = driver.find_element_by_id('zip')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        fn.send_keys("John")
        ln.send_keys("Doe")
        email.send_keys("myMail@web.com")
        conf_email.send_keys("myMail@web.com")
        psw.send_keys("myPass123")
        conf_psw.send_keys("Pass1234")
        zipcode.send_keys("12345")
        submit.click()

        # Assert that we were redirected to the sign up page with error
        elem = driver.find_element_by_css_selector('p')
        assert "Entered Passwords do not match" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


# Guanda Yuan ##############
# Tests:
# 1. Successfully logged in
class LoginTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("myMail@web.com")
        psw.send_keys("myPass")
        submit.click()

        # Assert that we were redirected to the home page
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


# 2. Failed with wrong email
class LoginWrongEmailTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign up page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("1263751267351723567@web.com")
        psw.send_keys("myPass")
        submit.click()

        # Assert that we were shown the error
        elem = driver.find_element_by_class_name('alert').find_element_by_css_selector('p')
        assert "Username or password is incorrect" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


# 3. Failed with wrong passwd
class LoginWrongPasswordTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign up page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("myMail@web.com")
        psw.send_keys("1256341526341265346514")
        submit.click()

        # Assert that we were shown the error
        elem = driver.find_element_by_class_name('alert').find_element_by_css_selector('p')
        assert "Username or password is incorrect" in elem.text

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()


# Add Events test
class AddEventTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("admin@mail.com")
        psw.send_keys("admin")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Admin" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("eventButton")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Add Event" in elem.text

        # Fills Form
        event_type = driver.find_element_by_id("eventType")
        event_zip = driver.find_element_by_id('eventZip')
        event_title = driver.find_element_by_id('eventTitle')
        event_desc = driver.find_element_by_id('eventDesc')
        submit = driver.find_element_by_id('button3')

        event_zip.send_keys("52246")
        event_title.send_keys("Tornado in Iowa City")
        event_desc.send_keys("100 MPH Level 4 tornado in Iowa City, Iowa at 23:00 3/15/21")
        submit.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to Admin" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        delete_event_row("Tornado in Iowa City")

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


# Add Events test
class addEventTestExisting(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("admin@mail.com")
        psw.send_keys("admin")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Admin" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("eventButton")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Add Event" in elem.text

        # Fills Form
        eventType = driver.find_element_by_id("eventType")
        eventZip = driver.find_element_by_id('eventZip')
        eventTitle = driver.find_element_by_id('eventTitle')
        eventDesc = driver.find_element_by_id('eventDesc')
        submit = driver.find_element_by_id('button3')

        eventZip.send_keys("00000")
        eventTitle.send_keys("Test")
        eventDesc.send_keys("100 MPH Level 4 tornado in Iowa City, Iowa at 23:00 3/15/21")
        submit.click()


        # Check unsuccessful navigation
        elem = driver.find_element_by_class_name('alert').find_element_by_css_selector('p')
        assert "Event already exists" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


# Functional tests for request creation
class createNewRequest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("recipient@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Recipient" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("requestButton")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Create" in elem.text

        # Fills Form
        dollar = driver.find_element_by_id('dollar')
        mats = driver.find_element_by_id('mats')
        submit = driver.find_element_by_id('button3')

        select = Select(driver.find_element_by_id('event'))
        select.select_by_visible_text("5, Test")
        dollar.send_keys("1000")
        mats.send_keys("10 Stacks of logs")
        submit.click()


        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to Recipient" in elem.text

        id = get_request_id("recipient@mail.com", 5)
        delete_request_row(id)
        commit()

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


class createNewRequestNoneFields(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("recipient@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Recipient" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("requestButton")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Create" in elem.text

        # Fills Form
        select = Select(driver.find_element_by_id('event'))
        select.select_by_visible_text("5, Test")
        submit = driver.find_element_by_id('button3')

        submit.click()

        # Check unsuccessful navigation
        elem = driver.find_element_by_class_name('alert').find_element_by_css_selector('p')
        assert "Please fill out" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


class createNewRequestFromSearch(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("recipient@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("button2")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Search" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("nameLink")
        button.click()

        # Go to create request page
        elem = driver.find_element_by_id("request")
        elem.click()

        # Fills Form
        select = Select(driver.find_element_by_id('event'))
        select.select_by_visible_text("5, Test")
        dollar = driver.find_element_by_id('dollar')
        submit = driver.find_element_by_id('button3')

        dollar.send_keys("500")
        submit.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        id = get_request_id("recipient@mail.com", 5)
        delete_request_row(id)

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


class createNewRequestFromSearchNoneFields(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("recipient@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("button2")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Search" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("nameLink")
        button.click()

        # Go to create request page
        elem = driver.find_element_by_id("request")
        elem.click()

        # Fills Form
        select = Select(driver.find_element_by_id('event'))
        select.select_by_visible_text("5, Test")
        submit = driver.find_element_by_id('button3')

        submit.click()

        # Check unsuccessful navigation
        elem = driver.find_element_by_class_name('alert').find_element_by_css_selector('p')
        assert "Please fill out" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


class createNewRequestNotLoggedIn(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("button2")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Search" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("nameLink")
        button.click()

        # Go to create request page
        elem = driver.find_element_by_id("request")
        elem.click()

        #Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Sign Up" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


class createExistingRequest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("recipient@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Recipient" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("requestButton")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Create" in elem.text

        # Fills Form
        dollar = driver.find_element_by_id('dollar')
        mats = driver.find_element_by_id('mats')
        submit = driver.find_element_by_id('button3')

        dollar.send_keys("1000")
        mats.send_keys("10 Stacks of logs")
        submit.click()

        # Check unsuccessful navigation
        elem = driver.find_element_by_class_name('alert').find_element_by_css_selector('p')
        assert "You already have" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


class createPledge(unittest.TestCase):
    """Test that pledge creation works"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("donor@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Donor" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("pledgeButton")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Create" in elem.text

        # Fills Form
        dollar = driver.find_element_by_id('dollar')
        submit = driver.find_element_by_id('button3')

        dollar.send_keys("122333")
        submit.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome" in elem.text

        # Delete the pledge
        delete_pledge_by_amount("donor@mail.com", 122333, "12345")

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


class createPledgeNone(unittest.TestCase):
    """Test that pledge with null values does not work"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("donor@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Donor" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("pledgeButton")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Create" in elem.text

        # Fills Form
        submit = driver.find_element_by_id('button3')

        submit.click()

        # Check unsuccessful navigation
        elem = driver.find_element_by_class_name('alert').find_element_by_css_selector('p')
        assert "Please fill" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()



class editRequest(unittest.TestCase):
    """Test that pledge with null values does not work"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("recipient@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_link_text("Edit")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Edit" in elem.text

        # Fills Form
        submit = driver.find_element_by_id('button3')

        submit.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


class editRequestNone(unittest.TestCase):
    """Test that pledge with null values does not work"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("recipient@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_link_text("Edit")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Edit" in elem.text

        # Fills Form
        dollar = driver.find_element_by_id("dollar")
        human = driver.find_element_by_id("human")
        mats = driver.find_element_by_id("mats")
        submit = driver.find_element_by_id('button3')

        dollar.clear()
        human.clear()
        mats.clear()
        submit.click()

        # Check unsuccessful navigation
        elem = driver.find_element_by_class_name('alert').find_element_by_css_selector('p')
        assert "Must" in elem.text

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()


# Functional tests for request creation
class expireRequest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        """Runs the associated test"""
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # Fill out the form
        email.send_keys("recipient@mail.com")
        psw.send_keys("myPass1234")
        submit.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()

        elem = driver.find_element_by_css_selector('h1')

        # Check successful navigation
        assert "Welcome to Recipient" in elem.text

        # Navigate to add events page
        button = driver.find_element_by_id("requestButton")
        button.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Create" in elem.text

        # Fills Form
        dollar = driver.find_element_by_id('dollar')
        mats = driver.find_element_by_id('mats')
        submit = driver.find_element_by_id('button3')

        select = Select(driver.find_element_by_id('event'))
        select.select_by_visible_text("5, Test")
        dollar.send_keys("1000")
        mats.send_keys("10 Stacks of logs")
        submit.click()


        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to Recipient" in elem.text

        id = get_request_id("recipient@mail.com", 5)

        button = driver.find_element_by_id("expireButton")
        button.click()

        select = Select(driver.find_element_by_id('request'))
        select.select_by_visible_text("{}, Test".format(id))
        submit = driver.find_element_by_id('button3')
        submit.click()

        # Check successful navigation
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to Recipient" in elem.text

        delete_request_row(id)
        commit()

        # Navigate to home page
        driver.get("http://localhost:5000/")

        # Get the title h1 element
        elem = driver.find_element_by_css_selector('h1')

        assert "Welcome to" in elem.text

        elem = driver.find_element_by_id('logout')
        elem.click()

        def tearDown(self):
            """Closes the web driver"""
            self.driver.close()

# Functional tests for request creation
class createDonationTest(unittest.TestCase):
    """Test that navigation works to and from the sign in page"""

    # initialization of webdriver
    def setUp(self):
        """Opens a new web driver"""
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def test_home_to_search_and_back(self):
        driver = self.driver

        # Navigate to DAMS homepage
        driver.get("http://localhost:5000/")
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to" in elem.text

        # Navigate to sign in page
        button = driver.find_element_by_id("signin")
        button.click()
        elem = driver.find_element_by_css_selector('h1')
        assert "Sign In" in elem.text

        # Find the form fields
        email = driver.find_element_by_id('email')
        psw = driver.find_element_by_id('psw')
        submit = driver.find_element_by_id('button3')

        # And log in...
        email.send_keys("donor@donor.com")
        psw.send_keys("Donor12345")
        submit.click()
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to Disaster" in elem.text

        # Navigate to dashboard page
        button = driver.find_element_by_id("dash_button")
        button.click()
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to Donor" in elem.text

        # Navigate to create donation page...
        button = driver.find_element_by_id("donationButton")
        button.click()
        elem = driver.find_element_by_css_selector('h1')
        assert "Create" in elem.text

        # Donate to the 1st entry
        button = driver.find_element_by_class_name("donate")
        button.click()
        elem = driver.find_element_by_css_selector('h1')
        assert "Make" in elem.text

        myZip = driver.find_element_by_id("myZip")
        dollar = driver.find_element_by_id("dollar")
        human = driver.find_element_by_id("human")
        mats = driver.find_element_by_id("mats")

        myZip.send_keys("66666")
        dollar.send_keys("99999")
        human.send_keys("Some Human")
        mats.send_keys("Some Materials")

        # Should be back to the dashboard...
        button = find_element_by_id("button3")
        button.click()
        elem = driver.find_element_by_css_selector('h1')
        assert "Welcome to" in elem.text

        table = driver.find_element_by_id("donations")

        delete_donation_by_info(myZip, dollar, human, mats, "donor@donor.com")

    def tearDown(self):
        """Closes the web driver"""
        self.driver.close()

if __name__ == "__main__":
    """Runs tests - run main.py before running"""
    unittest.main()
