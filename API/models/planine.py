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
        cur.execute("select d.naziv , pl.naziv, pl.id, v.naziv, v.nadmorska_visina from sbp.drzave as d inner join sbp.planine as pl on d.id=pl.drzava_id inner join sbp.vrhovi as v on pl.id=v.planina_id where v.nadmorska_visina=(SELECT v2.nadmorska_visina FROM sbp.vrhovi as v2 where v2.planina_id=pl.id and v.active='True' order  by v2.nadmorska_visina DESC limit 1) and pl.active='True' and d.active ='True' and v.active='True';")
        planine = cur.fetchall()
        cur.execute("select d.naziv , pl.naziv, pl.id from sbp.drzave as d inner join sbp.planine as pl on d.id=pl.drzava_id where d.active = 'True' and pl.active='True';")
        pl_bez_vrhova=cur.fetchall()
        cur.close()
        conn.close()
        cl=[]
        response = []
        for row in planine:
            cl.append(row[1])
            x={"drzava":row[0],"naziv":row[1], "id":row[2], "najvisi_vrh":row[3], "visina_vrha":row[4]}
            response.append(x)
        
        for row in pl_bez_vrhova:
            if row[1] in cl:
                pass
            else:
                x={"drzava":row[0],"naziv":row[1], "id":row[2], "najvisi_vrh":None, "visina_vrha":None}
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
    
    cur.execute("select d.naziv , pl.naziv, pl.id from sbp.drzave as d left join sbp.planine as pl on d.id=pl.drzava_id where pl.id="+ str(id) +" and pl.active=True and d.active='True';")



    planina=cur.fetchone()
 
    
    response={"drzava":planina[0],"naziv":planina[1], "id":planina[2]}
    try:
        cur.execute("select v.id , v.naziv, v.nadmorska_visina from sbp.vrhovi  as v where v.planina_id=" + str(id) + " and v.active = 'True' order by v.nadmorska_visina DESC;")
        vrhovi=cur.fetchall()
        cur.close()
        conn.close()

        vrh=[]
        response["najvisi_vrh"]=vrhovi[0][1]
        response["nadmorska_visina"]=vrhovi[0][2]
        for row in vrhovi: 
            x={"id":row[0], "naziv":row[1], "nadmorska_visina":row[2]}
            vrh.append(x)
        
        response["vrhovi"]=vrh

        return response
    except:
        response["najvisi_vrh"]=None
        response["nadmorska_visina"]=None
        response["vrhovi"]=[]
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

def put_planina_pg(id, drzava_id, naziv):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    
    cur= conn.cursor()
    cur.execute("UPDATE sbp.planine SET drzava_id='{}', naziv = '{}' where id = {};".format(drzava_id, naziv, id))

    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}

def del_planina_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    
    cur= conn.cursor()
    cur.execute("UPDATE sbp.planine SET active='False' where id = {};".format(id))

    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":200}