import psycopg2
from db import *

def get_postignuce_by_id_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur= conn.cursor()
    cur.execute("select * from sbp.postignuca as ps where ps.active='True' and ps.id ="+ str(id)+";")
    postignuce=cur.fetchone()
    cur.execute("select ko.id , ko.komentar_sadrzaj, ko.created_at, ko.korisnik_id from sbp.komentari as ko where ko.active='True' and ko.postignuce_id ="+ str(id)+";")
    kom=cur.fetchall()
    cur.execute("select s.id , s.link_slike, s.naziv, s.opis from sbp.slike_postignuca as s where s.active='True'and s.postignuce_id="+ str(id)+";")
    sl=cur.fetchall()
    response= {"id":postignuce[0], "korisnik_id":postignuce[1], "naslov":postignuce[2], "opis":postignuce[3], "link_gpx_traga":postignuce[4], "created_at":str(postignuce[5]), "updated_at":str(postignuce[6]), "komentari":[], "slike":[]}
    for row in kom:
        x={"id":row[0], "komentar":row[1], "created_at":str(row[2]), "korisnik_id":row[3]}
        response["komentari"].append(x)
    
    for row in sl:
        x={"id":row[0], "link_slike":row[1], "naziv":row[2], "opis":row[3]}
        response["slike"].append(x)
    
    return response

def post_postignuce_pg(korisnik_id, naslov, opis, link):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur = conn.cursor()
    cur.execute("INSERT INTO sbp.postignuca (korisnik_id, naslov, opis, link_gpx_traga) VALUES ('{}','{}','{}','{}');".format(korisnik_id, naslov, opis, link))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}

def put_postignuce_pg(id,korisnik_id, naslov, opis, link):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur = conn.cursor()
    cur.execute("UPDATE sbp.postignuca SET korisnik_id={}, naslov ='{}', opis='{}', link_gpx_traga='{}' where id = {};".format(korisnik_id, naslov, opis, link, id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}

def del_postignuce_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur = conn.cursor()
    cur.execute("UPDATE sbp.postignuca SET active='False' where id = {};".format( id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":200}




def post_slike_pg(postignuce_id, link_slike, naziv, opis):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur=conn.cursor()
    cur.execute("INSERT INTO sbp.slike_postignuca (postignuce_id, link_slike, naziv, opis) VALUES ('{}','{}','{}','{}');".format(postignuce_id, link_slike, naziv, opis))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}

def post_komentara_pg(postignuce_id, komentar_sadrzaj, korisnik_id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur=conn.cursor()
    cur.execute("INSERT INTO sbp.komentari (postignuce_id, komentar_sadrzaj, komentar_tip, korisnik_id) VALUES ('{}','{}','Komentar','{}');".format(postignuce_id, komentar_sadrzaj, korisnik_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}


def put_slike_pg():
    pass

def put_komentara_pg():
    pass
def del_slike_pg():
    pass

def del_kom_pg():
    pass