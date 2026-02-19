from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import Select
import json
from datetime import date
import os
from automatizadorXI import organiza, salvarArquivo, salvaLogs

def automata(pdf, tipo_modo, vre_coleta):
    razao, fantasia, cnpj, rua, bairro, cep, objeto_licenciado, numero_rua, cmvs, responsavel_legal, res_tecnico, substitutos, l, s, p, c, a, codigo_cnae_numero, codigo_descricao, cidade, email, numero, complemento = organiza(pdf)
    with open('../config.txt', "r", encoding="utf-8") as f:
        dados = json.load(f)
        num_estabelecimento = numero
        email_estabelecimento = email
        sigla = dados['crf']
        uf = dados['uf']
        num_acessoria = dados['telefone_acessoria']
        email_acessoria = dados['email_acessoria']
        tipo = tipo_modo


    driver = webdriver.Firefox()
    driver.maximize_window()
    diretorio_script = os.getcwd()
    driver.get(f'file:///{diretorio_script}/padrao/formulario_XII.pdf')
    sleep(2)

    try:
        #solicitação
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[8]/input').click()
        vre = driver.find_element(By.ID, 'pdfjs_internal_id_200R')
        vre.send_keys(vre_coleta)
        cmvs_campo = driver.find_element(By.XPATH, '//*[@id="pdfjs_internal_id_163R"]')
        cmvs_campo.send_keys(cmvs)
        cnae = driver.find_element(By.NAME, 'Caixa de lista 1_2')
        select = Select(cnae)
        select.select_by_value("8640-2/02 - LABORATÓRIOS CLÍNICOS")
        objeto_solicitacao = driver.find_element(By.NAME, 'Caixa de lista 1')
        select = Select(objeto_solicitacao)
        select.select_by_value(objeto_licenciado.title())
        tipo_solicitacao = driver.find_element(By.NAME, 'Caixa de lista 1_3')
        select = Select(tipo_solicitacao)
        if tipo == "Inicial":
            select.select_by_index(0)
        elif tipo == "Cancelamento":
            select.select_by_index(1)
        elif tipo == "Alteração":
            select.select_by_index(2)
        else:
            select.select_by_index(0)

    except Exception as e:
        salvaLogs(e, "Solicitação")
        pass



    try:
        #identificação do estabelecimento
        razao_campo = driver.find_element(By.ID, 'pdfjs_internal_id_170R')
        razao_campo.send_keys(razao)
        fantasia_campo = driver.find_element(By.ID, 'pdfjs_internal_id_172R')
        fantasia_campo.send_keys(fantasia)
        natureza = driver.find_element(By.NAME, 'Caixa de lista 2')
        select = Select(natureza)
        select.select_by_index(2) #para juridico 2 para fisico 1
        cnpj_campo = driver.find_element(By.ID, 'pdfjs_internal_id_176R')
        cnpj_campo.send_keys(cnpj)
    except Exception as e:
        salvaLogs(e, "Identificação do estabelecimento")
        pass

    try:
        #Localização do estabelecimento
        logradouro = driver.find_element(By.ID, 'pdfjs_internal_id_178R')
        logradouro.send_keys(rua)
        numero = driver.find_element(By.ID, 'pdfjs_internal_id_180R')
        numero.send_keys(numero_rua)
        if complemento:
            complemento_campo = driver.find_element(By.ID, 'pdfjs_internal_id_182R')
            complemento_campo.send_keys(complemento)
        bairro_campo = driver.find_element(By.ID, 'pdfjs_internal_id_184R')
        bairro_campo.send_keys(bairro)
        cep_campo = driver.find_element(By.ID, 'pdfjs_internal_id_206R')
        cep_campo.send_keys(cep)

        if num_estabelecimento:
            numero_estabelecimento = driver.find_element(By.ID, 'pdfjs_internal_id_208R')
            numero_estabelecimento.send_keys(num_estabelecimento)
        if email_estabelecimento:
            email_estabe = driver.find_element(By.ID, 'pdfjs_internal_id_210R')
            email_estabe.send_keys(email_estabelecimento)


        numero_associado_campo = driver.find_element(By.ID, 'pdfjs_internal_id_212R')
        numero_associado_campo.send_keys(num_acessoria)

        email_associado_campo = driver.find_element(By.ID, 'pdfjs_internal_id_214R')
        email_associado_campo.send_keys(email_acessoria)
    except Exception as e:
        salvaLogs(e, "Localização do estabelecimento")
        pass

    try:
        #caracterização do estabelecimento
        albergante = driver.find_element(By.NAME, 'Caixa de lista 1_5')
        select = Select(albergante)
        select.select_by_index(1)
        esfera_administrativa = driver.find_element(By.NAME, 'Caixa de lista 1_6')
        select = Select(esfera_administrativa)
        select.select_by_index(0)
        natureza_organizacao = driver.find_element(By.NAME, 'Caixa de lista 1_7')
        select = Select(natureza_organizacao)
        select.select_by_index(0)
    except Exception as e:
        salvaLogs(e, "Caracterização do estabelecimento")
        pass

    try:
        #responsaveis
        nome, cpf = responsavel_legal

        responsavel_legal_campo = driver.find_element(By.ID, 'pdfjs_internal_id_350R')
        responsavel_legal_campo.send_keys(nome)
        responsavel_legal_cpf = driver.find_element(By.ID, 'pdfjs_internal_id_352R')
        responsavel_legal_cpf.send_keys(cpf)

        descricao = driver.find_element(By.NAME, 'Caixa de lista 3_3')
        select = Select(descricao)
        select.select_by_value('9220 - ADMINISTRADOR')

        nome, cpf, codigo = res_tecnico

        responsavel_tecnico = driver.find_element(By.ID, 'pdfjs_internal_id_354R')
        responsavel_tecnico.send_keys(nome)
        responsavel_tecnico_cpf = driver.find_element(By.ID, 'pdfjs_internal_id_356R')
        responsavel_tecnico_cpf.send_keys(cpf)
        responsavel_tecnico_sigla = driver.find_element(By.ID, 'pdfjs_internal_id_358R')
        responsavel_tecnico_sigla.send_keys(sigla)
        responsavel_tecnico_uf = driver.find_element(By.ID, 'pdfjs_internal_id_360R')
        responsavel_tecnico_uf.send_keys(uf)
        responsavel_tecnico_inscricao = driver.find_element(By.ID, 'pdfjs_internal_id_362R')
        responsavel_tecnico_inscricao.send_keys(codigo)
        descricao = driver.find_element(By.NAME, 'Caixa de lista 3_2')
        select = Select(descricao)
        select.select_by_value('6710 -  FARMACÊUTICO, EM GERAL')
        if substitutos:
            quantidade = len(substitutos)
            nome, cpf, codigo = substitutos[0]

            responsavel_tecnico_sub1 = driver.find_element(By.ID, 'pdfjs_internal_id_366R')
            responsavel_tecnico_sub1.send_keys(nome)
            responsavel_tecnico_sub1_cpf = driver.find_element(By.ID, 'pdfjs_internal_id_368R')
            responsavel_tecnico_sub1_cpf.send_keys(cpf)
            responsavel_tecnico_sub1_sigla = driver.find_element(By.ID, 'pdfjs_internal_id_370R')
            responsavel_tecnico_sub1_sigla.send_keys(sigla)
            responsavel_tecnico_sub1_uf = driver.find_element(By.ID, 'pdfjs_internal_id_372R')
            responsavel_tecnico_sub1_uf.send_keys(uf)
            responsavel_tecnico_sub1_inscricao = driver.find_element(By.ID, 'pdfjs_internal_id_374R')
            responsavel_tecnico_sub1_inscricao.send_keys(codigo)

            descricao = driver.find_element(By.NAME, 'Caixa de lista 3_4')
            select = Select(descricao)
            select.select_by_value('6710 -  FARMACÊUTICO, EM GERAL')

            if quantidade == 2:
                nome, cpf, codigo = substitutos[1]
                responsavel_tecnico_sub2 = driver.find_element(By.ID, 'pdfjs_internal_id_376R')
                responsavel_tecnico_sub2.send_keys(nome)
                responsavel_tecnico_sub2_cpf = driver.find_element(By.ID, 'pdfjs_internal_id_378R')
                responsavel_tecnico_sub2_cpf.send_keys(cpf)
                responsavel_tecnico_sub2_sigla = driver.find_element(By.ID, 'pdfjs_internal_id_380R')
                responsavel_tecnico_sub2_sigla.send_keys(sigla)
                responsavel_tecnico_sub2_uf = driver.find_element(By.ID, 'pdfjs_internal_id_382R')
                responsavel_tecnico_sub2_uf.send_keys(uf)
                responsavel_tecnico_sub2_inscricao = driver.find_element(By.ID, 'pdfjs_internal_id_384R')
                responsavel_tecnico_sub2_inscricao.send_keys(codigo)
                descricao = driver.find_element(By.NAME, 'Caixa de lista 3_5')
                select = Select(descricao)
                select.select_by_value('6710 -  FARMACÊUTICO, EM GERAL')
    except Exception as e:
        salvaLogs(e, "Responsaveis")
        pass
        # ASSINATURAS DOS RESPONSÁVEIS LEGAL E TÉCNICO
    try:
        local = driver.find_element(By.ID, 'pdfjs_internal_id_542R')
        local.send_keys(cidade)
        hoje = date.today().strftime("%d/%m/%Y")
        data = driver.find_element(By.ID, 'pdfjs_internal_id_544R')
        data.send_keys(hoje)
    except Exception as e:
        salvaLogs(e, "Assinaturas dos responsaveis legal e tecnico")
        pass
    sleep(1)
    driver.find_element(By.ID, "downloadButton").click()
    sleep(2)
    salvarArquivo(tipo, razao, "FormularioXII")