from Util.header import headers
from Util.query_repositorios import query
from Scripts.github_repo_getter import get_repositorios
from Scripts.coverage_repo_getter import get_repos_com_coverage

def mainScript():
    repositorios = get_repositorios(headers, query)
    repos_com_coverage = get_repos_com_coverage(repositorios)

mainScript()