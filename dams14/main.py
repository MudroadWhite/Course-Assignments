"""This file will serve as application driver code, all existing code in file is placeholder
for pylint testing. To test pylint, run "pip install pylint" in terminal and execute with
pylint main.py

RUN: pip install selenium
     pip install pytest
     pip install flask
     pip install mysql-connector-python
     pip install flask_session
     pip install redis
     look for this"""

import re
import mysql.connector
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_session import Session
from bcrypt import hashpw, gensalt, checkpw
from database import get_event_name, create_request_row, \
    delete_request, create_pledge_row, create_donation_row, expire_request

app = Flask(__name__, template_folder="templates")
app.secret_key = "hfow875^&i3%3425tv9;2^$"

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

# Create a file called login.txt in the same directory as dams14, line1 = user line2 = password
login_file = open("../login.txt")
login_info = login_file.read().splitlines()  # This creates a list [user, password]

mydb = mysql.connector.connect(
    host="localhost",
    user=login_info[0],
    password=login_info[1],
    database="DAMS"
)


@app.route("/")
def home():
    """Displays the DAMS Homepage"""
    return render_template("index.html")


@app.route('/showSignIn')
def show_sign_in():
    """Displays DAMS sign in page"""
    return render_template("signIn.html")


@app.route('/showSignIn', methods=['POST'])
def get_sign_in():
    """Attempts sign in, creates session, redirects to home"""
    # Get info from form
    email = request.form['email']
    psw = request.form['psw'].encode('utf-8')
    db_name = None
    db_role = None
    db_zip = None
    db_pass = None

    # query database table users for info
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT * FROM users WHERE email = '{}'".format(email))
    db_result = my_cursor.fetchall()
    for i in db_result:
        db_pass = i[3].encode('utf-8')
        db_name = i[0]
        db_zip = i[4]
        db_role = i[5]
    # check that passwords match
    if db_pass is not None:
        if checkpw(psw, db_pass):
            # Passwords match
            session.permanent = False
            session['name'] = db_name
            session['email'] = email
            session['login'] = True
            session['zip'] = db_zip
            session['role'] = db_role
            return render_template("index.html")

    # Passwords don't match or user doesn't exist
    flash("Username or password is incorrect")
    return render_template("signIn.html")


@app.route('/logout')
def logout():
    """Logs out user"""
    '''session['name'] = None
    session['email'] = None
    session['login'] = False
    session['zip'] = None
    session['role'] = None'''
    session.clear()
    return render_template("index.html")


@app.route('/showDash', methods=['GET'])
def show_dash():
    """Logs out user"""
    if session['role'] == 'admin':
        return render_template("admin.html")
    elif session['role'] == 'donor':
        mydb.commit()
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute("SELECT * FROM donations WHERE email = '{}'".format(session['email']))
        data = my_cursor.fetchall()
        return render_template("donor.html", data=data)
    elif session['role'] == 'recipient':
        mydb.commit()
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute("SELECT * FROM requests WHERE email = '{}'".format(session['email']))
        data = my_cursor.fetchall()
        data = [row + (get_event_name(row[0]),) for row in data]
        return render_template("Recipient.html", data=data)
    return render_template("index.html")


@app.route('/createPledge')
def show_create_pledge():
    """Shows the pledge creation screen"""
    if session['role'] == 'donor':
        return render_template("createPledge.html")
    else:
        render_template("index.html")


@app.route('/createPledge', methods=['POST'])
def create_pledge():
    """Submits a new pledge"""

    # Get the field values
    zipcode = request.form['myZip']
    dollar = request.form['dollar']
    human = request.form['human']
    mats = request.form['mats']

    # Rewrite the values
    if zipcode == "":
        zipcode = None
    if dollar == "":
        dollar = None
    if human == "":
        human = None
    if mats == "":
        mats = None

    # Check that at least one field is filled
    if dollar is None and human is None and mats is None:
        flash("Please fill out at least one field (Dollar Amount, Human Resources, or Materials)")
        return render_template("createPledge.html")

    else:
        mydb.commit()
        create_pledge_row(session['email'], dollar, human, mats, zipcode)
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute("SELECT * FROM donations WHERE email = '{}'".format(session['email']))
        data = my_cursor.fetchall()
        return render_template("donor.html", data=data)


