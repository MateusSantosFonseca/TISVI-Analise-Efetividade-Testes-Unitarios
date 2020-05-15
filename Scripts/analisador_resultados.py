import pathlib
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import easygui
import shutil
import os

#Variável X: variável independente. Variável Y: variável dependente.
def exportar_grafico_regressao_linear(lista_variavel_independente_x, lista_variavel_dependente_y, variavel_x, variavel_y, deseja_mostrar_imagem):
    path = str(pathlib.Path().absolute()) + f"\\ResultadosEstatisticos\\regressao_linear_{variavel_x.lower().replace(' ','')}_{variavel_y.lower().replace(' ','')}.png"
    variavel_independente_x = np.array(lista_variavel_independente_x)
    variavel_dependente_y = np.array(lista_variavel_dependente_y)
    resultado = stats.linregress(variavel_independente_x, variavel_dependente_y)
    mn = np.min(variavel_independente_x)
    mx = np.max(variavel_independente_x)
    x1 = np.linspace(mn, mx, 500)
    y1 = resultado.slope * x1 + resultado.intercept
    
    plt.rcParams['figure.figsize'] = (9,5)
    plt.plot(variavel_independente_x, variavel_dependente_y, 'go', markersize=3)
    plt.plot(x1, y1, 'orange')
    plt.title(f"Regressão Linear entre {variavel_x} e {variavel_y}", pad=10)
    plt.xlabel(variavel_x, labelpad=10)
    plt.ylabel(variavel_y, labelpad=10)
    plt.savefig(path)
    if (deseja_mostrar_imagem):
        plt.show()
    
    return resultado

def montar_corpo_texto_valores_estatisticos(resultado_loc_bugs, resultado_coverage_bugs):
    valores_estatisticos_texto = f"""\n\
    Valores estatísticos para X = LOCs de Teste e Y = BUG Issues:
    Inclinação: {resultado_loc_bugs.slope}
    Intercepto: {resultado_loc_bugs.intercept}
    Erro padrão: {resultado_loc_bugs.stderr}
    Valor P: {resultado_loc_bugs.pvalue}
    Valor R: {resultado_loc_bugs.rvalue}\n
    Valores estatísticos para X = Coverage e Y = BUG Issues:
    Inclinação: {resultado_coverage_bugs.slope}
    Intercepto: {resultado_coverage_bugs.intercept}
    Erro padrão: {resultado_coverage_bugs.stderr}
    Valor P: {resultado_coverage_bugs.pvalue}
    Valor R: {resultado_coverage_bugs.rvalue}\n\n
    Observação: O Valor R é o Coeficiente de Correlação de Pearson.
    """
    return valores_estatisticos_texto

def exportar_resultado_estatistico(valores_estatisticos):
    path = str(pathlib.Path().absolute()) + "\\ResultadosEstatisticos\\valores_estatisticos_obtidos.txt"
    file = open(path, "w+")
    file.write(valores_estatisticos)
    file.close

def get_regressao_linear_e_coeficiente_pearson():
    path_arquivo_csv = str(pathlib.Path().absolute()) + "\\repositorios_analisados.csv"
    path_resultados_estatisticos = str(pathlib.Path().absolute()) + "\\ResultadosEstatisticos"
    
    lista_bug_issues = []
    lista_locs_teste = []
    lista_coverages = []
    
    with open(path_arquivo_csv, mode='r') as arquivo_csv:
        isHeader = True
        for linha in arquivo_csv:
            if (len(linha) != 0 and linha != f'\n'):
                if isHeader is True:
                    isHeader = False
                    continue
                else:
                    linha_splitada = linha.split(',')
                    lista_bug_issues.append(float(linha_splitada[3]))
                    lista_coverages.append(float(linha_splitada[2].replace("%","")))
                    lista_locs_teste.append(float(linha_splitada[5]))

    deseja_mostrar_imagem = easygui.ynbox("Você deseja ver os gráficos que serão exportados?",  "Mostrar gráficos?", ('Sim', 'Não'))
    
    if(deseja_mostrar_imagem is None):
        deseja_mostrar_imagem = False

    try:
        os.mkdir(path_resultados_estatisticos)
    except FileExistsError:
        pass
    
    resultado_locs_bugs = exportar_grafico_regressao_linear(lista_locs_teste, lista_bug_issues, "LOC de testes", "BUG Issues", deseja_mostrar_imagem)
    resultado_coverage_bugs = exportar_grafico_regressao_linear(lista_coverages, lista_bug_issues, "Coverage", "BUG Issues", deseja_mostrar_imagem)
    
    resultado_texto = montar_corpo_texto_valores_estatisticos(resultado_locs_bugs, resultado_coverage_bugs)
    exportar_resultado_estatistico(resultado_texto)