import requests
import plotly.express as px

# 执行 API 调用并查看响应
url = "https://api.github.com/search/repositories?q=language:python+sort:stars+stars:>10000"
headers = {"Accept": "application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
response_dict = r.json()

# 处理有关仓库的信息
repo_dicts = response_dict['items']
repo_links, stars, descriptions, owners = [], [], [], []
for repo_dict in repo_dicts:
    # 将仓库名转换为链接
    repo_name = repo_dict['name']
    repo_url = repo_dict['html_url']
    repo_link = f"<a href='{repo_url}'>{repo_name}</a>"
    repo_links.append(repo_link)
    stars.append(repo_dict['stargazers_count'])
    description = repo_dict['description'] if repo_dict['description'] else ""
    max_length = 100 if all(ord(char) < 128 for char in description) else 70
    short_description = (description[:max_length] + '...') if len(description) > max_length else description
    descriptions.append(short_description)
    owners.append(repo_dict['owner']['login'])

# 可视化
title = "Python 项目的星标数"
labels = {'x': '仓库', 'y': '星标数'}
fig = px.bar(x=repo_links, y=stars, title=title, labels=labels)
fig.update_traces(hovertemplate='仓库名称: <b>%{x}</b><br>星标数: %{y}<br>描述: %{customdata[0]}<br>所有者: %{customdata[1]}',
                  customdata=[(desc, owner) for desc, owner in zip(descriptions, owners)])
fig.update_layout(
    title_font_size=28,
    xaxis_title_font_size=20,  # 横坐标标题字体大小
    yaxis_title_font_size=20,
    xaxis_tickfont_size=14,  # 横坐标刻度标签字体大小
    hoverlabel=dict(
        bgcolor="white",
        font_size=14,
        font_family="Rockwell",
        align='left'
    )
)

# 定制条形的颜色和透明度
fig.update_traces(marker_color='SteelBlue', marker_opacity=0.6)

# 显示图形
fig.show()