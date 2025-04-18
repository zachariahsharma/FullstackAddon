# Assuming you have not changed the general structure of the template no modification is needed in this file.
from .lib import fusionAddInUtils as futil
from .lib.ImportModules import import_pymongo_from_venv
from .commands import Execute
import_pymongo_from_venv()
import pymongo
import time

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.4.2")
db = client['jira']
tasks = db['tasks']
imported = db['imported']

def run(context):
    try:
        # This will run the start function in each of your commands as defined in commands/__init__.py
        while True:
            for task in tasks.find({'Status': 'primed'}):
                children = [imported.find_one({'child': child}) for child in task['Parts']]
                task['Parts'] = children
                Execute.start(task)
                tasks.update_one({'_id': task['_id']},{'$set': {'Status': 'cammed'}})
            time.sleep(60)
    except:
        futil.handle_error('run')


def stop(context):
    try:
        # Remove all of the event handlers your app has created
        futil.clear_handlers()

        # This will run the start function in each of your commands as defined in commands/__init__.py

    except:
        futil.handle_error('stop')