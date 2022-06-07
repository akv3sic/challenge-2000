from flask_restful import Resource, reqparse
from models.postignuca import *

_p_req=reqparse.RequestParser()
_p_req.add_argument("korisnik_id", type=int)
_p_req.add_argument("naslov", type=str)
_p_req.add_argument("opis", type = str)
_p_req.add_argument("link_gpx_traga", type=str)

_s_req=reqparse.RequestParser()
_s_req.add_argument("link_slike", type=str)
_s_req.add_argument("naziv", type=str)
_s_req.add_argument("opis", type=str)

_k_parse=reqparse.RequestParser()
_k_parse.add_argument("komentar_sadrzaj", type=str)
_k_parse.add_argument("korisnik_id", type=int)



class Postignuce(Resource):
    def get(self,baza, id):
        if baza == "postgres":
            pos=get_postignuce_by_id_pg(id)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return{"status":200, "message":"Success", "postignuce":pos}, 200
    
    def put(self, baza, id):
        data=_p_req.parse_args()
        korisnik_id=data["korisnik_id"]
        naslov=data["naslov"]
        opis=data["opis"]
        link_gpx_traga=data["link_gpx_traga"]
        if baza == "postgres":
            resp=put_postignuce_pg(id, korisnik_id, naslov, opis, link_gpx_traga)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return resp, 201

    def delete(self, baza , id):
        if baza == "postgres":
            resp=del_postignuce_pg(id)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return resp, 200


class Postigunca(Resource):
    def post(self, baza):
        data=_p_req.parse_args()
        korisnik_id=data["korisnik_id"]
        naslov=data["naslov"]
        opis=data["opis"]
        link_gpx_traga=data["link_gpx_traga"]
        if baza == "postgres":
            resp=post_postignuce_pg(korisnik_id, naslov, opis, link_gpx_traga)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return resp, 201

class PostignucaSlike(Resource):
    def post(self, baza, id):
        data=_s_req.parse_args()
        if baza == "postgres":
            resp=post_slike_pg(id, data["link_slike"], data["naziv"],data["opis"])

        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return resp, 201


class PostignucaKomentari(Resource):
    def post(self, baza, id):
        data=_k_parse.parse_args()
        if baza == "postgres":
            resp=post_komentara_pg(id, data["komentar_sadrzaj"], data["korisnik_id"])


        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return resp, 201
