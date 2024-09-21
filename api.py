import json
import rds as db
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_employees():
    return jsonify("Shopify Api It's Online")

@app.route('/devolution', methods=['POST'])
def post_devolution():
    try:
        data = request.get_json()
        main_reason = data.get('main_reason', "")
        subsidiary = data.get('subsidiary', "")
        explanation = data.get('explanation', "")
        ticket_number = data.get('ticket_number', 0)
        client_number = data.get('client_number', 0)
        order_number = data.get('order_number', 0)
        date_product_arrived = data.get('date_product_arrived', "")
        items = data.get('items', [])

        devolution_id = db.process_devolution(
            main_reason, subsidiary, explanation, ticket_number, client_number, order_number, date_product_arrived, items
        )

        if not devolution_id:
            return jsonify({"error": "Failed to process devolution"}), 400

        devolution_data = db.get_devolution_with_items(devolution_id)

        if not devolution_data:
            return jsonify({"error": f"No se encontró la devolución con ID {devolution_id}"}), 404

        devolution = devolution_data["devolution"]
        devolution_items = devolution_data["items"]
        
        data = {
            "id": devolution[0],
            "status": devolution[1],
            "main_reason": devolution[2],
            "subsidiary": devolution[3],
            "explanation": devolution[4],
            "ticket_number": devolution[5],
            "client_number": devolution[6],
            "order_number": devolution[7],
            "createdAt": devolution[8],
            "returnment_label": devolution[9],
            "date_product_arrvie": devolution[10],
            "shipping_payment": devolution[11],
            "requires_label": devolution[12],
            "items": []
        }
        
        for item in devolution_items:
            item_data = {
                "sku": item[2],
                "cantidad": item[3]
            }
            data["items"].append(item_data)
        
        return jsonify(data)

    except Exception as e:
        print(f"Error processing devolution: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@app.route('/devolution/<int:id>', methods=['GET'])
def get_devolution(id):
    try:
        devolution_data = db.get_devolution_with_items(id)

        if not devolution_data:
            return jsonify({"error": f"No se encontró la devolución con ID {id}"}), 404

        devolution = devolution_data["devolution"]
        devolution_items = devolution_data["items"]
        
        data = {
            "id": devolution[0],
            "status": devolution[1],
            "main_reason": devolution[2],
            "subsidiary": devolution[3],
            "explanation": devolution[4],
            "ticket_number": devolution[5],
            "client_number": devolution[6],
            "order_number": devolution[7],
            "createdAt": devolution[8],
            "returnment_label": devolution[9],
            "date_product_arrvie": devolution[10],
            "shipping_payment": devolution[11],
            "requires_label": devolution[12],
            "items": []
        }
        
        for item in devolution_items:
            item_data = {
                "sku": item[2],
                "cantidad": item[3]
            }
            data["items"].append(item_data)
        
        return jsonify(data)

    except Exception as e:
        print(f"Error al obtener la devolución: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500




if __name__ == '__main__':
    app.run(debug=True,port=5000)