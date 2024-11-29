import plotly.graph_objects as go
import numpy as np

# 设置随机种子（可选，用于结果可重复）
#np.random.seed(42)#

# 模拟掷骰子次数
num_trials = 100000000

# 使用 numpy 模拟同时掷三个D6
# np.random.randint(low, high, size) 生成 [low, high) 之间的整数
dice_rolls = np.random.randint(1, 7, size=(num_trials, 3))
sums = dice_rolls.sum(axis=1)  # 计算每次掷骰子的总和

# 统计每个点数的出现次数
min_sum = 3
max_sum = 18
value_counts = np.bincount(sums, minlength=max_sum + 1)[min_sum:]

# 创建 x 轴标签
x_labels = list(range(min_sum, max_sum + 1))

# 创建柱状图
fig = go.Figure(
    data=[
        go.Bar(
            x=x_labels,
            y=value_counts,
            marker_color='indianred'
        )
    ]
)

# 更新布局
fig.update_layout(
    title=f'同时掷三个D6的结果分布（模拟次数：{num_trials}）',
    xaxis_title='点数总和',
    yaxis_title='出现次数',
    xaxis=dict(tickmode='linear'),
    width=800,
    height=600
)


# 显示图表
fig.show()
