# Stock Price Agent

Một ứng dụng Python để phân tích cổ phiếu sử dụng Gemini AI và Polygon API.

## ✨ Tính năng

- 📈 Lấy dữ liệu cổ phiếu real-time từ Polygon API
- 🤖 Phân tích thông minh với Google Gemini AI
- 📊 Tạo biểu đồ và dashboard tương tác
- 🔍 Phát hiện patterns và tính toán chỉ báo kỹ thuật
- 💬 Giao diện tương tác với AI chatbot
- 📈 Hỗ trợ nhiều loại biểu đồ (giá, volume, RSI, MA)

## 🏗️ Cấu trúc project

```
stock_price_agent/
│
├── agents/
│   ├── __init__.py
│   ├── stock_agent.py      # Agent lấy dữ liệu từ Polygon API
│   └── gemini_agent.py     # Agent phân tích với Gemini AI
│
├── processors/
│   ├── __init__.py
│   └── data_processor.py   # Xử lý dữ liệu và tính toán chỉ báo
│
├── utils/
│   ├── __init__.py
│   └── visualization.py    # Tạo biểu đồ và dashboard
│
├── main.py                 # File chạy chính
├── config.py              # Cấu hình ứng dụng
├── requirements.txt       # Dependencies
├── .env                   # API keys (cần tạo)
├── .gitignore
└── README.md
```

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd stock_price_agent
```

### 2. Tạo virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình API keys

Tạo file `.env` và thêm API keys:

```bash
GEMINI_API_KEY=your_gemini_api_key_here
POLYGON_API_KEY=your_polygon_api_key_here
```

#### Lấy API keys:

- **Gemini API Key**: Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Polygon API Key**: Đăng ký tại [Polygon.io](https://polygon.io/)

## 🎮 Sử dụng

### Chạy ứng dụng

```bash
python main.py
```

### Các chế độ có sẵn:

1. **Demo đơn giản**: Test cơ bản với ít API calls
2. **Demo đầy đủ**: Showcase tất cả tính năng
3. **Chế độ tương tác**: Interactive CLI với AI chatbot
4. **Thoát**: Dừng ứng dụng

### Lệnh trong chế độ tương tác:

```bash
price AAPL                          # Lấy giá hiện tại
daily AAPL 2024-01-15              # Dữ liệu ngày cụ thể
history AAPL 30                     # Lịch sử 30 ngày
analyze AAPL                        # Phân tích với AI
chart AAPL 30                       # Vẽ biểu đồ
dashboard AAPL 30                   # Tạo dashboard
ask xu hướng giá about AAPL         # Hỏi AI
models                              # Xem Gemini models
quit                                # Thoát
```

## 📊 Các loại biểu đồ

1. **Price History**: Lịch sử giá với moving averages
2. **Volume Chart**: Khối lượng giao dịch
3. **Technical Indicators**: RSI, MA, Volume indicators
4. **Price Distribution**: Phân phối thay đổi giá
5. **Summary Dashboard**: Tổng hợp tất cả thông tin

## 🔧 Tùy chỉnh

### Thay đổi Gemini model

Sửa trong `config.py`:

```python
GEMINI_MODEL = 'gemini-1.5-pro'  # hoặc model khác
```

### Thay đổi settings

```python
API_DELAY = 0.5              # Delay giữa API calls
DEFAULT_HISTORICAL_DAYS = 30  # Số ngày mặc định
DEFAULT_CHART_FIGSIZE = (12, 8)  # Kích thước biểu đồ
```

## 📝 Ví dụ sử dụng

### Import và sử dụng trực tiếp:

```python
from agents.stock_agent import StockDataAgent
from agents.gemini_agent import GeminiStockAnalyzer
from processors.data_processor import StockDataProcessor

# Khởi tạo
stock_agent = StockDataAgent()
gemini_analyzer = GeminiStockAnalyzer(stock_agent)
processor = StockDataProcessor()

# Lấy dữ liệu
data = stock_agent.get_current_price("AAPL")
analysis = gemini_analyzer.analyze_stock_data(data)
print(analysis)
```

## 🚨 Lưu ý

- **Rate Limiting**: Polygon API có giới hạn requests. App có built-in rate limiting.
- **API Keys**: Không commit API keys lên GitHub. Sử dụng file `.env`.
- **Internet**: Cần kết nối internet để gọi API.
- **Python Version**: Yêu cầu Python 3.8+

## 🐛 Troubleshooting

### Lỗi API Key:

```bash
ValueError: Missing required environment variables: GEMINI_API_KEY, POLYGON_API_KEY
```

→ Kiểm tra file `.env` và API keys

### Lỗi Rate Limit:

```bash
Rate limit reached. Waiting 60 seconds...
```

→ App tự động chờ, không cần can thiệp

### Lỗi matplotlib trên Linux:

```bash
pip install python3-tk
```

## 📈 Roadmap

- [ ] Thêm nhiều chỉ báo kỹ thuật (MACD, Bollinger Bands)
- [ ] Export dữ liệu ra Excel/CSV
- [ ] Web interface với Streamlit
- [ ] Real-time notifications
- [ ] Portfolio tracking
- [ ] Backtesting engine

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Liên hệ

- **Email**: truongthinhnguyen30303@gmail.com

## 🙏 Acknowledgments

- [Polygon.io](https://polygon.io/) - Financial data API
- [Google Gemini](https://ai.google.dev/) - AI analysis
- [Matplotlib](https://matplotlib.org/) - Data visualization
- [Pandas](https://pandas.pydata.org/) - Data processing
