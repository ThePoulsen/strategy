## -*- coding: utf-8 -*-

from app import db

class quarter(db.Model):
    __tablename__ = 'quarter'

    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(), unique=True)

class month(db.Model):
    __tablename__ = 'month'

    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(), unique=True)
    abbr = db.Column(db.String(), unique=True)

class weekDay(db.Model):
    __tablename__ = 'weekDay'

    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.Integer, unique=True)
    title = db.Column(db.String(), unique=True)
    abbr = db.Column(db.String(), unique=True)

class calendar(db.Model):
    __tablename__ = 'calendar'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True)
    weekNumber = db.Column(db.Integer)
    year = db.Column(db.Integer)

    weekDay_id = db.Column(db.Integer, db.ForeignKey('weekDay.id'))
    month_id = db.Column(db.Integer, db.ForeignKey('month.id'))
    quarter_id = db.Column(db.Integer, db.ForeignKey('quarter.id'))

class country(db.Model):
    __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    alpha2 = db.Column(db.String())
    alpha3 = db.Column(db.String())
    code = db.Column(db.Integer)

    subRegion_id = db.Column(db.Integer, db.ForeignKey('subRegion.id'))
    language_id = db.Column(db.Integer, db.ForeignKey('language.id'))

class language(db.Model):
    __tablename__ = 'language'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    locale = db.Column(db.String())

class region(db.Model):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    code = db.Column(db.Integer)

class subRegion(db.Model):
    __tablename__ = 'subRegion'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)
    code = db.Column(db.Integer)

    region_id = db.Column(db.Integer, db.ForeignKey('region.id'))

class taskStatus(db.Model):
    __tablename__ = 'taskStatus'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)

class strategyLevel(db.Model):
    __tablename__ = 'strategyLevel'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)

class responsibilityType(db.Model):
    __tablename__ = 'responsibilityType'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)

class responsibilityObject(db.Model):
    __tablename__ = 'responsibilityObject'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)

class responsibilityAssignment(db.Model):
    __tablename__ = 'responsibilityAssignment'
    __table_args__ = (db.UniqueConstraint('responsibilityObject_id', 'reference_uuid', 'responsibilityType_id', 'user_uuid'),)

    id = db.Column(db.Integer, primary_key=True)
    responsibilityObject_id = db.Column(db.Integer, db.ForeignKey('region.id'))
    reference_uuid = db.Column(db.String)
    responsibilityType_id = db.Column(db.Integer, db.ForeignKey('responsibilityType.id'))
    user_uuid = db.Column(db.String)

class UOM(db.Model):
    __tablename__ = 'UOM'
    __table_args__ = (db.UniqueConstraint('title', 'abbr', name='_title_abbr'),)

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)
    abbr = db.Column(db.String())

class actionStatus(db.Model):
    __tablename__ = 'actionStatus'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)

class measurementFrequency(db.Model):
    __tablename__ = 'measurementFrequency'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)

class processType(db.Model):
    __tablename__ = 'processType'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)
    desc = db.Column(db.String())

class indicatorType(db.Model):
    __tablename__ = 'indicatorType'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)
    desc = db.Column(db.String())

class goodPerformance(db.Model):
    __tablename__ = 'goodPerformance'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), unique=True)
    desc = db.Column(db.String())
