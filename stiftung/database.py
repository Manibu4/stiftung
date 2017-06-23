import logging
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    logging.debug('Opening connection to db')
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
    return conn


def search_db(cursor, input_params, input_values):
    """ Searches through DB based on the inputs """
    return results


def new_foundation(conn, values):
    """ Creates a new database entry for a foundation """
    cursor = conn.cursor()
    cursor.execute("SELECT foundationname FROM foundations WHERE foundationname LIKE ?", (values[0],))
    exists = cursor.fetchone()

    if exists:
        print("Entry for this foundation already exists")
    else:
        cursor.execute("INSERT INTO foundations VALUES (NULL, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?,?,?)", values)
        conn.commit()


def edit_foundation(conn, values):
    """ Creates a new database entry for a foundation """
    cursor = conn.cursor()
    cursor.execute("UPDATE foundations SET foundationname=? WHERE id=?", (values[0], values[24],))
    cursor.execute("UPDATE foundations SET keyword=? WHERE id=?", (values[1], values[24],))
    cursor.execute("UPDATE foundations SET address=? WHERE id=?", (values[2], values[24],))
    cursor.execute("UPDATE foundations SET pnumber=? WHERE id=?", (values[3], values[24],))
    cursor.execute("UPDATE foundations SET mail=? WHERE id=?", (values[4], values[24],))
    cursor.execute("UPDATE foundations SET website=? WHERE id=?", (values[5], values[24],))
    cursor.execute("UPDATE foundations SET contactperson=? WHERE id=?", (values[6], values[24],))
    cursor.execute("UPDATE foundations SET purpose=? WHERE id=?", (values[7], values[24],))
    cursor.execute("UPDATE foundations SET kindofboost=? WHERE id=?", (values[8], values[24],))
    cursor.execute("UPDATE foundations SET sum=? WHERE id=?", (values[9], values[24],))
    cursor.execute("UPDATE foundations SET currency=? WHERE id=?", (values[10], values[24],))
    cursor.execute("UPDATE foundations SET hitword=? WHERE id=?", (values[11], values[24],))
    cursor.execute("UPDATE foundations SET groups=? WHERE id=?", (values[12], values[24],))
    cursor.execute("UPDATE foundations SET broadness=? WHERE id=?", (values[13], values[24],))
    cursor.execute("UPDATE foundations SET condDoc=? WHERE id=?", (values[14], values[24],))
    cursor.execute("UPDATE foundations SET condSci=? WHERE id=?", (values[15], values[24],))
    cursor.execute("UPDATE foundations SET condElse=? WHERE id=?", (values[16], values[24],))
    cursor.execute("UPDATE foundations SET condAge=? WHERE id=?", (values[17], values[24],))
    cursor.execute("UPDATE foundations SET deadline=? WHERE id=?", (values[18], values[24],))
    cursor.execute("UPDATE foundations SET pending=? WHERE id=?", (values[19], values[24],))
    cursor.execute("UPDATE foundations SET noInfo=? WHERE id=?", (values[20], values[24],))
    cursor.execute("UPDATE foundations SET resContact=? WHERE id=?", (values[21], values[24],))
    cursor.execute("UPDATE foundations SET timeContact=? WHERE id=?", (values[22], values[24],))
    cursor.execute("UPDATE foundations SET lastChange=? WHERE id=?", (values[23], values[24],))
    conn.commit()


def handle_checkboxes(box_values):
    box_joint_vals = ''
    if len(box_values)>1:
        for i in range(0, len(box_values)-1):
            box_joint_vals = box_joint_vals + ''.join(box_values[i])+';'

        box_joint_vals = box_joint_vals + ''.join(box_values[-1])
    else:
        box_joint_vals = box_joint_vals + ''.join(box_values)

    return box_joint_vals


def unique_check(dl, pd, ni):
    if (dl != '' and pd == 'pending'):
        print('Fall1')
        print(dl)
        print(pd)
        return 1
    elif (dl != '' and ni == 'noInfo'):
        print('Fall2')
        print(dl)
        print(ni)
        return 1
    elif (pd == 'pending' and ni == 'noInfo'):
        print('Fall3')
        print(pd)
        print(ni)
        return 1
    else:
        return 0


def make_nice_display(text_in):
    display = []
    if len(text_in) > 0:
        for i in range(0,len(text_in)):
            cont = {}
            cont["kindofboost"] = text_in[i]["kindofboost"].split(";")
            cont["hitword"] = text_in[i]["hitword"].split(";")
            cont["groups"] = text_in[i]["groups"].split(";")
            cont["broadness"] = text_in[i]["broadness"].split(";")
            cont["condDoc"] = text_in[i]["condDoc"].split(";")
            cont["condSci"] = text_in[i]["condSci"].split(";")
            cont["condElse"] = text_in[i]["condElse"].split(";")
            if text_in[i]["deadline"]:
                cont["frist"] = text_in[i]["deadline"].split(";")
            elif text_in[i]["pending"]:
                cont["frist"] = text_in[i]["pending"].split(";")
            elif text_in[i]["noInfo"]:
                cont["frist"] = text_in[i]["noInfo"].split(";")
            else:
                cont["frist"] = ''

            display.append(cont)

    return display


def find_entries(flist, array_search):
    array = []
    array0 = array_search[0].split(";")
    array1 = array_search[1].split(";")
    array2 = array_search[2].split(";")
    array3 = array_search[3].split(";")
    array4 = array_search[4].split(";")
    array5 = array_search[5].split(";")
    for i in range(0, len(flist)):
        blu = flist[i]
        ctr = 0
        if (blu["condAge"] and array_search[6]):
            for j in range(0, len(array0)):
                if array0[j] in blu["kindofboost"]:
                    ctr += 1
            for j in range(0, len(array1)):
                if array1[j] in blu["groups"]:
                    ctr += 1
            for j in range(0, len(array2)):
                if array2[j] in blu["broadness"]:
                    ctr += 1
            for j in range(0, len(array3)):
                if array3[j] in blu["condDoc"]:
                    ctr += 1
            for j in range(0, len(array4)):
                if array4[j] in blu["condSci"]:
                    ctr += 1
            for j in range(0, len(array5)):
                if array5[j] in blu["condElse"]:
                    ctr += 1
            if (ctr == (len(array0) + len(array1) + len(array2) +
                        len(array3) + len(array4) + len(array5)) and
                        int(array_search[6]) <= int(blu["condAge"]) ):
                array.append(int(blu["id"]))
        else:
            for j in range(0, len(array0)):
                if array0[j] in blu["kindofboost"]:
                    ctr += 1
            for j in range(0, len(array1)):
                if array1[j] in blu["groups"]:
                    ctr += 1
            for j in range(0, len(array2)):
                if array2[j] in blu["broadness"]:
                    ctr += 1
            for j in range(0, len(array3)):
                if array3[j] in blu["condDoc"]:
                    ctr += 1
            for j in range(0, len(array4)):
                if array4[j] in blu["condSci"]:
                    ctr += 1
            for j in range(0, len(array5)):
                if array5[j] in blu["condElse"]:
                    ctr += 1
            if (ctr == (len(array0) + len(array1) + len(array2) +
                        len(array3) + len(array4) + len(array5)) ):
                array.append(int(blu["id"]))

    return array
