""" This file contains the initialisation routines for the db
    and all the routines including some html flie.
"""

import datetime
import sqlite3
from operator import itemgetter
from flask import Flask, request, redirect, url_for, render_template, session
from stiftung.database import create_connection, new_foundation, \
     handle_checkboxes, edit_foundation, make_nice_display, \
     find_entries, sort_by_date

blu = Flask(__name__, instance_relative_config=True)
blu.config.from_object('stiftung.default_config')
blu.config.from_pyfile('config.cfg', silent=True)
blu.debug = True

UNAME = blu.config['USER_NAME']
UPASSWORD = blu.config['USER_PASSWORD']
PATH_TO_DB = blu.config['PATH_TO_DB']
SUPER_USER = blu.config['SUPER_USER']
SUPER_PWD = blu.config['SUPER_PWD']

def get_db():
    """ Create a connection to the sqlite db and return it """
    datab = create_connection(PATH_TO_DB)
    return datab


def init_db():
    """ Fetch the database from 'get_db'
        and return the connection and cursor object
    """
    conn = get_db()
    with blu.open_resource('schema.sql', mode='r') as f:
        cursor = conn.cursor()
        cursor.executescript(f.read())
    return conn, cursor


@blu.route('/')
def main():
    """ Initialise the connection to the db
        Fetch all rows which are already stored and
        display the list of all names on the main page
    """
    #return render_template('index.html')
    #query ganzi db (limit 20)
    conn, cursor = init_db()
    cursor = conn.execute('SELECT ID, foundationname FROM foundations WHERE deleted=?', (0 ,))
    items = cursor.fetchall()
    items = sorted(items, key=itemgetter(1))
    if session.get('logged_in') == True:
        logged_in = 'true'
    elif session.get('superuser') == True:
        logged_in = 'super'
    else:
        logged_in = 'false'

    return render_template('index.html', items=items, log=logged_in)


@blu.route('/super_show')
def db_verwalten():
    conn, cursor = init_db()
    cursor = conn.execute('SELECT ID, foundationname, deleted FROM foundations')
    items = cursor.fetchall()
    return render_template('index.html', items=items, log='super')


@blu.route('/restore')
def restore_entry():
    conn, cursor = init_db()
    get_id = request.args.get('id')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE foundations SET deleted=0 WHERE id=?', (get_id,))
    conn.commit()
    return redirect(url_for('db_verwalten'))



@blu.route('/login')
def do_login():
    if session.get('logged_in') == True:
        return redirect(url_for('formular_in', id=request.args.get('id')))
    else:
        return render_template('login.html', msg={})


@blu.route('/verify', methods=['POST'])
def verify():
    if request.form['password'] == UPASSWORD and request.form['username'] == UNAME:
        session['logged_in'] = True
        return redirect(url_for('main'))
    elif request.form['password'] == SUPER_PWD and request.form['username'] == SUPER_USER:
        session['superuser'] = True
        return redirect(url_for('main'))
    else:
        return render_template('login.html', msg='Ungültige Eingabe')


@blu.route('/logout')
def logout():
    session['logged_in'] = False
    session['superuser'] = False
    return main()


@blu.route('/formular')
def formular_in():
    """ This function displays the input form.
        Either the fields in the form are empty, if a new entry is created
        or all entries which already have been saved for this foundation name
        appear in the according field in the form (they can be modified).
    """
    now = datetime.datetime.now()
    today = now.strftime("%d.%m.%y")
    if request.args.get('id'):
        get_id = request.args.get('id')
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM foundations WHERE id=?', (get_id,))
        items = cursor.fetchone()
        return render_template('formular_in.html', blubber=items, mode='edit', today=today)
    else:
        return render_template('formular_in.html', blubber={}, mode='new', today=today)



