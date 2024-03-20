import json
import googlemaps
import time
from tqdm import tqdm

gmaps = googlemaps.Client(key='AIzaSyCcvCeFEnkVH0XkZ_sztAtdhrhYQXk974Y')

def buscar_lojas(ramo_atividade, quantidade, localizacao):
    resultados = []
    lojas_visitadas = set()
    next_page_token = None

    with tqdm(total=quantidade, desc=f'Progresso em {localizacao}') as pbar:
        while len(resultados) < quantidade:
            
            # Use a API do Google Places para buscar lugares com base no ramo de atividade
            if next_page_token:
                places_result = gmaps.places(query=ramo_atividade, location=localizacao, page_token=next_page_token)
            else:
                places_result = gmaps.places(query=ramo_atividade, location=localizacao)

            for place in places_result['results']:
                nome_loja = place['name']
                place_id = place['place_id']
                segmento = place.get('types', [])

                # Se a loja já foi visitada, pule para a próxima
                if place_id in lojas_visitadas:
                    continue

                # Use o place_id para obter mais informações sobre a loja
                details = gmaps.place(place_id=place_id, fields=['name', 'formatted_phone_number', 'formatted_address'])

                # Adicione os dados ao resultado
                resultado_loja = {
                    'title': nome_loja,
                    'phone': details['result'].get('formatted_phone_number', 'N/A'),
                    'endereço': details['result'].get('formatted_address', 'N/A'),
                    'segmento': segmento
                }
                resultados.append(resultado_loja)
                lojas_visitadas.add(place_id)
                pbar.update(1)

            # Token da próxima página
            next_page_token = places_result.get('next_page_token')

            # Delay de 5 segundos para a próxima requisição
            if next_page_token:
                time.sleep(5)
            else:
                break

    return resultados

# Defina o ramo de atividade e a quantidade de lojas a serem buscadas
ramo_atividade = 'fisioterapia'
quantidade_lojas = 300

# Pergunte os locais que você deseja
localizacoes = []
while True:
    local = input("Digite o local que você deseja: ")
    localizacoes.append(local)
    mais_locais = input("Você quer adicionar mais locais? (s/n): ")
    if mais_locais.lower() != 's':
        break

for localizacao in localizacoes:
    # Converta o local em coordenadas de latitude e longitude
    geocode_result = gmaps.geocode(localizacao)
    localizacao_coordenadas = f"{geocode_result[0]['geometry']['location']['lat']},{geocode_result[0]['geometry']['location']['lng']}"

    resultado_final = buscar_lojas(ramo_atividade, quantidade_lojas, localizacao_coordenadas)

    # Salvar o resultado em um arquivo JSON
    with open(f'fisio_{localizacao.replace(", ", "_").replace(" ", "_")}.json', 'w', encoding='utf-8') as arquivo_json:
        json.dump(resultado_final, arquivo_json, ensure_ascii=False, indent=2)

    print(f'Dados das lojas foram salvos em "fisio_{localizacao.replace(", ", "_").replace(" ", "_")}.json".')

    # Adicione um atraso de 5 segundos entre as chamadas para a API do Google Places
    time.sleep(5)