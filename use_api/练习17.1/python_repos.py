import requests
import plotly.graph_objects as go  # 导入 plotly 的图形对象库

def get_popular_repos(language, repo_stars, repo_details):
    """获取指定语言的热门仓库并收集星标数据和详细信息"""
    url = "https://api.github.com/search/repositories"
    url += f"?q=language:{language}+sort:stars+stars:>10000"
    headers = {"Accept": "application/vnd.github.v3+json"}
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print(f"请求失败，状态码：{r.status_code}")
        return  # 如果请求失败，直接返回

    response_dict = r.json()
    if 'items' not in response_dict:
        print("API没有返回预期的数据。")
        return  # 如果没有 'items' 键，直接返回

    repos = response_dict['items']
    if not repos:
        print("没有找到仓库。")
        return  # 如果 'items' 列表为空，直接返回

    repo = repos[0]
    repo_stars.append(repo['stargazers_count'])
    repo_details.append(f"项目名：{repo['name']}<br>星标数：{repo['stargazers_count']}<br>描述：{repo['description']}<br>地址：{repo['html_url']}")

# 初始化列表来存储每种语言最受欢迎的仓库的星标数和详细信息
repo_stars = []
repo_details = []

# 遍历不同的编程语言，将 Python 放在第一个位置
languages = ['javascript', 'ruby', 'c', 'java', 'perl', 'haskell', 'go', 'python']
for language in languages:
    get_popular_repos(language, repo_stars, repo_details)

# 创建交互式条形图
fig = go.Figure(data=[go.Bar(
    x=languages,
    y=repo_stars,
    hovertext=repo_details,  # 使用 hovertext 属性来显示详细信息
    hoverinfo='text',  # 设置悬停信息显示为文本
    marker_color='blue'
)])

# 设置图表的布局
fig.update_layout(
    title='各编程语言最受欢迎仓库的星标数',
    xaxis_title='语言',
    yaxis_title='星标数',
    plot_bgcolor='white',
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="Rockwell")  # 调整悬停标签的背景色、字体大小和字体类型
)

# 调整条形的宽度和边框
fig.update_traces(marker_line_width=0.5)  # 设置条形边框的宽度

# 显示图表
fig.show()

