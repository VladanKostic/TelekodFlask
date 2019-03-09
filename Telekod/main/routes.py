from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from Telekod.main.forms import MockdataForm
import json
import sqlite3
from sqlite3 import Error


main = Blueprint("main", __name__)


@main.route('/')
def home():
    return render_template('home.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/dashboard')
def dashboard():
    if session['logged_in']:
        return render_template('dashboard.html')
    else:
        error = 'Invalid login'
        return render_template('login.html', error=error)


@main.route('/mockdata', methods=['GET', 'POST'])
def mockdata():
    populate_table_from_json()
    try:
        # noinspection PyShadowingNames
        conn = sqlite3.connect("telekod.db")
        c = conn.cursor()
        # Get category
        result_cat = c.execute("SELECT * FROM mock_data order by id")
        if result_cat:
            mockdatarows = c.fetchall()
            return render_template('mockdata.html', mockdatarows=mockdatarows)
        conn.close()
    except Error as e:
        print(e)


def populate_table_from_json():
    try:
        # noinspection PyShadowingNames
        conn = sqlite3.connect("telekod.db")
        c = conn.cursor()
        result_mockdata = c.execute("SELECT count(*) FROM mock_data")
        property_count = result_mockdata.fetchone()[0]
        print(property_count)
        if property_count == 0:
            with open('Telekod/assets/data/MOCK_DATA.json', mode="r", encoding="utf-8") as json_file:
                data = (json.load(json_file))
            for row_data in data:
                c.execute("INSERT INTO MOCK_DATA VALUES (?, ?, ?, ?, ?, ?)", (row_data["id"], row_data["first_name"], row_data["last_name"], row_data["address"], row_data["date_of_birth"], row_data["payment"]))
            conn.commit()
            conn.close()
    except Error as e:
        print(e)


@main.route('/mockdata_add', methods=['GET', 'POST'])
def mockdata_add():
        # noinspection PyGlobalUndefined
        global conn
        form = MockdataForm(request.form)
        if request.method == 'POST':  # and form.validate():
            id = form.id.data
            firstname = form.firstname.data
            lastname = form.firstname.data
            address = form.address.data
            dataofbirth = form.dataofbirth.data
            payment = form.payment.data

            # Create cursor
            try:
                conn = sqlite3.connect("telekod.db")
            except Error as e:
                print(e)
            cur = conn.cursor()
            # Execute
            cur.execute("INSERT INTO mock_data(id, first_name, last_name, address, date_of_birth, payment) VALUES(?, ?, ?, ?, ?, ?)", (id, firstname, lastname, address, dataofbirth, payment))
            # Commit to DB
            conn.commit()
            # Close connection
            conn.close()
            flash('Mock data created!', 'success')
            return redirect(url_for('main.mockdata'))
        return render_template('mockdata_add.html', form=form)


@main.route('/mockdata_edit/<string:md_id>', methods=['GET', 'POST'])
def mockdata_edit(md_id):
    # Create cursor
    try:
        conn_c = sqlite3.connect("telekod.db")
        cur = conn_c.cursor()
        t = [md_id]
        # Get article by id
        cur.execute("SELECT * FROM mock_data WHERE id = ?", t)
        mockdata_e = cur.fetchone()
        # Get form
        form = MockdataForm(request.form)
        # Populate category form fields
        form.id.data = mockdata_e[0]
        form.firstname.data = mockdata_e[1]
        form.lastname.data = mockdata_e[2]
        form.address.data = mockdata_e[3]
        form.dataofbirth.data = mockdata_e[4]
        form.payment.data = mockdata_e[5]
        if request.method == 'POST':  # and form.validate():
            # id = request.form['id']
            # firstname = request.form['firstname']
            # lastname = request.form['lastname']
            address = request.form['address']
            # dataofbirth = request.form['dataofbirth']
            payment = request.form['payment']

            # Execute
            cur.execute("UPDATE mock_data SET address = ?, payment = ? WHERE id = ?", (address, payment, md_id))
            # Commit to DB
            conn_c.commit()
            # Close connection
            cur.close()
            flash('Mock data updated!', 'success')
            return redirect(url_for('main.mockdata'))
        return render_template('mockdata_edit.html', form=form)
    except Error as e:
        print(e)


@main.route('/mockdata_delete/<string:md_id>', methods=['GET', 'POST'])
def mockdata_delete(md_id):
        # Create cursor
        # noinspection PyGlobalUndefined
        global conn
        try:
            conn = sqlite3.connect("telekod.db")
            cur = conn.cursor()
            # Execute
            cur.execute("DELETE FROM mock_data WHERE id = ?", [md_id])
            # Commit to DB
            conn.commit()
            # Close connection
            cur.close()
            flash('Mock data deleted!', 'success')
            return redirect(url_for('main.mockdata'))
        except Error as e:
            print(e)


@main.route('/graph')
def graph():
    try:
        # noinspection PyShadowingNames
        conn = sqlite3.connect("telekod.db")
        c = conn.cursor()

        # noinspection PyUnusedLocal
        results = []
        labels = []
        values = []

        results = c.execute("SELECT first_name, substr(payment,2,length(payment)) FROM mock_data")

        for row in results:
            labels.append(row[0])
            estimation = (row[1])
            values.append(estimation)

        line_labels = labels
        line_values = values
        return render_template('graph.html', title='Graph of the payment', max=10000, labels=line_labels, values=line_values)
    except Error as e:
        print(e)
