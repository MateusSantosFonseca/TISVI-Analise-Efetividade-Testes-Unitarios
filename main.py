from Util.header import headers
from Util.query_repositorios import query
from Scripts.github_repo_getter import get_repositorios

def mainScript():
    repositorios = get_repositorios(headers, query)
    
mainScript()