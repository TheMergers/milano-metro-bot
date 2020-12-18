import time
from re import search, sub
from subprocess import call
from wand.image import Image
import requests
import logging
from pyrogram import Client
from utils.get_config import get_config_file, get_chat, get_text_message
from utils.atm_api_functions import *

config = get_config_file("config.json")
api_id = config["api_id"]
api_hash = config["api_hash"]
token = config["bot_token"]
api_url = config["api_url"]
app = Client("metro_bot",api_id = api_id,api_hash =api_hash, bot_token = token)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

flood = dict()
flood['inline'] = dict()
flood['msg'] = dict()

fermate = {'amendola m1': ['Amendola M1', 'http://orari.atm-mi.it/M1_524.pdf'], 'bande nere m1': ['Bande Nere M1', 'http://orari.atm-mi.it/M1_512.pdf'], 'bisceglie m1': ['Bisceglie M1', 'http://orari.atm-mi.it/M1_509.pdf'], 'bonola m1': ['Bonola M1', 'http://orari.atm-mi.it/M1_519.pdf'], 'buonarroti m1': ['Buonarroti M1', 'http://orari.atm-mi.it/M1_525.pdf'], 'cadorna m1': ['Cadorna M1', 'http://orari.atm-mi.it/M1_528.pdf'], 'cairoli m1': ['Cairoli M1', 'http://orari.atm-mi.it/M1_529.pdf'], 'conciliazione m1': ['Conciliazione M1', 'http://orari.atm-mi.it/M1_527.pdf'], 'cordusio m1': ['Cordusio M1', 'http://orari.atm-mi.it/M1_530.pdf'], 'de angeli m1': ['De Angeli M1', 'http://orari.atm-mi.it/M1_514.pdf'], 'duomo m1': ['Duomo M1', 'http://orari.atm-mi.it/M1_531.pdf'], 'gambara m1': ['Gambara M1', 'http://orari.atm-mi.it/M1_513.pdf'], 'gorla m1': ['Gorla M1', 'http://orari.atm-mi.it/M1_542.pdf'], 'inganni m1': ['Inganni M1', 'http://orari.atm-mi.it/M1_510.pdf'], 'lampugnano m1': ['Lampugnano M1', 'http://orari.atm-mi.it/M1_521.pdf'], 'lima m1': ['Lima M1', 'http://orari.atm-mi.it/M1_537.pdf'], 'loreto m1': ['Loreto M1', 'http://orari.atm-mi.it/M1_538.pdf'], 'lotto m1': ['Lotto M1', 'http://orari.atm-mi.it/M1_523.pdf'], 'molino dorino m1': ['Molino Dorino M1', 'http://orari.atm-mi.it/M1_517.pdf'], 'pagano m1': ['Pagano M1', 'http://orari.atm-mi.it/M1_526.pdf'], 'palestro m1': ['Palestro M1', 'http://orari.atm-mi.it/M1_534.pdf'], 'pasteur m1': ['Pasteur M1', 'http://orari.atm-mi.it/M1_539.pdf'], 'pero m1': ['Pero M1', 'http://orari.atm-mi.it/M1_505.pdf'], 'porta venezia m1': ['Porta Venezia M1', 'http://orari.atm-mi.it/M1_536.pdf'], 'precotto m1': ['Precotto M1', 'http://orari.atm-mi.it/M1_543.pdf'], 'primaticcio m1': ['Primaticcio M1', 'http://orari.atm-mi.it/M1_511.pdf'], 'qt8 m1': ['QT8 M1', 'http://orari.atm-mi.it/M1_522.pdf'], 'rho fiera m1': ['Rho Fiera M1', 'http://orari.atm-mi.it/M1_504.pdf'], 'rovereto m1': ['Rovereto M1', 'http://orari.atm-mi.it/M1_540.pdf'], 'san babila m1': ['San Babila M1', 'http://orari.atm-mi.it/M1_533.pdf'], 'san leonardom1': ['San Leonardo M1', 'http://orari.atm-mi.it/M1_518.pdf'], 'sesto i maggio m1': ['Sesto I Maggio M1', 'http://orari.atm-mi.it/M1_547.pdf'], 'sesto marelli m1': ['Sesto Marelli M1', 'http://orari.atm-mi.it/M1_545.pdf'], 'sesto rondò m1': ['Sesto Rondò M1', 'http://orari.atm-mi.it/M1_546.pdf'], 'turro m1': ['Turro M1', 'http://orari.atm-mi.it/M1_541.pdf'], 'uruguay m1': ['Uruguay M1', 'http://orari.atm-mi.it/M1_520.pdf'], 'villa s. giovanni m1': ['Villa S. Giovanni M1', 'http://orari.atm-mi.it/M1_544.pdf'], 'wagner m1': ['Wagner M1', 'http://orari.atm-mi.it/M1_515.pdf'], 'abbiategrasso m2': ['Abbiategrasso M2', 'http://orari.atm-mi.it/M2_692.pdf'], 'assago m.forum m2': ['Assago M. Forum M2', 'http://orari.atm-mi.it/M2_694.pdf'], 'assago m. nord m2': ['Assago M. Nord M2', 'http://orari.atm-mi.it/M2_693.pdf'], 'bussero m2': ['Bussero M2', 'http://orari.atm-mi.it/M2_657.pdf'], 'cadorna m2': ['Cadorna M2', 'http://orari.atm-mi.it/M2_685.pdf'], 'caiazzo m2': ['Caiazzo M2', 'http://orari.atm-mi.it/M2_679.pdf'], 'cascina antonietta m2': ['Cascina Antonietta M2', 'http://orari.atm-mi.it/M2_654.pdf'], 'cascina burrona m2': ['Cascina Burrona M2', 'http://orari.atm-mi.it/M2_662.pdf'], 'cascina gobba m2': ['Cascina Gobba M2', 'http://orari.atm-mi.it/M2_670.pdf'], 'cassina de pecchi m2': ['Cassina de Pecchi M2', 'http://orari.atm-mi.it/M2_658.pdf'], 'centrale m2': ['Centrale M2', 'http://orari.atm-mi.it/M2_680.pdf'], 'cernusco m2': ['Cernusco M2', 'http://orari.atm-mi.it/M2_660.pdf'], 'cimiano m2': ['Cimiano M2', 'http://orari.atm-mi.it/M2_672.pdf'], 'cologno centro m2': ['Cologno Centro M2', 'http://orari.atm-mi.it/M2_668.pdf'], 'cologno nord m2': ['Cologno Nord M2', 'http://orari.atm-mi.it/M2_667.pdf'], 'cologno sud m2': ['Cologno Sud M2', 'http://orari.atm-mi.it/M2_669.pdf'], 'crescenzago m2': ['Crescenzago M2', 'http://orari.atm-mi.it/M2_671.pdf'], 'famagosta m2': ['Famagosta M2', 'http://orari.atm-mi.it/M2_690.pdf'], 'garibaldi m2': ['Garibaldi M2', 'http://orari.atm-mi.it/M2_682.pdf'], 'gessate m2': ['Gessate M2', 'http://orari.atm-mi.it/M2_653.pdf'], 'gioia m2': ['Gioia M2', 'http://orari.atm-mi.it/M2_681.pdf'], 'gorgonzola m2': ['Gorgonzola M2', 'http://orari.atm-mi.it/M2_655.pdf'], 'lambrate m2': ['Lambrate M2', 'http://orari.atm-mi.it/M2_674.pdf'], 'lanza m2': ['Lanza M2', 'http://orari.atm-mi.it/M2_684.pdf'], 'loreto m2': ['Loreto M2', 'http://orari.atm-mi.it/M2_677.pdf'], 'moscova m2': ['Moscova M2', 'http://orari.atm-mi.it/M2_683.pdf'], 'piola m2': ['Piola M2', 'http://orari.atm-mi.it/M2_676.pdf'], 'porta genova m2': ['Porta Genova M2', 'http://orari.atm-mi.it/M2_688.pdf'], 'romolo m2': ['Romolo M2', 'http://orari.atm-mi.it/M2_689.pdf'], 's.agostino m2': ['S.Agostino M2', 'http://orari.atm-mi.it/M2_687.pdf'], 's.ambrogio m2': ['S.Ambrogio M2', 'http://orari.atm-mi.it/M2_686.pdf'], 'udine m2': ['Udine M2', 'http://orari.atm-mi.it/M2_673.pdf'], 'villa fiorita m2': ['Villa Fiorita M2', 'http://orari.atm-mi.it/M2_659.pdf'], 'villa pompea m2': ['Villa Pompea M2', 'http://orari.atm-mi.it/M2_656.pdf'], 'vimodrone m2': ['VimodroneM2', 'http://orari.atm-mi.it/M2_663.pdf'], 'affori centro m3': ['Affori Centro M3', 'http://orari.atm-mi.it/M3_726.pdf'], 'affori fn m3': ['Affori FN M3', 'http://orari.atm-mi.it/M3_725.pdf'], 'brentam3': ['Brenta M3', 'http://orari.atm-mi.it/M3_742.pdf'], 'centralem3': ['Centrale M3', 'http://orari.atm-mi.it/M3_731.pdf'], 'comasina m3': ['Comasina M3', 'http://orari.atm-mi.it/M3_724.pdf'], 'corvetto m3': ['Corvetto M3', 'http://orari.atm-mi.it/M3_743.pdf'], 'crocetta m3': ['Crocetta M3', 'http://orari.atm-mi.it/M3_739.pdf'], 'dergano m3': ['Dergano M3', 'http://orari.atm-mi.it/M3_727.pdf'], 'duomo m3': ['Duomo M3', 'http://orari.atm-mi.it/M3_736.pdf'], 'lodit.i.b.b. m3': ['Lodi T.I.B.B. M3', 'http://orari.atm-mi.it/M3_741.pdf'], 'maciachini m3': ['Maciachini M3', 'http://orari.atm-mi.it/M3_728.pdf'], 'missori m3': ['Missori M3', 'http://orari.atm-mi.it/M3_737.pdf'], 'montenapoleone m3': ['Montenapoleone M3', 'http://orari.atm-mi.it/M3_735.pdf'], 'porta romana m3': ['Porta Romana M3', 'http://orari.atm-mi.it/M3_740.pdf'], 'porto di mare m3': ['Porto diMare M3', 'http://orari.atm-mi.it/M3_744.pdf'], 'repubblica m3': ['Repubblica M3', 'http://orari.atm-mi.it/M3_732.pdf'], 'rogoredo m3': ['Rogoredo M3', 'http://orari.atm-mi.it/M3_745.pdf'], 'san donato m3': ['San Donato M3', 'http://orari.atm-mi.it/M3_746.pdf'], 'sondrio m3': ['Sondrio M3', 'http://orari.atm-mi.it/M3_730.pdf'], 'turati m3': ['Turati M3', 'http://orari.atm-mi.it/M3_734.pdf'], 'zara m3': ['Zara M3', 'http://orari.atm-mi.it/M3_729.pdf'], 'bicocca m5': ['Bicocca M5', 'http://orari.atm-mi.it/M5_302.pdf'], 'bignami m5': ['Bignami M5', 'http://orari.atm-mi.it/M5_300.pdf'], 'ca’ granda m5': ['Ca’ Granda M5', 'http://orari.atm-mi.it/M5_303.pdf'], 'cenisio m5': ['Cenisio M5', 'http://orari.atm-mi.it/M5_310.pdf'], 'domodossola fn m5': ['Domodossola FN M5', 'http://orari.atm-mi.it/M5_312.pdf'], 'garibaldi fs m5': ['Garibaldi FS M5', 'http://orari.atm-mi.it/M5_308.pdf'], 'gerusalemme m5': ['Gerusalemme M5', 'http://orari.atm-mi.it/M5_311.pdf'], 'isola m5': ['Isola M5', 'http://orari.atm-mi.it/M5_307.pdf'], 'istria m5': ['Istria M5', 'http://orari.atm-mi.it/M5_304.pdf'], 'lotto m5': ['Lotto M5', 'http://orari.atm-mi.it/M5_315.pdf'], 'marche m5': ['Marche M5', 'http://orari.atm-mi.it/M5_305.pdf'], 'monumentale m5': ['Monumentale M5', 'http://orari.atm-mi.it/M5_309.pdf'], 'ponale m5': ['Ponale M5', 'http://orari.atm-mi.it/M5_301.pdf'], 'portello m5': ['Portello M5', 'http://orari.atm-mi.it/M5_314.pdf'], 'san siro ippodromo m5': ['San Siro IppodromoM5', 'http://orari.atm-mi.it/M5_317.pdf'], 'san siro stadio m5': ['San Siro Stadio M5', 'http://orari.atm-mi.it/M5_318.pdf'], 'segesta m5': ['Segesta M5', 'http://orari.atm-mi.it/M5_316.pdf'], 'tre torri m5': ['Tre Torri M5', 'http://orari.atm-mi.it/M5_313.pdf'], 'zara m5': ['Zara M5', 'http://orari.atm-mi.it/M5_306.pdf']}

