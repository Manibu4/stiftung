""" This file contains all helper functions for the interaction with the db """

import sqlite3

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = sqlite3.connect(db_file)
    return conn


def new_foundation(conn, values):
    """ Creates a new database entry for a foundation """
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO foundations VALUES
    (NULL, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?)""", values)
    conn.commit()


def edit_foundation(conn, values):
    """ Creates a new database entry for a foundation """
    cursor = conn.cursor()
    cursor.execute("""UPDATE foundations SET foundationname=?, keyword=?,
      address=?, pnumber=?, mail=?, website=?, contactperson=?, purpose=?,
      kindofboost=?, sum=?, currency=?, hitword=?, groups=?, broadness=?,
      condDoc=?, condSci=?, condElse=?, condAge=?, condEText=?, deadline=?,
      pending=?, noInfo=?, resContact=?, timeContact=?, lastChange=? WHERE id=?""", \
      (values[0], values[1], values[2], values[3], values[4], values[5], \
       values[6], values[7], values[8], values[9], values[10], values[11], \
       values[12], values[13], values[14], values[15], values[16], values[17], \
       values[18], values[19], values[20], values[21], values[22], values[23], \
       values[24], values[25],))
    conn.commit()


def handle_checkboxes(box_values):
    """ This function takes in an array of values for checked checkboxes,
        rearranges them into a string of the form array[0];array[1];...;array[end]
        and returns this string
    """
    box_joint_vals = ''
    if len(box_values) > 1:
        for i in range(0, len(box_values)-1):
            box_joint_vals = box_joint_vals + ''.join(box_values[i]) + ' / '

        box_joint_vals = box_joint_vals + ''.join(box_values[-1])
    else:
        box_joint_vals = box_joint_vals + ''.join(box_values)

    return box_joint_vals


def unique_check(deadline, pending, no_info):
    """ This function checks whether more than one of the following fields
        'a date', 'pending' or 'no information'
        have been selected in the form.
        If yes, an error message is displayed as choosing more than one
        option is not considered valid.
    """
    if (deadline and pending) or (deadline and no_info) or (pending and no_info):
        return 1
    else:
        return 0


def make_nice_display(text_in):
    """ This function takes in an array of strings and rearranges
        them into a form which is nicely displayable in a table
    """
    display = []
    if text_in:
        for i in range(0, len(text_in)):
            cont = {}
            # unklar ob das do no witer nötig isch...
            # cont["kindofboost"] = text_in[i]["kindofboost"].split("/")
            # cont["hitword"] = text_in[i]["hitword"].split("/")
            # cont["groups"] = text_in[i]["groups"].split("/")
            # cont["condDoc"] = text_in[i]["condDoc"].split("/")
            # cont["condSci"] = text_in[i]["condSci"].split("/")
            # cont["condElse"] = text_in[i]["condElse"].split("/")
            # if text_in[i]["deadline"]:
                # cont["frist"] = text_in[i]["deadline"].split("/")
            # elif text_in[i]["pending"]:
                # cont["frist"] = text_in[i]["pending"].split("/")
            # elif text_in[i]["noInfo"]:
                # cont["frist"] = text_in[i]["noInfo"].split("/")
            # else:
                # cont["frist"] = ''

            # if text_in[i]["condEText"]:
                # cont["condEText"] = text_in[i]["condEText"].split("/")
            # else:
                # cont["condEText"] = ''
            cont["broadness"] = text_in[i]["broadness"].split(" / ")
            display.append(cont)

    return display


def find_entries(flist, array_search):
    """ This function takes in
        - 'array_search', containing the data which the user has
          selected in the search form
        - flist: array containing all rows of the database for comparison

        It checks if array_search is a subset (except if the field in flist
        is empty) of any of the rows in the db and with an empty set in
        array_search always being a subset.
        The condition on the maximal age is, of course, considered accordingly.
    """
    array = []
    array0 = array_search[0].split(" / ")
    array1 = array_search[1].split(" / ")
    array2 = array_search[2].split(" / ")
    array3 = array_search[3].split(" / ")
    array4 = array_search[4].split(" / ")
    array5 = array_search[5].split(" / ")
    array6 = array_search[6]

    for one_item in flist:
        zero = one_item["kindofboost"].split(" / ")
        one = one_item["groups"].split(" / ")
        two = one_item["broadness"].split(" / ")
        three = one_item["condDoc"].split(" / ")
        four = one_item["condSci"].split(" / ")
        five = one_item["condElse"].split(" / ")
        six = one_item["condAge"]

        if ((array0 == [''] or zero == [''] or (str('Keine Angabe') in zero)
             or set(array0) <= set(zero)) and
                (array1 == [''] or one == [''] or set(array1) <= set(one)) and
                (array2 == [''] or two == [''] or set(array2) <= set(two)) and
                (array3 == [''] or three == [''] or set(array3) <= set(three)) and
                (array4 == [''] or four == [''] or set(array4) <= set(four)) and
                (array5 == [''] or five == [''] or set(array5) <= set(five)) and
                (array6 == '' or six == '' or int(array6) <= int(six))):
            array.append(int(one_item["id"]))

    return array
