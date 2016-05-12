#!/Users/kawasakitaku/Documents/python-PVM/ln-python2.7/bin/python2.7

from twisted.internet import reactor
from twisted.enterprise import adbapi

dbpool = adbapi.ConnectionPool("sqlite3","users.db", check_same_thread=False)

def _createuserstable(transaction,users):
    transaction.execute("create table users (email text,name text)")
    for email,name in users:
        transaction.execute("insert into users (email,name) values(?,?)",(email,name))

def createuserstable(users):
    return dbpool.runInteraction(_createuserstable,users)

def getName(email):
    return dbpool.runQuery("select name from users where email =?",(email,))

def printResults(results):
    for elt in results:
        print elt[0]

def finish():
    dbpool.close()
    reactor.stop()

users = [("",""),("","")]

d = createuserstable(users)
d.addCallback(lambda x: getName(""))
d.addCallback(printResults)
reactor.callLater(1, finish)

reactor.run()
