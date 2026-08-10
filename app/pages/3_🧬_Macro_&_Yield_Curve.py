import streamlit as st
import pandas as pd
from utils import load_config, load_processed_data
from src.charts.chart_generator import ChartGenerator
from src.analytics.yield_curve_analyzer import YieldCurveAnalyzer
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

st.set_page_config(page_title="宏觀與收益率", layout="wide")

st.title("🧬 宏觀視圖與收益率曲線")

yield_df = load_processed_data('yield_analysis.parquet')
returns_df = load_processed_data('returns.parquet')

if yield_df is not None:
    tab1, tab2 = st.tabs(["收益率曲線", "資產相關性"])
    
    with tab1:
        st.subheader("美國國債收益率曲線")
        # 修正這裡：從 ../ 改為 ../../
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/processed'))
        analyzer = YieldCurveAnalyzer(data_dir)

        col1, col2 = st.columns([2, 1])
        
        with col1:
            chart_gen = ChartGenerator()
            fig = chart_gen.plot_yield_curve(latest_curve)
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.metric("當前曲線形狀", analyzer.analyze_shape())
            if '10Y-2Y' in yield_df.columns:
                st.metric("10Y-2Y 利差", f"{yield_df['10Y-2Y'].iloc[-1]:.2f}%")
        
        st.markdown("---")
        st.subheader("歷史利差監測")
        fig_spread = chart_gen.plot_spread_history(yield_df, '10Y-2Y')
        st.plotly_chart(fig_spread, use_container_width=True)

    with tab2:
        if returns_df is not None:
            st.subheader("資產類別相關性")
            chart_gen = ChartGenerator()
            fig_corr = chart_gen.plot_correlation_heatmap(returns_df)
            st.plotly_chart(fig_corr, use_container_width=True)
            st.info("💡 相關性接近 1 表示同步漲跌，接近 -1 表示反向運動。")
else:
    st.error("找不到收益率數據。請確保已正確配置 FRED API Key。")
