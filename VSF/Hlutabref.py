#importa allt sem ég nota úr bottle
#  þurfum að setja pymysql upp í pyCharm (sama rútína og bottle-beaker)
import pymysql
from bottle import *
import datetime
from Classes import *

#bý til index sem skilar síðu þar sem hægt er að skrá sig inn / skrá nýjan user
@route('/')
def index():
    if request.get_cookie("login") and request.get_cookie("password"):
        #opna tengingu við sql database
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                               db='1503953219_lokaverkefni_3_onn')
        cur = conn.cursor()
        #næ í allt úr userbasebase
        cur.execute("SELECT * FROM user_info")
        #athuga hverja línu hvort username og password passi með for loop
        for row in cur:
            #athuga hverja línu hvort username og password passi
            if row[0]==request.get_cookie("login") and request.get_cookie("password")==row[1]:
                #loka öllu
                cur.close()
                conn.close()
                #birti síða þar sem notanda tókst að logga inn
                redirect('/stocks')
    else:
        return template('index.tpl')


#bý til route fyrir nýja notendur, hvort sem þeim tókst að búa til nýjan user eða ekki
@route('/newuser',method='POST')
def newuser():
    #opna connection í sql database
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    #næ í gildi fyrir nýjan user
    newuser=request.forms.get('newuser')
    newpass=request.forms.get('newpass')
    #sql query sem er count fyrir hversu oft newuser kemur fyrir
    #nota það query í raun til að vita hvort user er þegar til eða ekki
    cur.execute("SELECT count(*) FROM user_info where username='{}'".format(newuser))
    #næ í þessa einu línu
    user = cur.fetchone()
    #user er lína úr database, athuga fyrsta stak sem er username stakið hvort það er til eða ekki
    #username stakið er = 1 ef newuser er þegar til því ég bað um count(*) í query
    if user[0] <= 1:
        #loka öllu
        cur.close()
        conn.close()
        #birti síðu
        return template('newuserno.tpl')
    #ef user er ekki til þá bý ég hann til
    else:
        #bæti við nýjum user í database
        cur.execute("INSERT INTO User(bot) Values('{}'".format(1))
        cur.execute("SELECT MAX(UserID) FROM user")
        currentid = cur.fetchone()
        cur.execute("INSERT INTO User_info Values('{}','{}','{}')".format(currentid,newuser,newpass))
        conn.commit()
        #loka öllu
        cur.close()
        conn.close()
        #birti síðu
        return template('newuseryes.tpl')


#bý til login síðu fyrir notendur, hvort sem þeim tókst að loga inn eða ekki
@route('/login',method='POST')
def login():
    #opna tengingu við sql database
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    #sæki upplýsingar
    username=request.forms.get('username')
    password=request.forms.get('password')
    if username=="admin" and password=="tskoli123":
        redirect('/admin')
    #næ í allt úr database
    cur.execute("SELECT * FROM user_info")
    #athuga hverja línu hvort username og password passi með for loop
    for row in cur:
        #athuga hverja línu hvort username og password passi
        if row[0]==username and row[1]==password:
            #loka öllu
            cur.close()
            conn.close()
            #bý til tímabil fyrir cookies
            timabil=datetime.datetime.now() + datetime.timedelta(days=30)
            #set cookies fyrir login info
            response.set_cookie("login",row[0],expires=timabil)
            response.set_cookie("password",row[1],expires=timabil)
            cur.execute("SELECT UserID FROM User_info WHERE Username =  {}").format(row[0])
            userid=cur.fetchone()
            response.set_cookie("UserID",userid,expires=timabil)
            #birti síða þar sem notanda tókst að logga inn
            redirect('/stocks')
    #ef að return var ekki gefið í for loop þá þýðir það að við erum komnir hingað
    #þá loka ég öllu og birti síðu sem segir notanda að honum tókst ekki að logga inn
    cur.close()
    conn.close()
    redirect('/stocks')


@route('/logout')
#eyðir innskráningar cookie og fer með þig aftur á upphafsíðu
def logout():
    # Að eyða cookie, yfirskrifum gildið í gildi núll og stillum tíma á 0 svo hún rennur út strax.
    response.set_cookie("login", "", expires=0)
    response.set_cookie("password","",expires=0)
    response.set_cookie("UserID","",expires=0)
    redirect('/')


@route('/stocks')
def stocks():
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    cur.execute("SELECT * FROM stock")
    stocklisti=[]
    for row in cur:
        stocklisti.append(row)
    cur.execute("SELECT count(*) FROM stock")
    stockfj=cur.fetchone()
    return template('stocks.tpl',stocklisti=stocklisti,stockfj=stockfj)


@route('/admin')
def admin():
    return template('admin.tpl')
@route('/bots')
def bots():
    #opna tengingu við sql database
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    cur.execute("SELECT MAX(UserID) FROM user")
    nr = cur.fetchone()[0] + 1
    botsfj=request.forms.get('botsfj')
    upperrisk=request.forms.get('upperrisk')
    lowerrisk=request.forms.get('lowerrisk')
    buyrisk=request.forms.get('buyrisk')
    print(upperrisk, lowerrisk, buyrisk)
    for x in range(botsfj):
        y=Bots(nr, upperrisk,lowerrisk, buyrisk)
        y.newbot()

run()
