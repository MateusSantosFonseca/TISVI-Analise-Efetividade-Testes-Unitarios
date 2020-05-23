import pathlib
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import shutil
import os

#Variável X: variável independente. Variável Y: variável dependente.
def exportar_grafico_regressao_linear(lista_variavel_independente_x, lista_variavel_dependente_y,
                                     variavel_x, variavel_y, path, possui_zerados):
    path_final = f"{path}\\regressao_linear_{variavel_x.lower().replace(' ','')}_{variavel_y.lower().replace(' ','')}.png"
    variavel_independente_x = np.array(lista_variavel_independente_x)
    variavel_dependente_y = np.array(lista_variavel_dependente_y)
    resultado = stats.linregress(variavel_independente_x, variavel_dependente_y)
    mn = np.min(variavel_independente_x)
    mx = np.max(variavel_independente_x)
    x1 = np.linspace(mn, mx, 100)
    y1 = resultado.slope * x1 + resultado.intercept
    
    plt.rcParams['figure.figsize'] = (9,5)
    plt.plot(variavel_independente_x, variavel_dependente_y, 'go', markersize=3)
    plt.plot(x1, y1, 'orange')
    
    if(possui_zerados is True):
        plt.title(f"Regressão Linear entre {variavel_x} e {variavel_y}", pad=10)
    else:
        plt.title(f"Regressão Linear entre {variavel_x} e {variavel_y} com LOC de testes > 0", pad=10)
        
    plt.xlabel(variavel_x, labelpad=10)
    plt.ylabel(variavel_y, labelpad=10)
    plt.savefig(path_final)
    plt.show()
    
    return resultado

def interpreta_resultado_valor_r(valor_r):
    valor_r_float = float(valor_r)
    
    if(valor_r_float == 0):
        return f"De acordo com o valor R obtido: {str(valor_r_float)}, não existe correlação."
    
    elif(valor_r_float > -0.3 and valor_r_float < 0.3):
        return f"De acordo com o valor R obtido: {str(valor_r_float)}, a correlação é desprezível."
    
    elif((valor_r_float >= 0.3 and valor_r_float < 0.5) or (valor_r_float <= -0.3 and valor_r_float > -0.5)):
        return f"De acordo com o valor R obtido: {str(valor_r_float)}, a correlação é fraca."
    
    elif((valor_r_float >= 0.5 and valor_r_float < 0.7) or (valor_r_float <= -0.5 and valor_r_float > -0.7)):
        return f"De acordo com o valor R obtido: {str(valor_r_float)}, a correlação é moderada."
    
    elif((valor_r_float >= 0.7 and valor_r_float < 0.9) or (valor_r_float <= -0.7 and valor_r_float > -0.9)):
        return f"De acordo com o valor R obtido: {str(valor_r_float)}, a correlação é forte."
    
    else:
        return f"De acordo com o valor R obtido: {str(valor_r_float)}, a correlação é muito forte."
    
    

def montar_corpo_texto_valores_estatisticos(resultado_loc_bugs, resultado_coverage_bugs, locs_nz_resultado_loc_bugs=None,
                                            locs_nz_resultado_coverage_bugs=None):
    
    valores_estatisticos_texto = "    Para todos repositórios:\n"
    valores_estatisticos_texto += f"""\n\
    Valores estatísticos para X = LOCs de Teste e Y = BUG Issues:
    Inclinação: {resultado_loc_bugs.slope}
    Intercepto: {resultado_loc_bugs.intercept}
    Erro padrão: {resultado_loc_bugs.stderr}
    Valor P: {resultado_loc_bugs.pvalue}
    Valor R: {resultado_loc_bugs.rvalue}\n
    Interpretação do Coeficiente de Pearson:
    {interpreta_resultado_valor_r(resultado_loc_bugs.rvalue)}
    
    Valores estatísticos para X = Coverage e Y = BUG Issues:
    Inclinação: {resultado_coverage_bugs.slope}
    Intercepto: {resultado_coverage_bugs.intercept}
    Erro padrão: {resultado_coverage_bugs.stderr}
    Valor P: {resultado_coverage_bugs.pvalue}
    Valor R: {resultado_coverage_bugs.rvalue}\n
    Interpretação do Coeficiente de Pearson:
    {interpreta_resultado_valor_r(resultado_coverage_bugs.rvalue)}\n\n
    """
    if(locs_nz_resultado_loc_bugs is not None):
        valores_estatisticos_texto += "Para repositórios com LOC de Testes > 0:\n"
        valores_estatisticos_texto += f"""\n\
    Valores estatísticos para X = LOCs de Teste e Y = BUG Issues:
    Inclinação: {locs_nz_resultado_loc_bugs.slope}
    Intercepto: {locs_nz_resultado_loc_bugs.intercept}
    Erro padrão: {locs_nz_resultado_loc_bugs.stderr}
    Valor P: {locs_nz_resultado_loc_bugs.pvalue}
    Valor R: {locs_nz_resultado_loc_bugs.rvalue}\n
    Interpretação do Coeficiente de Pearson:
    {interpreta_resultado_valor_r(locs_nz_resultado_loc_bugs.rvalue)}\n
    Valores estatísticos para X = Coverage e Y = BUG Issues:
    Inclinação: {locs_nz_resultado_coverage_bugs.slope}
    Intercepto: {locs_nz_resultado_coverage_bugs.intercept}
    Erro padrão: {locs_nz_resultado_coverage_bugs.stderr}
    Valor P: {locs_nz_resultado_coverage_bugs.pvalue}
    Valor R: {locs_nz_resultado_coverage_bugs.rvalue}\n
    Interpretação do Coeficiente de Pearson:
    {interpreta_resultado_valor_r(locs_nz_resultado_coverage_bugs.rvalue)}
    """
    valores_estatisticos_texto += f"""\n\n    Observação: O Valor R é o Coeficiente de Correlação de Pearson.\n
    Tabela com valores de referência para o Coeficiente de Pearson:\n
    0.9 para mais ou para menos indica uma correlação muito forte.
    0.7 a 0.9 positivo ou negativo indica uma correlação forte.
    0.5 a 0.7 positivo ou negativo indica uma correlação moderada.
    0.3 a 0.5 positivo ou negativo indica uma correlação fraca.
    0 a 0.3 positivo ou negativo indica uma correlação desprezível.
    """
    
    return valores_estatisticos_texto

