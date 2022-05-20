from bs4 import BeautifulSoup
import pandas as pd
import requests
import ipdb
import re

# Fazendo requisição para receber os dados da pagina com a lib Requests
url = 'https://en.wikipedia.org/wiki/List_of_best-selling_music_artists'
response = requests.get(url)

# Analisando os dados recebidos com a lib Beautiful Soup
soup = BeautifulSoup(response.text, 'html.parser')

# Pegando Todas as tabelas dos dados analisados em html
artists_table = soup.findAll('table', class_='wikitable')

# Tratados os dados html recebido e transformando em um dataframe usando o Pandas
df = pd.read_html(str(artists_table))

# renomeando a primeira tabela
df[0] = df[0].rename(columns={
                     'Release year of first charted record': 'Release-year of first charted record'})

# Juntar todas as tabelas
all_df = pd.concat(
    [
        df[0],
        df[1],
        df[2],
        df[3],
        df[4],
        df[5],
    ],
    ignore_index=True
).iloc[0:, 0:6]

# Renomeando as colunas
all_df = all_df.rename(columns={
    'Artist': 'Artista',
    'Country / Market': 'País',
    'Period active': 'Periodo ativo',
    'Release-year of first charted record': 'Auge',
    'Genre': 'Genero',
    'Total certified units(from available markets)[a]': 'Vendas certificadas',
})


# Aplicando regex no nome das colunas para retirar links
all_df['Genero'] = all_df['Genero'].apply(
    lambda x: re.sub('\[\d+\]', '', x).strip())
all_df['Auge'] = all_df['Auge'].apply(
    lambda x: re.sub('\[\d+\]', '', x).strip())
all_df['Periodo ativo'] = all_df['Periodo ativo'].apply(
    lambda x: re.sub('\[\d+\]', '', x).strip())
all_df['Vendas certificadas'] = all_df['Vendas certificadas'].apply(
    lambda x: re.findall(':\s(\d*.\d*\s?\w*)', x)[0])

ipdb.set_trace()

# Salvando a tabela com todos os artistas em um arquivo .json
all_df.to_json('top-artists.json', orient='records', indent=2)
