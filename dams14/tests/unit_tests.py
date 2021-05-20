"""Unit Tests for Flask Application
   Import all functions that will need tested -- ex. to test function validate() from file
   tools.py, add from tools import validate to import modules"""

import unittest
from validate import check_equal, is_email, validate_email
from database import email_info_in_db, create_admin, delete_row, delete_request_row, \
    delete_event_row, create_request_row, provide_mats, provide_humans, expire_request, \
    get_event_name, get_request_id, create_event, get_event_id, create_pledge_row, delete_pledge_by_amount


class CheckEqualTest(unittest.TestCase):
    """Tests for function check_equal from module validate"""

    def test_is_equal(self):
        """Tests when both items are the same"""
        assert check_equal("Hello", "Hello") is True

    def test_is_not_equal(self):
        """Tests when items differ"""
        assert check_equal("Hi", "Hello") is False

    def test_different_types(self):
        """Tests when items are equal but not the same type
        for security, types need to be the same"""
        assert check_equal(3, 3.0) is False

    def test_different_case(self):
        """Tests when strings are the same but different cases"""
        assert check_equal("hello", "Hello") is False


class IsEmailTest(unittest.TestCase):
    """Tests for function is_email from validate"""

    def test_is_email(self):
        """tests a valid email"""
        assert is_email("myName@website.com") is True

    def test_is_not_email(self):
        """tests an invalid email"""
        assert is_email("hello there") is False

    def test_is_not_email2(self):
        """tests a new invalid email"""
        assert is_email("my_name@fakeSite-abcxyz") is False

    def test_wrong_type(self):
        """tests when an incorrect type is given"""
        assert is_email(42) is False


class ValidateEmailTests(unittest.TestCase):
    """Tests for function validate_email from module validate"""

    def test_is_valid(self):
        """Case for when emails match"""
        assert validate_email("myEmail@website.com", "myEmail@website.com") is True

    def test_is_not_match(self):
        """Case for when different emails appear"""
        assert validate_email("myEmail@website.com", "otherEmail@website.com") is False

    def test_different_case(self):
        """Case for when email cases differ"""
        assert validate_email("MyEmail@website.com", "myemail@website.com") is True

    def test_not_email(self):
        """Case when emails are not provided"""
        assert validate_email("Hi", "Hi") is False

    def test_different_types(self):
        """Case for when types differ"""
        assert validate_email("realEmail@web.net", 4) is False


class CreateAdmin(unittest.TestCase):
    """Tests for the create_admin function"""

    def test_create_new(self):
        """Case for a non-existing admin"""
        assert create_admin("newTestEmail@mail.web", "myPass1234", "12345", "Test", "Admin") is True
        delete_row("newTestEmail@mail.web")

    def test_create_existing(self):
        """Case for a duplicate admin"""
        assert create_admin("admin@mail.com", "myPass1234", "12345", "Test", "Admin") is False


class CheckUsersTest(unittest.TestCase):
    """Tests for email_info_in_db"""

    def test_exists(self):
        """Case for when the info is correct"""
        assert email_info_in_db("admin@mail.com", "admin", "admin", "00000") is True

    def test_no_email(self):
        """Case for when the email does not exist"""
        assert email_info_in_db("admin42NOP@mail.com", "admin", "admin", "00000") is False

    def test_wrong_psw(self):
        """Case for when the password is wrong"""
        assert email_info_in_db("admin@mail.com", "admin123NOP", "admin", "00000") is False

    def test_wrong_zip(self):
        """Case for when the zipcode is wrong"""
        assert email_info_in_db("admin@mail.com", "admin", "admin", "99991") is False

    def test_wrong_role(self):
        """Case for when the role is wrong"""
        assert email_info_in_db("admin@mail.com", "admin", "donor", "00000") is False


class RequestRow(unittest.TestCase):
    """Cases for the delete_request_row function and create_request_row function"""

    def test_row_exists(self):
        """case for a valid deletion"""
        create_request_row("test@mail.biz", 1, 100, None, None, "00000")
        id = get_request_id("test@mail.biz", 1)
        assert id is not None
        assert delete_request_row(id) is True
        assert get_request_id("test@mail.biz", 1) is None

    def test_row_does_not_exist(self):
        """case for a valid deletion"""
        id = get_request_id("test@mail.biz", 1)  # Should be None
        assert id is None
        assert delete_request_row(id) is False
        assert get_request_id("test@mail.biz", 1) is None


