from flask import *
import mysql.connector

app = Flask(__name__)
app.secret_key = '1581'

# FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC FUNC 

@app.before_request
def connection():
    con = mysql.connector.connect(
        host = '92.53.96.11',
        database = 'sch688_etobaza',
        user = 'sch688_etobaza',
        password = 'Qwerty123')
    g.conn = con

    
@app.teardown_request
def close_connection(er):
    g.conn.close()

    
def getUserByLogin(login):
    cursor = g.conn.cursor()
    cursor.execute("SELECT * FROM users WHERE sUserLogin = %s",(login,)) 
    data = cursor.fetchall()
    return {'user':data}

def addUser(user):
    cursor = g.conn.cursor()
    cursor.execute('INSERT INTO `users`(`sUserName`, `sUserLogin`, `sUserPassword`, `sUserPhone`, `sUserMail`, `sUserSurname`, `sUserStatus`) VALUES (%s, %s, %s, %s, %s, %s, %s)',(user['name'], user['login'], user['password'], user['phone'], user['mail'], user['surname'],0))
    g.conn.commit()
    data = cursor.lastrowid
    return {'lastid':data}


# ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTEROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE ROUTE
@app.route("/")
def registration():
    return render_template('main.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/cart")
def cart():
    return render_template('cart.html')

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')

@app.route("/adminadd")
def adminadd():
    if session:
        if session['status'] == 1:
            return render_template('adminadd.html', session = session)
        else:
            return render_template('403.html')
    else:
        return render_template('403.html')

@app.route("/ajax/registration", methods = ["POST"])
def ajax_rega():
    req = request.get_json()
    user = getUserByLogin(req['login'])
    if user['user']:
        user['error'] = 'Вас двое'
        user['result'] = False
        return jsonify(user)
    user = addUser(req)
    user ['result'] = True
    return jsonify(user)

@app.route("/ajax/login", methods = ["POST"])
def ajax_loga():
    req = request.get_json()
    user = getUserByLogin(req['login'])
    
    if not user['user']:
        user['error'] = 'Пользователь с таким логином или паролем не найден'
        user['result'] = False
        return jsonify(user)
    if req['password'] == user['user'][0][4]:
        user['result'] = True
        session['id'] = user['user'][0][0]
        session['name'] = user['user'][0][1]
        session['surname'] = user['user'][0][2]
        return jsonify(user)

    user['error'] = 'Пользователь с таким логином или паролем не найден'
    user['result'] = False
    return jsonify(user)

@app.route("/mainpage")
def mainpage():
    if session:
        return render_template('mainpage.html', session = session)
    else:
        return render_template('403.html')

if __name__ == '__main__':
    app.run(debug=True,port=8000)