def check_flood(chat_id):
	check = False
	temp = time.time()
	chat_id = str(chat_id)
	root = flood['msg']
	
	if not chat_id in root:
		root[chat_id] = list()
	
	chat_id = root[chat_id]
	
	if len(chat_id) >2:
		if temp - chat_id[0] <= 3:
			check = True
		chat_id.pop(0)
	
	chat_id.append(temp)
	
	return check
	
	

def downloadPdf(file_url):
	r = requests.get(file_url, stream = True)
	
	with open("atm.pdf","wb") as pdf:
		for chunk in r.iter_content(chunk_size=1024):
			# writing one chunk at a time to pdf file 
			if chunk: 
				pdf.write(chunk)
				
	with(Image(filename="atm.pdf", resolution=120)) as source: 
		images = source.sequence
		pages = len(images)
		for i in range(pages):
			#n = i + 1
			#newfilename = f[:-4] + str(n) + '.jpeg'
			newfilename = 'atm' + str(i) + '.jpeg'
			Image(images[i]).save(filename=newfilename)
			
	return pages

@app.on_message()
def echo(client, message):
	chat_id = get_chat(message)
	messaggio = get_text_message(message)
	if check_flood(chat_id):
		return
		
	if search("^/", message["text"]):
		message["text"] = message["text"].replace("/", "").replace("_", " ")
	
	if len(message["text"]) < 4:
		app.send_message(chat_id,'<i>Per cercare una fermata scrivi almeno 4 lettere</i>', parse_mode='html')
		return
	if "/start" in messaggio:
		app.send_message(chat_id,'Ciao, questo bot ti invia gli orari aggiornati della fermata metro da te scelta, ti basta scrivere nome o parte del nome della fermata.\nFunziona solo in privato!\n\nSviluppato da @Pilota\n\nIn data 29/11/2020 è stata trasferita la proprietà del bot a @MasterCruelty',parse_mode='html')
		return
	
	found = []
	msg = message["text"].lower()
	isStop = 0
	for f in fermate:
		ff = f.split(' ')
		ffl = len(ff)
		msgg = msg.split(' ')
		msgl = len(msgg)
		ok = 0
		for wrd in msgg:
			for ferm in ff:
				if wrd in ferm:
					ok+=1
					break
		
		if ok == msgl:
			isStop+=1
			nick = f
			nome = fermate[f][0]
			url = fermate[f][1]
			found.append(nome)
			
	
	if isStop == 0:
		app.send_message(chat_id,'<i>Nessuna fermata trovata, prova a scrivere parte del nome</i>', parse_mode='html')
		return
	if isStop > 1:
		testo = ''
		for n in found:
		        testo+='\n<code>'+n+'</code>'
		app.send_message(chat_id,'<i>Ho trovato diverse fermate:</i>'+testo+'\n<i>Specificane una scrivendo il suo nome</i>', parse_mode='html')
		return
	if "M1" in nome:
                linea = get_line(-1)
                nome = nome.replace("M1","")
                path = get_stop(linea,nome.upper())
                url = get_time_table(path)
                app.send_message(chat_id,url + "\n" + "eccolo qua " + nome,disable_web_page_preview=True)
                return
                app.send_message(chat_id,'<i>Sto scaricando gli orari per la fermata:</i>\n **'+nome+'**')
	pages = downloadPdf(url)
	
	for page in range(pages):
		f = open("atm"+str(page)+'.jpeg', 'rb')
		client.send_photo(chat_id, f)
		f.close()
	
	call(["rm", "atm.pdf"])
	
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	app.run()

if __name__ == '__main__':
    main()
