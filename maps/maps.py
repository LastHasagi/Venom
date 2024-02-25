import json
import googlemaps
import time
from tqdm import tqdm

gmaps = googlemaps.Client(key='AIzaSyCcvCeFEnkVH0XkZ_sztAtdhrhYQXk974Y')

def buscar_lojas(ramo_atividade, quantidade):
    resultados = []
    next_page_token = None

    with tqdm(total=quantidade, desc='Progresso') as pbar:
        while len(resultados) < quantidade:
            
            # Use a API do Google Places para buscar lugares com base no ramo de atividade
            if next_page_token:
                places_result = gmaps.places(query=ramo_atividade, page_token=next_page_token)
            else:
                places_result = gmaps.places(query=ramo_atividade)

            for place in places_result['results']:
                nome_loja = place['name']
                place_id = place['place_id']
                segmento = place.get('types', [])

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
                pbar.update(1)

                if len(resultados) >= quantidade:
                    break

            # Token da próxima página
            next_page_token = places_result.get('next_page_token')

            # Delay de 2 segundos para a próxima requisição
            if next_page_token:
                time.sleep(2)

    return resultados[:quantidade]

# Defina o ramo de atividade e a quantidade de lojas a serem buscadas
ramo_atividade = ['sorvete']
quantidade_lojas = 10
resultado_final = buscar_lojas(ramo_atividade, quantidade_lojas)

# Salvar o resultado em um arquivo JSON
with open('tattoo.json', 'w', encoding='utf-8') as arquivo_json:
    json.dump(resultado_final, arquivo_json, ensure_ascii=False, indent=2)

print(f'Dados das {quantidade_lojas} lojas foram salvos em "sorveteria.json".')
