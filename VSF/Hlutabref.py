#importa allt sem ég nota úr bottle
#  þurfum að setja pymysql upp í pyCharm (sama rútína og bottle-beake
import pymysql
from bottle import *
import datetime
from Classes.Bots import *
import os
#bý til index sem skilar síðu þar sem hægt er að skrá sig inn / skrá nýjan user
@route('/')
def index():
    if request.get_cookie("login") and request.get_cookie("password"):
        #opna tengingu við sql database
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                               db='1503953219_lokaverkefni_3_onn')
        cur = conn.cursor()
        #næ í allt úr user_info
        cur.execute("SELECT * FROM user_info")
        #athuga hverja línu hvort username og password passi með for loop
        for row in cur:
            #athuga hverja línu hvort username og password passi
            if row[1]==request.get_cookie("login") and request.get_cookie("password")==row[2]:
                #loka öllu
                cur.close()
                conn.close()
                #birti síða þar sem notanda tókst að logga inn
                redirect('/stocks/1')
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
    cur.execute("SELECT count(username) FROM user_info where username='{}'".format(newuser))
    #næ í þessa einu tölu
    user = cur.fetchone()[0]
    #user er lína úr database, athuga fyrsta stak sem er username stakið hvort það er til eða ekki
    #username stakið er = 1 ef newuser er þegar til því ég bað um count(*) í query
    if user >= 1:
        #loka öllu
        cur.close()
        conn.close()
        #birti síðu
        return template('newuserno.tpl')
    #ef user er ekki til þá bý ég hann til
    else:
        #bæti við nýjum user í database
        cur.execute("INSERT INTO User(bot) Values('{}')".format(1))
        #Sæki hæsta id til að finna nýjasta notendann(þann sem við erum að búa til)
        cur.execute("SELECT MAX(UserID) FROM user")
        #Nota það id til að bæta við password og username upplýsingum við réttan notenda
        currentid = cur.fetchone()[0]
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
        if row[1]==username and row[2]==password:
            #bý til tímabil fyrir cookies
            timabil=datetime.datetime.now() + datetime.timedelta(days=30)
            #set cookies fyrir login info
            response.set_cookie("login",row[1],expires=timabil)
            response.set_cookie("password",row[2],expires=timabil)
            cur.execute("SELECT UserID FROM User_info WHERE Username =  '%s'" %(username))
            userid=cur.fetchone()[0]
            response.set_cookie("UserID",str(userid),expires=timabil)
            #birti síða þar sem notanda tókst að logga inn
            redirect('/stocks/1')
    #ef að return var ekki gefið í for loop þá þýðir það að við erum komnir hingað
    #þá loka ég öllu og birti sendi aftur á index
    cur.close()
    conn.close()
    redirect('/')


@route('/logout')
#eyðir innskráningar cookie og fer með þig aftur á upphafsíðu
def logout():
    # Að eyða cookie, yfirskrifum gildið í gildi núll og stillum tíma á 0 svo hún rennur út strax.
    response.set_cookie("login", "", expires=0)
    response.set_cookie("password","",expires=0)
    response.set_cookie("UserID","",expires=0)
    redirect('/')

#Dynamic route sem sýnir mismunandi stocks eftir því hvar í routinu hann er
@route('/stocks/<id:int>')
def stocks(id):
    #Sækja userid úr cookie til að vita hvað notandi er loggaður inn
    CurrentID = int(request.get_cookie("UserID"))
    #tengjast við gagnagrunninn
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    #Sækja upplýsingar um notendann
    cur.execute("SELECT Username, Current_Cash, Total_Value FROM user_info, user WHERE (user.UserID = user_info.UserID) AND user.UserID = %d" %CurrentID)
    userinfo = cur.fetchone()
    name = userinfo[0]
    cash = userinfo[1]
    value = userinfo[2]
    #Sækja upplýsingar um það hlutabréf sem er til skoðunar
    cur.execute("SELECT StockID, Name, Original_market_price, Current_market_price, Last_percent_change, UserID, Status, "
    + "Sale_price FROM stock WHERE StockID = %d" %id)
    stock=cur.fetchone()
    sid = stock[0]
    sname = stock[1]
    ogprice = stock[2]
    currprice = stock[3]
    lpercent = stock[4]
    owner = stock[5]
    if owner == 4:
        owner = "Markaður"
    status = stock[6]
    sprice = stock[7]
    if status == 1:
        status = "On sale"
    else:
        status = "Not for sale"
        sprice = "Ekki til sölu"
    cur.execute("SELECT COUNT(StockID) FROM stock ")
    max_id = cur.fetchone()[0]
    nid = sid + 1
    if max_id < nid:
        nid = sid
    #loka connectioninu
    cur.close()
    conn.close()

    return template('stocks.tpl', name = name, cash = cash, value = value, sname = sname, ogprice = ogprice,
                    currprice = currprice, lpercent = lpercent, owner = owner, status = status, sprice = sprice,
                    nid = nid)
@route('/admin',method='POST')
def admin():
    return template('admin.tpl')
@route('/bots',method='POST')
def bots():
    #opna tengingu við sql database
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    cur.execute("SELECT MAX(UserID) FROM user")
    nr = cur.fetchone()[0] + 1
    botsfj=int(request.forms.get('botfj'))
    upperrisk=int(request.forms.get('upperrisk'))
    lowerrisk=int(request.forms.get('lowerrisk'))
    buyrisk=int(request.forms.get('buyrisk'))
    print(botsfj, upperrisk, lowerrisk, buyrisk)
    for x in range(botsfj):
        y=Bots(nr, upperrisk,lowerrisk, buyrisk)
        y.newbot()

@route('/stocks', method='POST')
def stocks():
    # opna tengingu við sql database
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                               db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    cur.execute("SELECT MAX(StockID) FROM stock")
    nr = cur.fetchone()[0] + 1
    stockfj = int(request.forms.get('stockfj'))
    name = int(request.forms.get('name'))
    market_price = int(request.forms.get('lowerrisk'))
    buyrisk = int(request.forms.get('buyrisk'))
    print(botsfj, upperrisk, lowerrisk, buyrisk)
    for x in range(stockfj):
        y = stocks(nr, name, market_price, normal_percent_change)
        y.newstock()


#bendi á static skráina og að allt í henni sé static
@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='./static')

run()
