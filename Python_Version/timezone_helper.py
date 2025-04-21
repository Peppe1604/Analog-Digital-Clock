import pytz
from datetime import datetime

# Lista di tutti i fusi orari disponibili
fusi_orari = pytz.all_timezones

def get_lista_paesi():
    # Restituisce la lista dei macro-paesi/aree disponibili nei fusi orari
    return sorted(set([tz.split('/')[0] for tz in fusi_orari if '/' in tz and tz.split('/')[0].isalpha()]))

def get_fusi_per_paese(paese):
    # Restituisce tutti i fusi orari per il paese selezionato
    return [tz for tz in fusi_orari if tz.startswith(paese + "/")]

def get_ora_corrente(nome_fuso):
    # Restituisce la data e ora corrente per il fuso orario scelto
    return datetime.now(pytz.timezone(nome_fuso))
