import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('C:/Users/86158/Desktop/惠州市交通事故数据.csv', encoding='gbk')

# 清理列名
df.columns = df.columns.str.strip().str.replace(r'[^\w\u4e00-\u9fff（）]', '', regex=True)

# 重命名列
df = df.rename(columns={
    '惠州市交通事故死亡人数': '全市死亡人数',
    '惠州市交通事故损失折款': '全市损失折款（万元）',
    '惠州市惠城区交通事故死亡人数': '惠城区死亡人数',
    '惠州市惠阳区交通事故死亡人数': '惠阳区死亡人数',
    '惠州市龙门县交通事故死亡人数': '龙门县死亡人数',
    '惠州市惠东县交通事故死亡人数': '惠东县死亡人数',
    '惠州市博罗县交通事故死亡人数': '博罗县死亡人数',
    '惠州市大亚湾区交通事故死亡人数': '大亚湾区死亡人数',
    '惠州市仲恺高新区交通事故死亡人数': '仲恺高新区死亡人数'
})

# 计算死亡人数占比
districts = ['惠城区死亡人数', '惠阳区死亡人数', '龙门县死亡人数',
             '惠东县死亡人数', '博罗县死亡人数', '大亚湾区死亡人数',
             '仲恺高新区死亡人数']

for district in districts:
    df[f'{district}_占比'] = round(df[district] / df['全市死亡人数'].replace(0, 1) * 100, 2)

# 仅保留 2016 年后的数据
df = df[df['年份'] >= 2016]

# **保存为 JSON**
df.to_json("data/huizhou_traffic_2016.json", orient='records', force_ascii=False)

print("✅ 数据已保存为 huizhou_traffic_2016.json，包含占比数据！")
