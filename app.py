import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request, jsonify
import gc

app = Flask(__name__)

request_counter = 0  # Contador de requisições

@app.after_request
def cleanup(response):
    global request_counter

    # Incrementa o contador de requisições
    request_counter += 1

    # Limpa a memória a cada 5 requisições
    if request_counter % 5 == 0:
        gc.collect()

    return response

@app.route('/')
def index():
        try:
            # Fazer a requisição HTTP para a página
            response = requests.get(request.args.get('url'))
            response.raise_for_status()  # Verificar se a requisição foi bem-sucedida

            # Parsear o HTML da página com BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Procurar todas as tags <script> com o atributo type="application/ld+json"
            ld_json_scripts = soup.find_all('script', type='application/ld+json')

            # Extrair e exibir o conteúdo JSON de cada script encontrado
            for script in ld_json_scripts:
                try:
                    json_content = json.loads(script.string)  # Carregar o conteúdo como JSON
                    return jsonify(json_content)
                    # print(json.dumps(json_content, indent=2))  # Imprimir o JSON formatado
                except json.JSONDecodeError:
                    print("Erro ao decodificar JSON")
        except Exception as e:
                return json.dumps({"error": str(e)}, ensure_ascii=False)

if __name__ == '__main__':
    app.run()
