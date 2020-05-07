from Util.header import headers
from Util.query_repositorios import query_repositorios
from Util.query_issues import query_issues
from Scripts.github_repo_getter import get_repositorios
from Scripts.coverage_repo_getter import get_repos_com_coverage
from Scripts.total_bug_issues_repo_getter import get_repos_total_bug_issues
from Scripts.repositorios_downloader import baixar_repositorios
from Scripts.total_loc_testes_repo_getter import get_repos_total_loc_teste
from Scripts.exportador_csv import exportar_repos_com_infos_csv
import easygui
import ctypes 

def main_script():
    repositorios = get_repositorios(headers, query_repositorios)
    repos_com_coverage = get_repos_com_coverage(repositorios)
    repos_com_total_bug_issues = get_repos_total_bug_issues(repos_com_coverage, headers, query_issues)
    
    path_repos_baixados = list()
    deseja_mostrar_progresso_download = easygui.ynbox("Ao fazer o download dos repositórios, você deseja que o progresso seja mostrado?",  "Mostrar progresso de download", ('Sim', 'Não'))
    
    if(deseja_mostrar_progresso_download is not None):
        path = easygui.diropenbox()
        if(not path):
            print("\nNenhum diretório foi selecionado, o programa foi interrompido.")
        else:
            path_repos_baixados = baixar_repositorios(path, repos_com_total_bug_issues, deseja_mostrar_progresso_download)
    else:
        print("\nNão foi escolhida nenhuma opção, o programa foi interrompido.")
    
    repos_com_total_loc_testes = get_repos_total_loc_teste(repos_com_total_bug_issues, path_repos_baixados)
    exportar_repos_com_infos_csv(repos_com_total_loc_testes)
    
    print("\nO Script foi finalizado com sucesso.")   
    
main_script()