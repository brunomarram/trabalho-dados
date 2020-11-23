import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def converter_dados_numericos_notacao_brasileira_para_float(value):
    if(value == '-'):
        return -1
    resultado = value.replace(" ", "")
    resultado = resultado.replace(".", "")
    resultado = resultado.replace(",", ".")
    return resultado

def carregar_dataset_e_converter_dados(nome_arquivo):

    df = pd.read_csv(nome_arquivo, index_col=False, squeeze=True)

    #Remove colunas unamed
    df = df.dropna(how='all', axis='columns')

    # Removendo aspas duplas e espaços em branco nos nomes das colunas
    df.columns = df.columns.str.replace('"', '')
    df.columns = df.columns.str.strip()

    # Removendo aspas duplas e espaços em branco nos tipos de despesas
    df.iloc[:, 0] = df.iloc[:, 0].str.replace('"', '')
    df.iloc[:, 0] = df.iloc[:, 0].str.strip()

    # Percorre as colunas selecionadas do DF e converte os valores numéricos na notação BR para o padrão float
    df.iloc[:, 1:9] = df.iloc[:, 1:9].applymap(converter_dados_numericos_notacao_brasileira_para_float) # Também funciona com .loc, a diferença é que requer os nomes da colunas.

    # Faz o casting nas colunas selecionadas do DF para float
    df.iloc[:, 1:9] = df.iloc[:, 1:9].astype('float') # Também funciona com .loc, a diferença é que requer os nomes da colunas.

    return df

def retorna_dataset_com_soma_colunas_classes_sociais(df, colunas_dataset):

    linhas_familia = list(df.index[-2:])

    soma_1908 = df.drop(linhas_familia)[colunas_dataset[1]]
    soma_1908 = soma_1908[soma_1908 >= 0].sum()

    soma_2862 = df.drop(linhas_familia)[colunas_dataset[2]]
    soma_2862 = soma_2862[soma_2862 >= 0].sum()

    soma_5724 = df.drop(linhas_familia)[colunas_dataset[3]]
    soma_5724 = soma_5724[soma_5724 >= 0].sum()

    soma_9540 = df.drop(linhas_familia)[colunas_dataset[4]]
    soma_9540 = soma_9540[soma_9540 >= 0].sum()

    soma_14310 = df.drop(linhas_familia)[colunas_dataset[5]]
    soma_14310 = soma_14310[soma_14310 >= 0].sum()

    soma_23850 = df.drop(linhas_familia)[colunas_dataset[6]]
    soma_23850 = soma_23850[soma_23850 >= 0].sum()

    soma_gastos = ["Total gasto por classes"]
    soma_gastos.append(soma_1908)
    soma_gastos.append(soma_2862)
    soma_gastos.append(soma_5724)
    soma_gastos.append(soma_9540)
    soma_gastos.append(soma_14310)
    soma_gastos.append(soma_23850)

    nova_linha = pd.DataFrame([soma_gastos], columns=colunas_dataset, index=[linhas_familia[-1]+1])

    df_resultante = pd.concat([df, nova_linha])

    return df_resultante

def retorna_indices_top_N_itens_mais_vendidos_por_classe_social(df, classe_social, colunas_dataset, qtd_top_itens):

    linhas_familia_e_total_por_classes = list(df.index[-3:])

    indice_soma_gastos = int(df.index[-1])
    soma_gastos = df.iloc[indice_soma_gastos, [classe_social]][0]

    despesas_classe_social = df.drop(linhas_familia_e_total_por_classes).iloc[:, [classe_social]].apply(lambda item: item/soma_gastos)
    despesas_classe_social.sort_values(by=colunas_dataset[classe_social], ascending=False, inplace=True)

    lista_top_N = list(despesas_classe_social.index[0:qtd_top_itens]) + list(df.index[-1:])
    # df.iloc[lista_top_N, [0, classe_social]]

    return lista_top_N

def retorna_lista_top_N_itens_mais_vendidos_classe_social(df, classe_social, lista_top_N):

    return df.iloc[lista_top_N, [0, classe_social]]

def plot_grafico_barras_lista_top_N_itens(df, classe_social, colunas_dataset, lista_top_N, cor):

    df.iloc[lista_top_N[:-1], [0, classe_social]].plot(kind='barh', x=colunas_dataset[0], y=colunas_dataset[classe_social], color=cor)
    plt.show()