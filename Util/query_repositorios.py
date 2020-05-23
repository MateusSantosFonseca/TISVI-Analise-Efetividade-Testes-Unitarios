#em language tem que ter placeholder

query_repositorios = """
{
    search(query:"stars:>100 language:{placeholder_nome_linguagem}", type:REPOSITORY, first:10 {placeholder}){
        nodes{
          ... on Repository
          {
            name
            nameWithOwner
            url
          }
        }
        pageInfo
        {
          hasNextPage
          endCursor
        }
      }
}
"""