import pathlib
import csv

def exportar_repos_com_infos_csv(repos_com_todas_informacoes, resultados_path, linguagem):
    path_arquivo_csv = resultados_path + f"repositorios_{linguagem}_analisados.csv"
    with open(path_arquivo_csv, mode='w+') as arquivo_csv:
        csv_writer = csv.writer(arquivo_csv)
        
        header = (["Nome", "Owner", "Coverage", "Qnt. de BUG Issues", "Último update nas BUG Issues", "Qnt. de LOC de teste", "URL"])
        csv_writer.writerow(header)
        
        for repositorio in repos_com_todas_informacoes:
            repo_informacoes = repositorio.split(',')
            
            # [0]= Owner, [1]= Nome, [2]= URL, [3]= Coverage, [4]= Qnt. de bug issues, [5]= Último update nas bug issues, [6]= Qnt. de loc de teste  
            dict_repo_info = {0: repo_informacoes[1], 1: repo_informacoes[0], 2: repo_informacoes[3],
                                3: repo_informacoes[4], 4: repo_informacoes[5], 5: repo_informacoes[6],
                                6: repo_informacoes[2]}

            csv_writer.writerow(dict_repo_info.values())

    print("A etapa de exportação dos repositórios com todas as informações obtidas para um arquivo .csv foi finalizada.") 
