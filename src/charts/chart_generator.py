import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class ChartGenerator:
    @staticmethod
    def plot_price_history(df, ticker, name):
        """繪製歷史價格圖"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df[ticker], mode='lines', name=name))
        fig.update_layout(
            title=f"{name} 歷史價格",
            xaxis_title="日期",
            yaxis_title="價格",
            template="plotly_white"
        )
        return fig

    @staticmethod
    def plot_yield_curve(tenors_dict):
        """繪製當前收益率曲線"""
        x = list(tenors_dict.keys())
        y = list(tenors_dict.values())
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Yield Curve'))
        fig.update_layout(
            title="當前美國國債收益率曲線",
            xaxis_title="期限",
            yaxis_title="收益率 (%)",
            template="plotly_white"
        )
        return fig

    @staticmethod
    def plot_correlation_heatmap(returns_df):
        """繪製資產相關性熱圖"""
        # 只保留有足夠有效資料的資產，去掉全是 NaN 的欄位
        clean = returns_df.dropna(axis=1, how='all')
        
        # 再去掉全是 NaN 的列
        clean = clean.dropna(how='all')
        
        # 計算相關性（自動忽略 NaN）
        corr = clean.corr()
        
        # 如果還是空的，回傳提示圖
        if corr.empty or corr.isna().all().all():
            fig = go.Figure()
            fig.update_layout(title="無法計算相關性（資料不足）", template="plotly_white")
            return fig
        
        fig = px.imshow(
            corr, 
            text_auto='.2f', 
            aspect="auto", 
            title="資產相關性熱圖",
            color_continuous_scale='RdBu_r',
            zmin=-1, 
            zmax=1
        )
        fig.update_layout(
            xaxis_title="",
            yaxis_title="",
            height=500
        )
        return fig

    @staticmethod
    def plot_spread_history(df, column='10Y-2Y'):
        """繪製歷史利差圖"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df[column], mode='lines', name=column))
        # 添加 0 線以識別倒掛
        fig.add_hline(y=0, line_dash="dash", line_color="red")
        fig.update_layout(
            title=f"歷史 {column} 利差 (倒掛監測)",
            xaxis_title="日期",
            yaxis_title="利差 (%)",
            template="plotly_white"
        )
        return fig
