import requests
import sys
import time
from datetime import datetime

# Função para obter as datas da API do Banco Central do Brasil
def get_last_dates(url_bcb, num_days):
    while True:
        try:
            response_bcb = requests.get(url_bcb)
            if response_bcb.status_code == 200:
                data_bcb = response_bcb.json()
                return [entry['data'] for entry in data_bcb[-num_days:]]
            else:
                print("Erro ao acessar a URL do Banco Central do Brasil:", response_bcb.status_code)
        except Exception as e:
            print("Erro durante a solicitação:", e)
        print("Tentando novamente...")
        time.sleep(1)

def format_date_for_ptax(date_str):
    parts = date_str.split('/')
    return "{}-{}-{}".format(parts[1], parts[0], parts[2])

def main():
    # Verifique se o número de dias foi fornecido como argumento de linha de comando
    if len(sys.argv) != 2:
        print("Número de dias não informado. Use o comando no formato: python ptax.py <número de dias>")
        return

    try:
        num_days = int(sys.argv[1])
    except ValueError:
        print("O argumento deve ser um número inteiro.")
        return

    # URL da API do Banco Central do Brasil para os últimos dias úteis
    url_bcb = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados?formato=json"
    
    if num_days == 0:
        # Usar a data de hoje no formato DD/MM/YYYY
        today_date = datetime.now().strftime("%d/%m/%Y")
        last_dates = [today_date]
    else:
        # Obter as últimas datas disponíveis
        last_dates = get_last_dates(url_bcb, num_days)

    print("Últimas datas:", last_dates)
    
    # Lista para armazenar as cotações de venda do dólar
    cotacoes_ptax = []
    
    # Loop pelas datas
    for last_date in last_dates:
        # Formate a data para o formato necessário na URL da API de PTAX
        formatted_date = format_date_for_ptax(last_date)
        
        # Construa a URL da API de PTAX com a última data
        url_ptax = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='USD'&@dataInicial='{}'&@dataFinalCotacao='{}'&$top=4&$format=json&$select=cotacaoVenda".format(formatted_date, formatted_date)
        
        try:
            # Faça uma solicitação GET para a URL da API de PTAX
            response_ptax = requests.get(url_ptax)
            if response_ptax.status_code == 200:
                data_ptax = response_ptax.json()
                if data_ptax['value']:
                    cotacoes = [entry['cotacaoVenda'] * 1000 for entry in data_ptax['value']]
                    cotacoes_ptax.extend(cotacoes)
                else:
                    print("Sem dados disponíveis para a data:", last_date)
            else:
                print("Erro ao acessar a URL de PTAX:", response_ptax.status_code)
        except Exception as e:
            print("Erro durante a solicitação da API de PTAX:", e)
    
    # Ordenar as cotações em ordem decrescente
    cotacoes_ptax.sort(reverse=True)
    
    # Imprimir as cotações em ordem decrescente no formato desejado
    print("Cotações de venda do dólar (multiplicadas por 1000) em ordem decrescente:")
    for i in range(len(cotacoes_ptax)):
        cotacao_formatada = "{:<7}".format("{:.1f}".format(cotacoes_ptax[i]))
        if i < len(cotacoes_ptax) - 1:
            diff = cotacoes_ptax[i] - cotacoes_ptax[i+1]
            diff_formatada = "{:.1f}".format(diff)
            print("{:7} [{}]".format(cotacao_formatada, diff_formatada))
        else:
            print(cotacao_formatada)
    
    # Imprimir o link construído para a API de PTAX, assim podemos verificar ERROS!
    # print("Link da API de PTAX:", url_ptax)

if __name__ == "__main__":
    main()
