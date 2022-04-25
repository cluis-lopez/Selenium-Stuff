import random
import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

USER="Carlos Luis Lopez"
PASSWORD="XXXXXX"
FIRST_DAY="2022-03-01" # Formato ISO Año-Mes-Día
LAST_DAY="2022-03-31"

STARTING_HOUR="09:00" # Formato ISO Hora:Minuto
EXTRA_TIME="01:30"
VARIANCE=60 # Minutos +/- hora de entrada

HOURS_WORKDAY="08:43" # Formato Horas:Minutos
HOURS_FRIDAY="06:30"

FIX_NATIONAL_HOLIDAYS = ['01-01', '01-06', '05-01', '08-15', '10-12', '11-01', '12-06', '12-08', '12-26']  # OJO !!! Modificado el día 25-12 que en 2022 se mueve al 26
VARIABLE_NATIONAL_HOLIDAYS = ['04-15'] # Viernes Santo 2022
LOCAL_HOLIDAYS = ['04-14', '05-02', '05-16', '07-25', '11-09']

URL_HOMEPAGE="https://XXXXX.com/iwom_web5/portal_apps.aspx"

WEEKDAYS = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

# Create empty global list of datetimes with the holidays
HOLIDAYS = []


def InitBrowser(browser):
	browser.get(URL_HOMEPAGE)

	wait = WebDriverWait(browser, 10)
	actions = ActionChains(browser)

	browser.find_element('id' , "LoginApps_UserName").clear()
	browser.find_element('id' , "LoginApps_UserName").send_keys(USER)
	browser.find_element('id' , "LoginApps_Password").clear()
	browser.find_element('id' , "LoginApps_Password").send_keys(PASSWORD)
	browser.find_element('id' , "LoginApps_btnlogin").click()
	window_before = browser.window_handles[0]
	browser.find_element('id' , "MainContent_tbl01").click()
	# browser.switch_to.window('iWom')
	window_after = browser.window_handles[1]
	browser.switch_to.window(window_after)

	menu = browser.find_element('id', 'ctl00_Menu1n1')
	actions.move_to_element(menu).perform()
	browser.find_element('link text' , "Registro jornada").click()

	# browse loads page to entry data
	dia = browser.find_element('id', 'ctl00_Sustituto_T_dia')
	browser.execute_script("arguments[0].disabled = false", dia)
	dia.clear()

def StoreData(browser, d, te, ts, wh): # Parametros datetime: día, hora entrada, hora de salida
	dia = str(d.day)+'/'+str(d.month)+'/'+str(d.year)
	he = te.time().isoformat(timespec='minutes').split(':')[0]
	me = te.time().isoformat(timespec='minutes').split(':')[1]
	hs = ts.time().isoformat(timespec='minutes').split(':')[0]
	ms = ts.time().isoformat(timespec='minutes').split(':')[1]
	hours= str(wh.hour) + ":" + str(wh.minute)

	d_field = browser.find_element('id', 'ctl00_Sustituto_T_dia')
	browser.execute_script("arguments[0].disabled = false", d_field)
	d_field.clear()
	browser.find_element('id', 'ctl00_Sustituto_T_dia').send_keys(dia)
	Select(browser.find_element('id', 'ctl00_Sustituto_d_hora_inicio1')).select_by_visible_text(he)
	Select(browser.find_element('id', 'ctl00_Sustituto_D_minuto_inicio1')).select_by_visible_text(me)
	Select(browser.find_element('id','ctl00_Sustituto_d_hora_final1')).select_by_visible_text(hs)
	Select(browser.find_element('id', 'ctl00_Sustituto_d_minuto_final1')).select_by_visible_text(ms)
	browser.find_element('id' , 'ctl00_Sustituto_T_efectivo').clear()
	browser.find_element('id' , 'ctl00_Sustituto_T_efectivo').send_keys(hours)
	browser.find_element('id' , 'ctl00_Sustituto_Btn_Guardar').click()

	if (browser.find_element('id', 'ctl00_Sustituto_L_error').text == 'Guardado correctamente'):
		return True
	
	return False

def GetHourData(d):
	st = datetime.time.fromisoformat(STARTING_HOUR)
	xt = datetime.time.fromisoformat(EXTRA_TIME)
	if (d.weekday() == 5 or d.weekday() == 6): # Sábado o Domingo
		return datetime.datetime(1,1,1), datetime.datetime(1,1,1)
	if (d in HOLIDAYS):
		return datetime.datetime(2,1,1), datetime.datetime(2,1,1)
	if (d.weekday() == 4): # Viernes
		wh = datetime.time.fromisoformat(HOURS_FRIDAY)
	else:
		wh = datetime.time.fromisoformat(HOURS_WORKDAY)

	StartTime = datetime.datetime(d.year, d.month, d.day, st.hour, st.minute) + datetime.timedelta(minutes=random.randrange(int(-VARIANCE/2),int(VARIANCE/2)))
	LastTime = StartTime + datetime.timedelta(hours = xt.hour + wh.hour, minutes = xt.minute + wh.minute)
	return StartTime, LastTime, wh

def InitHolidays(d):
	y = str(d.year)
	for i in FIX_NATIONAL_HOLIDAYS, VARIABLE_NATIONAL_HOLIDAYS, LOCAL_HOLIDAYS:
		for j in i:
			HOLIDAYS.append(datetime.date.fromisoformat(y+'-'+j))

def Main():
	StartDate = datetime.date.fromisoformat(FIRST_DAY)
	LastDate = datetime.date.fromisoformat(LAST_DAY)

	d = StartDate
	InitHolidays(d)
	
	browser  = webdriver.Chrome(ChromeDriverManager().install())
	InitBrowser(browser)
	
	while (d <= LastDate):
		times = GetHourData(d)
		if (times[0].year == 1):
			mess = 'El dia ' + d.isoformat() + ' es ' + WEEKDAYS[d.weekday()] + ' no se computa'
		elif (times[0].year == 2):
			mess = 'El dia ' + d.isoformat() + ' es FESTIVO en ' + str(d.year) + ' y no se computa'
		elif (StoreData(browser, d, times[0], times[1], times[2])):
			mess = 'GUARDADO día ' + d.isoformat() + ' es ' + WEEKDAYS[d.weekday()] + ' Entrada a las ' + times[0].time().isoformat(timespec='minutes') + ' Salida a las ' + times[1].time().isoformat(timespec='minutes')
		else:
			mess = 'ERROR no se ha podido grabar correctamente el día ' + d.isoformat() 
		print (mess)
		d = d + datetime.timedelta(days=1)

if __name__ == '__main__':
	Main()
