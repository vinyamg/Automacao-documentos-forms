from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import Select
from extrai_pdf import main
import json
from datetime import date
import os
from extrai_cnpj import extrator
import pyautogui
import pyperclip

def organiza(pdf):
    razao, fantasia, cnpj, rua, bairro, cep, objeto_licenciado, numero_rua, cmvs, cpfs, profs, res_legal, res_tecnico, res_tecnico_sub, l, s, p, c, a, codigo_cnae_numero, codigo_descricao, cidade = main(pdf)
    razao2, fantasia2, complemento, email, ddd, numero, cidade2, codigo_cnae_numero2 = extrator(cnpj)

    codigo_cnae_numero2 = f"{codigo_cnae_numero2[:4]}-{codigo_cnae_numero2[4]}/{codigo_cnae_numero2[5:]}"
    numero = f"({ddd}) {numero}"

    if razao2:
        if razao != razao2:
            razao = razao2
    if fantasia2:
        if fantasia != fantasia2:
            fantasia = fantasia2
    if cidade2:
        if cidade != cidade2:
            cidade = cidade2
    if codigo_cnae_numero2:
        if codigo_cnae_numero != codigo_cnae_numero2:
            codigo_cnae_numero = codigo_cnae_numero2


    substitutos = []
    responsavel_legal = (res_legal, cpfs[0])
    res_tecnico = (res_tecnico, cpfs[1], profs[0])
    if res_tecnico_sub:

        cpf_num = 2
        prof_num = 1
        for i in res_tecnico_sub:
            res_tecnico_sub_completo = (i, cpfs[cpf_num], profs[prof_num])
            substitutos.append(res_tecnico_sub_completo)
            cpf_num += 1
            prof_num += 1
    return razao, fantasia, cnpj, rua, bairro, cep, objeto_licenciado, numero_rua, cmvs, responsavel_legal, res_tecnico, substitutos, l, s, p, c, a, codigo_cnae_numero, codigo_descricao, cidade, email, numero, complemento
def salvarArquivo(tipo, razao, formulario):
    pyautogui.press("backspace")
    sleep(0.5)
    pyperclip.copy(f'{formulario} - {razao} {tipo}')
    pyautogui.hotkey('ctrl', 'v')

def salvaLogs(erro, onde):
    with open("modulos/LogsErros.txt", "a") as arq:
        arq.write("=" * 20 + "\n")
        arq.write(f"Local: {onde}\n\n{erro}")
        arq.write("=" * 20 + "\n")

