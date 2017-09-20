import csv
import os
import sys
import ast

class ImportPlaces:

    def __init__(self, path):

        # if self.pl_names_path Not:
        #     self.pl_names_path = 'spiders/db_import/PL_NAMES'

        # timezone.activate(pytz.timezone("Europe/Kiev"))
        self.path = path
        # If im n src folder:
        # project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        #print(project_dir)
        sys.path.append(project_dir)
        #os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.base'
        os.environ['DJANGO_SETTINGS_MODULE'] = 'event_placement.settings.production'
        import django
        django.setup()

        from events.models import Platform
        pl_path = os.path.join(project_dir, 'spiders', 'db_import', 'PL_NAMES')
        with open(pl_path, 'r') as plfile:
            PL_NAMES = ast.literal_eval(plfile.read())

        # PL_NAMES = {
        #         'Caribbean Club'            : 'CA',
        #         'Karabas.com'               : 'KA',
        #         'Concert.ua'                : 'CO',
        #         'Parter.ua'                 : 'PA',
        #         'fb_CaribbeanClub'          : 'FC',
        #         'fb_SalsaRulit'             : 'FS',
        #         'fb_JazzTime'               : 'FJ',
        #         'fb_CaribbeanConcertHall'   : 'FH',
        # }


        with open(self.path, encoding="utf-8", newline='') as csvfile:
            data = csv.reader(csvfile, delimiter=',')

            for row in data:
                if row[1] != 'link':
                    pl = Platform()

                    pl.name = row[0]
                    pl.short_name = PL_NAMES[row[0]]
                    pl.link = row[1]
                    pl.category = row[2]

                    try:
                        pl.save()
                    except:
                        pass


if __name__ == "__main__":
    #self.pl_names_path = 'spiders/db_import/PL_NAMES'
    ImportPlaces('spiders/db_import/platform.txt')
