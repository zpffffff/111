import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载清洗后的数据
df = pd.read_csv('cleaned_惠州交通事故数据.csv')

# 设置主题
sns.set_theme(style="whitegrid", font="SimHei")  # 确保中文字体支持

# --- 绘制死亡人数与损失折款双轴趋势图 ---
fig, ax1 = plt.subplots(figsize=(12, 6))

# 左轴：死亡人数
sns.lineplot(data=df, x='年份', y='全市死亡人数',
             marker='o', color='#FF6B6B', ax=ax1, label='死亡人数')
ax1.set_ylabel('全市交通事故死亡人数（人）', color='#FF6B6B')
ax1.tick_params(axis='y', labelcolor='#FF6B6B')

# 右轴：损失折款
ax2 = ax1.twinx()
sns.lineplot(data=df, x='年份', y='全市损失折款（万元）',
             marker='s', color='#4ECDC4', ax=ax2, label='经济损失')
ax2.set_ylabel('全市损失折款（万元）', color='#4ECDC4')
ax2.tick_params(axis='y', labelcolor='#4ECDC4')

# 标注2017年异常点
ax1.annotate('异常高损失', xy=(2017, 288), xytext=(2015, 300),
             arrowprops=dict(arrowstyle='->', color='gray'),
             fontsize=10, color='red')

plt.title('惠州市交通事故死亡人数与经济损失趋势（2005-2024）', pad=20)
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.tight_layout()
plt.savefig('趋势分析.png', dpi=300)
plt.show()