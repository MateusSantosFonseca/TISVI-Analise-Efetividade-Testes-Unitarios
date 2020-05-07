import requests

def requisitar_issues_por_repositorio(headers, query):
    request = requests.post('https://api.github.com/graphql', json = {'query': query}, headers = headers)
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 502:
        return requisitar_issues_por_repositorio(query, headers)
    else:
        raise Exception("A query falhou: {}. {}".format(request.status_code, query))


def get_repos_total_bug_issues(repositorios, headers, query):
    for i, repositorio in enumerate(repositorios):
        nome_owner_repositorio = repositorio.split(',')
        owner_repositorio = nome_owner_repositorio[0]
        nome_repositorio = nome_owner_repositorio[1]

        query_final = query.replace("{placeholder_nome_repo}", nome_repositorio)
        query_final = query_final.replace("{placeholder_owner_repo}", owner_repositorio)

        response = requisitar_issues_por_repositorio(headers, query_final)
        quantidade_bug_issues_repositorio = response["data"]["repository"]["issues"]["totalCount"]

        repositorios[i] += "," + str(quantidade_bug_issues_repositorio)

    print("A etapa de recuperação de bug issues dos repositórios foi finalizada.") 
    return repositorios

        
        
    
