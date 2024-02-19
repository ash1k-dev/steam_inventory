import datetime

import humanize

humanize.i18n.activate("ru_RU")


def time_convert(time: int) -> str:
    """Конвертирует время в часы:минуты:секунды"""
    return humanize.precisedelta(datetime.timedelta(seconds=time))
