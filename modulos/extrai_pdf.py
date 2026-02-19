import pdfplumber
import re
import json
from pdf2image import convert_from_path
import pytesseract

def ocr_leitor(pdf):
    paginas = convert_from_path(pdf, dpi=300)
    texto_final = ""

    for i, pagina in enumerate(paginas):
        texto = pytesseract.image_to_string(pagina, lang="por")
        texto_final += f"\n--- Página {i + 1} ---\n"
        texto_final += texto
    return texto_final
def extracao(pdf):
    with pdfplumber.open(pdf) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    texto_normaizado = re.sub(r'\s+', ' ', texto)
    return texto, texto_normaizado

def regex_simples(texto, modo):
    class regexs:
        cpf = r'CPF:\s(\d{11})'
        cnpj = r'CNPJ / CPF:\s(.*)'
        razao_social = r'RAZÃO SOCIAL:\s(.*)'
        fantasia = r'NOME FANTASIA:\s(.*)'
        rua_logadouro = r'LOGRADOURO:\s(.*)'
        complemento = r'COMPLEMENTO:\s(.*)'
        bairro = r'BAIRRO:\s(.*)'
        cidade = r'(\s\D+)\s\d{2}/\d{2}/\d{4}'
        cep2 = r'CEP:(\s\d+)' #r'CEP:(\s\d+-\d+)'
        cep1 = r'CEP:(\s\d+-\d+)'
        objeto_licenciado = r'OBJETO LICENCIADO:\s(.*)'
        cmvs = r'\d+\-\d+\-\d+\-\d+\-\d+'
        prof = r'CONSELHO\sPROF:\s(\d+)'
        responsavel_legal = r'RESPONSÁVEL\sLEGAL:\s(.*)'
        responsavel_tecnico = r'RESPONSÁVEL\sTÉCNICO:\s(.*)'
        responsavel_tecnico_substituto = r'RESPONSÁVEL\sTÉCNICO\sSUBSTITUTO:\s(.*)'

        codigo = r'(\d{4}-\d\/\d{2})\s(.*)'

        #serviços
        pressao_arterial = r'PRESSÃO\sARTERIAL'
        perfurar_lobulo = r'PERFURAR\sLÓBULO\sAURICULAR'
        temperatura = r'TEMPERATUR'
        controle_especial = r'CONTROLE\sESPECIAL'
        atencao_farmaceutica = r'ATENÇÃO\sFARMACÊUTICA'

    pressao = re.search(regexs.pressao_arterial, texto)
    lobulo = re.search(regexs.perfurar_lobulo, texto)
    temperatura = re.search(regexs.temperatura, texto)
    controle_especial = re.search(regexs.controle_especial, texto)
    atencao_farmaceutica = re.search(regexs.atencao_farmaceutica, texto)

    codigo_cnae = re.search(regexs.codigo, texto)
    cmvs = re.search(regexs.cmvs, texto)
    razao = re.search(regexs.razao_social, texto)
    nome_fantasia = re.search(regexs.fantasia, texto)
    cnpj = re.search(regexs.cnpj, texto)
    rua = re.search(regexs.rua_logadouro, texto) #mal estruturado, versão estruturada abaixo
    bairro = re.search(regexs.bairro, texto)
    cidade = re.findall(regexs.cidade, texto)
    verifica_cidade = len(cidade)

    # Formata os dados
    if verifica_cidade == 2:
        cidade = cidade[1]
    elif verifica_cidade > 2:
        cidade.clear()
        cidade.extend(" ")
        cidade.extend(" São Paulo")
        cidade = cidade[1]
    else:
        cidade.extend(" ")
    cep = re.search(regexs.cep1, texto)
    if not cep:
        cep = re.search(regexs.cep2, texto)
    objeto_licenciado = re.search(regexs.objeto_licenciado, texto)

    #Tipo de formato de dados
    if modo == "1":
        numero_rua = re.sub(r'.*:\s', '', rua.group(1))
        rua = re.sub(r':.*', '', rua.group(1))
    else:
        numero_rua = re.sub(r'.*NÚMERO:\s', '', rua.group(1))
        rua = re.sub(r'NÚMERO:.*', '', rua.group(1))
    razao = re.sub(r'\sCNPJ\sALBERGANTE:', '', razao.group(1))


    res_legal = re.search(regexs.responsavel_legal, texto)
    res_tecnico = re.search(regexs.responsavel_tecnico, texto)

    res_tecnico_substituto = re.findall(regexs.responsavel_tecnico_substituto, texto)
    prof = re.findall(regexs.prof, texto)
    cpf = re.findall(regexs.cpf, texto)

    if not codigo_cnae:
        codigo_cnae_numero = ""
        codigo_descricao = ""
    else:
        codigo_cnae_numero = codigo_cnae.group(1)
        codigo_descricao = codigo_cnae.group(2)


    return razao, nome_fantasia.group(1), cnpj.group(1), rua, bairro.group(1), cep.group(1), objeto_licenciado.group(1), numero_rua, cmvs.group(0), cpf, prof, res_legal.group(1), res_tecnico.group(1), res_tecnico_substituto, pressao, lobulo, temperatura, controle_especial, atencao_farmaceutica, codigo_cnae_numero, codigo_descricao, cidade.lstrip()

def main(nome):
    with open('../config.txt', "r", encoding="utf-8") as f:
        dados = json.load(f)
        modo_dado = dados['modo']
    try:
        dados, normalizado = extracao(nome)
        return regex_simples(dados, modo_dado)
    except Exception:
        dados = ocr_leitor(nome)
        return regex_simples(dados, modo_dado)

if __name__ == "__main__":
    main()