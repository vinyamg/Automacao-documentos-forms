import requests

def extrator(cnpj):
    url = f"https://api.opencnpj.org/{cnpj}"

    requisicao = requests.get(url)
    if requisicao.status_code == 200:
        formatando = requisicao.json()

        razao_social = formatando["razao_social"]
        nome_fantasia = formatando["nome_fantasia"]
        complemento = formatando["complemento"]
        email = formatando["email"]
        try:
            ddd = formatando['telefones'][0]['ddd']
            numero = formatando['telefones'][0]['numero']
        except Exception:
            ddd = ""
            numero = ""
        cidade = formatando['municipio']
        cnae = formatando['cnae_principal']

        return razao_social, nome_fantasia, complemento, email, ddd, numero, cidade, cnae

if __name__ == "__main__":
    extrator()