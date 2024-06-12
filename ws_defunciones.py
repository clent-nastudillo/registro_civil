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


from solve_captcha import solve_captcha
from get_ejecutar import connect_to_db, close_connection, get_defunciones_no_ejecutadas,update_row
import time
import sqlite3
from datetime import datetime





chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
service = ChromeService(executable_path=ChromeDriverManager().install())

db_name     = r"C:\Users\niky_\OneDrive\Escritorio\Demo\bd_registro_civil.db"
connection  = connect_to_db(db_name)


driver      = webdriver.Chrome(service=service, options=chrome_options)
url         = "https://www.registrocivil.cl/"
driver.get(url)


if connection:
    defunciones_no_ejecutadas = get_defunciones_no_ejecutadas(connection)
    print("|" + "-" *40 + "|")
    print("Datos encontrados: ", len(defunciones_no_ejecutadas))
    if defunciones_no_ejecutadas:
        for defuncion in defunciones_no_ejecutadas:
            print("Rut a Validar: ", defuncion[1])
            print("Id de ejecucion", defuncion[0])
            try:
                solve_captcha(driver)
            except:
                pass
            fecha_inicio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            rut = defuncion[1]

            time.sleep(2)
            iframe_element = driver.find_element(By.XPATH, '//iframe[@id="IframeOI"]')
            driver.switch_to.frame(iframe_element)

            element_to_click = driver.find_element(By.XPATH, '//*[@id="title_3"]')
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
            else:
                data = [1, "no", fecha_inicio, fecha_fin]
                update_row(connection, defuncion, data)

            driver.refresh()
        driver.close()
    close_connection(connection)