@app.route('/createDonation')
def show_create_donation():
    """Shows the donation creation screen"""
    if session['role'] == 'donor':

        mydb.commit()
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute("SELECT r.eventID, r.requestID, r.amount, r.amountCont, r.materials, r.matsReceived, \
	                        r.humanRes, r.humanReceived, r.zip, e.eventType \
                            FROM dams.requests AS r, dams.events AS e WHERE r.expired=0 AND r.eventID = e.id;")
        data = my_cursor.fetchall()

        data = [row + (get_event_name(row[0]),) for row in data]
        return render_template("createDonation.html", data=data)
    else:
        render_template("index.html")


@app.route('/createDonation', methods=['POST'])
def create_donation():
    """Deprecated"""
    pass


@app.route("/makeDonation/<string:rid>")
def show_make_donation(rid):
    """Shows the event approval page"""
    return render_template("makeDonation.html")


@app.route("/makeDonation/<string:rid>", methods=['POST'])
def make_donation(rid):
    """Makes a donation page for the event"""

    zipcode = request.form['myZip']
    dollar = request.form['dollar']
    human = request.form['human']
    mats = request.form['mats']

    if zipcode == "":
        zipcode = None
    if dollar == '':
        dollar = None
    if human == '':
        human = None
    if mats == '':
        mats = None

    if dollar is None and human is None and mats is None:
        flash("Please fill out at least one field (Dollar Amount, Human Resources, or Materials)")
        return show_make_donation(rid)

    else:
        mydb.commit()
        create_donation_row(session['email'], dollar, human, mats, zipcode, rid)
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute("SELECT * FROM donations WHERE email = '{}'".format(session['email']))
        data = my_cursor.fetchall()
        return render_template("donor.html", data=data)


@app.route('/createRequest', methods=['GET'])
def show_request():
    """Loads the request creation page"""
    mydb.commit()
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT id, eventTitle FROM events")
    data = my_cursor.fetchall()
    if session['role'] == 'recipient' or session['role'] == 'admin':
        return render_template("createRequest.html", data=data)
    else:
        render_template("index.html")


@app.route('/createRequest', methods=['POST'])
def create_request():
    """Submits the request"""

    # Get the field values
    event_id = int(request.form['event'].split(',')[0])
    zipcode = request.form['myZip']
    dollar = request.form['dollar']
    human = request.form['human']
    mats = request.form['mats']

    # Rewrite the values
    if dollar == "":
        dollar = None
    if human == "":
        human = None
    if mats == "":
        mats = None

    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT * FROM requests WHERE"
                      " email = '{}' AND eventID = {} AND expired = 0".format(session['email'], event_id))
    exists = my_cursor.fetchall()

    # Check that at least one field is filled
    if dollar is None and human is None and mats is None:
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute("SELECT id, eventTitle FROM events")
        data = my_cursor.fetchall()
        flash("Please fill out at least one field (Dollar Amount, Human Resources, or Materials)")
        return render_template("createRequest.html", data=data)

    # All required fields are filled correctly, attempt create entry
    elif exists:
        flash("You already have an open request for this event. Please close your request and try again")
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute("SELECT id, eventTitle FROM events")
        data = my_cursor.fetchall()
        return render_template("createRequest.html", data=data)

    else:
        mydb.commit()
        create_request_row(session['email'], int(event_id), dollar, mats, human, zipcode)
        my_cursor = mydb.cursor(buffered=True)
        my_cursor.execute("SELECT * FROM requests WHERE email = '{}'".format(session['email']))
        data = my_cursor.fetchall()
        data = [row + (get_event_name(row[0]),) for row in data]
        return render_template("Recipient.html", data=data)


@app.route('/deleteRequest', methods=['GET'])
def show_delete_request():
    """Shows the request deletion page"""
    my_cursor = mydb.cursor(buffered=True)
    # Get all requests
    my_cursor.execute("SELECT requestID, eventID FROM requests WHERE email = '{}'".format(session['email']))
    data = my_cursor.fetchall()

    # format the data
    data = [(a, get_event_name(b)) for (a, b) in data]

    # Check the user is a recipient
    if session['role'] == 'recipient' and data != []:
        return render_template("deleteRequest.html", data=data)
    elif session['role'] == 'recipient':
        flash("You have no requests to be deleted")
        return render_template("Recipient.html")
    else:
        return render_template("index.html")


