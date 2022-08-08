from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('powerrangers', user='newowner',
                        password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Powerrangers(BaseModel):
    name = CharField()
    age = IntegerField()


db.connect()

db.drop_tables([Powerrangers])
db.create_tables([Powerrangers])

Powerrangers(name='Raul', age=1000).save()
Powerrangers(name='Mack', age=2000).save()
Powerrangers(name='Tim', age=3000).save()
Powerrangers(name='James', age=4000).save()
Powerrangers(name='Mario', age=5000).save()

app = Flask(__name__)


@app.route('/powerrangers/', methods=['GET', 'POST'])
@app.route('/Powerrangers/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Powerrangers.get(Powerrangers.id == id)))
        else:
            powerrangers_list = []
            for powerrangers in Powerrangers.select():
                powerrangers_list.append(model_to_dict(powerrangers))
            return jsonify(powerrangers_list)

    if request.method == 'PUT':
        if request.method == 'PUT':
            body = request.get_json()
            Powerrangers.update(body).where(Powerrangers.id == id).execute()
            return "Powerrangers" + str(id) + " has been updated."

    if request.method == 'POST':
        new_powerrangers = dict_to_model(Powerrangers, request.get_json())
        new_powerrangers.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Powerrangers.delete().where(Powerrangers.id == id).execute()
        return "powerrangers" + str(id) + " deleted."


app.run(debug=True, port=5000)
