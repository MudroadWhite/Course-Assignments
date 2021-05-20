"""Contains functions pertaining to mySQL initialization
RUN: pip install mysql-connector-python
DO: Create a file called login.txt in the parent directory of dams14 where line one is
your username for MySQL and line two is your password"""

import mysql.connector
from bcrypt import checkpw, hashpw, gensalt

# Create a file called login.txt in the same directory as dams14, line1 = user line2 = password
login_file = open("../login.txt")
login_info = login_file.read().splitlines()  # This creates a list [user, password]

mydb = mysql.connector.connect(
    host="localhost",
    user=login_info[0],
    password=login_info[1],
    database="DAMS"
)

my_cursor = mydb.cursor(buffered=True)


def create_events_table():
    my_cursor.execute("CREATE TABLE IF NOT EXISTS events (id MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,"
                      "eventType VARCHAR(255), eventZip VARCHAR(255),"
                      "eventTitle VARCHAR(255), eventDesc VARCHAR(255),"
                      "PRIMARY KEY (id))")
    mydb.commit()


def create_users_table():
    """Creates an empty table called users that stores emails and passwords"""
    my_cursor.execute("CREATE TABLE IF NOT EXISTS users (fn VARCHAR(255), ln VARCHAR(255), "
                      "email VARCHAR(255), password VARCHAR(255)"
                      ", zip VARCHAR(8), role VARCHAR(32))")
    mydb.commit()


def create_requests_table():
    """Creates an empty table called users that stores emails and passwords"""
    my_cursor.execute("CREATE TABLE IF NOT EXISTS requests (eventID MEDIUMINT(8), requestID "
                      "MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT primary key, email VARCHAR(255),"
                      " amount VARCHAR(255), amountCont VARCHAR(255)"
                      ", materials VARCHAR(255), matsReceived TINYINT(1), humanRes VARCHAR(255),"
                      "humanReceived TINYINT(1), zip VARCHAR(8), expired TINYINT(1))")
    mydb.commit()


def create_pending_events_table():
    """Creates the table of events to be approved by admin"""
    my_cursor.execute("CREATE TABLE IF NOT EXISTS pendingEvents (id MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,"
                      "eventType VARCHAR(255), eventZip VARCHAR(255),"
                      "eventTitle VARCHAR(255), eventDesc VARCHAR(255), email VARCHAR(255), "
                      "PRIMARY KEY (id))")
    mydb.commit()


def create_donations_table():
    """Creates the table for donations and pledge"""
    my_cursor.execute(("CREATE TABLE IF NOT EXISTS donations (id MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,"
                       "requestID MEDIUMINT(8), email VARCHAR(255), amount VARCHAR(255),"
                       "amountDelivered TINYINT(1), humanRes VARCHAR(255), humanDelivered TINYINT(1),"
                       "materials VARCHAR(255), matsDelivered TINYINT(1), zip VARCHAR(8), expired TINYINT(1), "
                       "PRIMARY KEY (id))"))
    mydb.commit()


def email_info_in_db(email, psw, role, zipcode):
    """Checks that a row exists in users"""
    my_cursor.execute("SELECT * FROM users WHERE email = '{}'".format(email))
    results = my_cursor.fetchall()
    if len(results) == 0:
        # Email not in database
        return False

    for i in results:
        # Password matches
        if checkpw(psw, i[3]):
            # zipcode matches
            if i[4] == zipcode:
                # role matches
                if i[5] == role:
                    mydb.commit()
                    return True

    # Email does exist but password does not match
    mydb.commit()
    return False


def create_admin(email, password, zipcode, fn, ln):
    """Creates an admin account"""
    # Check if account exists
    my_cursor.execute("SELECT * FROM users WHERE email = '{}'".format(email))
    count = len(my_cursor.fetchall())

    if count == 0:
        # Account does not exist
        sql = "INSERT INTO users (fn, ln, email, password, zip, role) " \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        val = (fn, ln, email, hashpw(password.encode('utf-8'), gensalt(12)), zipcode, 'admin')
        my_cursor.execute(sql, val)
        mydb.commit()
        return True
    else:
        mydb.commit()
        return False


def delete_row(email):
    """Deletes a row based on unique identifier email"""
    my_cursor.execute("DELETE FROM users WHERE email = '{}'".format(email))
    mydb.commit()


