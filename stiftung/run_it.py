import os
import datetime
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from stiftung.database import create_connection, new_foundation, search_db, \
     handle_checkboxes, edit_foundation, unique_check, make_nice_display, \
     find_entries

blu = Flask(__name__)
blu.debug = True
database = 'stiftung/database/foundations.db'


def get_db():
    db = create_connection(database)
    return db


def init_db():
    conn = get_db()
    with blu.open_resource('schema.sql', mode='r') as f:
        cursor = conn.cursor()
        cursor.executescript(f.read())
    return conn, cursor


@blu.route('/')
def main(methods = ['GET', 'POST']):
    #return render_template('index.html')
    #query ganzi db (limit 20)
    conn, cursor = init_db()
    conn = get_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute('SELECT ID, foundationname FROM foundations')
    items=cursor.fetchall()
    return render_template('index.html', items=items)


@blu.route('/formular')
def formular_in():
    now = datetime.datetime.now()
    today = now.strftime("%d.%m.%y")
    if request.args.get('id'):
        blu = request.args.get('id')
        conn = get_db()
        conn.row_factory = sqlite3.Row
        cursor = conn.execute('SELECT * FROM foundations where id=?', blu)
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
    contactPerson = request.form["contactperson"]
    zweck = request.form["zweck"]
    money = request.form["money"]
    currency = request.form["currency"]
    conditionAge = request.form["conditionAge"]
    deadline = request.form["deadline"]
    resContact = request.form["resContact"]
    timeContact = request.form["timeContact"]
    lastChange = request.form["lastChange"]

    kindOfBoost = request.form.getlist("kindOfBoost")
    kindOfBoost = handle_checkboxes(kindOfBoost)
    hitword = request.form.getlist("hitword")
    hitword = handle_checkboxes(hitword)
    groups = request.form.getlist("groups")
    groups = handle_checkboxes(groups)
    broadness = request.form.getlist("broadness")
    broadness = handle_checkboxes(broadness)
    conditionsD = request.form.getlist("conditionsD")
    conditionsD = handle_checkboxes(conditionsD)
    conditionsS = request.form.getlist("conditionsS")
    conditionsS = handle_checkboxes(conditionsS)
    conditionsE = request.form.getlist("conditionsE")
    conditionsE = handle_checkboxes(conditionsE)

    pending = request.form.get("pending")
    noInfo = request.form.get("noInfo")

    array = [name, keyword, adress, phone, mail, website, contactPerson, zweck,
    kindOfBoost, money, currency, hitword, groups, broadness, conditionsD,
    conditionsS, conditionsE, conditionAge, deadline, pending, noInfo,
    resContact, timeContact, lastChange]

    unique = unique_check(deadline, pending, noInfo)
    if unique == 1:
        return render_template('error2.html')
    if mode=='new':
        cursor.execute("SELECT foundationname FROM foundations WHERE foundationname LIKE ?", (name,))
        exists = cursor.fetchone()
        if exists:
            return render_template('error.html')
        else:
            new_foundation(conn, array)
            return redirect(url_for('main'))
    else:
        cursor.execute("SELECT ID FROM foundations WHERE foundationname LIKE ?", (name,))
        blu = cursor.fetchone()
        array.append(blu[0])
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

    kindOfBoost = request.form.getlist("kindOfBoost")
    kindOfBoost = handle_checkboxes(kindOfBoost)
    groups = request.form.getlist("groups")
    groups = handle_checkboxes(groups)
    broadness = request.form.getlist("broadness")
    broadness = handle_checkboxes(broadness)
    conditionsD = request.form.getlist("conditionsD")
    conditionsD = handle_checkboxes(conditionsD)
    conditionsS = request.form.getlist("conditionsS")
    conditionsS = handle_checkboxes(conditionsS)
    conditionsE = request.form.getlist("conditionsE")
    conditionsE = handle_checkboxes(conditionsE)
    conditionAge = request.form["conditionAge"]
    search_array = [kindOfBoost, groups, broadness, conditionsD,
                    conditionsS, conditionsE, conditionAge]

    indices = find_entries(items, search_array)
    print(indices)
    items = []
    for i in range(0, len(indices)):
        cursor = conn.execute('SELECT * FROM foundations WHERE id=?', (indices[i],))
        blu = cursor.fetchall()
        items.append(blu[0])

    displays = make_nice_display(items)
    return render_template('results.html', items=items, displays=displays)


if __name__ == "__main__":
    app.run()
