from import_platforms import ImportPlaces
ImportPlaces('db_import/platform.txt')


from caribbean import Caribbean
caribbean = Caribbean()
caribbean.async()

from parter import Parter
parter = Parter()
parter.not_async()

from concert import Concert
concert = Concert()
concert.not_async()


from karabas import Karabas
karabas = Karabas()
karabas.async()


# import_ = ImportDb("CA_events.txt")
# import_.import_to_db()
