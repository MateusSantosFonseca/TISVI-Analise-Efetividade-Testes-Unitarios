from Util.header import headers
from Util.query_repositorios import query_repositorios
from Util.query_issues import query_issues
from Util.linguagens_extensoes_e_nomenclaturas_teste import linguagem_extensoes_teste, nomenclaturas_comuns_teste
from Scripts.github_repo_getter import get_repositorios
from Scripts.coverage_repo_getter import get_repos_com_coverage
from Scripts.total_bug_issues_repo_getter import get_repos_total_bug_issues
from Scripts.repositorios_downloader import baixar_repositorios
from Scripts.total_loc_testes_repo_getter import get_repos_total_loc_teste
from Scripts.exportador_csv import exportar_repos_com_infos_csv
from Scripts.analisador_resultados import get_regressao_linear_e_coeficiente_pearson
import easygui
import ctypes 
import os
import sys
import pathlib

def main_script():
    print("\nO Script foi iniciado.")  
    
    deseja_mostrar_progresso_download = easygui.ynbox("Ao fazer o download dos repositórios, você deseja que o progresso seja mostrado?",  "Mostrar progresso de download", ('Sim', 'Não'))    
    if(deseja_mostrar_progresso_download is None):
        print("\nNão foi escolhida nenhuma opção, o programa foi interrompido.\n")
        sys.exit()
        
    path_repos = easygui.diropenbox()
    if(not path_repos):
        print("\nNenhum diretório foi selecionado, o programa foi interrompido.\n")
        sys.exit()
        
    path_repos = path_repos + "Repositorios\\"
    criar_pasta(path_repos)
    
    path_base = str(pathlib.Path().absolute()) + "\\"
    
    resultados_path = path_base + "Resultados\\"
    criar_pasta(resultados_path)
    
    for linguagem in linguagem_extensoes_teste:
        print(f"\nIniciando scripts da linguagem: {linguagem}.")
        
        query_repos_atual = query_repositorios.replace("{placeholder_nome_linguagem}", linguagem)
        repositorios = get_repositorios(headers, query_repos_atual)
        
        repos_com_coverage = get_repos_com_coverage(repositorios)
        
        repos_com_total_bug_issues = get_repos_total_bug_issues(repos_com_coverage, headers, query_issues)
        
        path_repos_baixados = list()
        path_repos_baixados = baixar_repositorios(linguagem, path_repos, repos_com_total_bug_issues, deseja_mostrar_progresso_download)
        
        repos_com_total_loc_testes = get_repos_total_loc_teste(repos_com_total_bug_issues, path_repos_baixados, linguagem, linguagem_extensoes_teste, nomenclaturas_comuns_teste)
        
        resultados_por_linguagem_path = resultados_path + f"{linguagem}\\"
        criar_pasta(resultados_por_linguagem_path)
        
        exportar_repos_com_infos_csv(repos_com_total_loc_testes, resultados_por_linguagem_path, linguagem)
        get_regressao_linear_e_coeficiente_pearson(linguagem, resultados_por_linguagem_path)
    
    print("\nO Script foi finalizado com sucesso.")   

def criar_pasta(path):
    try:
        os.mkdir(path)
        print("\nDiretório ", path, "criado.")
    except FileExistsError:
        print("\nDiretório:", path, "não foi criado pois já existe.")
        
main_script()
