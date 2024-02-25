import json

# Ler o arquivo JSON
with open('tattoo.json', 'r', encoding='utf-8') as arquivo_json:
    dados = json.load(arquivo_json)

# Modificar os números de telefone
for loja in dados:
    telefone = loja.get('phone', '')
    if telefone != 'N/A':
        # Remover os caracteres não numéricos
        telefone = ''.join(c for c in telefone if c.isdigit())
        # Adicionar o prefixo '55'
        telefone = '55' + telefone
        # Atualizar o número de telefone na loja
        loja['phone'] = telefone

# Escrever os dados de volta no arquivo JSON
with open('tattoo1.json', 'w', encoding='utf-8') as arquivo_json:
    json.dump(dados, arquivo_json, ensure_ascii=False, indent=2)