import pandas as pd
import sys, os

def obter_hsp(coordenadas):
    lat, lon = coordenadas

    # Lendo o arquivo CSV para um DataFrame
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    df_path = "global_horizontal_means.csv"
    df_full_path = os.path.join(application_path, df_path)
    df = pd.read_csv(df_full_path, delimiter=';')

    # Convertendo os valores para float, se eles ainda não forem
    df['LON'] = df['LON'].astype(float)
    df['LAT'] = df['LAT'].astype(float)

    # Encontrando a linha com as coordenadas mais próximas
    # Calcula a diferença absoluta em relação ao ponto fornecido e encontra o índice do valor mínimo
    closest_idx = ((df['LAT'] - lat).abs() + (df['LON'] - lon).abs()).idxmin()

    # Obtendo a linha do DataFrame com os valores mais próximos
    closest_row = df.iloc[closest_idx]

    print(closest_row[['LON', 'LAT']])

    # Extraindo os valores de HSP mensais e anual
    hsp_values = closest_row[['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']].tolist()

    return hsp_values

