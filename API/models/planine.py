import psycopg2
from db import host, database,user,password, port

def get_planine_pg():
        conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cur= conn.cursor()
        cur.execute("select d.naziv , pl.naziv, pl.id, v.naziv, v.nadmorska_visina from sbp.drzave as d left join sbp.planine as pl on d.id=pl.drzava_id left join sbp.vrhovi as v on pl.id=v.planina_id where v.nadmorska_visina=(SELECT MAX(v2.nadmorska_visina) FROM sbp.vrhovi as v2 where v2.planina_id=pl.id);")
        planine = cur.fetchall()
        cur.close()
        conn.close()

        response = []
        for row in planine:
            x={"drzava":row[0],"naziv":row[1], "id":row[2], "najvisi_vrh":row[3], "visina_vrha":row[4]}
            response.append(x)

        return response

def get_planina_by_id_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur= conn.cursor()
    cur.execute("select d.naziv , pl.naziv, pl.id, v.naziv, v.nadmorska_visina from sbp.drzave as d left join sbp.planine as pl on d.id=pl.drzava_id left join sbp.vrhovi as v on pl.id=v.planina_id where v.nadmorska_visina=(SELECT MAX(v2.nadmorska_visina) FROM sbp.vrhovi as v2 where v2.planina_id="+ str(id) +");")

    planina=cur.fetchone()
    cur.execute("select v.id , v.naziv, v.nadmorska_visina from sbp.vrhovi  as v where v.planina_id=" + str(id) + ";")
    vrhovi=cur.fetchall()
    cur.close()
    conn.close()
    response={}
    
    response={"drzava":planina[0],"naziv":planina[1], "id":planina[2], "najvisi_vrh":planina[3], "visina_vrha":planina[4]}

    vrh=[]
    for row in vrhovi: 
        x={"id":row[0], "naziv":row[1], "nadmorska_visina":row[2]}
        vrh.append(x)
    
    response["vrhovi"]=vrh

    return response

def post_planine_pg(drzava_id, naziv):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur= conn.cursor()
    cur.execute("INSERT INTO sbp.planine (drzava_id, naziv) VALUES ('{}','{}');".format(drzava_id,naziv))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}