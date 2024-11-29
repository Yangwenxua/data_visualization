import matplotlib.pyplot as plt

class RandomWalk:
    def __init__(self, num_points=5000):
        self.num_points = num_points
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        while len(self.x_values) < self.num_points:
            x_step, y_step = self.get_step()
            self.x_values.append(self.x_values[-1] + x_step)
            self.y_values.append(self.y_values[-1] + y_step)

    def get_step(self):
        import random
        x_direction = random.choice([1, -1])
        x_distance = random.choice([0, 1, 2, 3, 4])
        y_direction = random.choice([1, -1])
        y_distance = random.choice([0, 1, 2, 3, 4])
        return (x_direction * x_distance, y_direction * y_distance)

# 创建 RandomWalk 实例
rw = RandomWalk()
rw.fill_walk()

# 创建绘图和坐标轴对象
fig, ax = plt.subplots()

# 使用 plot 绘制路径，设置线条宽度为 1，颜色为蓝色
ax.plot(rw.x_values, rw.y_values, linewidth=1, color='blue')

# 设置坐标轴范围（可选）
ax.set_xlim(0, max(rw.x_values) + 10)
ax.set_ylim(0, max(rw.y_values) + 10)

# 显示图形
plt.show()

