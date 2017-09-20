import datetime
import re
import os
import sys
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
print(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'
import django
django.setup()


def convert_query_to_dict(query):
    print(len(query))

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
            dictionary['%s' % i] = dict(zip(columns, item_))
        else:
            print(item_l)
            break

    return dictionary
    #return views.layout(dictionary)
    #return redirect('report')


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
        #print(items)

        items_ = items.split(', ')
        if len(items_) == len(columns):
            dictionary['%s' % i] = dict(zip(columns, items_))
        else:
            print(items)
            break

    return dictionary


def convert_qslist_to_dict(query):

    query_proc = query.replace('[', '').replace(']', '').split('), (')
    from events.models import Event, Platform
    queryset = Platform.objects.values_list('short_name', flat=True)

    columns = ['date', 'name']  # , 'ca', 'pa', 'ka', 'co'
    columns += [x.lower() for x in queryset]

    dictionary = {}
    for i, items in enumerate(query_proc):
        items_l = items#
        if len(items_l.split(", ")) == len(columns):
            items_l = items_l.replace("')", "'").replace("('", "'")
#             print(items_l)
#             break
            dictionary['%s' % i] = dict(zip(columns, items_l.lstrip("'").rstrip("'").split("', '")))
        else:
            print(len(items_l.split(", ")))
            print(items_l.split(", "))
            print(len(columns))
            print(columns)
            break
    print(dictionary)
    return dictionary

if __name__ == "__main__":
 convert_qslist_to_dict("""[('2017-09-20 19:30', 'СПЕКТАКЛЬ «РАЗДЕВАЙСЯ — БУДЕМ… ГОВОРИТЬ»', 'http://caribbean.com.ua/ru/concert_hall_ru/spektakl-razdevaysya-budem-govorit/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/12545.html', 'https://kiev.karabas.com/chernyj-kvadrat-razdevajsya-budem-govorit-6/', 'None', 'https://www.facebook.com/events/1801559460154255', 'None', 'None', 'https://www.facebook.com/events/1801559460154255'), ('2017-09-21 20:00', '«Джаз для взрослых» с Алексеем Коганом & NC 17', 'http://caribbean.com.ua/ru/concert_hall_ru/dzhaz-dlya-vzroslykh-s-alekseem-koganom-2/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/dzhaz_dlia_doroslykh_z_oleksiiem_kohanom.html', 'https://kiev.karabas.com/aleksej-kogan-dzhaz-dlya-vzroslyh-14/', 'None', 'https://www.facebook.com/events/162967787615077', 'None', 'https://www.facebook.com/events/162967787615077', 'https://www.facebook.com/events/162967787615077'), ('2017-09-21 22:00', 'Thursday Dance Storm', 'http://caribbean.com.ua/ru/night_club_ru/thursday-dance-storm-12/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-09-22 20:00', 'ГРУППА «ВИКТОР» ПЕСНИ ЦОЯ', 'http://caribbean.com.ua/ru/concert_hall_ru/gruppa-viktor/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/hrupa_viktor_pisni_tsoia.html', 'https://kiev.karabas.com/gruppa-viktor-1/', 'https://www.concert.ua/eventpage/viktor', 'None', 'None', 'None', 'https://www.facebook.com/events/1067487923381200'), ('2017-09-22 22:00', 'After Midnight Show', 'http://caribbean.com.ua/ru/night_club_ru/after-midnight-show-54/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-09-23 19:00', 'Открытие Евровидения 2017: NAVIBAND (Беларусь)', 'http://caribbean.com.ua/ru/concert_hall_ru/naviband/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/naviband.html', 'https://kiev.karabas.com/naviband/', 'https://www.concert.ua/eventpage/naviband', 'None', 'None', 'None', 'https://www.facebook.com/events/1299069380211157'), ('2017-09-23 22:00', 'After Midnight Show', 'http://caribbean.com.ua/ru/night_club_ru/no-coments-2/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-09-24 19:00', 'Alyona Salova & Latin Legacy', 'http://caribbean.com.ua/ru/concert_hall_ru/alyona-salova-latin-legacy/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/alyona_salova_latin_legacy.html', 'https://kiev.karabas.com/alyona-salova-and-latin-legacy/', 'https://www.concert.ua/eventpage/alyona-salova-latin-legacy', 'https://www.facebook.com/events/419094208492127', 'https://www.facebook.com/events/419094208492127', 'None', 'https://www.facebook.com/events/419094208492127'), ('2017-09-24 22:00', 'Crazy dance party', 'http://caribbean.com.ua/ru/night_club_ru/crazy-dance-party-8/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-09-25 22:00', 'Hot dance party', 'http://caribbean.com.ua/ru/night_club_ru/hot-dance-party-9/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-09-26 22:00', 'Wild dance party', 'http://caribbean.com.ua/ru/night_club_ru/wild-dance-party-7/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-09-27 19:30', 'CПЕКТАКЛЬ «ПРОСТИ.ПРОЩАЙ.МУСОР ВЫНЕСУ САМ»', 'http://caribbean.com.ua/ru/concert_hall_ru/cpektakl-prosti-proshhay-musor-vynesu-s/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/vystava_prosty_proshchai_smittia_ya_vynesu_sam.html', 'https://kiev.karabas.com/chernyj-kvadrat-prosti-proshaj-musor-vynesu-sam-2/', 'https://www.concert.ua/eventpage/prosti-proshai', 'https://www.facebook.com/events/121021031878362', 'None', 'None', 'https://www.facebook.com/events/121021031878362'), ('2017-09-28 20:00', 'Caribbean Jazz Dinner Show. Freedom Jazz с программой KISS', 'http://caribbean.com.ua/ru/concert_hall_ru/caribbean-jazz-dinner-show-freedom-jazz-s-programmoy-kiss-2/', 'None', 'https://kiev.karabas.com/caribbean-jazz-dinner-show-freedom-jazz/', 'https://www.concert.ua/events/caribbean-jazz-dinner-show', 'https://www.facebook.com/events/753420231524703', 'None', 'https://www.facebook.com/events/753420231524703', 'https://www.facebook.com/events/753420231524703'), ('2017-09-28 22:00', 'Thursday Dance Storm', 'http://caribbean.com.ua/ru/night_club_ru/chica-band-4/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-09-29 20:00', 'STAR & ORCHESTRA: Злата Огневич', 'http://caribbean.com.ua/ru/concert_hall_ru/star-orchestra-zlata-ognevich/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/star_orchestra__zlata_ohnevych.html', 'https://kiev.karabas.com/zlata-ognevich-2/', 'None', 'None', 'None', 'None', 'https://www.facebook.com/events/1900823983489674'), ('2017-09-29 22:00', 'After Midnight Show', 'http://caribbean.com.ua/ru/night_club_ru/elton-clapton/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-09-30 22:00', 'After Midnight Show', 'http://caribbean.com.ua/ru/night_club_ru/after-midnight-show-57/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-10-01 20:00', 'Juzzy Buzzy Concert', 'http://caribbean.com.ua/ru/concert_hall_ru/juzzy-buzzy-concert/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-10-02 20:00', 'Jeremy Pelt QUINTET', 'http://caribbean.com.ua/ru/concert_hall_ru/jeremy-pelt-quintet/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/jeremy_pelt_quartet.html', 'https://kiev.karabas.com/jeremy-pelt-quartet/', 'https://www.concert.ua/eventpage/jeremy-pelt-quartet', 'https://www.facebook.com/events/781413432043558', 'None', 'https://www.facebook.com/events/781413432043558', 'https://www.facebook.com/events/781413432043558'), ('2017-10-03 20:00', 'Одна ночь в отеле', 'http://caribbean.com.ua/ru/concert_hall_ru/odna-noch-v-otele/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/odna_nich_v_hoteli.html', 'https://kiev.karabas.com/odna-noch-v-otele/', 'None', 'None', 'None', 'None', 'None'), ('2017-10-04 19:30', 'Спектакль «21 минута До и После Секса или перебор горит»', 'http://caribbean.com.ua/ru/concert_hall_ru/spektakl-21-minuta-do-i-posle-seksa-ili/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/21_mynuta_do_y_posle_seksa_yly_perebor_horyt.html', 'https://kiev.karabas.com/chernyj-kvadrat-21-minuta-do-i-posle-seksa-ili-perebor-gorit/', 'https://www.concert.ua/eventpage/21-minuta-do-i-posle-seksa', 'https://www.facebook.com/events/115163412489948', 'None', 'None', 'https://www.facebook.com/events/115163412489948'), ('2017-10-06 20:00', '«EL MACHO DE CUBA!» RIGOBERT MUSTELIER', 'http://caribbean.com.ua/ru/concert_hall_ru/el-macho-de-cuba-rigobert-mustelier/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/el_macho_de_cuba_rigobert_mustelier.html', 'https://kiev.karabas.com/el-macho-de-cuba-1/', 'https://www.concert.ua/eventpage/rigobert-mustelier', 'None', 'None', 'None', 'https://www.facebook.com/events/145631199361201'), ('2017-10-07 19:00', 'Артемий Троицкий. Моя история в словах и музыке', 'http://caribbean.com.ua/ru/concert_hall_ru/artemiy-troickiy-moya-istoriya-v-slovakh/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/artemyi_troytskyi.html', 'https://kiev.karabas.com/artemij-troickij/', 'https://www.concert.ua/eventpage/artemii-troickii', 'https://www.facebook.com/events/114483842568864', 'None', 'None', 'https://www.facebook.com/events/114483842568864'), ('2017-10-09 19:30', 'Спектакль «Приговор оргазму не подлежит»', 'http://caribbean.com.ua/ru/concert_hall_ru/prigovor-orgazmu-ne-podlezh/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/pryhovor_orhazmu_ne_podlezhyt.html', 'https://kiev.karabas.com/prigovor-orgazmu-ne-podlezhit-2/', 'None', 'None', 'None', 'None', 'None'), ('2017-10-10 20:00', 'Shain Lee', 'http://caribbean.com.ua/ru/concert_hall_ru/shain-lee/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/shain_lee.html', 'https://kiev.karabas.com/shain-lee/', 'https://www.concert.ua/eventpage/shain-lee', 'None', 'None', 'None', 'None'), ('2017-10-11 19:30', 'СПЕКТАКЛЬ «НЕ СЛУЧАЙНЫЕ СВЯЗИ»', 'http://caribbean.com.ua/ru/concert_hall_ru/spektakl-ne-sluchaynye-svyazi/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/vystava_ne_vypadkovi_zviazky.html', 'https://kiev.karabas.com/chernyj-kvadrat-nesluchajnye-svyazi-5/', 'https://www.concert.ua/eventpage/ne-sluchainye-svjazi', 'https://www.facebook.com/events/276063442892395', 'None', 'None', 'https://www.facebook.com/events/276063442892395'), ('2017-10-13 20:00', 'STAR & ORCHESTRA: Владимир Ткаченко', 'http://caribbean.com.ua/ru/concert_hall_ru/star-orchestra-vladimir-tkachenko/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/star_orchestra_volodymyr_tkachenko.html', 'https://kiev.karabas.com/volodimir-tkachenko-1/', 'https://www.concert.ua/eventpage/star-and-orchestra-volodimir-tkachenko', 'https://www.facebook.com/events/170877543488028', 'None', 'https://www.facebook.com/events/170877543488028', 'https://www.facebook.com/events/170877543488028'), ('2017-10-15 20:00', 'Музыкально-танцевальное ретро-шоу «Эпоха Джаза»', 'http://caribbean.com.ua/ru/concert_hall_ru/muzykalno-tancevalnoe-retro-shou-yep/', 'None', 'None', 'None', 'None', 'None', 'None', 'None'), ('2017-10-17 20:00', 'Ricky Martin tribute-show', 'http://caribbean.com.ua/ru/concert_hall_ru/ricky-martin-tribute-show-2/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/ricky_martin_tribute_show.html', 'https://kiev.karabas.com/ricky-martin-tribute-show/', 'None', 'https://www.facebook.com/events/142507473017975', 'None', 'None', 'https://www.facebook.com/events/142507473017975'), ('2017-10-18 19:30', 'Спектакль «Тестостерон или Пир Духа»', 'http://caribbean.com.ua/ru/concert_hall_ru/pir-duha/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/pyr_dukha.html', 'https://kiev.karabas.com/testosteron-ili-pir-duha-2/', 'https://www.concert.ua/events/chernyi-kvadrat', 'https://www.facebook.com/events/1883423651975909', 'None', 'None', 'https://www.facebook.com/events/1883423651975909'), ('2017-10-21 19:00', 'Pippo Pollina', 'http://caribbean.com.ua/ru/concert_hall_ru/pippo-pollina/', 'None', 'None', 'https://www.concert.ua/eventpage/pippo-pollina', 'None', 'None', 'None', 'None'), ('2017-10-25 19:30', 'Спектакль «Любовь бывает дважды»', 'http://caribbean.com.ua/ru/concert_hall_ru/spektakl-lyubov-byvaet-dvazhdy/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/vystava_liubov_buvaie_dvichi.html', 'https://kiev.karabas.com/chernyj-kvadrat-lyubov-byvaet-dvazhdy-4/', 'None', 'None', 'None', 'None', 'None'), ('2017-10-28 20:00', 'STAR & ORCHESTRA: Оля Диброва', 'http://caribbean.com.ua/ru/concert_hall_ru/star-orchestra-olya-dibrova/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/star_orchestra_olia_dibrova.html', 'https://kiev.karabas.com/star-and-orchestra-olya-dibrova/', 'None', 'None', 'None', 'None', 'https://www.facebook.com/events/134178987194691'), ('2017-10-29 18:00', 'The Real Gone Tones (PL) & Ruki’V Bruki (UA) | Juicy Beats Party #3', 'http://caribbean.com.ua/ru/concert_hall_ru/the-real-gone-tones-pl-rukiv-bruki-ua-juicy-beats-party-3-2/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/the_real_gone_tones_pl____ruki_v_bruki__ua___juicy_beats_party__3.html', 'https://kiev.karabas.com/juicy-beats-party-3/', 'https://www.concert.ua/eventpage/the-real-gone-tones', 'https://www.facebook.com/events/281643498983672', 'None', 'None', 'https://www.facebook.com/events/281643498983672'), ('2017-10-31 20:00', 'B&B PROJECT', 'http://caribbean.com.ua/ru/concert_hall_ru/bb-project-2/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/b_b_project.html', 'https://kiev.karabas.com/b-and-b-project-1/', 'https://www.concert.ua/eventpage/bb-project', 'https://www.facebook.com/events/166604710554368', 'None', 'None', 'https://www.facebook.com/events/166604710554368'), ('2017-11-01 19:30', 'СПЕКТАКЛЬ «А-ЛЯ КОБЕЛЯ, ИЛИ ВСЁ, ЧТО ДВИЖЕТСЯ»', 'http://caribbean.com.ua/ru/concert_hall_ru/spektakl-a-lya-kobelya-ili-vsyo-chto-dvi/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/a-lia_kobelia_yly_vs_chto_dvyzhetsia.html', 'https://kiev.karabas.com/chernyj-kvadrat-a-lya-kobelya-ili-vse-chto-dvizhetsya-15/', 'None', 'None', 'None', 'None', 'None'), ('2017-11-14 20:00', 'Павел Табаков', 'http://caribbean.com.ua/ru/concert_hall_ru/pavlo-tabakov-3/', 'http://parter.ua/ru/event/concert-hall/caribbean_club/pavlo_tabakov.html', 'https://kiev.karabas.com/lyubov-zhiva-1/', 'https://www.concert.ua/eventpage/pavlo-tabakov-lyubov-zhiva', 'None', 'None', 'None', 'https://www.facebook.com/events/131952544066095')]
""")
