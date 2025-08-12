"""
Main application for Stock Price Agent
"""
import json
import os
from datetime import datetime, timedelta
from config import Config
from agents.stock_agent import StockDataAgent
from agents.gemini_agent import GeminiStockAnalyzer
from processors.data_processor import StockDataProcessor
from utils.visualization import StockVisualizer


class StockPriceApp:
    """
    Main application class
    """
    
    def __init__(self):
        # Validate configuration
        try:
            Config.validate()
        except ValueError as e:
            print(f"❌ Configuration Error: {e}")
            print("Please check your .env file and ensure all required API keys are set.")
            return
        
        # Initialize components
        self.stock_agent = StockDataAgent()
        self.gemini_analyzer = GeminiStockAnalyzer(self.stock_agent)
        self.data_processor = StockDataProcessor()
        self.visualizer = StockVisualizer()
        
        print("🤖 Stock Price Agent đã được khởi tạo thành công!")
        print("📊 Sẵn sàng phân tích cổ phiếu với Gemini AI và Polygon API")

    def demo_simple(self):
        """
        Demo đơn giản để tránh rate limit
        """
        symbol = "AAPL"
        print(f"\n🍎 DEMO ĐỚN GIẢN: Phân tích cổ phiếu {symbol}")
        print("=" * 50)

        # 1. Lấy giá hiện tại
        print("\n📈 1. Giá hiện tại:")
        current_price = self.stock_agent.get_current_price(symbol)
        print(json.dumps(current_price, indent=2, ensure_ascii=False))

        # 2. Phân tích với Gemini AI (nếu có dữ liệu)
        if "error" not in current_price:
            print(f"\n🧠 2. Phân tích AI:")
            analysis = self.gemini_analyzer.analyze_stock_data(current_price)
            print(analysis)

        # 3. Hỏi một câu đơn giản
        print(f"\n💭 3. Hỏi AI:")
        question = f"Dựa trên giá hiện tại, {symbol} có đáng mua không?"
        answer = self.gemini_analyzer.answer_stock_question(question, symbol)
        print(f"❓ Câu hỏi: {question}")
        print(f"🤖 Trả lời: {answer}")

    def demo_full(self):
        """
        Demo đầy đủ các tính năng
        """
        symbol = "AAPL"
        print(f"\n🍎 DEMO ĐẦY ĐỦ: Phân tích cổ phiếu {symbol}")
        print("=" * 50)

        # 1. Lấy giá hiện tại
        print("\n📈 1. Giá hiện tại:")
        current_price = self.stock_agent.get_current_price(symbol)
        print(json.dumps(current_price, indent=2, ensure_ascii=False))

        # 2. Lấy dữ liệu daily open/close
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"\n📊 2. Dữ liệu open/close ngày {yesterday}:")
        daily_data = self.stock_agent.get_daily_open_close(symbol, yesterday)
        print(json.dumps(daily_data, indent=2, ensure_ascii=False))

        # 3. Phân tích với Gemini AI
        print(f"\n🧠 3. Phân tích AI:")
        if "error" not in daily_data:
            analysis = self.gemini_analyzer.analyze_stock_data(daily_data)
            print(analysis)

        # 4. Lấy dữ liệu lịch sử
        print(f"\n📈 4. Dữ liệu lịch sử 10 ngày:")
        historical_data = self.stock_agent.get_historical_data(symbol, 10)

        if historical_data:
            df = self.data_processor.process_daily_data(historical_data)
            df_with_features = self.data_processor.create_ml_features(df)

            print(f"✅ Đã xử lý {len(df)} bản ghi")
            
            # 5. Thống kê
            stats = self.data_processor.calculate_statistics(df_with_features)
            print(f"\n📊 5. Thống kê:")
            print(f"Giá hiện tại: ${stats['price_stats']['current_price']:.2f}")
            print(f"Tổng lợi nhuận: {stats['performance']['total_return']:.2f}%")
            print(f"Volatility: {stats['price_stats']['price_volatility']:.2f}")

            # 6. Pattern detection
            patterns = self.data_processor.detect_patterns(df_with_features)
            print(f"\n🔍 6. Phát hiện patterns:")
            for key, value in patterns.items():
                print(f"  {key}: {value}")

            # 7. Visualization
            print(f"\n📊 7. Tạo biểu đồ:")
            self.visualizer.plot_price_history(df_with_features, symbol)
            self.visualizer.create_summary_dashboard(df_with_features, symbol, stats)

        # 8. Q&A với AI
        print(f"\n💭 8. Hỏi đáp với AI:")
        question = f"Phân tích xu hướng và đưa ra khuyến nghị cho {symbol}?"
        answer = self.gemini_analyzer.answer_stock_question(question, symbol)
        print(f"❓ Câu hỏi: {question}")
        print(f"🤖 Trả lời: {answer}")

    def interactive_mode(self):
        """
        Chế độ tương tác với người dùng
        """
        print("\n🤖 STOCK PRICE AGENT - Interactive Mode")
        print("=" * 50)
        print("Các lệnh có sẵn:")
        print("- 'price [SYMBOL]': Lấy giá hiện tại")
        print("- 'daily [SYMBOL] [DATE]': Lấy dữ liệu ngày cụ thể (YYYY-MM-DD)")
        print("- 'history [SYMBOL] [DAYS]': Lấy dữ liệu lịch sử")
        print("- 'analyze [SYMBOL]': Phân tích với AI")
        print("- 'chart [SYMBOL] [DAYS]': Vẽ biểu đồ")
        print("- 'dashboard [SYMBOL] [DAYS]': Tạo dashboard")
        print("- 'ask [question] about [SYMBOL]': Hỏi AI")
        print("- 'models': Xem danh sách Gemini models")
        print("- 'quit': Thoát")
        print("=" * 50)

        while True:
            try:
                command = input("\n💬 Nhập lệnh (hoặc 'quit' để thoát): ").strip()

                if command.lower() == 'quit':
                    print("👋 Tạm biệt!")
                    break

                parts = command.split()
                if not parts:
                    continue

                action = parts[0].lower()

                if action == 'price' and len(parts) >= 2:
                    symbol = parts[1].upper()
                    result = self.stock_agent.get_current_price(symbol)
                    print(f"\n📈 Giá hiện tại của {symbol}:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))

                elif action == 'daily' and len(parts) >= 3:
                    symbol = parts[1].upper()
                    date = parts[2]
                    result = self.stock_agent.get_daily_open_close(symbol, date)
                    print(f"\n📊 Dữ liệu {symbol} ngày {date}:")
                    print(json.dumps(result, indent=2, ensure_ascii=False))

                elif action == 'history' and len(parts) >= 3:
                    symbol = parts[1].upper()
                    days = int(parts[2])
                    result = self.stock_agent.get_historical_data(symbol, days)
                    print(f"\n📈 Lịch sử {symbol} trong {days} ngày:")
                    
                    if result:
                        df = self.data_processor.process_daily_data(result)
                        print(df[['date', 'open', 'close', 'price_change_pct', 'volume']].to_string(index=False))
                    else:
                        print("Không có dữ liệu")

                elif action == 'analyze' and len(parts) >= 2:
                    symbol = parts[1].upper()
                    current_data = self.stock_agent.get_current_price(symbol)
                    analysis = self.gemini_analyzer.analyze_stock_data(current_data)
                    print(f"\n🧠 Phân tích AI cho {symbol}:")
                    print(analysis)

                elif action == 'chart' and len(parts) >= 3:
                    symbol = parts[1].upper()
                    days = int(parts[2])
                    historical_data = self.stock_agent.get_historical_data(symbol, days)
                    
                    if historical_data:
                        df = self.data_processor.process_daily_data(historical_data)
                        df = self.data_processor.create_ml_features(df)
                        self.visualizer.plot_price_history(df, symbol)
                    else:
                        print("Không có dữ liệu để vẽ biểu đồ")

                elif action == 'dashboard' and len(parts) >= 3:
                    symbol = parts[1].upper()
                    days = int(parts[2])
                    historical_data = self.stock_agent.get_historical_data(symbol, days)
                    
                    if historical_data:
                        df = self.data_processor.process_daily_data(historical_data)
                        df = self.data_processor.create_ml_features(df)
                        stats = self.data_processor.calculate_statistics(df)
                        self.visualizer.create_summary_dashboard(df, symbol, stats)
                    else:
                        print("Không có dữ liệu để tạo dashboard")

                elif action == 'ask':
                    if 'about' in command:
                        question_part, symbol_part = command.split('about', 1)
                        question = question_part.replace('ask', '').strip()
                        symbol = symbol_part.strip().upper()

                        answer = self.gemini_analyzer.answer_stock_question(question, symbol)
                        print(f"\n🤖 AI trả lời về {symbol}:")
                        print(answer)
                    else:
                        question = ' '.join(parts[1:])
                        answer = self.gemini_analyzer.answer_stock_question(question)
                        print(f"\n🤖 AI trả lời:")
                        print(answer)

                elif action == 'models':
                    models = self.gemini_analyzer.get_available_models()
                    print(f"\n🔍 Các Gemini models có sẵn:")
                    for model in models:
                        print(f"  ✅ {model}")

                else:
                    print("❌ Lệnh không hợp lệ. Vui lòng thử lại.")

            except KeyboardInterrupt:
                print("\n👋 Tạm biệt!")
                break
            except Exception as e:
                print(f"❌ Lỗi: {e}")

    def run(self):
        """
        Chạy ứng dụng với menu chọn
        """
        if not hasattr(self, 'stock_agent'):
            return
            
        print("\n🚀 STOCK PRICE AGENT")
        print("=" * 30)
        print("1. Demo đơn giản")
        print("2. Demo đầy đủ")
        print("3. Chế độ tương tác")
        print("4. Thoát")
        
        while True:
            try:
                choice = input("\n👉 Chọn chế độ (1-4): ").strip()
                
                if choice == '1':
                    self.demo_simple()
                elif choice == '2':
                    self.demo_full()
                elif choice == '3':
                    self.interactive_mode()
                elif choice == '4':
                    print("👋 Tạm biệt!")
                    break
                else:
                    print("❌ Lựa chọn không hợp lệ. Vui lòng chọn 1-4.")
                    
            except KeyboardInterrupt:
                print("\n👋 Tạm biệt!")
                break


def main():
    """Main function"""
    app = StockPriceApp()
    app.run()


if __name__ == "__main__":
    main()