from flask_restful import Resource, reqparse
from models.postignuca import get_postignuce_by_id_pg , post_postignuce_pg

_p_req=reqparse.RequestParser()
_p_req.add_argument("korisnik_id", type=int)
_p_req.add_argument("naslov", type=str)
_p_req.add_argument("opis", type = str)
_p_req.add_argument("link_gpx_traga", type=str)



class Postignuce(Resource):
    def get(self,baza, id):
        if baza == "postgres":
            pos=get_postignuce_by_id_pg(id)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return{"status":200, "message":"Success", "postignuce":pos}, 200

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
