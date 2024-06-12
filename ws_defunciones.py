from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from solve_captcha import solve_captcha
from get_ejecutar import connect_to_db, close_connection, get_defunciones_no_ejecutadas,update_row
import time
import sqlite3
from datetime import datetime

db_name     = r"C:\Users\niky_\OneDrive\Escritorio\demo\registro_civil\bd_registro_civil.db"
connection  = connect_to_db(db_name)

# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.110 Safari/537.36"

# options = webdriver.ChromeOptions()
# options.add_argument(f"user-agent={user_agent}")
# options.add_experimental_option('excludeSwitches', ['enable-automation'])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--incognito")
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("window-size=1920,1080")
# options.add_argument("--start-maximized")
# # options.add_argument("--blink-settings=imagesEnabled=false")
# options.add_argument("--disable-infobars")
# options.add_argument("--disable-notifications")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--disable-webrtc")


proxy_ip_port = 'proxy.froxy.com:9008'  # Dirección IP y puerto del proxy
proxy_username = 'O3OFKf9r4W9tt7Tt'    # Nombre de usuario para la autenticación del proxy
proxy_password = 'wifi;cl;;;'                
chrome_options = Options()
chrome_options.add_argument('--proxy-server=%s' % proxy_ip_port)
chrome_options.add_argument('--proxy-auth=%s:%s' % (proxy_username, proxy_password))



# Inicialización del driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
url     = "https://www.registrocivil.cl"
driver.get(url)

if connection:
    defunciones_no_ejecutadas = get_defunciones_no_ejecutadas(connection)
    print(defunciones_no_ejecutadas)
    print("|" + "-" *40 + "|")
    if defunciones_no_ejecutadas:
        for defuncion in defunciones_no_ejecutadas:
            print("Rut a Validar: ", defuncion[1])
            print("Id de ejecucion", defuncion[0])
            try:
                solve_captcha(driver)
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//iframe[@id="IframeOI"]')))
            except:
                solve_captcha(driver)
                pass
            fecha_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            rut = defuncion[1]
            iframe_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//iframe[@id="IframeOI"]')))
            driver.switch_to.frame(iframe_element)

            element_to_click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="title_3"]')))
            element_to_click.click()

            time.sleep(1)
            script = """
                var elements = document.querySelectorAll('#divLista_3 ins');
                if (elements.length >= 3) {
                    elements[2].click();
                    return 'Elemento clickeado exitosamente';
                } else {
                    return 'Elemento no encontrado';
                }
                """
            result = driver.execute_script(script)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "idInputRun")]'))).send_keys({rut}) 
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "btn_agregarCarro")]'))).click()

            iframe_element = driver.find_element(By.XPATH, '//iframe[@id="cu_idIframe4"]')
            driver.switch_to.frame(iframe_element)
            
            try:
                solve_captcha(driver)
            except:
                pass

            driver.switch_to.default_content()
            iframe_element = driver.find_element(By.XPATH, '//iframe[@id="IframeOI"]')
            driver.switch_to.frame(iframe_element)
            
            try:
                WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@id, "carro_datosMailSolicitanteContainer")]')))
                encontro = True
            except:
                encontro = False

            
            fecha_fin = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if encontro:
                data = [1, "si", fecha_inicio, fecha_fin]
                update_row(connection, defuncion, data)
                try:
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="oi_icon_red"]'))).click()
                except:
                    pass
            else:
                data = [1, "no", fecha_inicio, fecha_fin]
                update_row(connection, defuncion, data)
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="oi_icon_red"]'))).click()
            except:
                pass

            driver.refresh()
        driver.close()
    close_connection(connection)

