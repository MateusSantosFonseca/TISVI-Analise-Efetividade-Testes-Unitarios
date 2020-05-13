from urllib.request import urlopen
from bs4 import BeautifulSoup

def get_repos_com_coverage(repositorios):

    quantidade_repos_com_coverage = 0
    quantidade_repos_sem_coverage = 0
    
    repos_com_coverage = []

    for repositorio in repositorios:
        url = f"https://coveralls.io/github/{repositorio['nameWithOwner']}"
        
        try:
            site = urlopen(url)
            content = site.read()
            
            soup = BeautifulSoup(content, 'lxml')
            coverage_repositorio = soup.find("div", {"id":"repoShowPercentage"})
            
            coverage_repositorio_texto = coverage_repositorio.text.strip()
            if (coverage_repositorio_texto.__contains__("master")):
                coverage_repositorio_texto = coverage_repositorio_texto.split("master")[0].strip()
                                
            nome_owner_repositorio = repositorio['nameWithOwner'].split('/')
            
            repos_com_coverage.append(
                nome_owner_repositorio[0] + "," + nome_owner_repositorio[1] + "," + repositorio['url'] + "," + coverage_repositorio_texto)

            quantidade_repos_com_coverage += 1
            
            if(quantidade_repos_com_coverage % 10 == 0):
                print(f"Já foram encontrados {quantidade_repos_com_coverage} repositórios com coverage.")

        except:
            quantidade_repos_sem_coverage += 1
            if(quantidade_repos_sem_coverage % 25 == 0):
                print(f"Até o momento, {quantidade_repos_sem_coverage} foram descartados.")
    
    print(f"\n{quantidade_repos_com_coverage} repositórios com coverage foram encontrados.")
    print(f"\n{quantidade_repos_sem_coverage} repositórios sem coverage foram descartados.")
    print("\nA etapa de recuperação de coverage dos repositórios foi finalizada.")    
    return repos_com_coverage