def exportar_resultado_estatistico(valores_estatisticos, resultados_linguagem_path, linguagem):
    path = resultados_linguagem_path + f"\\{linguagem}_valores_estatisticos_obtidos.txt"
    file = open(path, "w+")
    file.write(valores_estatisticos)
    file.close

def criar_pasta(path):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass

def get_regressao_linear_e_coeficiente_pearson(linguagem, resultados_linguagem_path):
    path_arquivo_csv = resultados_linguagem_path + f"\\repositorios_{linguagem}_analisados.csv"

    #locs_nz = Sufixo que remete aos repositórios cuja quantidade de LOC de testes != 0
    
    lista_bug_issues = []
    lista_locs_teste = []
    lista_coverages = []

    locs_nz_lista_bug_issues = []
    locs_nz_lista_coverages = []
    locs_nz_lista_locs_teste = []
    
    with open(path_arquivo_csv, mode='r') as arquivo_csv:
        isHeader = True
        for linha in arquivo_csv:
            if (len(linha) != 0 and linha != f'\n'):
                if isHeader is True:
                    isHeader = False
                    continue
                else:
                    linha_splitada = linha.split(',')
                    linha_bug_issues = float(linha_splitada[3])
                    linha_coverage = float(linha_splitada[2].replace("%",""))
                    linha_loc_testes = float(linha_splitada[5])
                    
                    lista_bug_issues.append(linha_bug_issues)
                    lista_coverages.append(linha_coverage)
                    lista_locs_teste.append(linha_loc_testes)
                    if(linha_loc_testes > 0):
                        locs_nz_lista_bug_issues.append(linha_bug_issues)
                        locs_nz_lista_locs_teste.append(linha_loc_testes)
                        locs_nz_lista_coverages.append(linha_coverage)
                        
    path_todos_repos = resultados_linguagem_path + "Todos_Repositorios"
    criar_pasta(path_todos_repos)
    
    resultado_locs_bugs = exportar_grafico_regressao_linear(lista_locs_teste, lista_bug_issues, "LOC de testes",
                                                            "BUG Issues", path_todos_repos, True)
    resultado_coverage_bugs = exportar_grafico_regressao_linear(lista_coverages, lista_bug_issues, "Coverage",
                                                            "BUG Issues", path_todos_repos, True)
    
    locs_nz_resultado_locs_bugs = None
    locs_nz_resultado_coverage_bugs = None
    
    # Análise dos repositórios que não tiveram LOC de testes zerados
    if(len(locs_nz_lista_locs_teste) > 0):
        locs_nz_path_repos = resultados_linguagem_path + "\\Repositorios_LOC_Testes"
        criar_pasta(locs_nz_path_repos)
        
        locs_nz_resultado_locs_bugs = exportar_grafico_regressao_linear(
                locs_nz_lista_locs_teste, locs_nz_lista_bug_issues,
                "LOC de testes", "BUG Issues", locs_nz_path_repos, False)
        
        locs_nz_resultado_coverage_bugs = exportar_grafico_regressao_linear(
                locs_nz_lista_coverages, locs_nz_lista_bug_issues,
                "Coverage", "BUG Issues", locs_nz_path_repos, False)

    if(locs_nz_resultado_locs_bugs is not None):
        resultado_texto = montar_corpo_texto_valores_estatisticos(resultado_locs_bugs, resultado_coverage_bugs,
                                                                  locs_nz_resultado_locs_bugs, locs_nz_resultado_coverage_bugs)
    else:
        resultado_texto = montar_corpo_texto_valores_estatisticos(resultado_locs_bugs, resultado_coverage_bugs)
    
    exportar_resultado_estatistico(resultado_texto, resultados_linguagem_path, linguagem)
    