import requests
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
conn = psycopg2.connect(database="service_db", user="postgres", password="Ermollaef32", host="localhost", port="5432")
cursor = conn.cursor()
cursor2 = cursor


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username') 
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        kirill = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        for i in name + login + password: 
            if i in kirill: return render_template('fail.html', full_name = 'данные не могут содержать кириллицу')
        for i in  login + password: 
            if i == " ": return render_template('fail.html', full_name = 'login и password не могут содержать пробелы')
        if len(name) == 0 or len(login) == 0 or len(password) == 0: return render_template('fail.html', full_name = 'вы должны заполнить все поля регистрации')
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES(%s, %s, %s);',(str(name), str(login), str(password)))
        conn.commit()
        return redirect('/login/')
    return render_template('registration.html')


if __name__ == "__main__":
    app.run()
