import psycopg2
from db import *

def get_vrh_by_id_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur= conn.cursor()
    cur.execute("select v.id , v.naziv, v.nadmorska_visina, pl.naziv from sbp.vrhovi  as v join sbp.planine as pl on v.planina_id=pl.id where v.id=" + str(id) + ";")
    vrh=cur.fetchone()
    cur.execute("select s.id, v.naziv, s.link_gpx_traga, s.naziv, s.opis from sbp.staze as s join sbp.vrhovi as v on s.vrh_id=v.id where s.vrh_id ="+ str(id) + ";")
    staze= cur.fetchall()
    cur.close()
    conn.close()
    response={"id":vrh[0], "naziv":vrh[1], "nadmorska_visina":vrh[2], "planina":vrh[3]}
    st=[]
    for row in staze:
        x={"id":row[0], "vrh": row[1], "link_gpx_traga":row[2], "naziv":row[3], "opis":row[4]}
        st.append(x)
    
    response["staze"]=st
    return response

def post_vrh_pg(planina_id, naziv, nadmorska_visina):
    conn=psycopg2.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port
    )
    cur=conn.cursor()
    cur.execute("INSERT INTO sbp.vrhovi (planina_id, naziv, nadmorska_visina) VALUES ('{}','{}','{}');".format(planina_id, naziv, nadmorska_visina))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}