@app.route('/deleteRequest', methods=['POST'])
def delete_request_form():
    """Deletes a selected request"""
    req = request.form['request']

    # Check that the request is valid
    if req is not None:
        # Request is valid
        rid = req.split(", ")[0]
        delete_request(rid)
        return show_dash()

    # Request is None
    flash("Please select a valid request")
    return show_delete_request()


@app.route('/requestEvent')
def show_request_event():
    """Displays Add Event page"""
    return render_template("requestEventCreation.html")


@app.route('/requestEvent', methods=['POST'])
def request_event():
    """Requests an event for creation"""
    event_type = request.form['event']
    event_zip = request.form['eventZip']
    event_title = request.form['eventTitle']
    event_desc = request.form['eventDesc']

    # Check if event exists
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT * FROM events WHERE eventTitle = '{}'".format(event_title))
    count = len(my_cursor.fetchall())

    # Event doesnt exist
    if count == 0:
        sql = "INSERT INTO pendingEvents (eventType, eventZip, eventTitle, eventDesc, email)" \
              "VALUES (%s, %s, %s, %s, %s)"
        val = (event_type, event_zip, event_title, event_desc, session['email'])
        my_cursor.execute(sql, val)
        mydb.commit()
        flash("Request successfully submitted!")
        return show_dash()

    # Event already exists
    flash("Event already exists. Please create a request from the dashboard.")
    return show_request_event()


@app.route('/editEvent', methods=['GET','POST'])
def show_edit_event():
    """Shows drop down of events to edit"""
    my_cursor = mydb.cursor(buffered=True)
    # Get all requests
    my_cursor.execute("SELECT id, eventTitle FROM events")
    data = my_cursor.fetchall()
    print(data)

    if request.method == 'POST':
        event = request.form['event']
        session['tempEvent'] = event
        return redirect(url_for('show_add_edited_event', event=event))

    return render_template("editEvent.html", data=data)


@app.route("/addEditedEvent", methods=['GET'])
def show_add_edited_event():
    """ Updates page to editing menu"""
    event = session['tempEvent']
    event_id = re.search(r'\d+', event).group()
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT * FROM events WHERE id=%s", (event_id[0],))
    data = my_cursor.fetchone()

    return render_template("addEditedEvent.html", data=data)


@app.route("/addEditedEvent", methods=['POST'])
def post_add_edited_event():
    """ Updates changes in data base"""
    event = session['tempEvent']
    event_id = re.search(r'\d+', event).group()

    event_Type = request.form['eventType']
    event_Zip = request.form['eventZip']
    event_Title = request.form['eventTitle']
    event_Desc = request.form['eventDesc']

    my_cursor = mydb.cursor()
    my_cursor.execute("""
        UPDATE events 
        SET eventType=%s, eventZip=%s, eventTitle=%s, eventDesc=%s
        WHERE id=%s 
        """, (event_Type, event_Zip, event_Title, event_Desc, event_id[0]))

    mydb.commit()
    flash("Event successfully edited!")

    return show_dash()


@app.route("/deleteEvent", methods=['GET'])
def show_delete_event():
    """ Display delete event page """
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT id, eventTitle FROM events")
    data = my_cursor.fetchall()

    return render_template("deleteEvent.html", data=data)


@app.route("/deleteEvent", methods=['POST'])
def post_delete_event():
    """ Delete event from database"""
    event = request.form['event']
    event_id = re.search(r'\d+', event).group()
    print(event_id)

    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("DELETE FROM events WHERE id=%s", (event_id,))
    mydb.commit()

    return show_dash()


@app.route("/adminDeleteRequestEvent", methods=['GET'])
def show_admin_delete_request_event():
    """Loads event selection page for request deletion"""
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT id, eventTitle FROM events")
    data = my_cursor.fetchall()

    return render_template("adminDeleteRequestEvent.html", data=data)


@app.route("/adminDeleteRequestEvent", methods=['POST'])
def post_admin_delete_request_event():
    """ Submits drop down form"""
    eventTitle = request.form['event']
    event_id = re.search(r'\d+', eventTitle).group()
    session['requestEventID'] = event_id

    return redirect(url_for('show_admin_delete_request', event_id=event_id))


