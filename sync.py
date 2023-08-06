from runit_database import Document
from datetime import datetime
from time import sleep
import shelve

Document.initialize(
    'http://runit.test:9000/api',
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NjkzMDQxNCwianRpIjoiOWU5YmIwMDAtOWJkNS00ZWI4LTg4YWEtYWViMjYzNDU3NGI0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYyYjAxY2E4ZGVmN2YzMTcwMDNiZWUyYiIsIm5iZiI6MTY4NjkzMDQxNCwiZXhwIjoxNjg5NTIyNDE0fQ.OJq8c4DgBI1haEgbS9NHMDxYAQtaFIzTHSopaiZNeSc',
    '648c7f6886abacf21d21faf2'
)

def backup():
    try:
        db = shelve.open('scratch.db')
        items = []
        
        if 'items' in db.keys():
            items = db['items']
        if len(items):
            for item in items:
                if item['type'] == 'reminder':
                    dt = item['date_time']
                    item['date_time'] = dt.strftime("%a %b %d %Y %H:%M:%S")
                    
                if item['_id'] is None:
                    result = Document.scratch.insert_one(document=item)
                    if (result['status'] == 'success'):
                        item['_id'] = result['msg']
                else:
                    updated = item
                    
                    del updated['_id']
                    result = Document.scratch.update(_filter={'id': item['_id']}, update=updated)
                
                if item['type'] == 'reminder':
                    item['date_time'] = dt
                    
            db['items'] = items
            db.close()
    except:
        pass
        
def auto_backup(interval=18000):
    while True:
        try:
            backup()
            sleep(interval)
        except:
            pass
