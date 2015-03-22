from flask import Flask
from flask.ext import restful
import bluetooth, json
import sqlite3

app = Flask(__name__)
api = restful.Api(app)
db = sqlite3.connect('data.sqlite')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE if not exists users(id INTEGER PRIMARY KEY, name TEXT,
                       device TEXT, address TEXT unique)
''')
db.commit()
db.close()
class HelloWorld(restful.Resource):
    def get(self):
        return "Home"

class Devices(restful.Resource):
    def get(self):
        db = sqlite3.connect('data.sqlite')
        cursor = db.cursor()
        devices=[]
        nearby_devices = bluetooth.discover_devices(lookup_names = True)
        for addr, name in nearby_devices:
            new_device={}
            new_device["address"] = addr
            new_device["name"] = name
            devices.append(new_device.copy())
            try:
                cursor.execute('''INSERT INTO users(name, device, address) VALUES(?,?,?)''', ("placeholder", name, addr))
                db.commit()
            except sqlite3.IntegrityError as err:
               print err
                
        db.close()
        json_string = json.dumps(devices)
        return json_string

class Services(restful.Resource):
    def get(self):
        db = sqlite3.connect('data.sqlite')
        cursor = db.cursor()
        target = None
        services = bluetooth.find_service(address=target)
        db.close()
        json_string = json.dumps(services)
        return json_string

class List(restful.Resource):
    def get(self):
        db = sqlite3.connect('data.sqlite')
        cursor = db.cursor()
        cursor.execute('''SELECT * FROM users''')
        all_rows = cursor.fetchall()
        devices=[]
	#for id, name, device, addr in all_rows:
        #    services = bluetooth.find_service(addr)
        #    json_string = json.dumps(services)
        #    return json_string
        db.close()
        json_string = json.dumps(all_rows)
        return json_string

api.add_resource(HelloWorld, '/')
api.add_resource(Devices, '/devices')
api.add_resource(Services, '/services')
api.add_resource(List, '/list')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
