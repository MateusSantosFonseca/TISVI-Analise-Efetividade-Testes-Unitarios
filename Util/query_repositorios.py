query_repositorios = """
{
    search(query:"stars:>100 language:Javascript", type:REPOSITORY, first:10 {placeholder}){
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