@blu.route('/formularadd', methods=['POST'])
def formular_add():
    """ Add a new entry to the database
        If the input comes from an 'edit', the old values which are stored
        in the database entry will be replaced by the new ones.
        If the input is a 'new' one, check if there already exists an entry
        in the db for the proposed foundation name.
        If yes, an error will appear. If not, add the entry to the db.
    """
        
    conn = get_db()
    cursor = conn.cursor()
    mode = request.form["mode"]
    name = request.form["name"]
    adress = request.form["adress"]
    phone = request.form["phone"]
    mail = request.form["mail"]
    website = request.form["website"]
    contact_person = request.form["contactperson"]
    zweck = request.form["zweck"]
    money = request.form["money"]
    currency = request.form["currency"]
    deadline1 = request.form["deadline1"]
    deadline2 = request.form["deadline2"]
    deadline = ''
    if deadline1 and deadline2:
        deadline = ''.join(deadline1) + ' / ' + ''.join(deadline2)
    elif deadline1:
        deadline = deadline1
    elif deadline2:
        deadline = deadline2

    pending = request.form.get("pending")
    no_info = request.form.get("noInfo")
    if (deadline and pending) or (deadline and no_info) or (pending and no_info):
        return render_template('error2.html')

    variabel = request.form.get("variabel")
    fix = request.form.get("fix")
    if variabel and fix:
        return render_template('error3.html')

    cond_else = request.form["condElse"]
    res_contact = request.form["resContact"]
    notes = request.form["notes"]
    time_contact = request.form["timeContact"]
    last_change = request.form["lastChange"]

    kind_of_boost = request.form.getlist("kindOfBoost")
    kind_of_boost = handle_checkboxes(kind_of_boost)
    broadness = request.form.getlist("broadness")
    broadness = handle_checkboxes(broadness)
    acad_degree = request.form.getlist("acadDegree")
    acad_degree = handle_checkboxes(acad_degree)
    sondierung = request.form.get("sondierung")

    array = [name, adress, phone, mail, website, contact_person,
             zweck, kind_of_boost, money, currency, broadness, acad_degree,
             cond_else, deadline, variabel, fix, pending, no_info, res_contact,
             notes, time_contact, last_change, 0, sondierung]

    if mode == 'new':
        cursor.execute("""SELECT foundationname FROM foundations WHERE
                          foundationname LIKE ?""", (name,))
        exists = cursor.fetchone()
        if exists:
            return render_template('error.html')
        else:
            new_foundation(conn, array)
            return redirect(url_for('main'))
    else:
        cursor.execute("""SELECT ID FROM foundations WHERE
                          foundationname LIKE ?""", (name,))
        fetch_id = cursor.fetchone()
        array.append(fetch_id[0])
        print(array)
        edit_foundation(conn, array)
        return redirect(url_for('main'))

@blu.route('/delete')
def delete():
    """ Delete entry from table
    """
    conn, cursor = init_db()
    get_id = request.args.get('id')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE foundations SET deleted=1 WHERE id=?', (get_id,))
    conn.commit()
    return redirect(url_for('main'))


@blu.route('/permanent_delete')
def p_delete():
    """ Delete entry from table
    """
    conn, cursor = init_db()
    get_id = request.args.get('id')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM foundations WHERE id=?', (get_id,))
    conn.commit()
    return render_template(url_for('main'))


@blu.route('/infos')
def information():
    """ Display information site """
    return render_template('information.html')


@blu.route('/search')
def show_search():
    """ Render the form to search for entries in the db """
    return render_template('formular_search.html')


@blu.route('/results', methods=['POST'])
def do_search():
    """ Take input from the search form
        Check for matching entries in the db (find_entries)
        and display the result (make_nice_display)
    """
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT * FROM foundations')
    items = cursor.fetchall()

    # kind_of_boost = request.form.getlist("kindOfBoost")
    # kind_of_boost = handle_checkboxes(kind_of_boost)
    broadness = request.form.getlist("broadness")
    broadness = handle_checkboxes(broadness)
    sondierung = request.form.getlist("sondierung")
    sondierung = handle_checkboxes(sondierung)

    if '/' in sondierung:
        return render_template('error4.html')

    # acad_degree = request.form.getlist("acadDegree")
    # acad_degree = handle_checkboxes(acad_degree)
    # search_array = [kind_of_boost, broadness, acad_degree]

    search_array = [broadness, sondierung]

    indices = find_entries(items, search_array)
    print(indices)
    # indices = []
    items = []
    for i in range(0, len(indices)):
        cursor = conn.execute("""SELECT id, foundationname, deadline, variabel,
                                 fix, pending, noInfo FROM foundations
                                 WHERE id LIKE ?""", (indices[i],))
        get_ind = cursor.fetchall()
        items.append(get_ind[0])

    # items = sort_by_date(items)
    # for item in items:
    #     print(item['id'])
    return render_template('results.html', items=items, n_res=len(indices))

@blu.route('/show_card')
def show_card():
    """ Show the detailed information for one foundation
    """

    get_id = request.args.get('id')
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT * FROM foundations where id=?', (get_id,))
    item = cursor.fetchone()
    display = make_nice_display([item])
    return render_template('single_result.html', item=item, display=display[0])