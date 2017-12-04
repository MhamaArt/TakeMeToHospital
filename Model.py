from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey, Time, Boolean
from geoalchemy2 import Geography

Base = declarative_base()


class SymptomLocation(Base):
    __tablename__ = 'SymptomLocation'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)

    symptoms = relationship(
        'Symptom',
        cascade="all, delete-orphan",
        back_populates='locations'
    )

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Symptom(Base):
    __tablename__ = 'Symptom'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    location = Column(Integer, ForeignKey('SymptomLocation.id'))
    description = Column(String(500))
    gender = Column(Boolean)
    locations = relationship(
        SymptomLocation,
        back_populates='symptoms'
    )

    deceases = relationship(
        'Decease',
        secondary='SymptomDecease',
        back_populates='symptoms'
    )

    def __init__(self, name, loc=None, gen=None, desc=None):
        self.name = name
        self.location = loc
        self.description = desc
        self.gender = gen


SymptomDecease = Table(
    'SymptomDecease', Base.metadata,
    Column('symptom', Integer, ForeignKey('Symptom.id'), nullable=False),
    Column('decease', Integer, ForeignKey('Decease.id'), nullable=False)
)


class Decease(Base):
    __tablename__ = 'Decease'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(500))

    symptoms = relationship(
        Symptom,
        secondary=SymptomDecease,
        back_populates='deceases'
    )

    specialities = relationship(
        'Speciality',
        secondary='DeceaseSpeciality',
        back_populates='deceases'
    )

    def __init__(self, name):
        self.name = name


DeceaseSpeciality = Table(
    'DeceaseSpeciality', Base.metadata,
    Column('decease', Integer, ForeignKey('Decease.id'), nullable=False),
    Column('speciality', Integer, ForeignKey('Speciality.id'), nullable=False)
)


class Speciality(Base):
    __tablename__ = 'Speciality'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String(500))

    deceases = relationship(
        Decease,
        secondary=DeceaseSpeciality,
        back_populates='specialities'
    )

    doctors = relationship(
        'Doctor',
        secondary='SpecialityDoctor',
        back_populates='specialities'
    )

    def __init__(self, name):
        self.name = name


SpecialityDoctor = Table(
    'SpecialityDoctor', Base.metadata,
    Column('speciality', Integer, ForeignKey('Speciality.id'), nullable=False),
    Column('doctor', Integer, ForeignKey('Doctor.id'), nullable=False)
)


class Doctor(Base):
    __tablename__ = 'Doctor'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    second_name = Column(String(30), nullable=False)
    fathers_name = Column(String(30))

    phone = Column(String(12))
    cabinet = Column(String(12))

    specialities = relationship(
        Speciality,
        secondary=SpecialityDoctor,
        back_populates='doctors'
    )

    clinic = Column(Integer, ForeignKey('Clinic.id'), nullable=False)
    clinics = relationship(
        'Clinic',
        back_populates='doctors'
    )

    def __init__(self, first_name, second_name):
        self.first_name = first_name
        self.second_name = second_name


class Clinic(Base):
    __tablename__ = 'Clinic'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    location = Column(Geography, nullable=False)
    opening = Column(Time)
    closure = Column(Time)

    doctors = relationship(
        Doctor,
        cascade="all, delete-orphan",
        back_populates='clinics'
    )

    def __init__(self, name, location):
        self.name = name
        self.location = Geography.from_text(location)


def create_schema(engine):
    Base.metadata.create_all(engine)


def delete_schema(engine):
    Base.metadata.drop_all(engine)



    #     session.add_all([
    #     Symptom("Втрату слуху", 1, None, None),
    #     Symptom("Капловухість", 1, None, None),
    #     Symptom("Шум у вухах", 1, None, None),
    #     Symptom("Амнезія", 2, None, None),
    #     Symptom("Випадіння волосся", 2, None, None),
    #     Symptom("Галюцинації", 2, None, None),
    #     Symptom("Жар", 2, None, None),
    #     Symptom("Запаморочення", 2, None, None),
    #     Symptom("Тремор", 2, None, None)
    # ])
    # session.commit()