@app.route("/adminDeleteRequest", methods=['GET'])
def show_admin_delete_request():
    """ Show delete requests page """
    event_id = session['requestEventID']

    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT requestID, email FROM requests WHERE eventID=%s", (event_id[0], ))
    data = my_cursor.fetchall()

    return render_template("adminDeleteRequest.html", data=data)


@app.route("/adminDeleteRequest", methods=['POST'])
def post_admin_delete_request():
    """ Deletes desired request"""
    deleteRequest = request.form['event']
    request_id = re.search(r'\d+', deleteRequest).group()

    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("DELETE FROM requests WHERE requestID=%s", (request_id[0],))
    mydb.commit()

    return show_dash()


@app.route("/editRequestEvent", methods=['GET'])
def show_edit_request_event():
    """Loads event selection page for request edit"""
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT id, eventTitle FROM events")
    data = my_cursor.fetchall()

    return render_template("editRequestEvent.html", data=data)


@app.route("/editRequestEvent", methods=['POST'])
def post_edit_request_event():
    """ Submits event for request"""
    eventTitle = request.form['event']
    event_id = re.search(r'\d+', eventTitle).group()
    session['requestEventID'] = event_id

    return redirect(url_for('show_edit_request_select', event_id=event_id))


@app.route("/editRequestSelect", methods=['GET'])
def show_edit_request_select():
    """ Show list of requests to edit """
    event_id = session['requestEventID']

    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT requestID, email FROM requests WHERE eventID=%s", (event_id[0],))
    data = my_cursor.fetchall()

    return render_template("editRequestSelect.html", data=data)


@app.route("/editRequestSelect", methods=['POST'])
def post_edit_request_select():
    """ Selects request to be edited """
    requestTitle = request.form['request']
    request_id = re.search(r'\d+', requestTitle).group()
    session['requestID'] = request_id

    return redirect(url_for('show_edit_request', request_id=request_id))


@app.route("/editRequest", methods=['GET'])
def show_edit_request():
    """ Show edit request page"""
    request_id = session['requestID']
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT * FROM requests WHERE requestID=%s", (request_id,))
    data = my_cursor.fetchone()

    return render_template("editRequest.html", data=data)


@app.route("/editRequest", methods=['POST'])
def post_edit_request():
    request_id = session['requestID']
    zipcode = request.form['myZip']
    dollar = request.form['dollar']
    human = request.form['human']
    mats = request.form['mats']

    # Rewrite the values
    if dollar == "":
        dollar = None
    if human == "":
        human = None
    if mats == "":
        mats = None

    if dollar is None and human is None and mats is None:
        flash("Please fill out at least one field (Dollar Amount, Human Resources, or Materials)")
        return render_template("editRequest.html")

    my_cursor = mydb.cursor()
    my_cursor.execute("""
            UPDATE requests
            SET zip=%s, amount=%s, humanRes=%s, materials=%s
            WHERE requestID=%s 
            """, (zipcode, dollar, human, mats, request_id[0]))

    mydb.commit()

    return show_dash()


@app.route("/donationMatch", methods=['GET'])
def show_donation_match():
    """ Display donor match page"""
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT id,zip,amount,humanRes,materials FROM donations WHERE requestID IS NULL")
    data1 = my_cursor.fetchall()

    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT requestID,zip,amount,humanRes,materials FROM requests")
    data2 = my_cursor.fetchall()

    return render_template("donationMatch.html", data1=data1, data2=data2)


@app.route("/donationMatch", methods=['POST'])
def post_donation_match():
    """ Updates data base with new matches"""
    donation = request.form['donation']
    req = request.form['request']

    print(req)

    request_id = re.search(r'\d+', req).group()
    donation_id = re.search(r'\d+', donation).group()
    print(donation_id)
    print(request_id)

    my_cursor = mydb.cursor()
    my_cursor.execute("""
                UPDATE donations
                SET requestID=%s
                WHERE id=%s
                """, (request_id, donation_id))

    mydb.commit()
    if request_id is not None and donation_id is not None:
        flash('Match Successful!', 'success')
    return redirect(url_for('show_donation_match'))


@app.route("/approveEvent")
def show_approve_event():
    """Shows the event approval page"""
    if session['role'] == 'admin':
        my_cursor = mydb.cursor()
        my_cursor.execute("SELECT * FROM pendingEvents")
        data = my_cursor.fetchall()
        return render_template("managePendingEvents.html", data=data)
    return render_template("index.html")


