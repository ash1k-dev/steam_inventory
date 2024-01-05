import datetime

import humanize

humanize.i18n.activate("ru_RU")


def time_convert(time: int):
    return humanize.precisedelta(datetime.timedelta(seconds=time))
