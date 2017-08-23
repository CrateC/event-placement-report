from datetime import datetime

import pendulum
from custom_date_to_number import date_to_number
import sys
sys.setdefaultencoding(‘utf-8’)

def datetime_process(dd):
    dd_type = type(dd)
    # print(f"dd_type: {dd_type}")
    if dd_type is str:
        # print("type: str")
        return data_parse(dd)
    elif dd_type is 'dict':
        pass

    print(f"===============================================")
    print("")

    dl = ['month', 'day', 'time_start']

    try:
        dd['month'] = date_to_number(dd['month'].lower())
    except Exception as e:
        dt_string = dd
        print("//////Exception")

    try:
        dt_string = date_time_to_var(dd)
    except Exception as e:
        print(
            f"""//////Exception
                month_to_number: {e}
                input (dt_string): {dt_string}
            """)
    finally:
        dd['date'] = str(data_parse(dt_string))
        print(
            f"""
                input (dd): {dd}
                result (dd['date']): {dd['date']}
            """)

    return {k: v for k, v in dd.items() if k not in ['month',
                                                     'day',
                                                     'time_start'
                                                    ]}

def data_parse(dt):

    if '-' in str(dt):
        dt = str(dt).split('-', 1)[0]

    try:
        # print(str(pendulum.parse(dt, strict=True).format('%Y-%m-%d %H:%M')))
        return str(pendulum.parse(dt, strict=True).format('%Y-%m-%d %H:%M'))
    except:
        pass

    dt_formats = ['%Y-%m-%d %H:%M',
                  '%b %d %Y %H:%M',
                  '%m %d %Y %H:%M',
                  '%B %d %H:%M',
                  '%Y %B %d',
                 ]
    # print(len(dt_formats))

    for i, dt_format in enumerate(dt_formats):
        try:
            # print(dt)
            # print(str(datetime.strptime(dt, dt_format)))
            return str(datetime.strptime(dt, dt_format))
        except:

            if i == len(dt_formats)-1:
                print(i)
                print(
                    f"""//////Exception
                        dt_format: {dt_format}
                        input (dt): {dt}
                        """)

def month_to_number(month):
    return date_to_number(month.lower())

def date_time_to_var(dd):
    year = datetime.today().year
    return f'{dd["month"]} {dd["day"]} {year} {dd["time_start"]}'
