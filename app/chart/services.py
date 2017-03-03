from app.masterData.models import month, calendar
from app.performance.models import indicatorTarget
from datetime import date

def mthRange(indicator_uuid, tenant_uuid, year):
    data = {}
    months = [[m.no, str(m.abbr)] for m in month.query.all()]
    months.insert(0,0)
    data['xTicks'] = months

    target = indicatorTarget.query.filter_by(indicator_uuid=indicator_uuid,
                                             tenant_uuid=tenant_uuid).all()

    date['fromTarget']=[]
    date['toTarget']=[]
    for t in target:
        validFrom = calendar.query.filter_by(year=year, id=t.validFrom).first().date
        validTo = calendar.query.filter_by(year=year, id=t.validFrom).first().date
        fromTarget = t.fromTarget
        toTarget = t.toTarget

        dd = [validFrom + timedelta(days=x) for x in range((validTo-validFrom).days + 1)]
        for d in dd:
            date['fromTarget'].append([d.month, fromTarget])


def mthAbove():
    pass

def mthBelow():
    pass

def mthOn():
    pass

def weekRange():
    pass

def weekAbove():
    pass

def weekBelow():
    pass

def weekOn():
    pass
