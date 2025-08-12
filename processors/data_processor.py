"""
Data Processor - Handles data processing and feature engineering
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Any


class StockDataProcessor:
    """
    Xử lý và chuẩn bị dữ liệu cho phân tích
    """

    def __init__(self):
        pass

    def process_daily_data(self, data_list: List[Dict[str, Any]]) -> pd.DataFrame:
        """
        Chuyển đổi dữ liệu daily thành DataFrame pandas
        """
        if not data_list:
            return pd.DataFrame()
            
        df = pd.DataFrame(data_list)

        if not df.empty:
            # Chuyển đổi kiểu dữ liệu
            df['date'] = pd.to_datetime(df['date'])
            numeric_columns = ['open', 'close', 'high', 'low', 'volume']

            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            # Tính toán các chỉ số bổ sung
            df['price_change'] = df['close'] - df['open']
            df['price_change_pct'] = (df['price_change'] / df['open'] * 100).round(2)
            df['daily_range'] = df['high'] - df['low']
            df['daily_range_pct'] = (df['daily_range'] / df['open'] * 100).round(2)

            # Sắp xếp theo ngày
            df = df.sort_values('date').reset_index(drop=True)

        return df

    def create_ml_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Tạo features cho mô hình machine learning
        """
        if df.empty:
            return df

        # Tính moving averages
        df['ma_5'] = df['close'].rolling(window=5).mean()
        df['ma_10'] = df['close'].rolling(window=10).mean()
        df['ma_20'] = df['close'].rolling(window=20).mean()

        # Tính RSI đơn giản
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # Tính volatility
        df['volatility'] = df['close'].rolling(window=10).std()

        # Tính volume indicators
        df['volume_ma'] = df['volume'].rolling(window=5).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma']

        return df

    def calculate_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Tính toán thống kê cơ bản
        """
        if df.empty:
            return {}

        stats = {
            'total_records': len(df),
            'date_range': {
                'start': df['date'].min().strftime('%Y-%m-%d'),
                'end': df['date'].max().strftime('%Y-%m-%d')
            },
            'price_stats': {
                'current_price': df['close'].iloc[-1] if not df.empty else None,
                'max_price': df['high'].max(),
                'min_price': df['low'].min(),
                'avg_price': df['close'].mean(),
                'price_volatility': df['close'].std()
            },
            'volume_stats': {
                'avg_volume': df['volume'].mean(),
                'max_volume': df['volume'].max(),
                'min_volume': df['volume'].min()
            },
            'performance': {
                'total_return': ((df['close'].iloc[-1] - df['open'].iloc[0]) / df['open'].iloc[0] * 100) if len(df) > 0 else 0,
                'best_day': df['price_change_pct'].max(),
                'worst_day': df['price_change_pct'].min(),
                'avg_daily_change': df['price_change_pct'].mean()
            }
        }

        return stats

    def detect_patterns(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Phát hiện các pattern đơn giản trong dữ liệu
        """
        if df.empty or len(df) < 5:
            return {}

        patterns = {}

        # Trend detection
        recent_closes = df['close'].tail(5).values
        if len(recent_closes) >= 5:
            if all(recent_closes[i] <= recent_closes[i+1] for i in range(len(recent_closes)-1)):
                patterns['trend'] = 'upward'
            elif all(recent_closes[i] >= recent_closes[i+1] for i in range(len(recent_closes)-1)):
                patterns['trend'] = 'downward'
            else:
                patterns['trend'] = 'sideways'

        # Volume analysis
        if 'volume_ratio' in df.columns:
            recent_volume_ratio = df['volume_ratio'].tail(5).mean()
            if recent_volume_ratio > 1.5:
                patterns['volume_activity'] = 'high'
            elif recent_volume_ratio < 0.5:
                patterns['volume_activity'] = 'low'
            else:
                patterns['volume_activity'] = 'normal'

        # RSI analysis
        if 'rsi' in df.columns and not df['rsi'].isna().all():
            current_rsi = df['rsi'].dropna().iloc[-1] if not df['rsi'].dropna().empty else None
            if current_rsi:
                if current_rsi > 70:
                    patterns['rsi_signal'] = 'overbought'
                elif current_rsi < 30:
                    patterns['rsi_signal'] = 'oversold'
                else:
                    patterns['rsi_signal'] = 'neutral'

        return patterns