@app.route("/approveEvent/<string:eid>/<int:approved>", methods=['GET', 'POST'])
def approve_event(eid, approved):
    """Deletes an event request or adds it to the event database"""
    my_cursor = mydb.cursor()
    if approved == 1:
        # Add it to the events table and remove it from the pending
        my_cursor.execute("SELECT * FROM pendingEvents WHERE id = {}".format(eid))
        data = my_cursor.fetchone()
        sql = "INSERT INTO events (eventType, eventZip, eventTitle, eventDesc)" \
              "VALUES (%s, %s, %s, %s)"
        val = (data[1], data[2], data[3], data[4])
        my_cursor.execute(sql, val)
        mydb.commit()

        # Delete the item from the pending table
        my_cursor.execute("DELETE FROM pendingEvents WHERE id = {}".format(eid))
        mydb.commit()

        flash("Event Successfully Approved")
        return show_approve_event()
    else:
        # Drop the entry
        my_cursor.execute("DELETE FROM pendingEvents WHERE id = {}".format(eid))
        mydb.commit()
        flash("Event Rejected Successfully")
        return show_approve_event()


@app.route("/editRequest/<string:rid>", methods=['GET'])
def show_edit_request_recipient(rid):
    """Shows the request editing page"""
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT * FROM requests WHERE requestID = {}".format(rid))
    data = my_cursor.fetchone()

    if data is None:
        # Request is invalid
        flash("Request is invalid")
        if session['role'] == "recipient":
            return render_template("Recipient.html")
        return render_template("index.html")

    # Request is valid
    data_new = data + (get_event_name(data[0]),)
    return render_template("editRequestRecipient.html", data=data_new)


@app.route("/editRequest/<string:rid>", methods=['POST'])
def edit_request_recipient(rid):
    """Edits a specific request"""
    event_zip = request.form['myZip']
    dollar = request.form['dollar']
    human = request.form['human']
    mats = request.form['mats']
    rid = int(request.form['rid'])

    # Get the associated entry
    my_cursor = mydb.cursor()
    my_cursor.execute("SELECT * FROM requests WHERE requestID = {}".format(int(rid)))
    data = my_cursor.fetchone()

    # Perform conversions
    # Rewrite the values
    if dollar == "":
        dollar = None
    if human == "":
        human = None
    if mats == "":
        mats = None

    # Check at least one value is filled
    if mats is None and dollar is None and human is None:
        flash("Must leave at least one request filled non-blank")
        return show_edit_request_recipient(rid)

    # Update the values
    if event_zip != data[9]:
        my_cursor.execute("UPDATE requests SET zip = '{}' WHERE requestID = {}".format(event_zip, rid))
        mydb.commit()

    if dollar != data[3] and dollar is not None:
        if int(dollar) >= int(data[4]):  # Check there is not more contributed than set
            my_cursor.execute("UPDATE requests SET amount = '{}' WHERE requestID = {}".format(dollar, rid))
            mydb.commit()
        else:
            flash("Please set requested dollar amount higher than amount contributed")
            return show_edit_request_recipient(rid)

    elif dollar != data[3] and dollar is None:
        if int(data[4]) == 0:  # Check there is not more contributed than set
            sql = "UPDATE requests SET amount = %s WHERE requestID = %s"
            val = (dollar, rid)
            my_cursor.execute(sql, val)
            mydb.commit()
        else:
            flash("Please set requested dollar amount higher than amount contributed")
            return show_edit_request_recipient(rid)

    if human != data[7]:
        sql = "UPDATE requests SET humanRes = %s WHERE requestID = %s"
        val = (human, rid)
        my_cursor.execute(sql, val)
        mydb.commit()

    if mats != data[5]:
        sql = "UPDATE requests SET materials = %s WHERE requestID = %s"
        val = (mats, rid)
        my_cursor.execute(sql, val)
        mydb.commit()

    return show_dash()


@app.route('/showSignUp')
def show_sign_up():
    """Displays DAMS sign up page"""
    return render_template("signUp.html", data=[None, None, None, None, None, None, None])


@app.route('/addEvent')
def add_event():
    """Displays Add Event page"""
    return render_template("addEvent.html")


