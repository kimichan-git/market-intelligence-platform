import pandas as pd
import os
from datetime import datetime

class SummaryEngine:
    def __init__(self, processed_data_dir, config):
        self.processed_data_dir = processed_data_dir
        self.config = config

    def get_market_highlights(self):
        """提取市場亮點數據"""
        returns_df = pd.read_parquet(os.path.join(self.processed_data_dir, 'returns.parquet'))
        yield_df = pd.read_parquet(os.path.join(self.processed_data_dir, 'yield_analysis.parquet'))
        
        # --- 新增：檢查數據是否為空 ---
        if returns_df.empty:
            print("Warning: returns_df is empty. Using placeholder data.")
            return self._get_empty_highlights()
        # ---------------------------

        last_returns = returns_df.iloc[-1]
        
        # 1. 表現最好與最差的資產
        top_performer = last_returns.idxmax()
        top_val = last_returns.max() * 100
        
        worst_performer = last_returns.idxmin()
        worst_val = last_returns.min() * 100
        
        # 2. 收益率曲線變化
        spread_10y2y = yield_df['10Y-2Y'].iloc[-1]
        spread_change = yield_df['10Y-2Y'].iloc[-1] - yield_df['10Y-2Y'].iloc[-2]
        
        highlights = {
            "date": returns_df.index[-1].strftime('%Y-%m-%d'),
            "top_performer": {"name": top_performer, "change": f"{top_val:.2f}%"},
            "worst_performer": {"name": worst_performer, "change": f"{worst_val:.2f}%"},
            "yield_spread_10y2y": f"{spread_10y2y:.2f}%",
            "yield_spread_change": f"{spread_change:.4f}%",
            "all_returns": last_returns.to_dict()
        }
        
        return highlights

    def generate_rule_based_text(self, highlights):
        """生成基於規則的簡單文本摘要"""
        text = f"### 📅 市場摘要 ({highlights['date']})\n\n"
        text += f"今日市場表現最強勁的資產是 **{highlights['top_performer']['name']}**，漲幅達 {highlights['top_performer']['change']}。\n"
        text += f"表現最弱的則是 **{highlights['worst_performer']['name']}**，跌幅為 {highlights['worst_performer']['change']}。\n\n"
        
        text += f"**宏觀環境：**\n"
        text += f"美國 10Y-2Y 國債利差目前為 {highlights['yield_spread_10y2y']}。今日變動為 {highlights['yield_spread_change']}。\n"
        
        return text
    
# 新增一個輔助方法處理空數據情況
    def _get_empty_highlights(self):
        return {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "top_performer": {"name": "N/A", "change": "0.00%"},
            "worst_performer": {"name": "N/A", "change": "0.00%"},
            "yield_spread_10y2y": "N/A",
            "yield_spread_change": "0.0000%",
            "all_returns": {}
        }