def delete_event_row(title):
    """Deletes a row based on unique identifier email"""
    if title is not None:
        my_cursor.execute("DELETE FROM events WHERE eventTitle = '{}'".format(title))
        mydb.commit()
        return True
    mydb.commit()
    return False


def delete_request_row(rid):
    """Deletes a row based on unique identifier email"""
    if rid is not None:
        my_cursor.execute("DELETE FROM requests WHERE requestID = {}".format(rid))
        mydb.commit()
        return True
    mydb.commit()
    return False


def has_request(email, event_id):
    """Returns True if the user already has an open request for an event id"""
    my_cursor.execute("SELECT * FROM requests WHERE "
                      "eventID = {} AND email = '{}' AND expired = 0".format(event_id, email))
    mydb.commit()
    return len(my_cursor.fetchall()) != 0


def create_request_row(email, event_id, amount, mats, human_rec, zipcode):
    """Creates an entry in the requests table does not already have an active request for an
    event"""
    if has_request(email, event_id) is False:
        sql = "INSERT INTO requests (eventID, email, amount, amountCont, materials, matsReceived, " \
              "humanRes, humanReceived, zip, expired)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (event_id, email, amount, 0, mats, 0, human_rec, 0, zipcode, 0)
        my_cursor.execute(sql, val)
        mydb.commit()
        return True
    mydb.commit()
    return False


def get_request_id(email, event_id):
    """returns the open request id given an email and eventID"""
    my_cursor.execute("SELECT requestID FROM requests WHERE "
                      "email = '{}' AND eventID = {} AND expired = 0".format(email, int(event_id)))
    data = my_cursor.fetchone()
    if data is not None:
        return data[0]
    return None


def expire_request(rid):
    """Expires a request given the id"""
    if rid is not None:
        my_cursor.execute("UPDATE requests SET expired = 1 WHERE requestID = {}".format(rid))
        mydb.commit()
        return True
    mydb.commit()
    return False

def delete_donation_by_info(myZip, dollar, human, mats, email):
    my_cursor.execute("DELETE FROM donations WHERE zip = {}" \
                      "AND amount = {} AND humanRes = {} and materials = {}" \
                      "AND email = {}"
                      .format(myZip, dollar, human, mats, email))
    mydb.commit()
    return False

def provide_humans(rid):
    """Sets requested human status to provided"""
    if rid is not None:
        my_cursor.execute("UPDATE requests SET humanReceived = 1 WHERE requestID = {}".format(rid))
        mydb.commit()
        return True
    mydb.commit()
    return False


def provide_mats(rid):
    """Sets requested materials status to provided"""
    if rid is not None:
        my_cursor.execute("UPDATE requests SET matsReceived = 1 WHERE requestID = {}".format(rid))
        mydb.commit()
        return True
    mydb.commit()
    return False


def get_event_name(rid):
    """gets an event name given the event id"""
    if rid is not None:
        my_cursor.execute("SELECT eventTitle FROM events WHERE id = {}".format(rid))
        result = my_cursor.fetchone()
        if result is None:
            return "Event Does not Exist"
        return result[0]
    return None


def create_event(event_title, event_type, event_zip, event_desc):
    """Creates a new event"""
    # Check if event exists
    my_cursor.execute("SELECT * FROM events WHERE eventTitle = '{}'".format(event_title))
    count = len(my_cursor.fetchall())

    # Event doesnt exist
    if count == 0:
        sql = "INSERT INTO events (eventType, eventZip, eventTitle, eventDesc)" \
              "VALUES (%s, %s, %s, %s)"
        val = (event_type, event_zip, event_title, event_desc)
        my_cursor.execute(sql, val)
        mydb.commit()


def get_event_id(event_title):
    """returns the event id given a title"""
    my_cursor.execute("SELECT id FROM events WHERE "
                      "eventTitle = '{}'".format(event_title))
    data = my_cursor.fetchone()
    if data is not None:
        return data[0]
    return None


def commit():
    """Commits the database"""
    mydb.commit()


def get_remaining(request_id):
    """Given a request id, return the amount of money needed to hit goal"""
    my_cursor.execute("SELECT amount FROM requests WHERE requestID = {}".format(request_id))
    amount = my_cursor.fetchone()
    my_cursor.execute("SELECT amountCont FROM requests WHERE requestID = {}".format(request_id))
    contributed = my_cursor.fetchone()

    # Check that both amounts exist
    if amount is None or contributed is None:
        return 0

    return int(amount[0]) - int(contributed[0])


