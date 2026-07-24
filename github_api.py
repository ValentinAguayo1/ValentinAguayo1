def get_basic_profile(self) -> GitHubStats:
    query = """
    query($login: String!) {
      user(login: $login) {

        avatarUrl(size: 256)

        url

        createdAt

        followers {
          totalCount
        }

        following {
          totalCount
        }

        repositories(
          ownerAffiliations: OWNER
          isFork: false
          first: 100
        ) {

          totalCount

          nodes {
            stargazerCount
            forkCount
          }
        }
      }
    }
    """

    data = self.execute(
        query,
        {
            "login": PROFILE.username,
        },
    )

    user = data["user"]

    stars = sum(repo["stargazerCount"] for repo in user["repositories"]["nodes"])
    forks = sum(repo["forkCount"] for repo in user["repositories"]["nodes"])

    return GitHubStats(
        repositories=user["repositories"]["totalCount"],
        followers=user["followers"]["totalCount"],
        following=user["following"]["totalCount"],
        stars=stars,
        forks=forks,
        avatar_url=user["avatarUrl"],
        profile_url=user["url"],
        created_at=user["createdAt"],
    )