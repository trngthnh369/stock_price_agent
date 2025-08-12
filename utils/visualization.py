"""
Visualization utilities for stock data
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Dict, Any, Optional
from config import Config


class StockVisualizer:
    """
    Tạo các biểu đồ cho dữ liệu cổ phiếu
    """

    def __init__(self, figsize: tuple = None):
        self.figsize = figsize or Config.DEFAULT_CHART_FIGSIZE
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")

    def plot_price_history(self, df: pd.DataFrame, symbol: str, save_path: str = None) -> None:
        """
        Vẽ biểu đồ lịch sử giá cổ phiếu
        """
        if df.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Price chart
        ax1.plot(df['date'], df['close'], marker='o', linewidth=2, label='Close Price')
        if 'ma_5' in df.columns:
            ax1.plot(df['date'], df['ma_5'], label='MA 5', alpha=0.7)
        if 'ma_10' in df.columns:
            ax1.plot(df['date'], df['ma_10'], label='MA 10', alpha=0.7)
        
        ax1.set_title(f'{symbol} - Lịch sử giá cổ phiếu', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Giá ($)', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Volume chart
        ax2.bar(df['date'], df['volume'], alpha=0.6, color='orange')
        ax2.set_title(f'{symbol} - Khối lượng giao dịch', fontsize=14)
        ax2.set_ylabel('Volume', fontsize=12)
        ax2.set_xlabel('Ngày', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # Rotate x-axis labels
        for ax in [ax1, ax2]:
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()

    def plot_price_change_distribution(self, df: pd.DataFrame, symbol: str, save_path: str = None) -> None:
        """
        Vẽ phân phối thay đổi giá hằng ngày
        """
        if df.empty or 'price_change_pct' not in df.columns:
            print("Không có dữ liệu price_change_pct để vẽ biểu đồ")
            return

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Daily returns bar chart
        colors = ['green' if x > 0 else 'red' for x in df['price_change_pct']]
        ax1.bar(df['date'], df['price_change_pct'], color=colors, alpha=0.7)
        ax1.set_title(f'{symbol} - Thay đổi giá hằng ngày (%)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('% Thay đổi', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        
        # Distribution histogram
        ax2.hist(df['price_change_pct'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.set_title(f'{symbol} - Phân phối thay đổi giá', fontsize=14, fontweight='bold')
        ax2.set_xlabel('% Thay đổi', fontsize=12)
        ax2.set_ylabel('Tần suất', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.axvline(x=0, color='red', linestyle='--', alpha=0.7)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()

    def plot_technical_indicators(self, df: pd.DataFrame, symbol: str, save_path: str = None) -> None:
        """
        Vẽ các chỉ báo kỹ thuật
        """
        if df.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        fig, axes = plt.subplots(3, 1, figsize=(12, 12))
        
        # Price with Moving Averages
        axes[0].plot(df['date'], df['close'], label='Close Price', linewidth=2)
        if 'ma_5' in df.columns:
            axes[0].plot(df['date'], df['ma_5'], label='MA 5', alpha=0.7)
        if 'ma_10' in df.columns:
            axes[0].plot(df['date'], df['ma_10'], label='MA 10', alpha=0.7)
        if 'ma_20' in df.columns:
            axes[0].plot(df['date'], df['ma_20'], label='MA 20', alpha=0.7)
        
        axes[0].set_title(f'{symbol} - Giá và Moving Averages', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Giá ($)', fontsize=12)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # RSI
        if 'rsi' in df.columns and not df['rsi'].isna().all():
            axes[1].plot(df['date'], df['rsi'], color='purple', linewidth=2)
            axes[1].axhline(y=70, color='red', linestyle='--', alpha=0.7, label='Overbought (70)')
            axes[1].axhline(y=30, color='green', linestyle='--', alpha=0.7, label='Oversold (30)')
            axes[1].fill_between(df['date'], 30, 70, alpha=0.1, color='gray')
            axes[1].set_title(f'{symbol} - RSI (Relative Strength Index)', fontsize=14)
            axes[1].set_ylabel('RSI', fontsize=12)
            axes[1].set_ylim(0, 100)
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)
        else:
            axes[1].text(0.5, 0.5, 'Không đủ dữ liệu để tính RSI', 
                        transform=axes[1].transAxes, ha='center', va='center', fontsize=12)
        
        # Volume with Moving Average
        axes[2].bar(df['date'], df['volume'], alpha=0.6, color='orange', label='Volume')
        if 'volume_ma' in df.columns:
            axes[2].plot(df['date'], df['volume_ma'], color='red', linewidth=2, label='Volume MA 5')
        
        axes[2].set_title(f'{symbol} - Khối lượng giao dịch', fontsize=14)
        axes[2].set_ylabel('Volume', fontsize=12)
        axes[2].set_xlabel('Ngày', fontsize=12)
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        # Rotate x-axis labels for all subplots
        for ax in axes:
            ax.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()

    def plot_candlestick_simple(self, df: pd.DataFrame, symbol: str, save_path: str = None) -> None:
        """
        Vẽ biểu đồ nến đơn giản (không dùng mplfinance)
        """
        if df.empty:
            print("Không có dữ liệu để vẽ biểu đồ")
            return

        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Simple candlestick representation using bar charts
        for i, (idx, row) in enumerate(df.iterrows()):
            color = 'green' if row['close'] > row['open'] else 'red'
            
            # Body of the candle
            body_height = abs(row['close'] - row['open'])
            body_bottom = min(row['open'], row['close'])
            ax.bar(i, body_height, bottom=body_bottom, color=color, alpha=0.7, width=0.8)
            
            # Wicks
            ax.plot([i, i], [row['low'], row['high']], color='black', linewidth=1)
        
        ax.set_title(f'{symbol} - Biểu đồ nến', fontsize=14, fontweight='bold')
        ax.set_ylabel('Giá ($)', fontsize=12)
        ax.set_xlabel('Ngày', fontsize=12)
        
        # Set x-axis labels
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels([d.strftime('%m/%d') for d in df['date']], rotation=45)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()

    def create_summary_dashboard(self, df: pd.DataFrame, symbol: str, stats: Dict[str, Any], save_path: str = None) -> None:
        """
        Tạo dashboard tổng hợp
        """
        if df.empty:
            print("Không có dữ liệu để tạo dashboard")
            return

        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Main price chart
        ax1 = fig.add_subplot(gs[0, :2])
        ax1.plot(df['date'], df['close'], linewidth=2, label='Close Price')
        if 'ma_5' in df.columns:
            ax1.plot(df['date'], df['ma_5'], alpha=0.7, label='MA 5')
        if 'ma_10' in df.columns:
            ax1.plot(df['date'], df['ma_10'], alpha=0.7, label='MA 10')
        ax1.set_title(f'{symbol} - Giá cổ phiếu', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # Statistics text
        ax2 = fig.add_subplot(gs[0, 2])
        ax2.axis('off')
        stats_text = f"""
        THỐNG KÊ {symbol}
        
        Giá hiện tại: ${stats.get('price_stats', {}).get('current_price', 'N/A'):.2f}
        Giá cao nhất: ${stats.get('price_stats', {}).get('max_price', 'N/A'):.2f}
        Giá thấp nhất: ${stats.get('price_stats', {}).get('min_price', 'N/A'):.2f}
        
        Tổng lợi nhuận: {stats.get('performance', {}).get('total_return', 'N/A'):.2f}%
        Ngày tốt nhất: {stats.get('performance', {}).get('best_day', 'N/A'):.2f}%
        Ngày tệ nhất: {stats.get('performance', {}).get('worst_day', 'N/A'):.2f}%
        
        Số ngày: {stats.get('total_records', 'N/A')}
        """
        ax2.text(0.05, 0.95, stats_text, transform=ax2.transAxes, fontsize=10,
                verticalalignment='top', fontfamily='monospace')
        
        # Volume chart
        ax3 = fig.add_subplot(gs[1, :2])
        ax3.bar(df['date'], df['volume'], alpha=0.6, color='orange')
        ax3.set_title('Khối lượng giao dịch', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Price change distribution
        ax4 = fig.add_subplot(gs[1, 2])
        if 'price_change_pct' in df.columns:
            ax4.hist(df['price_change_pct'], bins=15, alpha=0.7, color='skyblue', edgecolor='black')
            ax4.set_title('Phân phối % thay đổi', fontsize=12)
            ax4.axvline(x=0, color='red', linestyle='--', alpha=0.7)
        
        # Daily returns
        ax5 = fig.add_subplot(gs[2, :])
        if 'price_change_pct' in df.columns:
            colors = ['green' if x > 0 else 'red' for x in df['price_change_pct']]
            ax5.bar(df['date'], df['price_change_pct'], color=colors, alpha=0.7)
            ax5.set_title('Thay đổi giá hằng ngày (%)', fontsize=12)
            ax5.axhline(y=0, color='black', linestyle='-', alpha=0.5)
            ax5.tick_params(axis='x', rotation=45)
            ax5.grid(True, alpha=0.3)
        
        plt.suptitle(f'{symbol} - Dashboard Phân Tích Cổ Phiếu', fontsize=16, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        plt.show()