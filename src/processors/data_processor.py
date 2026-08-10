import pandas as pd
import numpy as np
import os

class DataProcessor:
    def __init__(self, raw_data_dir, processed_data_dir):
        self.raw_data_dir = raw_data_dir
        self.processed_data_dir = processed_data_dir
        os.makedirs(self.processed_data_dir, exist_ok=True)

    def process_market_data(self, filename='market_data.parquet'):
        """處理市場數據：計算回報率、波動率等"""
        df = pd.read_parquet(os.path.join(self.raw_data_dir, filename))
        
        # --- 數據清洗 ---
        # 刪除全為 NaN 的列（例如無效 ticker）
        df = df.dropna(axis=1, how='all')
        # 刪除全空的行
        df = df.dropna(how='all')
        # --------------------

        # 計算日回報（保留 NaN，不填充假日，避免虛假 0 回報）
        returns = df.pct_change()
        # 只丟棄全部為 NaN 的行
        returns = returns.dropna(how='all')

        # 2. 計算滾動波動率 (20日) — 自動忽略 NaN
        volatility = returns.rolling(window=20, min_periods=5).std() * np.sqrt(252)
        
        # 3. 計算累計回報
        filled_returns = returns.fillna(0)
        cum_returns = (1 + filled_returns).cumprod()
        
        # 4. 計算最大回撤
        rolling_max = cum_returns.rolling(window=252, min_periods=1).max()
        drawdown = cum_returns / rolling_max - 1
        
        # 儲存處理後的數據
        returns.to_parquet(os.path.join(self.processed_data_dir, 'returns.parquet'))
        volatility.to_parquet(os.path.join(self.processed_data_dir, 'volatility.parquet'))
        cum_returns.to_parquet(os.path.join(self.processed_data_dir, 'cum_returns.parquet'))
        drawdown.to_parquet(os.path.join(self.processed_data_dir, 'drawdown.parquet'))
        
        print(f"Processed market data and saved to {self.processed_data_dir}")
        return df, returns

    def process_yield_data(self, filename='yield_data.parquet'):
        """處理收益率數據：計算利差"""
        df = pd.read_parquet(os.path.join(self.raw_data_dir, filename))
        
        # 確保數據是數值型並處理缺失值
        df = df.apply(pd.to_numeric, errors='coerce').ffill()
        
        # 計算關鍵利差
        if 'DGS10' in df.columns and 'DGS2' in df.columns:
            df['10Y-2Y'] = df['DGS10'] - df['DGS2']
        
        if 'DGS10' in df.columns and 'DGS5' in df.columns:
            df['10Y-5Y'] = df['DGS10'] - df['DGS5']
            
        # 儲存處理後的數據
        df.to_parquet(os.path.join(self.processed_data_dir, 'yield_analysis.parquet'))
        print(f"Processed yield data and saved to {self.processed_data_dir}")
        return df

if __name__ == "__main__":
    processor = DataProcessor('data/raw', 'data/processed')
    processor.process_market_data()
    processor.process_yield_data()
