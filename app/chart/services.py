from app.masterData.models import month, calendar
from app.performance.models import indicatorTarget, indicator
from datetime import date, datetime

epoch = datetime.utcfromtimestamp(0)

def miliseconds(date=None, dt=None):
    if date == None and dt != None:        
        return (dt - epoch).total_seconds() * 1000.0
    elif date != None and dt == None:
        dt = datetime.combine(date, datetime.min.time())
        return (dt - epoch).total_seconds() * 1000.0

def targetRange(indicator_uuid, tenant_uuid, fillMissingData=False):
    ind = indicator.query.filter_by(uuid=indicator_uuid,
                                    tenant_uuid=tenant_uuid).first()
#    targets = ind.targets
    targets = [[t.validFrom, t.validTo, t.fromTarget, t.toTarget] for t in ind.targets]
    targets.sort(key = lambda row: row[0])
    data = {}
    fromData = []
    toData = []
    for t in targets:    
        validFrom = miliseconds(calendar.query.filter_by(id=t[0]).first().date)
        validTo = miliseconds(calendar.query.filter_by(id=t[1]).first().date)
                
        fromData.append([validFrom, t[2]])
        fromData.append([validTo, t[2]])
        if not fillMissingData:
            fromData.append([None,None])
        toData.append([validFrom, t[3]])
        toData.append([validTo, t[3]])
        if not fillMissingData:
            toData.append([None, None])
    
    data['from'] = fromData
    data['to'] = toData
    return data