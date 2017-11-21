#importa allt sem ég nota úr bottle
from bottle import *
import pymysql
#routið sem heldur utan um login formið
@route('/upphafsida')
#formið fyrir loggin
def login():
    return '''
        <form action="/login" method="post">
            Notendanafn: <input name="username" type="text" />
            Lykilorð: <input name="password" type="password" />
            <input value="Innskrá" type="submit" />
        </form>
        <form action="/skra" method="post">
            Notendanafn: <input name="username" type="text" />
            Lykilorð: <input name="password" type="password" />
            <input value="nýskrá" type="submit" />
        </form>
            '''
#route sem tekur við upplýsingum frá loggin forminu
@route('/login',  method = 'post')
#Tjekkar hvort notendanafn og lykilorð var rétt
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    findinguser = []
    # tengir okkur við þjón og ákveðinn grunn. cursor object veitir okkur tilvísun á ákveðinn gagnagrunn.
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword', db='1503953219_vef2verk11')
    cur = conn.cursor()
    # lesa alla úr töflunni
    cur.execute("SELECT skraningarnumer FROM bilar")
    for row in cur:
        findinguser.append(row[0])
    cur.close()
    conn.close()
    if username in findinguser:
        # tengir okkur við þjón og ákveðinn grunn. cursor object veitir okkur tilvísun á ákveðinn gagnagrunn.
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                               db='1503953219_vef2verk11')
        cur = conn.cursor()
        # lesa alla úr töflunni
        cur.execute("SELECT * FROM bilar WHERE skraningarnumer = %s", (username))
        for row in cur:
            user = row
        cur.close()
        conn.close()
        password = user[1]
    #ef þau voru rétt, senda þig á leynisíðu og cookies eru verndaðar með leynilykli
    if username in usernames and  password in passwords:
        response.set_cookie("account", username, secret='some-secret-key')
        redirect('/restricted')
    #Annars birta villuboð
    else:
        return "<p>Innskráning mistókst rangt notendanafn</p>"
@route('/skra', method = 'post')
def skra():
    # tengir okkur við þjón og ákveðinn grunn. cursor object veitir okkur tilvísun á ákveðinn gagnagrunn.
    conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                           db='1503953219_vef2verk11')
    cur = conn.cursor()
    t = request.forms.get('tegund')
    nr = request.forms.get('skraningarnr')
    cur.execute("Insert into notendur values('{}','{}')".format(nr, t))
    conn.commit()
    cur.close()
    conn.close()
    return 'Skráning tókst, vinsamlegast farðu á upphafsíðu og skráðu þig inn!<br><a href="http://localhost:8080/leita">Upphafsíða</a>'
#leynisíða sem hleypir þér ekki inn nema þú sért með köku sem þú færð við að logga þig inn
@route('/restricted')
def restricted_area():
    username = request.get_cookie("account", secret='some-secret-key')
    #ef þú ert loggaður inn birta síðu með texta og logout takka
    if username:
        return template('''
        <h1>Velkomin {{name}}.</h1>
        <form action="/logout" method="get">
            <input value="Útskrá" type="submit" />
        </form>
            ''' , name=username)
    #Ef þú ert ekki loggaður inn, birta rétt skilaboð
    else:
        return "Aðgangur lokaður, Þú ert ekki skráður inn"
@route('/logout')
#eyðir innskráningar cookie og fer með þig aftur á upphafsíðu
def logout():
    # Að eyða cookie, yfirskrifum gildið í gildi núll og stillum tíma í fortíðina (mínustala) svo hún rennur út strax.
    response.set_cookie("account", "", expires=0)
    redirect('/upphafsida')