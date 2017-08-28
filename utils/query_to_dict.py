import datetime
import re


def convert_query_to_dict(query):
    with open('select_out.txt', 'w', encoding='utf-8') as file:
        file.write(str(query))

    query = (
        query.replace("#", "")
        .replace("), (", ";")
        .replace("(date", "date")
        .replace("))", "")
        .replace("(", "", 1)
    )

    ev_list = query.split(';')

    columns = ['date', 'name', 'ca', 'pa', 'co', 'ka']

    dictionary = {}
    for i, items in enumerate(list(ev_list)):
        item_l = items.replace("'", "")

        date = re.search(
            r'(?<=time\()[^\)]+(?=\))',
            item_l.replace("(datetime", "datetime")
        ).group().split(', ')

        dt = datetime.datetime(*map(int, date))
        dt = str(dt).replace(":00", "", 1)

        item_l_ = re.sub('dat[^\)]+', str(dt), item_l)
        item_l_ = re.sub(r'\((?=\d)|(?<=\d)\)', '', item_l_)
        item_ = [x.strip() for x in item_l_.split(',')]

        if len(item_) == len(columns):
            dictionary['%d' % i] = dict(zip(columns, item_))
        else:
            print(item_l)
            break

    return dictionary


def convert_sqlite_query_to_dict(query):
    query = (query.replace("#", "")
                    .replace("), (", ";")
                    .replace("(", "")
                    .replace("[", "")
                    .replace("]", "")
                    .replace("'", "")
                    .replace("None)", "None")
           )
    # print(len(query_a))
    ev_list = query.split(';')
    # print(len(ev_list))
    columns = ['date', 'name', 'ca', 'pa', 'co', 'ka']
    dictionary = {}
    for i, items in enumerate(list(ev_list)):
    #     print(items)

        items_ = items.split(', ')
        if len(items_) == len(columns):
            dictionary['%d' % i]  = dict(zip(columns, items_))
        else:
            print(item_l)
            break

    return dictionary