@app.route('/addEvent', methods=['POST'])
def get_event():
    """Adds event and redirects user"""
    event_type = request.form['eventType']
    event_zip = request.form['eventZip']
    event_title = request.form['eventTitle']
    event_desc = request.form['eventDesc']

    # Check if event exists
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT * FROM events WHERE eventTitle = '{}'".format(event_title))
    count = len(my_cursor.fetchall())

    # Event doesnt exist
    if count == 0:
        sql = "INSERT INTO events (eventType, eventZip, eventTitle, eventDesc)" \
              "VALUES (%s, %s, %s, %s)"
        val = (event_type, event_zip, event_title, event_desc)
        my_cursor.execute(sql, val)
        mydb.commit()
        return show_dash()
    flash("Event already exists in database")
    return render_template("addEvent.html")


@app.route('/showSignUp', methods=['POST'])
def get_sign_up():
    """Attempts account creation and redirects user"""
    fn = request.form['fn']
    ln = request.form['ln']
    email = request.form['email']
    psw = request.form['psw'].encode('utf-8')
    role = request.form['role']
    zipcode = request.form['zip']
    data = [fn, ln, email, request.form['conf_email'], request.form['psw'], request.form['conf_psw'], zipcode]
    if email == request.form['conf_email']:
        # Emails match
        if psw == request.form['conf_psw'].encode('utf-8'):
            # Passwords match

            # Check if account exists
            my_cursor = mydb.cursor(buffered=True)
            my_cursor.execute("SELECT * FROM users WHERE email = '{}'".format(email))
            count = len(my_cursor.fetchall())

            if count == 0:
                # Account does not exist
                sql = "INSERT INTO users (fn, ln, email, password, zip, role) " \
                      "VALUES (%s, %s, %s, %s, %s, %s)"
                val = (fn, ln, email, hashpw(psw, gensalt(12)), zipcode, role)
                my_cursor.execute(sql, val)
                mydb.commit()
                return render_template("index.html")

            # Account does exist
            flash("Entered Email already has an account. Please log in.")
            return render_template("signUp.html", data=data)

        # Passwords don't match
        flash("Entered Passwords do not match")
        return render_template("signUp.html", data=data[:4] + [None, None] + data[6:])

    # Emails do not match
    flash("Entered Emails do not match")
    return render_template("signUp.html", data=data)


@app.route('/showSearchPage')
def search_page():
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT * FROM events")
    data = my_cursor.fetchall()
    return render_template("searchEvents.html", data=data)


@app.route('/showSearchPage', methods=['POST'])
def search_events():
    keyword = request.form['search']
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT * FROM events WHERE "
                      "( eventType LIKE '%{key}%' OR eventZip LIKE '%{key}%'"
                      "OR eventTitle LIKE '%{key}%' OR eventDesc LIKE '%{key}%')".format(key=keyword))
    data = my_cursor.fetchall()
    return render_template("searchEvents.html", data=data)


@app.route('/showEventPage/<string:eid>', methods=['POST', 'GET'])
def show_event_page(eid):
    my_cursor = mydb.cursor(buffered=True)
    my_cursor.execute("SELECT * FROM events WHERE id = '{}'".format(eid))
    data = my_cursor.fetchone()
    return render_template("event_page.html", data=data)


@app.route('/expireRequest', methods=['GET'])
def show_expire_request():
    """Shows the request expiration page"""
    my_cursor = mydb.cursor(buffered=True)
    # Get all requests
    my_cursor.execute("SELECT requestID, eventID, expired FROM requests WHERE email = '{}'".format(session['email']))
    data = my_cursor.fetchall()

    # format the data
    data = [(a, get_event_name(b), c) for (a, b, c) in data if int(c) == 0]

    # Check the user is a recipient
    if session['role'] == 'recipient' and data != []:
        return render_template("expireRequestRecipient.html", data=data)
    elif session['role'] == 'recipient':
        flash("You have no open requests to expire")
        return render_template("Recipient.html")
    else:
        return render_template("index.html")


@app.route('/expireRequest', methods=['POST'])
def expire_request_form():
    """Deletes a selected request"""
    req = request.form['request']

    # Check that the request is valid
    if req is not None:
        # Request is valid
        rid = req.split(", ")[0]
        expire_request(rid)
        return show_dash()

    # Request is None
    flash("Please select a valid request")
    return show_expire_request()


def main():
    """Defines main function to be used by automated testing"""
    app.run()
    mydb.close()


if __name__ == "__main__":
    main()
