import psycopg2
from db import *

def post_staze_pg(vrh_id, link_gpx_traga, naziv, opis):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur=conn.cursor()
    cur.execute("INSERT INTO sbp.staze(vrh_id, link_gpx_traga, naziv, opis) VALUES ('{}','{}','{}', '{}');".format(vrh_id, link_gpx_traga, naziv, opis))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}


def put_staze_pg(id, vrh_id, link_gpx_traga, naziv, opis ):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur=conn.cursor()
    cur.execute("UPDATE sbp.staze SET vrh_id= {}, link_gpx_traga= '{}', naziv= '{}', opis= '{}' where id ={}; ".format(vrh_id,link_gpx_traga, naziv, opis, id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}

def del_staze_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur=conn.cursor()
    cur.execute("UPDATE sbp.staze SET active='False' where id ={}; ".format(id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":200}