def contribute(cont, request_id):
    """Contributes the given amount towards a request"""
    my_cursor.execute("SELECT amountCont FROM requests WHERE requestID = {}".format(request_id))
    amount = my_cursor.fetchone()

    if amount is None:
        # Request item does not exist
        return False

    my_cursor.execute("SELECT amount FROM requests WHERE requestID = {}".format(request_id))
    need = my_cursor.fetchone()

    amount = int(amount[0])
    give = amount + cont
    need = int(need[0])

    # Check that the donation won't exceed the requested amount
    if give > need:
        return False

    # Otherwise add it to the request column
    my_cursor.execute("UPDATE requests SET amountCont = {} WHERE requestID = {}".format(give, request_id))
    mydb.commit()
    return True


def delete_request(request_id):
    """Deletes a request from the requests table"""
    # Check if request exists
    my_cursor.execute("SELECT * FROM requests WHERE requestID = {}".format(request_id))
    count = len(my_cursor.fetchall())

    if count == 0:
        # Request does not exist, do nothing
        return False

    # Account does exist, delete it and return true
    my_cursor.execute("DELETE FROM requests WHERE requestID = {}".format(request_id))
    mydb.commit()
    return True


def create_pledge_row(email, amount, humans, mats, zipcode):
    """Creates a new pledge"""
    sql = "INSERT INTO donations (requestID, email, amount, amountDelivered, humanRes, " \
          "humanDelivered, materials, matsDelivered, zip, expired)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (None, email, amount, 0, humans, 0, mats, 0, zipcode, 0)
    my_cursor.execute(sql, val)
    mydb.commit()
    return True


def delete_pledge_by_amount(email, amount, zipcode):
    """Deletes a pledge by info"""

    temp_cursor = mydb.cursor()

    if amount is not None:
        temp_cursor.execute("SELECT * FROM donations WHERE email = '{}' AND amount = {} AND "
                          "zip = '{}'".format(email, amount, zipcode))
        count_loc = len(temp_cursor.fetchall())
        print(count_loc)

        if count_loc == 0:
            # Request does not exist, do nothing
            return False

        temp_cursor.execute("DELETE FROM donations WHERE email = '{}' AND amount = '{}' AND "
                          "zip = '{}'".format(email, amount, zipcode))
        mydb.commit()
        return True
    else:
        temp_cursor.execute("SELECT * FROM donations WHERE email = '{}' AND amount IS NULL AND "
                          "zip = '{}'".format(email, amount, zipcode))
        count_loc = len(temp_cursor.fetchall())

        if count_loc == 0:
            # Request does not exist, do nothing
            return False

        temp_cursor.execute("DELETE FROM donations WHERE email = '{}' AND amount IS NULL AND "
                          "zip = '{}'".format(email, amount, zipcode))
        mydb.commit()
        return True


def create_donation_row(email, amount, humans, mats, zipcode, rid):
    """Creates a new donation"""
    sql = "INSERT INTO donations (requestID, email, amount, amountDelivered, humanRes, " \
          "humanDelivered, materials, matsDelivered, zip, expired)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (rid, email, amount, 0, humans, 0, mats, 0, zipcode, 0)
    my_cursor.execute(sql, val)
    mydb.commit()

    # Update the corresponded amount of dollars received for the corresponded recipient...
    update_request_amount_count(rid, amount)
    return True


def update_request_amount_count(rid, amount):
    """Updates(add) the amount of dollars to a specific request"""
    sql = "UPDATE requests " \
          "SET amountCont = amountCont + %s" \
          "WHERE requestID = %s"
    val = (amount, rid)
    my_cursor.execute(sql, val)
    mydb.commit()
    return True


if __name__ == "__main__":
    # create_admin("admin@admin.com", "Admin12345", "12345", "Asd", "Asd")
    # create_pending_events_table()
    create_events_table()

    pass
    # create_donations_table()
    # create_pending_events_table()
    # create_requests_table()

# donor@donor.com
# Donor12345

# recipient@recipient.com
# Recipient12345

# admin@admin.com
# Admin12345