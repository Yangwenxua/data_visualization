import requests

def get_popular_repos(language):
    """获取指定语言的热门仓库"""
    # 执行 API 调用并查看响应
    url = "https://api.github.com/search/repositories"
    url += f"?q=language:{language}+sort:stars+stars:>10000"
    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)
    print(f"Status code: {r.status_code}")

    # 将响应转换为字典
    response_dict = r.json()

    # 处理结果
    print(f"\n{language} 仓库信息:")
    print(f"总仓库数: {response_dict['total_count']}")

    # 探索有关仓库的信息
    repos = response_dict['items']
    print(f"返回的仓库数: {len(repos)}")

    # 查看第一个仓库
    repo = repos[0]
    print("\n最受欢迎的仓库信息:")
    print(f"名称: {repo['name']}")
    print(f"所有者: {repo['owner']['login']}")
    print(f"星标数: {repo['stargazers_count']}")
    print(f"仓库地址: {repo['html_url']}")
    print(f"描述: {repo['description']}")

# 遍历不同的编程语言
languages = ['javascript', 'ruby', 'c', 'java', 'perl', 'haskell', 'go']
for language in languages:
    get_popular_repos(language)
    print("\n" + "="*50 + "\n")  # 添加分隔线
