import requests
import pandas as pd
import numpy as np
import plotly.express as px

# 执行 API 调用并查看响应
url = "https://api.github.com/search/repositories?q=language:python+sort:stars+stars:>10000"
headers = {"Accept": "application/vnd.github.v3+json"}
r = requests.get(url, headers=headers)
response_dict = r.json()

# 使用 pandas 处理数据
repos_data = response_dict['items']
df = pd.DataFrame(repos_data)

# 提取和处理所需的列
df['repo_link'] = df.apply(lambda x: f"<a href='{x['html_url']}'>{x['name']}</a>", axis=1)
df['stars'] = df['stargazers_count']
df['description'] = df['description'].fillna('No description').apply(lambda x: (x[:100] + '...') if len(x) > 100 else x)
df['owner'] = df['owner'].apply(lambda x: x['login'])

# 使用 numpy 计算星标数的统计数据
average_stars = np.mean(df['stars'])
median_stars = np.median(df['stars'])
print(f"平均星标数: {average_stars}")
print(f"中位星标数: {median_stars}")

# 可视化
title = "Python 项目的星标数"
fig = px.bar(df, x='repo_link', y='stars', title=title, labels={'x': '仓库', 'y': '星标数'})
fig.update_traces(hovertemplate='仓库名称: <b>%{x}</b><br>星标数: %{y}<br>描述: %{customdata[0]}<br>所有者: %{customdata[1]}',
                  customdata=np.column_stack((df['description'], df['owner'])))
fig.update_layout(
    title_font_size=28,
    xaxis_title_font_size=24,
    yaxis_title_font_size=20,
    xaxis_tickfont_size=16,
    hoverlabel=dict(
        bgcolor="white",
        font_size=16,
        font_family="Rockwell",
        align='left'
    )
)

# 定制条形的颜色和透明度
fig.update_traces(marker_color='SteelBlue', marker_opacity=0.6)

# 显示图形
fig.show()