def automata2(pdf, tipo_modo, decisao, vre):
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
    driver.get(f'file:///{diretorio_script}/padrao/formulario_XI.pdf')
    sleep(2)

    try:
        #solicitação
        if tipo == "Alteração" and (decisao == "Baixa(Tecnico)" or decisao == "Assunção(Tecnico)"):
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[3]/input').click()
        else:
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[2]/div[1]/div[3]/section[9]/input').click()
        if vre:
            vre_campo = driver.find_element(By.ID, 'pdfjs_internal_id_209R')
            vre_campo.send_keys(vre)
        cmvs_campo = driver.find_element(By.XPATH, '//*[@id="pdfjs_internal_id_215R"]')
        cmvs_campo.send_keys(cmvs)
        objeto_solicitacao = driver.find_element(By.NAME, 'Caixa de lista 1_3')
        select = Select(objeto_solicitacao)
        select.select_by_value(objeto_licenciado.title())

        tipo_solicitacao = driver.find_element(By.NAME, 'Caixa de lista 1_5')
        select = Select(tipo_solicitacao)
        if tipo == 'Inicial':
            select.select_by_index(0)
        elif tipo == 'Renovação':
            select.select_by_index(1)
        elif tipo == 'Alteração':
            select.select_by_index(2)
            tipo_alteracao = driver.find_element(By.NAME, 'Caixa de lista 1_6')
            select = Select(tipo_alteracao)
            if decisao == "Baixa(Tecnico)":
                select.select_by_index(1)
            elif decisao == "Assunção(Tecnico)":
                select.select_by_index(0)
            elif decisao == "Responsavel legal":
                select.select_by_index(5)
            elif decisao == "Razão Social":
                select.select_by_index(3)
            elif decisao == "Endereço":
                select.select_by_index(2)
            elif decisao == "Nome Fantasia":
                select.select_by_index(4)

        elif tipo == "Cancelamento":
            select.select_by_index(4)
        else:
            select.select_by_index(1)

    except Exception as e:
        salvaLogs(e, "Solicitação")
        pass

    try:
        #identificação do estabelecimento
        razao_campo = driver.find_element(By.ID, 'pdfjs_internal_id_221R')
        razao_campo.send_keys(razao)
        fantasia_campo = driver.find_element(By.ID, 'pdfjs_internal_id_223R')
        fantasia_campo.send_keys(fantasia)
        natureza = driver.find_element(By.NAME, 'Caixa de lista 2')
        select = Select(natureza)
        select.select_by_index(2) #para juridico 2 para fisico 1
        cnpj_campo = driver.find_element(By.ID, 'pdfjs_internal_id_227R')
        cnpj_campo.send_keys(cnpj)
    except Exception as e:
        salvaLogs(e, "Identificação do estabelecimento")
        pass

    try:
        #Localização do estabelecimento
        logradouro = driver.find_element(By.ID, 'pdfjs_internal_id_181R')
        logradouro.send_keys(rua)
        numero = driver.find_element(By.ID, 'pdfjs_internal_id_185R')
        numero.send_keys(numero_rua)
        if complemento:
            complemento_campo = driver.find_element(By.ID, 'pdfjs_internal_id_187R')
            complemento_campo.send_keys(complemento)

        bairro_campo = driver.find_element(By.ID, 'pdfjs_internal_id_189R')
        bairro_campo.send_keys(bairro)
        cep_campo = driver.find_element(By.ID, 'pdfjs_internal_id_237R')
        cep_campo.send_keys(cep)

        if num_estabelecimento:
            numero_estabelecimento = driver.find_element(By.ID, 'pdfjs_internal_id_191R')
            numero_estabelecimento.send_keys(num_estabelecimento)
        if email_estabelecimento:
            email_estabe = driver.find_element(By.ID, 'pdfjs_internal_id_193R')
            email_estabe.send_keys(email_estabelecimento)

        numero_associado_campo = driver.find_element(By.ID, 'pdfjs_internal_id_229R')
        numero_associado_campo.send_keys(num_acessoria)

        email_associado_campo = driver.find_element(By.ID, 'pdfjs_internal_id_231R')
        email_associado_campo.send_keys(email_acessoria)
    except Exception as e:
        salvaLogs(e, "Localização do estabelecimento")
        pass

    try:
        #caracterização do estabelecimento
        #albergante = driver.find_element(By.NAME, 'Caixa de lista 1_5')
        #select = Select(albergante)
        #select.select_by_index(1)
        esfera_administrativa = driver.find_element(By.NAME, 'Caixa de lista 1')
        select = Select(esfera_administrativa)
        select.select_by_index(0)
        natureza_organizacao = driver.find_element(By.NAME, 'Caixa de lista 1_2')
        select = Select(natureza_organizacao)
        select.select_by_index(0)
        try:
            cnae = driver.find_element(By.NAME, 'Caixa de lista 1_4')
            select = Select(cnae)
            for option in select.options:
                value = option.get_attribute("value")
                if value.startswith(codigo_cnae_numero):
                    select.select_by_value(value)
                    break
        except Exception as e:
            pass
    except Exception as e:
        salvaLogs(e, "Caracterização do estabelecimento")
        pass

    try:
        #responsaveis
        nome, cpf = responsavel_legal

        responsavel_legal_campo = driver.find_element(By.ID, 'pdfjs_internal_id_389R')
        responsavel_legal_campo.send_keys(nome)
        responsavel_legal_cpf = driver.find_element(By.ID, 'pdfjs_internal_id_391R')
        responsavel_legal_cpf.send_keys(cpf)

        descricao = driver.find_element(By.NAME, 'Caixa de lista 3')
        select = Select(descricao)
        select.select_by_value('9220 - ADMINISTRADOR')

        nome, cpf, codigo = res_tecnico

        responsavel_tecnico = driver.find_element(By.ID, 'pdfjs_internal_id_395R')
        responsavel_tecnico.send_keys(nome)
        responsavel_tecnico_cpf = driver.find_element(By.ID, 'pdfjs_internal_id_397R')
        responsavel_tecnico_cpf.send_keys(cpf)
        responsavel_tecnico_sigla = driver.find_element(By.ID, 'pdfjs_internal_id_399R')
        responsavel_tecnico_sigla.send_keys(sigla)
        responsavel_tecnico_uf = driver.find_element(By.ID, 'pdfjs_internal_id_401R')
        responsavel_tecnico_uf.send_keys(uf)
        responsavel_tecnico_inscricao = driver.find_element(By.ID, 'pdfjs_internal_id_403R')
        responsavel_tecnico_inscricao.send_keys(codigo)
        try:
            descricao = driver.find_element(By.NAME, 'Caixa de lista 3_2')
            select = Select(descricao)
            select.select_by_value('6710 - FARMACÊUTICO, EM GERAL')
        except Exception as e:
            print(e)
            pass
        if decisao != "Assunção(Tecnico)" and decisao != "Baixa(Tecnico)":
            if substitutos:
                quantidade = len(substitutos)
                nome, cpf, codigo = substitutos[0]

                responsavel_tecnico_sub1 = driver.find_element(By.ID, 'pdfjs_internal_id_405R')
                responsavel_tecnico_sub1.send_keys(nome)
                responsavel_tecnico_sub1_cpf = driver.find_element(By.ID, 'pdfjs_internal_id_407R')
                responsavel_tecnico_sub1_cpf.send_keys(cpf)
                responsavel_tecnico_sub1_sigla = driver.find_element(By.ID, 'pdfjs_internal_id_409R')
                responsavel_tecnico_sub1_sigla.send_keys(sigla)
                responsavel_tecnico_sub1_uf = driver.find_element(By.ID, 'pdfjs_internal_id_411R')
                responsavel_tecnico_sub1_uf.send_keys(uf)
                responsavel_tecnico_sub1_inscricao = driver.find_element(By.ID, 'pdfjs_internal_id_413R')
                responsavel_tecnico_sub1_inscricao.send_keys(codigo)

                try:
                    descricao = driver.find_element(By.NAME, 'Caixa de lista 3_3')
                    select = Select(descricao)
                    select.select_by_value('6710 - FARMACÊUTICO, EM GERAL')
                except Exception as e:
                    print(e)
                    pass

                if quantidade == 2:
                    nome, cpf, codigo = substitutos[1]
                    responsavel_tecnico_sub2 = driver.find_element(By.ID, 'pdfjs_internal_id_415R')
                    responsavel_tecnico_sub2.send_keys(nome)
                    responsavel_tecnico_sub2_cpf = driver.find_element(By.ID, 'pdfjs_internal_id_417R')
                    responsavel_tecnico_sub2_cpf.send_keys(cpf)
                    responsavel_tecnico_sub2_sigla = driver.find_element(By.ID, 'pdfjs_internal_id_419R')
                    responsavel_tecnico_sub2_sigla.send_keys(sigla)
                    responsavel_tecnico_sub2_uf = driver.find_element(By.ID, 'pdfjs_internal_id_421R')
                    responsavel_tecnico_sub2_uf.send_keys(uf)
                    responsavel_tecnico_sub2_inscricao = driver.find_element(By.ID, 'pdfjs_internal_id_423R')
                    responsavel_tecnico_sub2_inscricao.send_keys(codigo)
                    try:
                        descricao = driver.find_element(By.NAME, 'Caixa de lista 3_4')
                        select = Select(descricao)
                        select.select_by_value('6710 - FARMACÊUTICO, EM GERAL')
                    except Exception as e:
                        print(e)
                        pass
    except Exception as e:
        salvaLogs(e, "Responsaveis")
        pass
    # ASSINATURAS DOS RESPONSÁVEIS LEGAL E TÉCNICO
    try:
        local = driver.find_element(By.ID, 'pdfjs_internal_id_385R')
        if cidade:
            local.send_keys(cidade)
        else:
            local.send_keys("São Paulo")
        hoje = date.today().strftime("%d/%m/%Y")
        data = driver.find_element(By.ID, 'pdfjs_internal_id_387R')
        data.send_keys(hoje)
    except Exception as e:
        salvaLogs(e, "Assinatura dos responsaveis legal e tecnico")
        pass
    sleep(1)
    driver.find_element(By.ID, "downloadButton").click()
    sleep(2)
    salvarArquivo(tipo, razao, "FormularioXI")