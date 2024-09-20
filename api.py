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
    
    data = request.get_json()
    
    main_reason = data.get('main_reason', "")
    subsidiary = data.get('subsidiary', "")
    explanation = data.get('explanation', "")
    ticket_number = data.get('ticket_number', 0)
    client_number = data.get('client_number', 0)
    order_number = data.get('order_number', 0)
    date_product_arrived = data.get('date_product_arrived', "")
    items = data.get('items', [])
    
    
    db.insert_devolution(main_reason, subsidiary, explanation, ticket_number, client_number, order_number, date_product_arrived)
    details = db.get_devolutions()
    
    for item in items:
        sku = item.get('sku')
        quantity = item.get('cantidad', 1)  # Valor por defecto: 1
        db.insert_devolution_item(details[-1][0], sku, quantity)
        
        
    # Build Json with all data
    
    return jsonify(details[-1])

@app.route('/devolution/<int:id>', methods=['GET'])
def get_devolution(id):
    devolution = db.get_devolution(id)
    devolution_items = db.get_devolution_items(id)
    
    data = {
        "id" : devolution[0][0],
        "status": devolution[0][1],
        "main_reason": devolution[0][2],
        "subsidiary": devolution[0][3],
        "explanation": devolution[0][4],
        "ticket_number": devolution[0][5],
        "client_number": devolution[0][6],
        "order_number": devolution[0][7],
        "createdAt": devolution[0][8],
        "returnment_label": devolution[0][9],
        "date_product_arrvie": devolution[0][10],
        "shipping_payment": devolution[0][11],
        "requires_label": devolution[0][12],
        "items": []
    }
    
    for item in devolution_items:
        item_data = {
            "sku": item[0],
            "cantidad": item[1]
        }
        data["items"].append(item_data)
    
    return jsonify(data)



if __name__ == '__main__':
    app.run(debug=True,port=5000)