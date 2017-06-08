from django import template

register = template.Library()


class Unit(object):
    def __init__(self, name, nsecs):
        self.name = name
        self.plural = name + "s"
        self.nsecs = nsecs

SECOND = Unit("second",1)
MINUTE = Unit("minute", SECOND.nsecs * 60)
HOUR = Unit("hour", MINUTE.nsecs * 60)
DAY = Unit("day", HOUR.nsecs * 24)
WEEK = Unit("week", DAY.nsecs * 7)
MONTH = Unit("month", DAY.nsecs * 30)
YEAR = Unit("year", DAY.nsecs * 365)

@register.filter
def hc_duration(td):
    remaining_seconds = int(td.total_seconds()) 
    result = []

    for unit in (YEAR, MONTH, WEEK, DAY, HOUR, MINUTE,SECOND):
        if unit == YEAR and remaining_seconds % unit.nsecs != 0:
            # Say "8 days" instead of "1 week 1 day"
            continue

        v, remaining_seconds = divmod(remaining_seconds, unit.nsecs)
        if v == 1:
            result.append("1 %s" % unit.name)
        elif v > 1:
            result.append("%d %s" % (v, unit.plural))

    return " ".join(result)
