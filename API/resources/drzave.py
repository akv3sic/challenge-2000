from flask_restful import Resource, reqparse

from models.drzave import *
_drzava_parser=reqparse.RequestParser()
_drzava_parser.add_argument("naziv", type=str)
_drzava_parser.add_argument("id", type=int)


class Drzave(Resource):

    def get(self, baza):
        if baza=="postgres":
            drzave = get_drzave_pg()
        elif baza=="mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400
        
        return{"status":200, "message":"Success", "drzave":drzave}, 200

    def post(self, baza):
        data= _drzava_parser.parse_args()
        naziv=data["naziv"]
        if baza=="postgres":
            
            resp=post_drzave_pg(naziv)
        elif baza == "mongo":
            resp = post_drzave_mg(naziv)
        else:
            return{"status":400, "message":"Bad Request"}, 400
        return resp, 201
    
class Drzava(Resource):

    def put(self, baza, id):
        if baza=="postgres":
            data= _drzava_parser.parse_args()
            naziv=data["naziv"]
            resp=put_drzave_pg(id, naziv)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400
        return resp, 201

    def delete(self, baza, id):
        if baza=="postgres":
            resp=del_drzava_pg(id)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400
        return resp, 201
