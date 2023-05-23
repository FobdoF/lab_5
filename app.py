from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="K89164466539k!",
                        host="localhost",
                        port="5432")

cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if not username:
                return render_template('login.html', error="Введите логин")
            if not password:
                return render_template('login.html', error="Введите пароль")
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())

            return render_template('account.html', full_name=records[0][1], username=records[0][2], password=records[0][3])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        if not name:
            return render_template('registration.html', error="Введите имя")
        if not password:
            return render_template('registration.html', error="Введите пароль")
        if not login:
            return render_template('registration.html', error="Введите логин")

        try:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))
            conn.commit()
            return redirect('/login/')
        except:
            conn.commit()
            return render_template('registration.html', error="Пользователь существует")




    return render_template('registration.html')
