from flask_restful import Resource, reqparse
from flask import request
from models.drzave import get_drzave_pg, post_drzave_pg

_drzava_parser=reqparse.RequestParser()
_drzava_parser.add_argument("naziv", type=str)

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
        if baza=="postgres":
            data= _drzava_parser.parse_args()
            naziv=data["naziv"]
            resp=post_drzave_pg(naziv)
        elif baza == "mongo":
            pass
        else:
            return{"status":400, "message":"Bad Request"}, 400
        return resp, 201