import ast
import html
import os
import re
import sys



class ImportDb:

    def __init__(self, path):

        # timezone.activate(pytz.timezone("Europe/Kiev"))
        self.path = path
        # print(path)

        # self.PLATFORM_NAMES = {
        #         'CA': 'Caribbean Club',
        #         'KA': 'Karabas.com',
        #         'CO': 'Concert.ua',
        #         'PA': "Parter.ua"
        # }

        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pl_path = os.path.join(self.project_dir, 'spiders', 'db_import', 'PL_NAMES')

        with open(pl_path, 'r') as plfile:
            PL_NAMES = ast.literal_eval(plfile.read())

        self.PLATFORM_NAMES = {y:x for x,y in PL_NAMES.items()}

    def import_to_db(self):

        #project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #print(project_dir)
        sys.path.append(self.project_dir)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'

        import django
        django.setup()
        from events.models import Event, Platform


        place_code = re.search(r'[^\/|\\|fb_]+(?=_events)', self.path).group()
        platform_name = self.PLATFORM_NAMES[place_code]
        print(platform_name)
        # pass

        with open(self.path, encoding="utf-8", newline='') as dictfile:
            ev_dict = ast.literal_eval(dictfile.read())
        i = 0
        for lang, value in ev_dict.items():

            for ev_value in value.values():
                # print(ev_value['link'])
                # print(ev_value['name'])
                # print(ev_value['date'])

                event = Event()
                event.platform = Platform.objects.get(
                        name=platform_name
                )
                event.name = html.unescape(ev_value['name'])
                event.link = ev_value['link']
                event.date = ev_value['date']
                event.language = lang
                try:
                    event.save()
                    i += 1
                except Exception as e:
                    pass  # print(e)
        print("added: %s" % i)
        return "'%s': { 'added': '%s' }" % (platform_name, i)


if __name__ == "__main__":
    out_path = 'spiders/data/CA_events.txt'
    import_ = ImportDb(out_path)
    added = import_.import_to_db()
    print(added)