class ProvideTests(unittest.TestCase):
    """Test cases for provide_mats and provide_humans functions"""

    def test_requested_not_provided(self):
        """Case for is materials or human resources are requested but not yet provided"""
        create_request_row("test@myMail.net", 1, 1000, "Materials", "Help", "12345")
        id = get_request_id("test@myMail.net", 1)
        assert id is not None
        assert provide_humans(id) is True
        assert provide_mats(id) is True
        assert delete_request_row(id) is True

    def test_not_requested_not_provided(self):
        """Case for is materials or human resources are not requested and not yet provided"""
        create_request_row("test@myMail.net", 1, 1000, None, None, "12345")
        id = get_request_id("test@myMail.net", 1)
        assert id is not None
        assert provide_humans(id) is True
        assert provide_mats(id) is True
        assert delete_request_row(id) is True

    def test_requested_provided(self):
        """Case for is materials or human resources are requested and already provided"""
        create_request_row("test@myMail.net", 1, 1000, "Materials", "Help", "12345")
        id = get_request_id("test@myMail.net", 1)
        assert id is not None
        assert provide_humans(id) is True
        assert provide_mats(id) is True
        assert provide_humans(id) is True
        assert provide_mats(id) is True
        assert delete_request_row(id) is True

    def test_not_requested_provided(self):
        """Case for is materials or human resources are not requested and already marked provided"""
        create_request_row("test@myMail.net", 1, 1000, None, None, "12345")
        id = get_request_id("test@myMail.net", 1)
        assert id is not None
        assert provide_humans(id) is True
        assert provide_mats(id) is True
        assert provide_humans(id) is True
        assert provide_mats(id) is True
        assert delete_request_row(id) is True

    def test_request_does_not_exist(self):
        """Case for is materials or human resources are not requested and already marked provided"""
        id = get_request_id("dne@myMail.net", 1)
        assert id is None
        assert provide_humans(id) is False
        assert provide_mats(id) is False
        assert delete_request_row(id) is False


class ExpireTests(unittest.TestCase):
    """Test cases for expire_item function"""

    def test_item_exists_not_expired(self):
        """Base Case"""
        create_request_row("test@myMail.net", 1, 1000, None, None, "12345")
        id = get_request_id("test@myMail.net", 1)
        assert id is not None
        assert expire_request(id) is True
        assert delete_request_row(id) is True

    def test_item_exists_is_expired(self):
        """Case for when item is already expired"""
        create_request_row("test@myMail.net", 1, 1000, None, None, "12345")
        id = get_request_id("test@myMail.net", 1)
        assert id is not None
        assert expire_request(id) is True
        assert expire_request(id) is True
        assert delete_request_row(id) is True

    def test_item_dne(self):
        """Case for no matching request item"""
        id = get_request_id("test@myMail.net", 1)
        assert id is None
        assert expire_request(id) is False
        assert delete_request_row(id) is False


class EventTests(unittest.TestCase):
    """Cases for get_event_name, create_event, and delete_event functions"""

    def test_event_exists(self):
        """Base Case"""
        create_event("Big Storm", "Tornado", "12345", "Bad")
        id = get_event_id("Big Storm")
        assert id is not None
        assert get_event_name(id) == "Big Storm"
        assert delete_event_row("Big Storm") is True

    def test_event_dne(self):
        """Case for no matching event"""
        id = get_event_id("Big Storm Fake Test")
        assert id is None
        assert get_event_name(id) is None
        assert delete_event_row("Big Storm") is True


class PledgeTests(unittest.TestCase):
    """Cases for create_pledge_row function"""

    def test_create_pledge_1(self):
        """Base Case"""
        assert create_pledge_row("MartyMcFly@BTTF.biz", 500, None, None, "00000") is True
        assert delete_pledge_by_amount("MartyMcFly@BTTF.biz", 500, "00000") is True

    def test_create_pledge_2(self):
        """Second case"""
        assert create_pledge_row("notARealEmail@fakeStuff.com", 1000, None, "Stuff", "00001") is True
        assert delete_pledge_by_amount("notARealEmail@fakeStuff.com", 1000, "00001") is True


if __name__ == "__main__":
    unittest.main()
