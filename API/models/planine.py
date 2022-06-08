import psycopg2
import pymongo
from bson.objectid import ObjectId
from mongoCl import dr
from db import host, database,user,password, port

def post_planine_mg(drzava_id, naziv):
    
    drzava= dr.find_one({"_id":ObjectId(drzava_id)} )
    planina={"_id":ObjectId(), "naziv":naziv, "active":"True", "vrhovi":[]}
    pl= drzava["planine"]
    print(pl)
    pl.append(planina)
    print(pl)
    dr.update_one({"_id":ObjectId(drzava_id)}, {"$set":{"planine":pl}})
    return {"message":"Success", "status":201}


def get_planine_mg():
    drzave= list(dr.find({"active":"True"}))
    resp=[]
    for x in drzave:
        d=str(x["naziv"])
        for y in x["planine"]:
            maxV=None
            if len(y["vrhovi"])>0:
                
                maxV = max(y["vrhovi"], key=lambda x:x['nadmorska_visina'])
            if maxV== None:
                naziv=None
                nad_vis=None
            else:
                naziv=maxV["naziv"]
                nad_vis=maxV["nadmorska_visina"]
            x={"drzava":d,"naziv":y["naziv"], "id":str(y["_id"]), "najvisi_vrh":naziv, "visina_vrha":nad_vis}
            resp.append(x)
    
    return resp




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

def get_planina_by_id_mg(id):
    maxV = None
    drzave= list(dr.find({"planine":{"$elemMatch":{"_id":ObjectId(id)}}}))
    drzave=drzave[0]
    drzava=drzave["naziv"]
    planine=drzave["planine"]
    for x in planine:
        if x["_id"]==ObjectId(id):
            planina=x
        else:
            pass
    if len(planina["vrhovi"])>0:
                
                maxV = max(planina["vrhovi"], key=lambda x:x['nadmorska_visina'])
    if maxV== None:
                naziv=None
                nad_vis=None
    else:
                naziv=maxV["naziv"]
                nad_vis=maxV["nadmorska_visina"]

    resp={"drzava":drzava,"naziv":planina["naziv"], "id":str(planina["_id"]), "vrhovi":[]}

    if len(planina["vrhovi"])>0:
        for row in planina["vrhovi"]:
            y={"id":str(row["_id"]), "naziv":row["naziv"], "nadmorska_visina":row["nadmorska_visina"]}
            resp["vrhovi"].append(y)
    
    return resp



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