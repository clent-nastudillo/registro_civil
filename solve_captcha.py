
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha


def solve_captcha(driver):
    img_xpath = '/html/body/img[2]'
    input_xpath = '//*[@id="ans"]'
    check_button_xpath = '//*[@id="jar"]'
    try:
        captcha_img = WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH, img_xpath)))
        captcha_img.screenshot(r"C:\Users\niky_\OneDrive\Escritorio\demo\registro_civil\captcha.png")
        solver = TwoCaptcha('f81915426f6d04b7152414d4457221c0')
        try:
            print("RESOLVIENDO CAPTCHA")
            result = solver.normal(r"C:\Users\niky_\OneDrive\Escritorio\demo\registro_civil\captcha.png")
        except Exception as e:
            print(e)
        else:
            code = result['code']
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, input_xpath))).send_keys(code)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, check_button_xpath))).click()
    except:
        pass