from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json
import os
import re
from automatizadorXI import organiza, salvarArquivo, salvaLogs


def automata3(pdf, tipo_modo, decisao):
    razao, fantasia, cnpj, rua, bairro, cep, objeto_licenciado, numero_rua, cmvs, responsavel_legal, res_tecnico, substitutos, l, s, p, c, a, codigo_cnae_numero, codigo_descricao, cidade, email, numero, complemento = organiza(pdf)

    driver = webdriver.Firefox()
    driver.maximize_window()
    with open('../config.txt', "r", encoding="utf-8") as f:
        dados = json.load(f)
        num_estabelecimento = numero
        email_estabelecimento = email
        num_acessoria = dados['telefone_acessoria']
        email_acessoria = dados['email_acessoria']
        sigla = dados['crf']
        uf = dados['uf']
        tipo = tipo_modo

    diretorio_script = os.getcwd()
    driver.get(f'file:///{diretorio_script}/padrao/formulario_III.pdf')
    sleep(2)


    #solicitação
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[1]/input').click()
        codigo_atividade = driver.find_element(By.ID, 'pdfjs_internal_id_4538R')
        codigo_atividade.send_keys(codigo_cnae_numero)
        descricao_atividade = driver.find_element(By.ID, 'pdfjs_internal_id_4539R')
        descricao_atividade.send_keys(codigo_descricao + " " + "DE FÓRMULAS") #arrumar

        cves = re.search(r'(\d+)-(\d+)-(\d+)-(\d+)-(\d+)', cmvs)
        cves_parte1 = cves.group(1)
        cves_parte2 = cves.group(2)
        cves_parte3 = cves.group(3)
        cves_parte4 = cves.group(4)
        cves_parte5 = cves.group(5)

        campo1_cve = driver.find_element(By.ID, 'pdfjs_internal_id_4550R')
        campo1_cve.send_keys(cves_parte1)
        campo2_cve = driver.find_element(By.ID, 'pdfjs_internal_id_4551R')
        campo2_cve.send_keys(cves_parte2)
        campo3_cve = driver.find_element(By.ID, 'pdfjs_internal_id_4552R')
        campo3_cve.send_keys(cves_parte3)
        campo4_cve = driver.find_element(By.ID, 'pdfjs_internal_id_4553R')
        campo4_cve.send_keys(cves_parte4)
        campo5_cve = driver.find_element(By.ID, 'pdfjs_internal_id_4554R')
        campo5_cve.send_keys(cves_parte5)

        if tipo == "Inicial":
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[21]/input').click()
        elif tipo == "Cancelamento":
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[22]/input').click()
        elif tipo == "Renovação":
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[23]/input').click()
        elif tipo == "Alteração":
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[24]/input').click()
        else:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[21]/input').click()
    except Exception as e:
        salvaLogs(e, "Solicitação")
        pass

    #identificação do estabelecimento
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[39]/input').click()

        cnpj_campo = driver.find_element(By.ID, 'pdfjs_internal_id_4573R')
        cnpj_campo.send_keys(cnpj)
        razao_social = driver.find_element(By.ID, 'pdfjs_internal_id_4574R')
        razao_social.send_keys(razao)
        nome_fantasia = driver.find_element(By.ID, 'pdfjs_internal_id_4575R')
        nome_fantasia.send_keys(fantasia)

        #Localização do estabelecimento

        tipo_logra = re.search(r'\w+', rua)
        ddd_pegar = re.search(r'\((\w+\))\s(.*)', num_estabelecimento)

        cep_campo = driver.find_element(By.ID, 'pdfjs_internal_id_725R')
        cep_campo.send_keys(cep)
        tipo_logradouro = driver.find_element(By.ID, 'pdfjs_internal_id_728R')
        if tipo_logra.group(0).startswith("R."):
            tipo_logradouro.send_keys("Rua")
        elif tipo_logra.group(0).startswith("Av"):
            tipo_logradouro.send_keys("Avenida")
        elif tipo_logra.group(0).startswith("Est"):
            tipo_logradouro.send_keys("Estrada")
        elif tipo_logra.group(0).startswith("Rod"):
            tipo_logradouro.send_keys("Rodovia")
        else:
            tipo_logradouro.send_keys(tipo_logra.group(0))
        logradouro = driver.find_element(By.ID, 'pdfjs_internal_id_726R')
        logradouro.send_keys(rua)
        numero = driver.find_element(By.ID, 'pdfjs_internal_id_727R')
        numero.send_keys(numero_rua)
        if complemento:
            complemento_campo = driver.find_element(By.ID, 'pdfjs_internal_id_729R')
            complemento_campo.send_keys(complemento)
        bairro_campo = driver.find_element(By.ID, 'pdfjs_internal_id_730R')
        bairro_campo.send_keys(bairro)
        municipio = driver.find_element(By.ID, 'pdfjs_internal_id_735R')
        municipio.send_keys(cidade) #Resolver, precisa de regex para pegar a cidade
        if num_estabelecimento:
            if num_estabelecimento[5].startswith("9"):
                ddd = driver.find_element(By.ID, 'pdfjs_internal_id_741R')
                ddd.send_keys(ddd_pegar.group(1))
                celular = driver.find_element(By.ID, 'pdfjs_internal_id_742R')
                celular.send_keys(ddd_pegar.group(2))
            else:
                ddd = driver.find_element(By.ID, 'pdfjs_internal_id_738R')
                ddd.send_keys(ddd_pegar.group(1))
                celular = driver.find_element(By.ID, 'pdfjs_internal_id_734R')
                celular.send_keys(ddd_pegar.group(2))
        if email_estabelecimento:
            email = driver.find_element(By.ID, 'pdfjs_internal_id_745R')
            email.send_keys(email_estabelecimento)
    except Exception as e:
        salvaLogs(e, "Identificação do estabelecimento")
        pass


    #Caracterização do estabelecimento
    try:
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/section[26]/input').click()
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/section[31]/input').click()
    except Exception as e:
        salvaLogs(e, "Caracterização do estabelecimento")
        pass

    #Identificação dos responsáveis: Tecnico e legal
    try:
        nome, cpf = responsavel_legal

        nome_responsavel = driver.find_element(By.ID, 'pdfjs_internal_id_851R')
        nome_responsavel.send_keys(nome)
        cpf_responsavel = driver.find_element(By.ID, 'pdfjs_internal_id_864R')
        cpf_responsavel.send_keys(cpf)

        nome, cpf, codigo = res_tecnico

        nome_tecnico = driver.find_element(By.ID, 'pdfjs_internal_id_863R')
        nome_tecnico.send_keys(nome)
        cpf_tecnico = driver.find_element(By.ID, 'pdfjs_internal_id_858R')
        cpf_tecnico.send_keys(cpf)
        sigla_tecnico = driver.find_element(By.ID, 'pdfjs_internal_id_856R')
        sigla_tecnico.send_keys(sigla)
        uf_tecnico = driver.find_element(By.ID, 'pdfjs_internal_id_853R')
        uf_tecnico.send_keys(uf)
        codigo_tecnico = driver.find_element(By.ID, 'pdfjs_internal_id_854R')
        codigo_tecnico.send_keys(codigo)
        if decisao == "Nenhum":
            if substitutos:
                quantidade = len(substitutos)
                nome, cpf, codigo = substitutos[0]

                nome_substituto1 = driver.find_element(By.ID, 'pdfjs_internal_id_859R')
                nome_substituto1.send_keys(nome)
                cpf_substituto1 = driver.find_element(By.ID, 'pdfjs_internal_id_862R')
                cpf_substituto1.send_keys(cpf)
                sigla_substituto1 = driver.find_element(By.ID, 'pdfjs_internal_id_860R')
                sigla_substituto1.send_keys(sigla)
                uf_substituto1 = driver.find_element(By.ID, 'pdfjs_internal_id_861R')
                uf_substituto1.send_keys(uf)
                codigo_substituto1 = driver.find_element(By.ID, 'pdfjs_internal_id_866R')
                codigo_substituto1.send_keys(codigo)

                if quantidade == 2:
                    nome, cpf, codigo = substitutos[1]

                    nome_substituto2 = driver.find_element(By.ID, 'pdfjs_internal_id_836R')
                    nome_substituto2.send_keys(nome)
                    cpf_substituto2 = driver.find_element(By.ID, 'pdfjs_internal_id_835R')
                    cpf_substituto2.send_keys(cpf)
                    sigla_substituto2 = driver.find_element(By.ID, 'pdfjs_internal_id_837R')
                    sigla_substituto2.send_keys(sigla)
                    uf_substituto2 = driver.find_element(By.ID, 'pdfjs_internal_id_840R')
                    uf_substituto2.send_keys(uf)
                    codigo_substituto2 = driver.find_element(By.ID, 'pdfjs_internal_id_838R')
                    codigo_substituto2.send_keys(codigo)

                if quantidade == 3:
                    nome, cpf, codigo = substitutos[2]

                    nome_substituto3 = driver.find_element(By.ID, 'pdfjs_internal_id_843R')
                    nome_substituto3.send_keys(nome)
                    cpf_substituto3 = driver.find_element(By.ID, 'pdfjs_internal_id_833R')
                    cpf_substituto3.send_keys(cpf)
                    sigla_substituto3 = driver.find_element(By.ID, 'pdfjs_internal_id_844R')
                    sigla_substituto3.send_keys(sigla)
                    uf_substituto3 = driver.find_element(By.ID, 'pdfjs_internal_id_848R')
                    uf_substituto3.send_keys(uf)
                    codigo_substituto3 = driver.find_element(By.ID, 'pdfjs_internal_id_849R')
                    codigo_substituto3.send_keys(codigo)
    except Exception as e:
        salvaLogs(e, "Identificação dos responsaveis tecnico e legal")
        pass
    #declaração de responsabilidade

    try:
        local = driver.find_element(By.ID, 'pdfjs_internal_id_850R')
        if cidade:
            local.send_keys(cidade)
        else:
            local.send_keys("São paulo")
    except Exception as e:
        salvaLogs(e, "Declaração de responsabilidade")
        pass
    sleep(1)
    driver.find_element(By.ID, "downloadButton").click()
    sleep(2)
    salvarArquivo(tipo, razao, "FormularioIII")



