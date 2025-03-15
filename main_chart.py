import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('C:/Users/86158/Desktop/惠州市交通事故数据.csv', encoding='gbk')

# 清理列名（去掉前后空格）
df.columns = df.columns.str.strip()

# ✅ 手动重命名列名（与前端代码完全一致）
df = df.rename(columns={
    '惠州市交通事故死亡人数': '全市死亡人数',
    '惠州市交通事故损失折款': '全市损失折款（万元）',
    '惠州市:惠城区交通事故死亡人数': '惠城区死亡人数',
    '惠州市:惠阳区交通事故死亡人数': '惠阳区死亡人数',
    '惠州市:龙门县交通事故死亡人数': '龙门县死亡人数',
    '惠州市:惠东县交通事故死亡人数': '惠东县死亡人数',
    '惠州市:博罗县交通事故死亡人数': '博罗县死亡人数',
    '惠州市:大亚湾区交通事故死亡人数': '大亚湾区死亡人数',
    '惠州市:市辖区交通事故死亡人数': '市辖区死亡人数',
    '惠州市:仲恺高新区交通事故死亡人数': '仲恺高新区死亡人数'
})

# 只保留 2016 年后的数据
df = df[df['年份'] >= 2016]

# 保存为 JSON（处理 NaN 值）
df.fillna(0).to_json("huizhou_traffic_2016.json", orient='records', force_ascii=False)
print("✅ 数据已保存为 huizhou_traffic_2016.json")