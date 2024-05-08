from flask import Flask, render_template, request, redirect, url_for
import sqlite3

def sql():
    con = sqlite3.connect("doctor_reservation.db")
    cur = con.cursor()
    cur.execute("create table if not exists doctors(name text, patient text, contact integer,hospital text, slot integer)")
    cur.execute("create table if not exists doctors_available(name text, spec text, hospital text)")
    return con


app = Flask(__name__)

@app.route('/')
def main():
    con = sql()
    row = con.execute("select * from doctors").fetchall()
    drow = con.execute("select * from doctors_available").fetchall()
    con.close()
    return render_template("d_index.html", booked_doc=row, doctors=drow)

@app.route('/book_doc', methods=('GET', 'POST'))
def book_doc():
    con = sql()
    if request.method == "POST":
        pname = request.form['pname']
        contact = request.form['contact']
        doc = request.form['docs']
        print(doc)
        slot = request.form['slot']
        r = con.execute('select * from doctors_available where name=(?)', (doc,)).fetchone()
        print(r)
        con.execute('insert into doctors values(?,?,?,?,?)', (doc, pname, contact, r[2], slot))
        con.commit()
        con.close()
    return redirect(url_for('main'))


@app.route('/add_doc', methods=('GET', 'POST'))
def add_doc():
    con = sql()
    if request.method == "POST":
        dname = request.form['dname']
        spec = request.form['spec']
        hname = request.form['hname']
        con.execute("insert into doctors_available values(?,?,?)", (dname, spec, hname))
        con.commit()
        con.close()
    return redirect(url_for('main'))

if __name__ == '__main__':
    app.run(debug=True)