from datetime import datetime
from events.enums import Precision
from dateutil.parser import parse
from typing import Union


MONTH_CASES = {
    'nomn': {
        1: 'январь', 2: 'февраль', 3: 'март',
        4: 'апрель', 5: 'май', 6: 'июнь',
        7: 'июль', 8: 'август', 9: 'сентябрь',
        10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'
    },
    'gent': {
        1: 'января', 2: 'февраля', 3: 'марта',
        4: 'апреля', 5: 'мая', 6: 'июня',
        7: 'июля', 8: 'августа', 9: 'сентября',
        10: 'октября', 11: 'ноября', 12: 'декабря'
    }
}


class DateRange:
    def __init__(
            self,
            start: str,
            end: str,
            precision: Precision) -> None:
        self.start: str = start
        self.end: str = end
        self.precision: Precision = precision
        self.start_date: datetime = self._parse_date(self.start)
        self.end_date: datetime = self._parse_date(self.end)

    def _parse_date(self, date_str: str) -> Union[datetime, None]:
        try:
            if not date_str:
                return None

            return parse(date_str, dayfirst=True, fuzzy=True)
        except (ValueError, TypeError):
            raise ValueError(f'Не удалось распознать дату: {date_str}')

    def _format_single_date(self, date: datetime) -> str:
        if not date:
            return None

        if self.precision == Precision.YEAR:
            return date.strftime('%Y')
        elif self.precision == Precision.MONTH:
            return f'{MONTH_CASES['nomn'][date.month]} {date.year}'
        elif self.precision == Precision.DAY:
            return f'{date.day} {MONTH_CASES['gent'][date.month]} {date.year}'
        elif self.precision == Precision.TIME:
            return f'{date.day} {MONTH_CASES['gent'][date.month]} {date.year} {date.strftime('%H:%M')}'
        else:
            return str(date)

    def range_display(self) -> str:
        start_fmt = self._format_single_date(self.start_date)
        end_fmt = self._format_single_date(self.end_date)

        if end_fmt is None:
            return f'{start_fmt}'
        elif start_fmt is not None:
            if (self.precision == Precision.TIME and
                    self.start_date.date() == self.end_date.date()):
                day = self.start_date.day
                month = MONTH_CASES['gent'][self.start_date.month]
                year = self.start_date.year

                start_time = self.start_date.strftime('%H:%M')
                end_time = self.end_date.strftime('%H:%M')

                return f'{day} {month} {year} {start_time}-{end_time}'
            return f'{start_fmt} - {end_fmt}'
        else:
            return ''
