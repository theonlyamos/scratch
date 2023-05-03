from runit_database import Document
from datetime import datetime
from time import sleep
import shelve

Document.initialize(
    'http://runit.test:9000/api',
    'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NDg1NDgyNiwianRpIjoiMTNkOTEyZmUtOGI2Zi00ZmQxLWJmYjAtNDA0Y2IzMTA4YWY3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6IjYzNWFiM2EzNzU0NGFjZDZjZDAyZGVkMiIsIm5iZiI6MTY3NDg1NDgyNiwiZXhwIjoxNjc3NDQ2ODI2fQ.CMnKSzYb7iscYq3Lu2MS_rFnq7KwL9Wl0zW3Rdy6UfQ',
    '63d6a50cf55a1a560f5a6de4'
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