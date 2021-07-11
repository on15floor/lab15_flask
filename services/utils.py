from datetime import datetime
from pytz import timezone
from config import Vars


def localize(d: datetime) -> datetime:
    return timezone(Vars.TIME_ZONE).localize(d)


def get_now() -> datetime:
    return localize(datetime.now())
