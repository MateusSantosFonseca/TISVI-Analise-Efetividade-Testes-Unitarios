import pathlib
import csv
import pandas as pd

def exportar_coeficientes(coeficiente_bug_locs_teste, coeficiente_bugs_coverages):
    path = str(pathlib.Path().absolute()) + "\\coeficientes_pearson_de_valores_dos_repos.txt"
    corpo = f"Valores de coeficientes de correlação de Pearson: \n\nCoeficiente de Pearson obtidos pelas medidas BUG Issues e LOC de testes: {coeficiente_bug_locs_teste}.\nCoeficiente de Pearson obtidos pelas medidas BUG Issues e Coverage: {coeficiente_bugs_coverages}.\n"
    file = open(path, "w+")
    file.write(corpo)
    file.close

def get_coeficientes_correlacao_pearson():
    path_arquivo_csv = str(pathlib.Path().absolute()) + "\\repositorios_analisados.csv"
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
                    lista_locs_teste.append(float(linha_splitada[2].replace("%","")))
                    lista_coverages.append(float(linha_splitada[5]))

    panda_bug_issues = pd.Series(lista_bug_issues)
    panda_locs_teste = pd.Series(lista_locs_teste)
    panda_coverages = pd.Series(lista_coverages)

    coeficiente_correlacao_pearson_bug_locs_teste = panda_bug_issues.corr(panda_locs_teste)
    coeficiente_correlacao_pearson_bugs_coverages = panda_bug_issues.corr(panda_coverages)
    
    exportar_coeficientes(str(coeficiente_correlacao_pearson_bug_locs_teste), str(coeficiente_correlacao_pearson_bugs_coverages))