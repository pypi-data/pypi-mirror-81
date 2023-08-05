import dbm
import shelve
import pathlib
import ZODB, BTrees.OOBTree, BTrees.IIBTree, BTrees.IOBTree
import time

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class EmbeddedCache(metaclass=Singleton):
    def __init__(self):
        # print('Which db: ', dbm.whichdb('./cache.db'))
        db = None
        while(not db):
            db = self.create()
            if not db:
                time.sleep(1)
        connection = db.open()
        root = connection.root
        root.t = BTrees.OOBTree.BTree()
        self.db = root.t

    def create(self):
        try:
            db = ZODB.DB(str(pathlib.Path(__file__).parent.absolute())+'/db/cache.fs')
            # print('First connect DB')
            return db
        except:
            # print('Try connect DB')
            return None
        

    def insert(self, key, parent=None, data=None):
        if parent:
            key = '.'.join((parent, key))

        # with dbm.open('cache', 'c') as db:
        # with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'c') as db:
        #     db[key] = data
            # assert db[key.encode('utf-8')] == data.encode('utf-8')
            # assert db[key] == data.encode('utf-8')
        self.db[key] = data

    def search(self, key, parent=None):
        if parent:
            key = '.'.join((parent, key))
        
        # with dbm.open('cache', 'r') as db:
        # with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'r') as db:
        #     return db.get(key, None)
        return self.db[key]

    def keys(self):
        # with dbm.open('cache', 'r') as db:
        # with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'r') as db:
        #     return db.keys()
        return self.db.keys()

    def list_all(self):
        # with dbm.open('cache', 'r') as db:
        # with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'r') as db:
        #     # print('All keys():', db.keys())
        #     return dict(map(lambda k: (k, db.get(k)), db.keys()))
        return dict(map(lambda k: (k, self.db.get(k)), self.db.keys()))

    def delete(self, key, parent=None):
        if parent:
            key = '.'.join((parent, key))
        
        # with dbm.open('cache', 'w') as db:
        # with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'w') as db:
        #     if db.get(key, None):
        #         del db[key]
            # print('Remaining keys():', db.keys())
        del self.db[key]

    def clear(self):
        # with dbm.open('cache', 'w') as db:
        # with shelve.open(str(pathlib.Path(__file__).parent.absolute())+'/db/log', 'w') as db:
        #     db.clear()
                # del db[key]
        self.db.clear()

