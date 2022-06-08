from flask_restful import Resource, reqparse
from models.vrhovi import *

_vrh_reqparse=reqparse.RequestParser()
_vrh_reqparse.add_argument("planina_id")
_vrh_reqparse.add_argument("naziv", type=str)
_vrh_reqparse.add_argument("nadmorska_visina", type=int)

class Vrh(Resource):

    def get(self, baza, id):
        if baza == "postgres":
            vrh=get_vrh_by_id_pg(id)
        elif baza == "mongo":
            pass
        else:
            return {"status":400, "message":"Bad Request"}, 400
        return {"status":200, "message":"Success", "vrh":vrh}, 200
    
    def put(self, baza, id):
        data=_vrh_reqparse.parse_args()
        planina_id=data["planina_id"]
        naziv=data["naziv"]
        nadmorska_visina=data["nadmorska_visina"]
        if baza == "postgres":
            resp=put_vrh_pg(id, planina_id, naziv, nadmorska_visina)
        elif baza == "mongo":
            pass
        else:
            return {"status":400, "message":"Bad Request"}, 400   
        return resp, 201
    
    def delete(self, baza, id):
        if baza == "postgres":
            resp=del_vrh_pg(id)
        elif baza == "mongo":
            pass
        else:
            return {"status":400, "message":"Bad Request"}, 400  
        return resp, 200 




class Vrhovi(Resource):

    def post(self, baza):
        data=_vrh_reqparse.parse_args()
        planina_id=data["planina_id"]
        naziv=data["naziv"]
        nadmorska_visina=data["nadmorska_visina"]
        if baza == "postgres":
            resp=post_vrh_pg(planina_id, naziv, nadmorska_visina)
        elif baza == "mongo":
            resp=post_vrh_mg(planina_id, naziv, nadmorska_visina)
        else:
            return {"status":400, "message":"Bad Request"}, 400   
        return resp, 201