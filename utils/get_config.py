import utils_config

"""
carica il file di configurazione
"""
def get_config_file(json_file):
    config = utils_config.load_config(json_file)
    return utils_config.serialize_config(config)

#Restituisce l'id chat
def get_chat(message):
    return message["chat"]["id"]

#Restituisce il testo del messaggio
def get_text_message(message):
    return message["text"]
