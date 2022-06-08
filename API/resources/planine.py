from flask_restful import Resource, reqparse
from flask import request
from models.planine import *

_planina_reqparse= reqparse.RequestParser()
_planina_reqparse.add_argument("drzava_id")
_planina_reqparse.add_argument("naziv", type=str)

class Planine(Resource):

    def get(self, baza):
        if baza == "postgres":
            planine= get_planine_pg()
        elif baza == "mongo":
            planine=get_planine_mg()
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
            resp=post_planine_mg(drzava_id, naziv)
        else:
            return{"status":400, "message":"Bad Request"}, 400
        return resp, 201


class Planina(Resource):
    def get(self, baza, id):
        if baza == "postgres":
            id = int(id)
            planina= get_planina_by_id_pg(id)
        elif baza =="mongo":
            planina=get_planina_by_id_mg(id)
        else:
            return {"status":400, "message":"Bad Request"}, 400
        return {"status":200, "message":"Success", "planine":planina}, 200

    def put(self, baza, id):
        data=_planina_reqparse.parse_args()
        drzava_id=data["drzava_id"]
        naziv=data["naziv"]
        if baza == "postgres":
            
            resp= put_planina_pg(id,drzava_id, naziv)
            
        elif baza =="mongo":
            pass
        else:
            return {"status":400, "message":"Bad Request"}, 400
        return resp, 201

    def delete(self, baza , id):
        if baza == "postgres":
            
            resp= del_planina_pg(id)
            
        elif baza =="mongo":
            pass
        else:
            return {"status":400, "message":"Bad Request"}, 400
        return resp, 200