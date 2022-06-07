import psycopg2
from db import host, database,user,password, port




    
def get_drzave_pg():
        conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cur= conn.cursor()

        cur.execute("select drzave.id , drzave.naziv, drzave.created_at , count(planine.drzava_id) as broj_planina from sbp.drzave as drzave left join sbp.planine as planine on drzave.id=planine.drzava_id group by drzave.id;")  
        drzave=cur.fetchall()
        cur.close()
        conn.close()
        response=[]
        for row in drzave:
            print(row)
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
