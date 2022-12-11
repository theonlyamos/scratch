from runit_database import Document
from datetime import datetime
from time import sleep
import shelve

Document.initialize('http://runit.test:9000/api','eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3MDQzNzY5NiwianRpIjoiY2Y4NmFmMGQtYzNhNy00ZjIzLWI0YmMtZjRlOTNiZWQ3MDk4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYzNWFiM2EzNzU0NGFjZDZjZDAyZGVkMiIsIm5iZiI6MTY3MDQzNzY5NiwiZXhwIjoxNjczMDI5Njk2fQ.hcu83fucYzHwFm7VytmnXaWS7yN1yrCxeBsHZAQtKBc','6395056c2791b22537a99730')

def backup():
    try:
        db = shelve.open('scratch.db')
        items = []
        
        if 'items' in db.keys():
            items = db['items']
        if len(items):
            for item in items:
                if item['type'] == 'reminder':
                    item['date_time'] = item['date_time'].strftime("%a %b %d %Y %H:%M:%S")

            results = Document.items.insert_one(document=items)
    except:
        pass
        
def auto_backup(interval=18000):
    while True:
        try:
            backup()
            sleep(interval)
        except:
            pass