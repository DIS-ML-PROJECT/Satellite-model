from typing import Tuple
from datetime import date

def surveyyear_to_range(year: int,satellitename: str) -> Tuple[str, str]:
    if satellitename == "S2":
        if 2012<=year<=2015:
            start_date = '2015-06-24'
            end_date = '2016-01-01'
        elif year == 2016:
            start_date = '2016-01-01'
            end_date = '2017-01-01'
        elif year == 2017:
            start_date = '2017-01-01'
            end_date = '2018-01-01'
        elif year == 2018:
            start_date = '2018-01-01'
            end_date = '2019-01-01'
        elif year == 2019:
            start_date = '2019-01-01'
            end_date = '2020-01-01'
        elif year == 2020:
            start_date = '2020-01-01'
            end_date = '2021-01-01'
        elif year == 2021:
            start_date = '2021-01-01'
            end_date = date.today().strftime('%Y-%m-%d')
        else:
            raise ValueError(f'Jahr wird nicht unterstützt: {year}. '
                            'Alle Jahre vor 2012 werden nicht beachtet.')
    elif satellitename == "nl":
        if year == 2012:
            start_date = '2012-01-01'
            end_date = '2013-01-01'
        elif year == 2013:
            start_date = '2013-01-01'
            end_date = '2014-01-01'
        elif year == 2014:
            start_date = '2014-01-01'
            end_date = '2015-01-01'
        elif year == 2015:
            start_date = '2015-01-01'
            end_date = '2016-01-01'
        elif year == 2016:
            start_date = '2016-01-01'
            end_date = '2017-01-01'
        elif year == 2017:
            start_date = '2017-01-01'
            end_date = '2018-01-01'
        elif year == 2018:
            start_date = '2018-01-01'
            end_date = '2019-01-01'
        elif year == 2019:
            start_date = '2019-01-01'
            end_date = '2020-01-01'
        elif year == 2020:
            start_date = '2020-01-01'
            end_date = '2021-01-01'
        elif year == 2021:
            start_date = '2021-01-01'
            end_date = date.today().strftime('%Y-%m-%d')
        else:
            raise ValueError(f'Jahr wird nicht unterstützt: {year}. '
                            'Alle Jahre vor 2012 werden nicht beachtet.')
    return start_date, end_date