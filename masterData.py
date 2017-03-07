## -*- coding: utf-8 -*-
import csv
from app import db
from app.masterData.models import weekDay, month, quarter, calendar, region, subRegion, country, taskStatus, responsibilityType, responsibilityObject, strategyLevel, UOM, measurementFrequency, actionStatus, processType, indicatorType, goodPerformance, chartType, containerSize

weekDays = [('Monday','Mon','1'),
        ('Tuesday','Tue','2'),
        ('Wednesday','Wed','3'),
        ('Thursday','Thu','4'),
        ('Friday','Fri','5'),
        ('Saturday','Sat','6'),
        ('SunDay','Sun','7')]

months = [('January','Jan','1'),
          ('February','Feb','2'),
          ('March','Mar','3'),
          ('April','Apr','4'),
          ('May','May','5'),
          ('June','Jun','6'),
          ('July','Jul','7'),
          ('August','Aug','8'),
          ('September','Sep','9'),
          ('October','Oct','10'),
          ('November','Nov','11'),
          ('December','Dec','12')]

quarters = [('Q1','1'),
            ('Q2','2'),
            ('Q3','3'),
            ('Q4','4')]

taskStat = ['Not started','In progress','On hold','Complete']

actionStat = ['Planned but not started','Late','In progress','Complete','Cancelled']

stratLevel = ['Level 0','Level 1','Level 2','Level 3']

respObject = ['Mission','Vision','Objective','Strategy','Project','Task','Task Initiator','Indicator']

respType = ['Owner','Driver','Responsible','Support','Resources','Expertise']

uom = ['Absolute value','Currency','Percent','Index','Milestones','Days','Hours','Minutes','Seconds']

measurementFreq = ['Daily','Weekly','Monthly','Quarterly']

processTyp = ['Safety','Quality','Delivery','Cost','Productivity']

indicatorTyp = ['KPI','PPI','PI','KRI']

goodPerf = ['Above target', 'Below target', 'On target', 'Range']

chartTyp = ['line', 'area']

containerSiz = [('small','col-xs-12 col-sm-12 col-md-3 col-lg-3'),
                 ('medium','col-xs-12 col-sm-12 col-md-6 col-lg-6'),
                 ('large','col-xs-12 col-sm-12 col-md-9 col-lg-9'),
                 ('veryLarge','col-xs-12 col-sm-12 col-md-12 col-lg-12')]

calData = csv.reader(open('calendar.csv','r'), delimiter=';')
next(calData, None)

world = csv.reader(open('world.csv','r'))
next(world, None)

def createMasterData():
    for ct in chartTyp:
        list = [r.title for r in chartType.query.all()]
        if not ct in list:
            db.session.add(chartType(title=ct))

    for cs in containerSiz:
        list = [r.title for r in containerSize.query.all()]
        if not cs[0] in list:
            db.session.add(containerSize(title=cs[0], size=cs[1]))

    for g in goodPerf:
        list = [r.title for r in goodPerformance.query.all()]
        if not g in list:
            db.session.add(goodPerformance(title=g))

    for p in processTyp:
        list = [r.title for r in processType.query.all()]
        if not p in list:
            db.session.add(processType(title=p))

    for t in indicatorTyp:
        list = [r.title for r in indicatorType.query.all()]
        if not t in list:
            db.session.add(indicatorType(title=t))

    for mf in measurementFreq:
        list = [r.title for r in measurementFrequency.query.all()]
        if not mf in list:
            db.session.add(measurementFrequency(title=mf))

    for st in actionStat:
        list = [r.title for r in actionStatus.query.all()]
        if not st in list:
            db.session.add(actionStatus(title=st))

    for unit in uom:
        list = [r.title for r in UOM.query.all()]
        if not unit in list:
            db.session.add(UOM(title=unit))

    for obj in respObject:
        list = [r.title for r in responsibilityObject.query.all()]
        if not obj in list:
            db.session.add(responsibilityObject(title=obj))

    for typ in respType:
        list = [r.title for r in responsibilityType.query.all()]
        if not typ in list:
            db.session.add(responsibilityType(title=typ))

    for stat in taskStat:
        list = [r.title for r in taskStatus.query.all()]
        if not stat in list:
            db.session.add(taskStatus(title=stat))

    for lvl in stratLevel:
        list = [r.title for r in strategyLevel.query.all()]
        if not lvl in list:
            db.session.add(strategyLevel(title=lvl))

    for day, abbr, no in weekDays:
        if not weekDay.query.filter_by(no=no,title=day,abbr=abbr).first():
            db.session.add(weekDay(no=no,title=day,abbr=abbr))

    for mo, abbr, no in months:
        if not month.query.filter_by(no=no,title=mo,abbr=abbr).first():
            db.session.add(month(no=no,title=mo,abbr=abbr))

    for qty, no in quarters:
        if not quarter.query.filter_by(no=no,title=qty).first():
            db.session.add(quarter(no=no,title=qty))

    for calDate, day, week, mo, qty, year in calData:
        weekDay_id = weekDay.query.filter_by(no=day).first().id
        month_id = month.query.filter_by(no=mo).first().id
        quarter_id = quarter.query.filter_by(no=qty).first().id

        if not calendar.query.filter_by(date=calDate,
                                        weekDay_id=weekDay_id,
                                        weekNumber=week,
                                        month_id=month_id,
                                        quarter_id=quarter_id,
                                        year=year).first():

            calEntry = calendar(date=calDate,
                                weekDay_id=weekDay_id,
                                weekNumber=week,
                                month_id=month_id,
                                quarter_id=quarter_id,
                                year=year)
            db.session.add(calEntry)

    for r in world:
        if r[5]:
            if not region.query.filter_by(name=r[5]).first():
                db.session.add(region(name=r[5],code=r[7]))
        if r[6]:
            if not subRegion.query.filter_by(name=r[6]).first():
                reg = region.query.filter_by(code=r[7]).first()
                db.session.add(subRegion(name=r[6],code=r[8], region_id=reg.id))
        if r[0]:
            if not country.query.filter_by(name=r[0]).first():
                if r[6]:
                    subReg = subRegion.query.filter_by(code=r[8]).first()
                    db.session.add(country(name=r[0],
                                       alpha2=r[1],
                                       alpha3=r[2],
                                       code=r[3],
                                       subRegion_id=subReg.id))
                else:
                    db.session.add(country(name=r[0],
                                       alpha2=r[1],
                                       alpha3=r[2],
                                       code=r[3]))

    db.session.commit()
