import json
import os

# Verifique se o diretório 'contatos_unificados' existe, se não, crie-o
if not os.path.exists('contatos_unificados'):
    os.makedirs('contatos_unificados')

# Obter a lista de todos os arquivos JSON na pasta atual
arquivos_json = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')]

# Lista para armazenar todos os dados
todos_dados = []

for arquivo in arquivos_json:
    # Ler o arquivo JSON
    with open(arquivo, 'r', encoding='utf-8') as arquivo_json:
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

    # Adicionar os dados à lista de todos os dados
    todos_dados.extend(dados)

# Escrever todos os dados em um único arquivo JSON
with open('contatos_unificados/todos_contatos.json', 'w', encoding='utf-8') as arquivo_json:
    json.dump(todos_dados, arquivo_json, ensure_ascii=False, indent=2)