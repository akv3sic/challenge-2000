from flask import Flask
from flask_restful import Api , Resource
from flask_cors import CORS , cross_origin
from resources.drzave import Drzave
from resources.korisnici import Korisnici, Korisnik
from resources.planine import Planina, Planine
from resources.staze import Staze
from resources.vrhovi import Vrh, Vrhovi
from resources.postignuca import Postignuce, Postigunca


app = Flask(__name__)

CORS(app, supports_credentials=True)
app.config.from_pyfile("config.cfg")
api=Api(app)

api.add_resource(Drzave, "/<string:baza>/drzave"),
api.add_resource(Planine, "/<string:baza>/planine"),
api.add_resource(Korisnici,"/<string:baza>/korisnici"),
api.add_resource(Planina, "/<string:baza>/planine/<string:id>"),
api.add_resource(Vrh, "/<string:baza>/vrhovi/<string:id>"),
api.add_resource(Korisnik, "/<string:baza>/korisnici/<string:id>"),
api.add_resource(Postignuce, "/<string:baza>/postignuca/<string:id>"),
api.add_resource(Vrhovi, "/<string:baza>/vrhovi"),
api.add_resource(Staze, "/<string:baza>/staze"),
api.add_resource(Postigunca, "/<string:baza>/postignuca" ),



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9595, debug=True)
    