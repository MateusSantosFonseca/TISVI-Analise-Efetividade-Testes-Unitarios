from Util.header import headers
from Util.query_repositorios import query_repositorios
from Util.query_issues import query_issues
from Scripts.github_repo_getter import get_repositorios
from Scripts.coverage_repo_getter import get_repos_com_coverage
from Scripts.total_bug_issues_repo_getter import get_repos_total_bug_issues

def mainScript():
    repositorios = get_repositorios(headers, query_repositorios)
    repos_com_coverage = get_repos_com_coverage(repositorios)
    repos_com_total_bug_issues = get_repos_total_bug_issues(repos_com_coverage, headers, query_issues)

mainScript()