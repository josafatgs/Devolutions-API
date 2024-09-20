import json
import rds as db
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_employees():
    res = db.get_devolution()
    print(res)
    return jsonify("res")

@app.route('/devolution', methods=['POST'])
def post_devolution():
    main_reason = "Example"
    subsidiary = "Example"
    explanation = "Example"
    ticket_number = 1
    client_number = 1
    order_number = 1
    date_product_arrived = "2020-05-22 09:06:28.580"
    db.insert_devolution(main_reason, subsidiary, explanation, ticket_number, client_number, order_number, date_product_arrived)
    details = db.get_devolutions()
    print(details)
    for detail in details:
        var = detail
    return var

@app.route('/devolution', methods=['GET'])
def get_devolution():
    
    details = db.get_devolution(1)
    return details

if __name__ == '__main__':
    app.run(debug=True,port=5000)