import psycopg2
import pymongo
from mongoCl import dr
from db import host, database,user,password, port
from datetime import datetime


def post_drzave_mg(naziv):
    content = {"naziv": naziv, "active":"True", "planine":[], "created_at":datetime.now()}
    dr.insert_one(content)
    return {"message":"Success", "status":201}

def get_drzave_mg():
    drzave= list(dr.find({"active":"True"}))
    d=[]
    for row in drzave:
        x={"id":str(row["_id"]), "naziv": row["naziv"], "created_at":str(row["created_at"]), "broj_planina":len(row["planine"])}
        d.append(x)
    
    return d


    

def put_drzave_mg():
    pass

def del_drzave():
    pass


    
def get_drzave_pg():
        conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cur= conn.cursor()

        cur.execute("select drzave.id , drzave.naziv, drzave.created_at , count(planine.drzava_id) as broj_planina from sbp.drzave as drzave left join sbp.planine as planine on drzave.id=planine.drzava_id where drzave.active='True' group by drzave.id;")  
        drzave=cur.fetchall()
        cur.close()
        conn.close()
        response=[]
        for row in drzave:
            x={"id":row[0], "naziv": row[1], "created_at":str(row[2]), "broj_planina":row[3]}
            
            response.append(x)
        
    
            

        return response

def post_drzave_pg(naziv):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur = conn.cursor()
    cur.execute("INSERT INTO sbp.drzave (naziv) VALUES ('" + str(naziv) +"');")
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}

def put_drzave_pg(id, naziv):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur = conn.cursor()
    cur.execute("UPDATE sbp.drzave SET naziv= '" + str(naziv) +"' WHERE id = " + str(id) + ";")
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}

def del_drzava_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur = conn.cursor()
    cur.execute("UPDATE sbp.drzave SET active = 'False' WHERE id = " + str(id) + ";")
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Deleted", "status":200}
    