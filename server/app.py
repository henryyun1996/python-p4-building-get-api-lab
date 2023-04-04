#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "id": bakery.id,
            "name": bakery.name,
            "created_at": bakery.created_at
        }
        bakeries.append(bakery_dict)

    response = make_response(
        jsonify(bakeries),
        200,
        {"Content-Type": "application/json"}
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(
        jsonify(bakery_dict),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    # baked_goods_serialized = [item.to_dict() for item in baked_goods]

    baked_goods = []
    for baked_good in goods_by_price:
        good_dict = {
            "id": baked_good.id,
            "name": baked_good.name,
            "price": baked_good.price,
            "bakery_id": baked_good.bakery_id,
            "created_at": baked_good.created_at,
            "updated_at": baked_good.updated_at
        }
        baked_goods.append(good_dict)
    
    response = make_response(
        jsonify(baked_goods),
        200
    )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    most_expensive_good_serialized = most_expensive_good.to_dict()

    response = make_response(
        jsonify(most_expensive_good_serialized),
        200
    )
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == '__main__':
    app.run(port=555, debug=True)
