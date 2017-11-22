# þurfum að setja pymysql upp í pyCharm (sama rútína og bottle-beaker)
import pymysql
from bottle import *
#bý til index sem skilar síðu þar sem hægt er að skrá sig inn / skrá nýjan user
@route('/')
def index():
    if request.get_cookie("login") and request.get_cookie("password"):
        #opna tengingu við sql database
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='2601994049', passwd='mypassword',
                               db='2601994049_skilaverkefni10')
        cur = conn.cursor()
        #næ í allt úr userbasebase
        cur.execute("SELECT * FROM userbase")
        #athuga hverja línu hvort username og password passi með for loop
        for row in cur:
            #athuga hverja línu hvort username og password passi
            if row[0]==request.get_cookie("login") and request.get_cookie("password"):
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
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='2601994049', passwd='mypassword',
                           db='2601994049_skilaverkefni10')
    cur = conn.cursor()
    #næ í gildi fyrir nýjan user
    newuser=request.forms.get('newuser')
    newpass=request.forms.get('newpass')
    #sql query sem er count fyrir hversu oft newuser kemur fyrir
    #nota það query í raun til að vita hvort user er þegar til eða ekki
    cur.execute("SELECT count(*) FROM userbase where username='{}'".format(newuser))
    #næ í þessa einu línu
    user = cur.fetchone()
    #user er lína úr database, athuga fyrsta stak sem er username stakið hvort það er til eða ekki
    #username stakið er = 1 ef newuser er þegar til því ég bað um count(*) í query
    if user[0] == 1:
        #loka öllu
        cur.close()
        conn.close()
        #birti síðu
        return template('newuserno.tpl')
    #ef user er ekki til þá bý ég hann til
    else:
        #bæti við nýjum user í database
        cur.execute("INSERT INTO userbase Values('{}','{}')".format(newuser,newpass))
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
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='2601994049', passwd='mypassword',
                           db='2601994049_skilaverkefni10')
    cur = conn.cursor()
    #sæki upplýsingar
    username=request.forms.get('username')
    password=request.forms.get('password')
    #næ í allt úr database
    cur.execute("SELECT * FROM userbase")
    #athuga hverja línu hvort username og password passi með for loop
    for row in cur:
        #athuga hverja línu hvort username og password passi
        if row[0]==username and row[1]==password:
            #loka öllu
            cur.close()
            conn.close()
            response.set_cookie("login", row[0])
            response.set_cookie("password", row[1])
            #birti síða þar sem notanda tókst að logga inn
            redirect('/stocks')
    #ef að return var ekki gefið í for loop þá þýðir það að við erum komnir hingað
    #þá loka ég öllu og birti síðu sem segir notanda að honum tókst ekki að logga inn
    cur.close()
    conn.close()
    redirect('/')
run()
