import pandas as pd
import numpy as np
from pmdarima import auto_arima

def load_and_clean_data():
    df = pd.read_csv('C:/Users/86158/Desktop/惠州市交通事故数据.csv', encoding='gbk')

    df.columns = df.columns.str.strip().str.replace(r'[^\w\u4e00-\u9fff（）]', '', regex=True)

    df = df.rename(columns={
        '惠州市交通事故死亡人数': '全市死亡人数'
    })

    df = df[df['年份'] >= 2016]

    df['全市死亡人数'] = df['全市死亡人数'].fillna(method='ffill')
    return df

def forecast_deaths(df):
    SCALING_FACTOR = 1.5  # 适当降低缩放因子
    df['全市死亡人数_scaled'] = df['全市死亡人数'] / SCALING_FACTOR

    train_data = df[df['年份'] >= 2016]['全市死亡人数_scaled'].values

    model = auto_arima(
        train_data,
        seasonal=False,
        trace=True,
        error_action='ignore',
        suppress_warnings=True,
        max_d=2,
        max_p=3,
        max_q=3,
        trend='t',
        stepwise=True  # 加速计算
    )

    forecast_years = 6
    forecast_scaled, conf_int_scaled = model.predict(
        n_periods=forecast_years,
        return_conf_int=True
    )

    # 逆缩放
    forecast = forecast_scaled * SCALING_FACTOR
    conf_int = conf_int_scaled * SCALING_FACTOR

    # **修改 np.clip，避免所有预测值都变成100**
    forecast = np.minimum(forecast, 100)  # 只限制上限，避免预测值全是100
    conf_int[:, 1] = np.minimum(conf_int[:, 1], 100)  # 只限制预测区间的上限

    forecast_df = pd.DataFrame({
        '年份': range(2025, 2025 + forecast_years),
        '预测死亡人数': forecast.round(2),
        '预测下限': conf_int[:, 0].round(2),
        '预测上限': conf_int[:, 1].round(2)
    })

    return forecast_df

if __name__ == "__main__":
    df = load_and_clean_data()
    forecast_df = forecast_deaths(df)
    forecast_df.to_json("data/huizhou_forecast.json", orient='records', force_ascii=False)
    print("✅ 预测数据已保存为 data/huizhou_forecast.json", forecast_df)
