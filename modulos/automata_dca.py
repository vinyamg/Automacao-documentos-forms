import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json
from automatizadorXI import organiza

with open('../config.txt', "r", encoding="utf-8") as f:
    dados = json.load(f)
    email_associado = dados['email_acessoria']
    numero_associado = dados['telefone_acessoria']

def dca(pdf, micro, termo, crf_num, horas, retnoicas):
    microbiano = micro == 1
    termolabeis = termo == 1
    retnoi = retnoicas == 1

    crf = crf_num
    horario = horas

    razao, fantasia, cnpj, rua, bairro, cep, objeto_licenciado, numero_rua, cmvs, responsavel_legal, res_tecnico, substitutos, pressao, lobulo, temperatura, controle_especial, atencao_farmaceutica, cidade, codigo_cnae_numero, codigo_descricao, email, numero, complemento = organiza(pdf)
    nome, cpf, codigo = res_tecnico
    driver = webdriver.Firefox()
    driver.maximize_window()
    cep_novo = re.sub(r'-', '', cep)
    cep_final = cep_novo.replace(" ", "")

    numero = re.sub(r"[()\-\s]", "", numero_associado)
    numero_final = numero.replace(" ", "")
    driver.get('https://forms_anonimizado.com')
    sleep(2)
    razao_social1 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[1]/div[2]/div/span/input')
    razao_social1.send_keys(razao)

    cnpj_campo2 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[2]/div[2]/div/span/input')
    cnpj_campo2.send_keys(cnpj)

    endereco3 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[3]/div[2]/div/span/input')
    endereco3.send_keys(f'{rua.strip()}, {numero_rua}')

    bairro4 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[4]/div[2]/div/span/input')
    bairro4.send_keys(bairro)

    cep_campo5 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[5]/div[2]/div/span/input')
    cep_campo5.send_keys(cep_final)

    email6 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[6]/div[2]/div/span/input')
    email6.send_keys(email_associado)
    telefone7 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[7]/div[2]/div/span/input')
    telefone7.send_keys(numero_final)
    horario_funcionamento8 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[8]/div[2]/div/span/input')
    horario_funcionamento8.send_keys(horario)
    crf9 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[9]/div[2]/div/span/input')
    crf9.send_keys(crf)
    responsavel_tecnico10 = driver.find_element(By.XPATH, '//*[@id="question-list"]/div[10]/div[2]/div/span/input')
    responsavel_tecnico10.send_keys(nome)
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[11]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    if temperatura:
        driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[11]/div[2]/div/div/div[2]/div/label/span[1]/input').click()
    if pressao:
        driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[11]/div[2]/div/div/div[3]/div/label/span[1]/input').click()
    if lobulo:
        driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[11]/div[2]/div/div/div[4]/div/label/span[1]/input').click()
    if atencao_farmaceutica:
        driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[11]/div[2]/div/div/div[5]/div/label/span[1]/input').click()

    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[12]/div[2]/div/div/div[2]/div/label/span[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[13]/div[2]/div/div/div[2]/div/label/span[1]/input').click()
    for i in range(1, 5):
        dado = driver.find_element(By.XPATH, f'//*[@id="question-list"]/div[14]/div[2]/div/div/div[{i}]/div/label/span[1]/input')
        t = dado.get_attribute('value')
        if controle_especial:
            if t == 'Dispensação de medicamentos da Portaria 344/98':
                dado.click()
        if microbiano:
            if t == 'Dispensação de antimicrobianos':
                dado.click()
        if retnoi:
            if t == 'Dispensação da Lista "C2" (Retinóicas)':
                dado.click()
        if not microbiano and not controle_especial:
            if t == 'Nenhuma das classes descritas':
                dado.click()
                break
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[15]/div[2]/div/div/div[1]/div/label/span[1]/input').click()

    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[16]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[17]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    if termolabeis:
        driver.find_element(By.XPATH,'//*[@id="question-list"]/div[18]/div[2]/div/div/div[1]/div/label/span[1]/input').click()

    else:
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[18]/div[2]/div/div/div[3]/div/label/span[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[19]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    if controle_especial:
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[20]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[21]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[22]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[23]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[24]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[25]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    else:
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[20]/div[2]/div/div/div[2]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[21]/div[2]/div/div/div[3]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[22]/div[2]/div/div/div[2]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[23]/div[2]/div/div/div[2]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[24]/div[2]/div/div/div[3]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[25]/div[2]/div/div/div[3]/div/label/span[1]/input').click()
    if not microbiano:
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[26]/div[2]/div/div/div[3]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[27]/div[2]/div/div/div[3]/div/label/span[1]/input').click()
    elif microbiano:
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[26]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[27]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    else:
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[26]/div[2]/div/div/div[2]/div/label/span[1]/input').click()
        driver.find_element(By.XPATH, '//*[@id="question-list"]/div[27]/div[2]/div/div/div[3]/div/label/span[1]/input').click()

    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[28]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[29]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[30]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[31]/div[2]/div/div/div[1]/div/label/span[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[32]/div[2]/div/div/div[1]/div/label/span[1]/input').click()

    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[33]/div[2]/div/div/div/div/label/span[1]/input').click()
    driver.find_element(By.XPATH, '//*[@id="question-list"]/div[34]/div[2]/div/div/div/div/label/span[1]/input').click()