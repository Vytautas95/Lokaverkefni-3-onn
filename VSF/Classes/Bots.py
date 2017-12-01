#importa random og pymysql
import pymysql
import random
class Bots():
    def __init__(self, numer,  upperRisk = random.randint(1,5), lowerRisk = random.randint(-5, -1), buyRisk = random.randint(1,5)):
        self.u = upperRisk
        self.l = lowerRisk
        self.b = buyRisk
        self.nr = numer
    def newbot(self):
        #opna connection í sql database
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                               db='1503953219_lokaverkefni_3_onn')
        cur = conn.cursor()
        cur.execute("INSERT INTO User(bot) Values('{}')".format(0))
        cur.execute("SELECT MAX(UserID) FROM user")
        currentid = cur.fetchone()
        cur.execute("INSERT INTO bot_info Values('{}','{}','{}', '{}')".format(self.nr ,self.u,self.l, self.b))
        conn.commit()
        #loka öllu
        cur.close()
        conn.close()
        return "Bot nr " + str(currentid) + " búinn til"

class Stocks():
    def __init__(self, name, market_price = random.randint(1000, 20000), normal_percent_change = random.randint(1, 5)):
        self.n = name
        self.m = market_price
        self.p = normal_percent_change
    def newstock(self):
        #opna connection í sql database
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1503953219', passwd='mypassword',
                               db='1503953219_lokaverkefni_3_onn')
        cur = conn.cursor()
        cur.execute("INSERT INTO stock(name, Original_market_price, Current_market_price, Last_percent_change, Normal_percent_change, Status, sale_price) Values('{}','{}','{}','{}','{}','{}','{}')".format(self.n, self.m, self.m, self.p, self.p, 1, self.m))
        conn.commit()
        #loka öllu
        cur.close()
        conn.close()
        return "hlutabréfið " + str(self.n) + " búið til"
