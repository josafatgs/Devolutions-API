import pymysql
import aws_credentials as rds

conn = pymysql.connect(
        host= rds.host, #endpoint link
        port = rds.port, # 3306
        user = rds.user, # admin
        password = rds.password, #adminadmin
        db = rds.db, #test
        )

def insert_devolution(main_reason, subsidiary, explanation, ticket_number, client_number, order_number, date_product_arrived):
    cur=conn.cursor()
    cur.execute("INSERT INTO Devolution (mainReason,sucursal,explanation,ticketNumber,clientNumber,orderNumber,dateProductArrive) VALUES (%s,%s,%s,%s,%s,%s,%s)", (main_reason,subsidiary,explanation,ticket_number,client_number,order_number, date_product_arrived))
    conn.commit()

def get_devolution(id):
    cur=conn.cursor()
    cur.execute(f"SELECT * FROM Devolution WHERE id=${id}")
    details = cur.fetchall()
    return details

def get_devolutions():
    cur=conn.cursor()
    cur.execute("SELECT *  FROM Devolution;")
    details = cur.fetchall()
    return details