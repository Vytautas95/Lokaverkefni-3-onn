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
            global userid
            userid=cur.fetchone()[0]
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
    #tengjast við gagnagrunninn
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    #Sækja upplýsingar um notendann og set pening sem global breytu þar sem við gætum þurft að nota hana seinna
    cur.execute("SELECT Username, Current_Cash, Total_Value FROM user_info, user WHERE (user.UserID = user_info.UserID) AND user.UserID = %d" %userid)
    userinfo = cur.fetchone()
    name = userinfo[0]
    global cash
    cash = userinfo[1]
    value = userinfo[2]
    #Sækja upplýsingar um það hlutabréf sem er til skoðunar, set Stock id, verð og owner id sem global breytur því við þurfum að nota þær í öðru routi
    cur.execute("SELECT StockID, Name, Original_market_price, Current_market_price, Last_percent_change, UserID, Status, "
    + "Sale_price FROM stock WHERE StockID = %d" %id)
    stock=cur.fetchone()
    global sid
    sid = stock[0]
    sname = stock[1]
    ogprice = stock[2]
    currprice = stock[3]
    lpercent = stock[4]
    global owner
    owner = stock[5]
    ownername = owner
    if ownername == 4:
        ownername = "Markaður"
    else:
        cur.execute("SELECT bot FROM user WHERE UserID = %d" % ownername)
        bot = cur.fetchone()[0]
        print(bot)
        if bot == 1:
            cur.execute("SELECT Username FROM user_info WHERE UserID = %d" % ownername)
            ownername = cur.fetchone()[0]
        else:
            ownername = "Bot" + str(ownername)
    status = stock[6]
    global sprice
    sprice = stock[7]
    if status == 1:
        status = "On sale"
    else:
        status = "Not for sale"
        sprice = "Ekki til sölu"
    cur.execute("SELECT COUNT(StockID) FROM stock ")
    max_id = cur.fetchone()[0]
    nid = sid + 1
    lid = sid - 1
    if max_id < nid:
        nid = sid
    if sid == 1:
        lid = 1
    #loka connectioninu
    cur.close()
    conn.close()
    return template('stocks.tpl', name = name, cash = cash, value = value, sname = sname, ogprice = ogprice,
                    currprice = currprice, lpercent = lpercent, owner = ownername, status = status, sprice = sprice,
                    nid = nid, lid = lid)
@route('/kaupa', method='POST')
def kaupa():
    if sprice == "Ekki til Sölu":
        return '''Þetta hlutabréf er ekki til sölu <a href="/stocks/%d">Fara til baka</a> ''' %sid
    elif sprice > cash:
        return '''Þú átt ekki nóg af pening til að kaupa þetta hlutabréf <a href="/stocks/%d">Fara til baka</a> ''' %sid
    else:
        # tengjast við gagnagrunninn
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                               db='1503953219_lokaverkefni_3_onn')
        cur = conn.cursor()
        cur.execute("INSERT INTO transaction(Price, BuyerID, SellerID, StockID) Values('{}','{}','{}', '{}')".format(sprice, userid, owner, sid))
        conn.commit()
        return '''Kaup staðfest! <a href="/stocks/%d">Fara til baka</a>''' %sid
@route('/minbref/<id:int>')
def minbref(id):
    #tengjast við gagnagrunninn
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    #Sækja upplýsingar um notendann
    cur.execute("SELECT Username, Current_Cash, Total_Value FROM user_info, user WHERE (user.UserID = user_info.UserID) AND user.UserID = %d" %userid)
    userinfo = cur.fetchone()
    name = userinfo[0]
    cash = userinfo[1]
    value = userinfo[2]
    #Sækja upplýsingar um það hlutabréf sem er til skoðunar
    cur.execute("SELECT StockID, Name, Original_market_price, Current_market_price, Last_percent_change, UserID, Status, "
    + "Sale_price FROM stock WHERE UserID = %d" %userid)
    usedid = id - 1
    stock=cur.fetchall()[usedid]
    print(stock)
    global sid
    sid = stock[0]
    sname = stock[1]
    ogprice = stock[2]
    currprice = stock[3]
    lpercent = stock[4]
    owner = stock[5]
    ownername = owner
    cur.execute("SELECT Username FROM user_info WHERE UserID = %d" % ownername)
    ownername = cur.fetchone()[0]
    status = stock[6]
    sprice = stock[7]
    if status == 1:
        status = "On sale"
    else:
        status = "Not for sale"
        sprice = "Ekki til sölu"
    cur.execute("SELECT COUNT(StockID) FROM stock WHERE UserID = %d" %userid)
    max_id = cur.fetchone()[0]
    nid = id + 1
    lid = id - 1
    if max_id < nid:
        nid = id
    if usedid == 0:
        lid = 1
    #loka connectioninu
    cur.close()
    conn.close()
    return template('minstocks.tpl', name = name, cash = cash, value = value, sname = sname, ogprice = ogprice,
                    currprice = currprice, lpercent = lpercent, owner = ownername, status = status, sprice = sprice,
                    nid = nid, lid = lid)
@route('/selja', method='POST')
def selja():
    price = int(request.forms.get('price'))
    # tengjast við gagnagrunninn
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                               db='1503953219_lokaverkefni_3_onn')
    cur = conn.cursor()
    cur.execute("UPDATE Stock SET Status = 1, Sale_price = '{}' WHERE StockID = '{}'".format(price, sid))
    conn.commit()
    redirect('/minbref/%d'%sid)
@route('/admin')
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
    for x in range(botsfj):
        y=Bots(nr, upperrisk,lowerrisk, buyrisk)
        y.newbot()
    return '''Skráning tókst!, <a href="/admin">Fara til baka</a>"'''

@route('/stocks', method='POST')
def stocks():
    stockfj = int(request.forms.get('stockfj'))
    name = request.forms.get('name')
    market_price = int(request.forms.get('mprice'))
    normal_percent_change = int(request.forms.get('npchange'))
    for x in range(stockfj):
        y = Stocks(name, market_price, normal_percent_change)
        y.newstock()
    return '''Skráning tókst!, <a href="/admin">Fara til baka</a>'''

#bendi á static skráina og að allt í henni sé static
@route('/static/<filename>')
def static(filename):
    return static_file(filename, root='./static')

run()
