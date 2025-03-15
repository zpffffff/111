import pandas as pd
from pmdarima import auto_arima

# ----------------------
# 1. 读取数据并清理列名
# ----------------------
try:
    df = pd.read_csv(
        r'C:\Users\86158\Desktop\惠州市交通事故数据.csv',
        encoding='gbk'
    )

    # 清理列名（保留括号和汉字/数字/字母）
    df.columns = df.columns.str.strip().str.replace(
        r'[^a-zA-Z0-9\u4e00-\u9fff（）]',
        '',
        regex=True
    )

    # 手动重命名关键列
    df = df.rename(columns={
        '惠州市交通事故损失折款': '全市损失折款（万元）',
        '惠州市交通事故死亡人数': '全市死亡人数'
    })

    print("清理后的列名:", df.columns.tolist())  # 验证列名

except Exception as e:
    print("文件读取失败:", str(e))
    exit()

# ----------------------
# 2. 数据处理
# ----------------------
# 确保年份为整数
df['年份'] = pd.to_numeric(df['年份'], errors='coerce')

# 处理缺失值
df['全市损失折款（万元）'] = pd.to_numeric(df['全市损失折款（万元）'], errors='coerce')
df['全市损失折款（万元）'] = df['全市损失折款（万元）'].interpolate(method='linear')

# ----------------------
# 3. 训练ARIMA模型
# ----------------------
try:
    model = auto_arima(df['全市损失折款（万元）'], seasonal=False)
    df['预测值'] = model.predict_in_sample()
except Exception as e:
    print("ARIMA模型失败:", str(e))
    df['预测值'] = df['全市损失折款（万元）']  # 回退到原始值

# ----------------------
# 4. 保存为JSON
# ----------------------
output_data = df[['年份', '全市损失折款（万元）', '预测值']]
output_data.to_json("arima_result.json", orient='records', force_ascii=False)
print("数据已保存为 arima_result.json")