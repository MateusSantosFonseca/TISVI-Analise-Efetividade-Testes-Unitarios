from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_repos_com_coverage(repositorios):

    quantidade_repos_com_coverage = 0
    repos_com_coverage = []

    for repositorio in repositorios:
        if(quantidade_repos_com_coverage > 100):
            break
        
        url = f"https://coveralls.io/github/{repositorio['nameWithOwner']}"
        
        try:
            site = urlopen(url)
            content = site.read()
            
            soup = BeautifulSoup(content, 'lxml')
            coverage_repositorio = soup.find("div", {"id":"repoShowPercentage"})
            repos_com_coverage.append(repositorio['name'] + "," + repositorio['url'] + "," + coverage_repositorio.text)
            
            quantidade_repos_com_coverage += 1
            
        except:
            print("O repositório não possui coverage cadastrado.")
        
    return repos_com_coverage