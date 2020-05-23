import os

def contar_loc_teste_repo(start, linguagem, linguagem_extensoes_teste, nomenclaturas_comuns_teste, lines=0, header=True, begin_start=None):
    try:
        for arquivo in os.listdir(start):
            arquivo = os.path.join(start, arquivo)
            if (os.path.isfile(arquivo)):
                arquivo_splitted = arquivo.split('\\')
                arquivo_comparador = arquivo_splitted[len(arquivo_splitted)-1].lower()
                if (checar_arquivo_de_teste(arquivo_comparador, linguagem_extensoes_teste[linguagem], nomenclaturas_comuns_teste)):
                    with open(arquivo, 'r') as f:
                        newlines = f.readlines()
                        newlines = len(newlines)
                        lines += newlines

                        if (begin_start is not None):
                            reldir_of_thing = '.' + arquivo.replace(begin_start, '')
                        else:
                            reldir_of_thing = '.' + arquivo.replace(start, '')

        for arquivo in os.listdir(start):
            arquivo = os.path.join(start, arquivo)
            if os.path.isdir(arquivo):
                lines = contar_loc_teste_repo(arquivo, linguagem, linguagem_extensoes_teste, nomenclaturas_comuns_teste, lines, header=False, begin_start=start)
    except:
        pass

    return lines

def checar_arquivo_de_teste(arquivo, lista_extensoes, nomenclaturas_comuns_teste):
    if(len(lista_extensoes) == 0):
        return False
    
    for extensao in lista_extensoes:
        if(arquivo.__contains__(extensao)):
            return True
        
    for nomenclatura in nomenclaturas_comuns_teste:
        if(arquivo.__contains__(nomenclatura)):
            return True
        
    return False

def get_repos_total_loc_teste(repos_com_total_bug_issues, path_repos_baixados, linguagem, linguagem_extensoes_teste, nomenclaturas_comuns_teste):
    repos_com_total_loc_testes = repos_com_total_bug_issues.copy()
    
    for i, path_repositorio in enumerate(path_repos_baixados):
        linhas_loc_teste = contar_loc_teste_repo(path_repositorio, linguagem, linguagem_extensoes_teste, nomenclaturas_comuns_teste)
        repos_com_total_loc_testes[i] += "," + str(linhas_loc_teste)
    
    print("\nA etapa de recuperação de LOC de teste dos repositórios foi finalizada.") 
    return repos_com_total_loc_testes