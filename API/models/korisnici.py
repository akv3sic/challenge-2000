import psycopg2
from db import host, database,user,password, port

def get_korisnici_pg():
        conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        cur= conn.cursor()

        cur.execute("select u.id , u.ime, u.prezime, u.email, u.is_admin from sbp.korisnici as u ;")
        korisnici=cur.fetchall()
        cur.close()
        conn.close()
        response = []
        for row in korisnici:
            x={"id":row[0], "ime":row[1], "prezime":row[2], "email":row[3]}
            if row[4]==True:
                x["rola"]="Admin"
            else:
                x["rola"]="Korisnik"

            response.append(x)
        
        return response

def get_korisnik_by_id_pg(id):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur= conn.cursor()
    cur.execute("select u.id, u.ime, u.prezime, u.email, u.is_admin, u.created_at, u.updated_at from sbp.korisnici as u where u.id ="+ str(id) + ";")
    korisnik=cur.fetchone()
    cur.execute("select ps.id, ps.naslov , ps.opis, ps.link_gpx_traga, s.link_slike from sbp.postignuca as ps  join sbp.slike_postignuca as s on s.postignuce_id=ps.id where ps.korisnik_id=" + str(id) +"and s.id=(select MIN(s2.id) from sbp.slike_postignuca as s2 where s2.postignuce_id= ps.id);")
    postignuca=cur.fetchall()
    response={"id":korisnik[0], "ime":korisnik[1], "prezime":korisnik[2], "email":korisnik[3], "created_at":str(korisnik[5]), "updated_at":str(korisnik[6])}
    cur.close()
    conn.close()
    if korisnik[4]==True:
        response["rola"]="Admin"
    else:
        response["rola"]="Korisnik"
    
    pos=[]
    for row in postignuca:
        x={"id":row[0], "naslov":row[1], "opis":row[2], "link_gpx_traga":row[3], "link_slike":row[4]}
        pos.append(x)
    
    response["postignuca"]= pos
    return response

def post_korisnik_pg(ime, prezime, email, lozinka, rola):
    conn=psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
    cur=conn.cursor()
    cur.execute("INSERT INTO sbp.korisnici (ime, prezime, email, lozinka, is_admin) VALUES ('{}','{}','{}','{}','{}');".format(ime, prezime, email, lozinka, rola))
    conn.commit()
    cur.close()
    conn.close()
    return {"message":"Success", "status":201}