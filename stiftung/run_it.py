import datetime
import sqlite3
from flask import Flask, request, redirect, url_for, render_template
from database import create_connection, new_foundation, \
     handle_checkboxes, edit_foundation, unique_check, make_nice_display, \
     find_entries

blu = Flask(__name__)
blu.debug = True
database = 'stiftung/foundations.db'


def get_db():
    datab = create_connection(database)
    return datab


def init_db():
    conn = get_db()
    with blu.open_resource('schema.sql', mode='r') as f:
        cursor = conn.cursor()
        cursor.executescript(f.read())
    return conn, cursor


@blu.route('/')
def main():
    #return render_template('index.html')
    #query ganzi db (limit 20)
    conn, cursor = init_db()
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT ID, foundationname FROM foundations')
    items = cursor.fetchall()
    return render_template('index.html', items=items)


@blu.route('/formular')
def formular_in():
    now = datetime.datetime.now()
    today = now.strftime("%d.%m.%y")
    if request.args.get('id'):
        get_id = request.args.get('id')
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM foundations where id=?', get_id)
        items = cursor.fetchone()
        return render_template('formular_in.html', blubber=items, mode='edit', today=today)
    else:
        return render_template('formular_in.html', blubber={}, mode='new', today=today)



@blu.route('/formularadd', methods=['POST'])
def formular_add():
    conn = get_db()
    cursor = conn.cursor()

    mode = request.form["mode"]
    name = request.form["name"]
    keyword = request.form["keyword"]
    adress = request.form["adress"]
    phone = request.form["phone"]
    mail = request.form["mail"]
    website = request.form["website"]
    contact_person = request.form["contactperson"]
    zweck = request.form["zweck"]
    money = request.form["money"]
    currency = request.form["currency"]
    condition_age = request.form["conditionAge"]
    deadline = request.form["deadline"]
    res_contact = request.form["resContact"]
    time_contact = request.form["timeContact"]
    last_change = request.form["lastChange"]

    kind_of_boost = request.form.getlist("kindOfBoost")
    kind_of_boost = handle_checkboxes(kind_of_boost)
    hitword = request.form.getlist("hitword")
    hitword = handle_checkboxes(hitword)
    groups = request.form.getlist("groups")
    groups = handle_checkboxes(groups)
    broadness = request.form.getlist("broadness")
    broadness = handle_checkboxes(broadness)
    conditions_d = request.form.getlist("conditionsD")
    conditions_d = handle_checkboxes(conditions_d)
    conditions_s = request.form.getlist("conditionsS")
    conditions_s = handle_checkboxes(conditions_s)
    conditions_e = request.form.getlist("conditionsE")
    conditions_e = handle_checkboxes(conditions_e)

    pending = request.form.get("pending")
    no_info = request.form.get("noInfo")

    array = [name, keyword, adress, phone, mail, website, contact_person, zweck,
             kind_of_boost, money, currency, hitword, groups, broadness, conditions_d,
             conditions_s, conditions_e, condition_age, deadline, pending, no_info,
             res_contact, time_contact, last_change]

    unique = unique_check(deadline, pending, no_info)
    if unique == 1:
        return render_template('error2.html')
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
        cursor.execute("SELECT ID FROM foundations WHERE foundationname LIKE ?", (name,))
        fetch_id = cursor.fetchone()
        array.append(fetch_id[0])
        edit_foundation(conn, array)
        return redirect(url_for('main'))


@blu.route('/showsearch')
def show_search():
    return render_template('formular_search.html')


@blu.route('/dosearch', methods=['POST'])
def do_search():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT * FROM foundations')
    items = cursor.fetchall()

    kind_of_boost = request.form.getlist("kindOfBoost")
    kind_of_boost = handle_checkboxes(kind_of_boost)
    groups = request.form.getlist("groups")
    groups = handle_checkboxes(groups)
    broadness = request.form.getlist("broadness")
    broadness = handle_checkboxes(broadness)
    conditions_d = request.form.getlist("conditionsD")
    conditions_d = handle_checkboxes(conditions_d)
    conditions_s = request.form.getlist("conditionsS")
    conditions_s = handle_checkboxes(conditions_s)
    conditions_e = request.form.getlist("conditionsE")
    conditions_e = handle_checkboxes(conditions_e)
    condition_age = request.form["conditionAge"]
    search_array = [kind_of_boost, groups, broadness, conditions_d,
                    conditions_s, conditions_e, condition_age]

    indices = find_entries(items, search_array)
    items = []
    for i in range(0, len(indices)):
        cursor = conn.execute('SELECT * FROM foundations WHERE id=?', (indices[i],))
        get_ind = cursor.fetchall()
        items.append(get_ind[0])

    displays = make_nice_display(items)
    return render_template('results.html', items=items, displays=displays)
