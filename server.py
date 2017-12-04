import falcon
import json
from waitress import serve
from Settings import *
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from Model import *


class Symptoms(object):
    def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_JSON

        session = Session()
        resp.body = json.dumps([{
            'id': location.id,
            'name': location.name,
            'symptoms': [{
                'id': s.id,
                'name': s.name,
                'gender': s.gender,
                'description': s.description
                } for s in session.query(Symptom)
                    .filter(Symptom.location == location.id)
                    # .filter(or_(
                    #     Symptom.gender == None,
                    #     Symptom.gender == req.get_header('gender')
                    #     ))
                    .all()
                ]
            } for location in session.query(SymptomLocation).all()])
        session.close()
        resp.status = falcon.HTTP_200


class Hospital(object):
    def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_JSON

        session = Session()

        # session.query(Decease).filter(Decease.symptoms.any())



        respp = {
            'name': 'Central clinic 2',
            'location': '50.450789, 30.497336',
            'opening': '9:00',
            'closure': '19:00',
            'doctors': [{
                'fname': "Vasiliy",
                'sname': 'Lasorischinets',
                'pname': 'V',
                'specialities': ['Surgeon', 'Therapy'],
                'cabinet': '410',
                'phone': '+380632280797'
                }]
        }
        resp.body = json.dumps(respp)
        resp.status = falcon.HTTP_200


if __name__ == "__main__":
    # Database connection setup
    engine = create_engine(DB_TYPE+'://'+DB_LOGIN+':'+DB_PASSWORD+'@'+DB_HOST+':'+DB_PORT+'/'+DB, echo=True)
    Session = sessionmaker(bind=engine)

    # HTTP server setup
    app = falcon.API()

    session = Session()

    # session.query(Decease).filter(Decease.symptoms.any(Decease == ))

    app.add_route('/symptoms', Symptoms())
    app.add_route('/hospital', Hospital())

    # serve(app, listen='*:5678')
