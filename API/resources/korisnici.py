from flask_restful import Resource, reqparse
from models.korisnici import get_korisnici_pg, get_korisnik_by_id_pg, post_korisnik_pg

_k_req= reqparse.RequestParser()
_k_req.add_argument("ime", type=str)
_k_req.add_argument("prezime",type=str)
_k_req.add_argument("email",type=str)
_k_req.add_argument("lozinka",type=str)
_k_req.add_argument("rola", type=str)

class Korisnici(Resource):
    def get(self, baza):
        if baza == "postgres":
            korisnici=get_korisnici_pg()
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return{"status":200, "message":"Success", "korisnici":korisnici}, 200

    def post(self, baza):
        data=_k_req.parse_args()
        ime=data["ime"]
        prezime=data["prezime"]
        email=data["email"]
        lozinka=data["lozinka"]
        if data["rola"]=="Admin":
            rola=True
        else:
            rola=False
        if baza == "postgres":
            resp=post_korisnik_pg(ime, prezime, email, lozinka, rola)
        elif baza == "mongo":
            pass
        else:
            return {"status":400, "message":"Bad Request"}, 400   
        return resp, 201
        



class Korisnik(Resource):
    def get(self, baza, id):
        if baza == "postgres":
            korisnik=get_korisnik_by_id_pg(id)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return{"status":200, "message":"Success", "korisnici":korisnik}, 200
