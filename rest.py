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

class HelloWorld(restful.Resource):
    def get(self):
        return "Home"

class Devices(restful.Resource):
    def get(self):
        devices=[]
        nearby_devices = bluetooth.discover_devices(lookup_names = True)
        for addr, name in nearby_devices:
            new_device={}
            new_device["address"] = addr
            new_device["name"] = name
            devices.append(new_device.copy())
            cursor.execute('''INSERT INTO users(name, device, address) VALUES(?,?,?)''', ("placeholder", name, addr))
        db.commit()
        json_string = json.dumps(devices)
        return json_string

class Services(restful.Resource):
    def get(self):
        target = None
        services = bluetooth.find_service(address=target)
        json_string = json.dumps(services)
        return json_string

api.add_resource(HelloWorld, '/')
api.add_resource(Devices, '/devices')
api.add_resource(Services, '/services')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
