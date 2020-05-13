import os
import keyboard
import shutil
import time
import datetime
from git import Repo, RemoteProgress

class ProgressPrinter(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print("\nProgresso do download: ")
        print(int(cur_count), int(max_count), format((cur_count / (max_count or 100.0)*100), '.2f'))

def exportar_log_downloads(repos_path, log_downloads):
    path_logs = repos_path + r"\log_downloads.txt"
    file = open(path_logs, "w+")  
    file.write(log_downloads)
    file.close

def baixar_repositorios(path, repositorios, deseja_mostrar_progresso_download):
    repos_path = path + r"Repositorios"

    repos_baixados_list_path = []
    
    try:
        os.mkdir(repos_path)
        print("\nDiretório ", repos_path, "criado.\n")
    except FileExistsError:
        print("\nDiretório:", repos_path, "não foi criado pois já existe.\n")

    count_repos_baixados = 0
    log_downloads = ""

    for repositorio in repositorios:
        count_repos_baixados += 1
        splitted_repo = repositorio.split(',')
        nome_repositorio = splitted_repo[1]
        path_repo_baixado = repos_path + "\\" + "{:04n}".format(count_repos_baixados) + "_" + nome_repositorio

        repos_baixados_list_path.append(path_repo_baixado)

        try:
            if not os.path.exists(path_repo_baixado):
                os.mkdir(path_repo_baixado)
                print("\nVoce está baixando o repositório: " + nome_repositorio + " ele é o " + str(count_repos_baixados) + "° repositório baixado.")
                time.sleep(1)
                
                if(deseja_mostrar_progresso_download):
                    Repo.clone_from(splitted_repo[2], path_repo_baixado, progress=ProgressPrinter())
                else:
                    Repo.clone_from(splitted_repo[2], path_repo_baixado)
                    
            else:
                print("\nO repositório: " + nome_repositorio + " já foi baixado!!")
            
            
            now = datetime.datetime.now()
            log_downloads += "O repositório: " + nome_repositorio + " foi baixado (ou já estava baixado), ele é o repositorio de número: " + str(count_repos_baixados) + ". Hora do término do download: " + now.strftime("%Y-%m-%d %H:%M:%S") + '\n\n'
            
        except KeyboardInterrupt:   
            now = datetime.datetime.now()  
            print ('CTRL + C foi inserido, pulando o repositório: ' + nome_repositorio + " ele era o repositório de número:" + str(count_repos_baixados))
            log_downloads += "O repositório: " + nome_repositorio + " foi pulado e não foi baixado, ele era o repositorio de número: " + str(count_repos_baixados) + ". Hora do erro: " + now.strftime("%Y-%m-%d %H:%M:%S") + '\n\n'
        
        except:
            now = datetime.datetime.now()
            log_downloads += "O repositório: " + nome_repositorio + " apresentou problemas no download, ele era o repositório de número: " + str(count_repos_baixados) + ". Hora do erro: " + now.strftime("%Y-%m-%d %H:%M:%S") + '\n\n'

    print("\nO script de download de repositórios foi finalizado normalmente.")
    print(f"\nLembre-se de deletar os repositórios em: {repos_path}!")
    exportar_log_downloads(repos_path, log_downloads)
    time.sleep(3)
    return repos_baixados_list_path
    
    
    
    
    
    

