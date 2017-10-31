
# A very simple Bottle Hello World app for you to get started with...
import bottle
from bottle import default_app, route, template, request, error
from beaker.middleware import SessionMiddleware
import sqlite3
import requests

session_opts={
    'session.type':'memory',
    'session.cookie_expires':400,
}

@error(404)
def error404(error):
    return "<p>404 - Page not found</p>"

@route('/')
def hello_world():
    return template("/home/berlinab/mysite/index")

@route('/issn')
def modulus_assignment():
    return template("/home/berlinab/mysite/issn")

@route('/',method="POST")
def signin():
    email=request.forms.get("email")
    password=request.forms.get("password")
    connection=sqlite3.connect("/home/berlinab/mysite/users.db")
    c=connection.cursor()
    c.execute("SELECT * from account WHERE userEmail=? AND userPassword=?",(email,password))
    row=c.fetchone()
    if row == None:
        return "<p>User not found</p>"
    else:
        cookie=bottle.request.environ.get('beaker.session')
        cookie['logged_in']=1
        cookie.save()
        return bottle.redirect("/admin")

@route('/admin')
def apanel():
    cookie=bottle.request.environ.get('beaker.session')
    if 'logged_in' in cookie:
        return '''
        <p>You are logged in. You are in the VIP/admin page. Check your cookies!</p>
        <p><a href="http://berlinab.pythonanywhere.com">Click here to go to main page</a></p>
        <a href="/logout"> Logout</a>
        '''
    else:
        return bottle.redirect('/')

@route('/logout')
def logout():
    cookie=bottle.request.environ.get('beaker session')
    cookie.delete()
    return '''
    <meta http-equiv="refresh" content="2; url=/">
    <p>You are logged out. Redirecting ...</p>
    '''

@route('/signin')
def sign_in_display():
    return template("/home/berlinab/mysite/signin")

@route('/signup')
def sign_up_display():
    return template("/home/berlinab/mysite/signup")

@route('/signup', method="POST")
def sign_up_process():
    email=request.forms.get("email")
    password1=request.forms.get("password")
    password2=request.forms.get("password2")
    if password1 != password2:
        return "<p>password do not match</p>"
    else:
        connection=sqlite3.connect("/home/berlinab/mysite/users.db")
        c=connection.cursor()
        c.execute("insert into account (userEmail, userPassword) values (?,?)", (email,password1))
        connection.commit()
        c.close()
        return "<p>You've been signed up</p>"

@route('/modulus', method="POST")
def modulus_assignment():
    num = request.forms.get("issn_num")
    weight = 8
    total = 0
    if len(num)<7 or len(num)>7:
        final_issn = "Length of string is invalid"
        return template("/home/berlinab/mysite/modulus", final_issn = final_issn)
    else:
        for x in num:
            running_total = int(x) * weight
            weight -= 1
            total = running_total + total
            modulus=total%11
            remainder=11-modulus
            final_issn = str(num)+str(remainder)
            return template("/home/berlinab/mysite/modulus", final_issn = final_issn)


@route('/contact', method='POST')
def submitr():
    subject = "Comment"
    item1 =  request.forms.get('name')
    item2 =  request.forms.get('email')
    item3 =  request.forms.get('comment')
    text = str(item1) + " " + str(item2) + " " + str(item3)
    requests.post("https://api.mailgun.net/v3/sandbox92b6c85a89974c7380478939171df4ea.mailgun.org/messages",
    auth=("api", "key-03e2b73105e6602305dc18d34cb19e5c"),
    data={"from": "Mailgun Sandbox <postmaster@sandbox92b6c85a89974c7380478939171df4ea.mailgun.org>",
        "to": "End Police Brutality <standupall2@gmail.com>",
        "subject": subject,
        "html": text})
    return '''
    <meta http-equiv="refresh" content="4; url=/">
    <p>Received - Thank you! Redirecting ...</p>
    '''

@route('/post',method="POST")
def show_it():
    connection=sqlite3.connect("/home/berlinab/mysite/users.db")
    c=connection.cursor()
    c.execute("SELECT * from account")
    row=c.fetchall()
    return template("/home/berlinab/mysite/post", row=row)

#application = default_app()
application=SessionMiddleware(bottle.default_app(), session_opts)
