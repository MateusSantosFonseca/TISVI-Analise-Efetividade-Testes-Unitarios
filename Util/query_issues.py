query_issues = """
{
  repository(name: "{placeholder_nome_repo}", owner: "{placeholder_owner_repo}") {
    issues(filterBy: {labels: ["BUG", "bug", "Bug", "Type: Bug", "Type: BUG", "Type: bug", "type: Bug",
              "type: BUG", "type: bug", "browser bug", "Error", "ERROR", "error", "Failure", "FAILURE", "failure",
              "Confirmed Bug", "confirmed bug", "Type: Bug / Error", "good first bug", "Good First Bug",
              "GOOD FIRST BUG", "confirmed-bug", "bug critical", "bug minor", "bug moderate", "type:bug",
              "Type:bug", "type:Bug", "Type:Bug"]}, first: 1, orderBy: {field: UPDATED_AT, direction: DESC}) {
      totalCount
      nodes {
        updatedAt
      }
    }
  }
}
"""