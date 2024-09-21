import pymysql
import aws_credentials as rds

conn = pymysql.connect(
        host= rds.host, #endpoint link
        port = rds.port, # 3306
        user = rds.user, # admin
        password = rds.password, #adminadmin
        db = rds.db, #test
        )


def insert_devolution(cur, main_reason, subsidiary, explanation, ticket_number, client_number, order_number, date_product_arrived):
    """
    Inserta una devolución en la base de datos.
    """
    cur.execute("""
        INSERT INTO Devolution (mainReason, sucursal, explanation, ticketNumber, clientNumber, orderNumber, dateProductArrive)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (main_reason, subsidiary, explanation, ticket_number, client_number, order_number, date_product_arrived))
    
    # Retorna el ID de la devolución recién insertada
    return cur.lastrowid

def insert_devolution_item(cur, devolution_id, sku, qty):
    """
    Inserta un item asociado a una devolución en la base de datos.
    """
    cur.execute("""
        INSERT INTO Devolution_Item (devolutionId, sku, quantity)
        VALUES (%s, %s, %s);
    """, (devolution_id, sku, qty))

def process_devolution(main_reason, subsidiary, explanation, ticket_number, client_number, order_number, date_product_arrived, items):
    """
    Función principal que maneja la transacción completa. Inserta la devolución y sus items.
    """
    try:
        # Iniciar la transacción
        cur = conn.cursor()
        
        
        # Insertar la devolución
        devolution_id = insert_devolution(
            cur, main_reason, subsidiary, explanation, ticket_number, client_number, order_number, date_product_arrived
        )
        
        # Insertar los items relacionados
        for item in items:
            sku = item.get('sku')
            quantity = item.get('cantidad', 1) 
            insert_devolution_item(cur, devolution_id, sku, quantity)
        
        # Confirmar los cambios si todo fue exitoso
        conn.commit()
        #print("Devolution and items inserted successfully.")
        
        return devolution_id  # Retorna el ID de la devolución insertada
        
    except Exception as e:
        # Hacer rollback si ocurre un error en cualquier punto
        conn.rollback()
        print(f"Error processing devolution: {e}")
        return None
        
    finally:
        cur.close()


def get_devolution_with_items(devolution_id):
    """
    Obtiene la devolución y sus items, manejando las excepciones adecuadamente.
    """
    try:
        cur = conn.cursor()

        # Obtener los detalles de la devolución
        cur.execute("SELECT * FROM Devolution WHERE id = %s", (devolution_id,))
        devolution_details = cur.fetchone()  # Utilizar fetchone porque es un único resultado

        if not devolution_details:
            raise Exception(f"No se encontró la devolución con ID {devolution_id}")

        # Obtener los items de la devolución
        cur.execute("SELECT * FROM Devolution_Item WHERE devolutionId = %s", (devolution_id,))
        devolution_items = cur.fetchall()

        # Estructurar los datos
        data = {
            "devolution": devolution_details,
            "items": devolution_items
        }
        
        return data
    
    except Exception as e:
        print(f"Error al obtener la devolución o los items: {e}")
        return None
    
    finally:
        cur.close()

def get_devolutions():
    cur=conn.cursor()
    cur.execute("SELECT *  FROM Devolution;")
    details = cur.fetchall()
    return details