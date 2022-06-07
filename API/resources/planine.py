from flask_restful import Resource, reqparse
from flask import request
from models.planine import get_planine_pg , get_planina_by_id_pg, post_planine_pg

_planina_reqparse= reqparse.RequestParser()
_planina_reqparse.add_argument("drzava_id", type=int)
_planina_reqparse.add_argument("naziv", type=str)

class Planine(Resource):

    def get(self, baza):
        if baza == "postgres":
            planine= get_planine_pg()
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400

        return {"status":200, "message":"Success", "planine":planine}, 200

    def post(self, baza):
        data=_planina_reqparse.parse_args()
        drzava_id=data["drzava_id"]
        naziv=data["naziv"]
        if baza == "postgres":
            resp=post_planine_pg(drzava_id, naziv)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400
        return resp, 201


class Planina(Resource):
    def get(self, baza, id):
        if baza == "postgres":
            id = int(id)
            planina= get_planina_by_id_pg(id)
        elif baza =="mongo":
            pass
        else:
            return {"status":400, "message":"Bad Request"}, 400
        return {"status":200, "message":"Success", "planine":planina}, 200

    