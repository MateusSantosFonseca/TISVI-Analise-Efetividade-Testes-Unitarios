import requests
from datetime import datetime, timedelta
import dateutil.parser

def requisitar_issues_por_repositorio(headers, query):
    request = requests.post('https://api.github.com/graphql', json = {'query': query}, headers = headers)
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 502:
        return requisitar_issues_por_repositorio(query, headers)
    else:
        raise Exception("A query falhou: {}. {}".format(request.status_code, query))

def get_repos_total_bug_issues(repositorios, headers, query):
    repos_com_bug_issues = []
    data_referencia = datetime.strptime(datetime.strftime(datetime.now() - timedelta(days=31), f"%d/%m/%y"), f"%d/%m/%y")
    quantidade_repos_com_coverage_e_bug_issues = 0
    
    for i, repositorio in enumerate(repositorios):
        if(quantidade_repos_com_coverage_e_bug_issues >= 100):
            break
        
        nome_owner_repositorio = repositorio.split(',')
        owner_repositorio = nome_owner_repositorio[0]
        nome_repositorio = nome_owner_repositorio[1]

        query_final = query.replace("{placeholder_nome_repo}", nome_repositorio)
        query_final = query_final.replace("{placeholder_owner_repo}", owner_repositorio)

        response = requisitar_issues_por_repositorio(headers, query_final)
        
        if(response["data"]["repository"]["issues"]["totalCount"] == 0):
            continue
        
        if(len(response["data"]["repository"]["issues"]["nodes"]) != 0):
            issues_maior_updated_at = response["data"]["repository"]["issues"]["nodes"][0]["updatedAt"]
        else:
            continue
        
        issues_maior_updated_at = datetime.strptime(datetime.strftime(dateutil.parser.parse(issues_maior_updated_at), f"%d/%m/%y"), f"%d/%m/%y")
        
        if(issues_maior_updated_at > data_referencia):
            quantidade_repos_com_coverage_e_bug_issues += 1
            quantidade_bug_issues_repositorio = response["data"]["repository"]["issues"]["totalCount"]
            repos_com_bug_issues.append(repositorios[i] + "," + str(quantidade_bug_issues_repositorio) + "," + datetime.strftime(issues_maior_updated_at, f"%d/%m/%y"))
        else:
            continue
    
    print(f"\nForam recuperados {str(len(repos_com_bug_issues))} repositórios com informações de coverage e que continham BUG Issues.")
    print("\nA etapa de recuperação de bug issues dos repositórios foi finalizada.") 
    return repos_com_bug_issues

        
        
    
