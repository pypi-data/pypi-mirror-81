__version__ = "0.1.0"

# first import all of the necessary firebase stuff
from firebase_admin import firestore, credentials, auth, storage

ArrayUnion = firestore.firestore.ArrayUnion
ArrayRemove = firestore.firestore.ArrayRemove
DESCENDING = firestore.firestore.Query.DESCENDING
ASCENDING = firestore.firestore.Query.ASCENDING
Increment = firestore.firestore.Increment
SERVER_TIMESTAMP = firestore.firestore.SERVER_TIMESTAMP
DELETE_FIELD = firestore.firestore.DELETE_FIELD

DocumentReference = firestore.firestore.DocumentReference
CollectionReference = firestore.firestore.CollectionReference

DocumentSnapshot = firestore.firestore.DocumentSnapshot

Query = firestore.firestore.Query

# give access to connect right from magicdb
from magicdb.database import connect, db


# to connect to the raw db, do db.conn
def batch(*args, **kwargs):
    return db.conn.batch(*args, **kwargs)


def transaction(*args, **kwargs):
    return db.conn.transaction(*args, **kwargs)
