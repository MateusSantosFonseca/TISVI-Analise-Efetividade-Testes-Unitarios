import os

def contar_loc_teste_repo(start, lines=0, header=True, begin_start=None):
    try:
        for arquivo in os.listdir(start):
            arquivo = os.path.join(start, arquivo)
            if os.path.isfile(arquivo):
                # trocar depois pra inserir o resto e dar o splir pegando todos depois do primeiro .
                if arquivo.__contains__('.spec.js') or arquivo.__contains__('.test.js') or arquivo.__contains__('.tests.js') or arquivo.__contains__('.karma.js'):
                    with open(arquivo, 'r') as f:
                        newlines = f.readlines()
                        newlines = len(newlines)
                        lines += newlines

                        if begin_start is not None:
                            reldir_of_thing = '.' + arquivo.replace(begin_start, '')
                        else:
                            reldir_of_thing = '.' + arquivo.replace(start, '')

        for arquivo in os.listdir(start):
            arquivo = os.path.join(start, arquivo)
            if os.path.isdir(arquivo):
                lines = contar_loc_teste_repo(arquivo, lines, header=False, begin_start=start)
    except:
        pass

    return lines

def get_repos_total_loc_teste(repos_com_total_bug_issues, path_repos_baixados):
    repos_com_total_loc_testes = repos_com_total_bug_issues.copy()
    
    for i, path_repositorio in enumerate(path_repos_baixados):
        linhas_loc_teste = contar_loc_teste_repo(path_repositorio)
        repos_com_total_loc_testes[i] += "," + str(linhas_loc_teste)
    
    print("A etapa de recuperação de LOC de teste dos repositórios foi finalizada.") 
    return repos_com_total_loc_testes