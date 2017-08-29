try:
    from caribbean import Caribbean
    caribbean = Caribbean()
    caribbean.async()
except:
    pass

try:
    from parter import Parter
    parter = Parter()
    parter.not_async()
except:
    pass

try:
    from concert import Concert
    concert = Concert()
    concert.not_async()
except:
    pass

try:
    from karabas import Karabas
    karabas = Karabas()
    karabas.async()
except:
    pass
# import_ = ImportDb("CA_events.txt")
# import_.import_to_db()
