import pandas as pd
import numpy as np
from pmdarima import auto_arima


def load_and_clean_data():
    """加载并清理交通事故经济损失数据"""
    df = pd.read_csv('C:/Users/86158/Desktop/惠州市交通事故数据.csv', encoding='gbk')
    df.columns = df.columns.str.strip().str.replace(r'[^\w\u4e00-\u9fff（）]', '', regex=True)
    df = df[df['年份'] >= 2016].rename(columns={'惠州市交通事故损失折款': '全市损失折款'})
    df['全市损失折款'] = df['全市损失折款'].fillna(method='ffill')
    return df


def forecast_economic_loss(df):
    df['损失_log'] = np.log1p(df['全市损失折款'])
    model = auto_arima(
        df['损失_log'], seasonal=False, trace=True,
        error_action='ignore', suppress_warnings=True, trend='t'
    )
    forecast_years = 6
    forecast_log, conf_int_log = model.predict(
        n_periods=forecast_years, return_conf_int=True
    )
    forecast = np.expm1(forecast_log).round(2)
    conf_int = np.expm1(conf_int_log).round(2)

    return pd.DataFrame({
        '年份': [2025 + i for i in range(forecast_years)],
        '预测损失折款': forecast,
        '预测下限': conf_int[:, 0],
        '预测上限': conf_int[:, 1]
    })


if __name__ == "__main__":
    df = load_and_clean_data()
    forecast_df = forecast_economic_loss(df)

    # 保存独立的历史数据和预测数据（不合并）
    df[['年份', '全市损失折款']].rename(columns={'全市损失折款': '实际损失折款'}) \
        .to_json("data/huizhou_economic_traffic_2016.json", orient='records', force_ascii=False)
    forecast_df.to_json("data/huizhou_economic_forecast.json", orient='records', force_ascii=False)
    print("✅ 预测数据已保存！")