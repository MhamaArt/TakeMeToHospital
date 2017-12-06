import falcon
import json
from waitress import serve
from Settings import *
from sqlalchemy import create_engine, or_, and_, func, any_, desc,asc
from sqlalchemy.orm import sessionmaker
from Model import *
from geoalchemy2 import func


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
                    .filter(or_(
                        Symptom.gender == None,
                        Symptom.gender == req.get_header('gender')
                        ))
                    .order_by(asc(Symptom.name)).all()
                ]
            } for location in session.query(SymptomLocation).all()])
        session.close()
        resp.status = falcon.HTTP_200


class Hospital(object):
    def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_JSON

        session = Session()

        matchedSpecs = session.query(Speciality.id) \
            .join(Speciality.symptoms) \
            .filter(Symptom.id.in_(json.loads(req.get_header('symptoms')))) \
            .all()

        location = 'POINT('+req.get_header("latitude")+' '+req.get_header("longitude")+')'

        clinicsForSpecs = {}
        for specId in matchedSpecs:
            results = session.query(Clinic.id) \
                .join(Clinic.doctors) \
                .join(Doctor.specialities) \
                .filter(Speciality.id == specId) \
                .distinct(Clinic.id).all()

            clinicsList = []
            for idd in results:
                clinicsList.append(idd)
                clinicsForSpecs[specId] = clinicsList

        distinctClinicsList = []
        for specId in clinicsForSpecs:
            for clinicId in clinicsForSpecs[specId]:
                if clinicId not in distinctClinicsList:
                    distinctClinicsList.append(clinicId)

        for specId in clinicsForSpecs:
            for clinicId in distinctClinicsList:
                if clinicId not in clinicsForSpecs[specId]:
                    distinctClinicsList.remove(clinicId)

        closestClinic = session.query(Clinic.id) \
            .filter(Clinic.id.in_(distinctClinicsList)) \
            .order_by(asc(func.ST_Distance(Clinic.location, func.ST_GeographyFromText(location)))) \
            .first()

        if closestClinic is None:
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({})
            return

        clinicOutput = session.query(Clinic).filter(Clinic.id == closestClinic.id).first()

        doctorsOutput = session.query(Doctor).join(Doctor.clinics).join(Doctor.specialities) \
            .filter(Clinic.id == closestClinic.id).filter(Speciality.id.in_(matchedSpecs)).distinct(Doctor.id).all()

        specsOutput = session.query(Speciality.name).join(Clinic.doctors).join(Doctor.specialities)\
            .filter(Clinic.id == closestClinic.id).filter(Speciality.id.in_(matchedSpecs))

        losationStringX = session.query(func.ST_X(clinicOutput.location).label('x')).first()
        losationStringY = session.query(func.ST_Y(clinicOutput.location).label('y')).first()

        respp = {
            'name': clinicOutput.name,
            'location': str(losationStringX.x) + ' ' + str(losationStringY.y),
            'opening': clinicOutput.opening,
            'closure': clinicOutput.closure,
            'doctors':  [{
                'fname': doctor.first_name,
                'sname': doctor.second_name,
                'pname': doctor.fathers_name,
                'specialities': [
                    spec.name for spec in specsOutput.filter(Doctor.id == doctor.id).all()
                ],
                'cabinet': doctor.cabinet,
                'phone': doctor.phone
                } for doctor in doctorsOutput
            ]
        }
        resp.body = json.dumps(respp)
        resp.status = falcon.HTTP_200

if __name__ == "__main__":
    # Database connection setup
    engine = create_engine(DB_TYPE+'://'+DB_LOGIN+':'+DB_PASSWORD+'@'+DB_HOST+':'+DB_PORT+'/'+DB, echo=True)
    Session = sessionmaker(bind=engine)

    create_schema(engine)

    # # HTTP server setup
    # app = falcon.API()
    # app.add_route('/symptoms', Symptoms())
    # app.add_route('/hospital', Hospital())
    #
    # serve(app, listen='*:5678')
