import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_df_estado(estado):
    #realiza tratamento de todas as células discutidas no topo
    nome_arquivo_despesas = "../dados-limpos/aquisicao_por_classe_de_rendimento_e_estado/%s/dados-limpos/%s_tipos_despesas.csv" % (estado, estado)
    
    df_despesas = carregar_dataset_e_converter_dados(nome_arquivo_despesas)
    df_despesas = df_despesas.drop(columns=['Total'])
    df_despesas = df_despesas.drop(columns=['Despesa monetária e não monetária média mensal familiar (R$)'])
    df_despesas = df_despesas.drop([0, 1, 2]).reset_index(drop=True)
    df_despesas = retorna_dataset_com_soma_colunas_classes_sociais(df_despesas)
    
    return df_despesas

def get_df_estado_alimentacao(estado):
    #realiza tratamento de todas as células discutidas no topo
    nome_arquivo_alimentacao = "../dados-limpos/aquisicao_por_classe_de_rendimento_e_estado/%s/dados-limpos/%s_alimentacao.csv" % (estado, estado)
    
    df_despesas = carregar_dataset_e_converter_dados(nome_arquivo_alimentacao)
    df_despesas = df_despesas.drop(columns=['Total'])
    df_despesas = df_despesas.drop(columns=['Despesa monetária e não monetária média mensal familiar (R$)'])
    df_despesas = df_despesas.drop([0]).reset_index(drop=True)
    df_despesas = retorna_dataset_com_soma_colunas_classes_sociais(df_despesas)
    
    return df_despesas

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

def retorna_dataset_com_soma_colunas_classes_sociais(df):

    colunas_df = retorna_colunas_df(df)

    linhas_familia = list(df.index[-2:])

    soma_gastos = ["Total gasto por classes"]

    for coluna in colunas_df[1:]:

        soma = df.drop(linhas_familia)[coluna]
        soma = soma[soma >= 0].sum()

        soma_gastos.append(soma)

    nova_linha = pd.DataFrame([soma_gastos], columns=colunas_df, index=[linhas_familia[-1]+1])

    df_resultante = pd.concat([df, nova_linha])

    return df_resultante

def retorna_indices_top_N_itens_mais_vendidos_por_classe_social(df, id_classe_social, qtd_top_itens):

    colunas_df = retorna_colunas_df(df)

    linhas_familia_e_total_por_classes = list(df.index[-3:])

    indice_soma_gastos = int(df.index[-1])
    soma_gastos = df.iloc[indice_soma_gastos, [id_classe_social]][0]

    despesas_id_classe_social = df.drop(linhas_familia_e_total_por_classes).iloc[:, [id_classe_social]].apply(lambda item: item/soma_gastos)
    despesas_id_classe_social.sort_values(by=colunas_df[id_classe_social], ascending=False, inplace=True)

    lista_top_N = list(despesas_id_classe_social.index[0:qtd_top_itens]) + list(df.index[-1:])

    return lista_top_N

def retorna_lista_top_N_itens_mais_vendidos_classe_social(df, classe_social, qtd_top_itens):

    id_classe_social = retorna_id_classe_social(df, classe_social)

    lista_top_N = retorna_indices_top_N_itens_mais_vendidos_por_classe_social(df, id_classe_social, qtd_top_itens)

    return df.iloc[lista_top_N, [0, id_classe_social]]

def plot_grafico_barras_lista_top_N_itens(df, classe_social, qtd_top_itens, cor):

    id_classe_social = retorna_id_classe_social(df, classe_social)

    lista_top_N = retorna_indices_top_N_itens_mais_vendidos_por_classe_social(df, id_classe_social, qtd_top_itens)

    colunas_df = retorna_colunas_df(df)

    df.iloc[lista_top_N[:-1], [0, id_classe_social]].plot(kind='barh', x=colunas_df[0], y=colunas_df[id_classe_social], color=cor)
    plt.show()

def plot_todos_graficos_barras_lista_top_N_itens(df, qtd_top_itens, cores):

    fig, axes = plt.subplots(nrows=6, ncols=1)

    colunas_df = retorna_colunas_df(df)

    for i, coluna in enumerate(colunas_df[1:]):

        id_classe_social = retorna_id_classe_social(df, coluna)

        lista_top_N = retorna_indices_top_N_itens_mais_vendidos_por_classe_social(df, id_classe_social, qtd_top_itens)

        df.iloc[lista_top_N[:-1], [0, id_classe_social]].plot(kind='barh', x=colunas_df[0], y=colunas_df[id_classe_social], color=cores[i], ax=axes[i], figsize=(6,20))
    
    plt.show()

def retorna_colunas_df(df):

    return list(df.columns)

def dicionario_classe_id(df):

    dicionario_colunas_df = {}

    colunas_df = retorna_colunas_df(df)

    for i, coluna in enumerate(colunas_df):
        dicionario_colunas_df.update({coluna:i})
    
    return dicionario_colunas_df

def retorna_id_classe_social(df, classe_social):

    dicionario_df = dicionario_classe_id(df)

    return dicionario_df[classe_social]