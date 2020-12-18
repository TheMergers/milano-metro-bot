import requests
import json
import utils.get_config 

config = utils.get_config.get_config_file("config.json")
api = config["api_url"]

#recupera il json della linea 
def get_line(line_number):
    request = "tpl/journeyPatterns/" + str(line_number) + "%7C0"
    get = api + "" + request
    resp = requests.get(get)
    return resp.json()

#recupera il path che porta al json della fermata avendo il json di tutta la linea corrispondente
def get_stop(line,stop):
    url =""
    stops = line["Stops"]
    for item in stops:
        if item["Description"].strip() == stop.strip():
            url = item["Links"][0]["Href"]
            return url

#recupera il link alla tabella degli orari della fermata richiesta
def get_time_table(path):
    get = api + "" + path
    resp = requests.get(get)
    data = resp.json()
    Lines= data["Lines"]
    for item in Lines:
        time_table = item["BookletUrl"]
        break
    return time_table
