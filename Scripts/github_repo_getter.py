import requests

def requisitar_repositorios(headers, query):
    request = requests.post('https://api.github.com/graphql', json = {'query': query}, headers = headers)
    if request.status_code == 200:
        return request.json()
    elif request.status_code == 502:
        return requisitar_repositorios(query, headers)
    else:
        raise Exception("A query falhou: {}. {}".format(request.status_code, query))

def get_repositorios(headers, query):
    response = requisitar_repositorios(headers, query.replace("{placeholder}", ""))
    quantidade_execucoes = 1 

    cursor_final_atual = response["data"]["search"]["pageInfo"]["endCursor"] 
    possui_proxima_pagina = response["data"]["search"]["pageInfo"]["hasNextPage"] 
    repositorios_retornados = response["data"]["search"]["nodes"]

    while (quantidade_execucoes < 100 and possui_proxima_pagina):
        query_final = query.replace("{placeholder}", ', after: "%s"' % cursor_final_atual)
        response = requisitar_repositorios(headers, query_final)
        
        repositorios_retornados += response["data"]["search"]["nodes"]
        quantidade_execucoes += 1
    
        possui_proxima_pagina = response["data"]["search"]["pageInfo"]["hasNextPage"] 
        cursor_final_atual = response["data"]["search"]["pageInfo"]["endCursor"] 
    
    print("A etapa de recuperação dos repositórios foi finalizada.") 
    return repositorios_retornados