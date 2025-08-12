"""
Gemini AI Agent - Uses Google Gemini for stock analysis
"""
import google.generativeai as genai
import json
from typing import Dict, Any
from config import Config


class GeminiStockAnalyzer:
    """
    Agent sử dụng Gemini để phân tích và trả lời câu hỏi về cổ phiếu
    """

    def __init__(self, stock_agent=None, api_key: str = None):
        self.stock_agent = stock_agent
        self.api_key = api_key or Config.GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError("Gemini API key is required")
            
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def analyze_stock_data(self, stock_data: Dict[str, Any]) -> str:
        """
        Sử dụng Gemini để phân tích dữ liệu cổ phiếu
        """
        if "error" in stock_data:
            return f"Không thể phân tích do lỗi: {stock_data['error']}"

        prompt = f"""
        Hãy phân tích dữ liệu cổ phiếu sau:

        Mã cổ phiếu: {stock_data.get('symbol')}
        Ngày: {stock_data.get('date')}
        Giá mở cửa: ${stock_data.get('open')}
        Giá đóng cửa: ${stock_data.get('close')}
        Giá cao nhất: ${stock_data.get('high')}
        Giá thấp nhất: ${stock_data.get('low')}
        Khối lượng: {stock_data.get('volume')}

        Hãy đưa ra:
        1. Phân tích xu hướng giá trong ngày
        2. Đánh giá về khối lượng giao dịch
        3. Tính toán % thay đổi giá
        4. Nhận xét tổng quan

        Trả lời bằng tiếng Việt và ngắn gọn.
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Lỗi khi phân tích với Gemini: {e}"

    def answer_stock_question(self, question: str, symbol: str = None) -> str:
        """
        Trả lời câu hỏi về cổ phiếu
        """
        try:
            # Nếu có symbol, lấy dữ liệu mới nhất
            context = ""
            if symbol and self.stock_agent:
                current_data = self.stock_agent.get_current_price(symbol)
                historical_data = self.stock_agent.get_historical_data(symbol, 5)

                context = f"""
                Dữ liệu hiện tại của {symbol}:
                {json.dumps(current_data, indent=2, ensure_ascii=False)}

                Dữ liệu 5 ngày gần đây:
                {json.dumps(historical_data, indent=2, ensure_ascii=False)}
                """

            prompt = f"""
            Bạn là một chuyên gia tài chính. Hãy trả lời câu hỏi sau về cổ phiếu:

            Câu hỏi: {question}

            {context}

            Hãy trả lời một cách chính xác, dựa trên dữ liệu có sẵn (nếu có), và đưa ra lời khuyên hợp lý.
            Trả lời bằng tiếng Việt.
            """

            response = self.model.generate_content(prompt)
            return response.text

        except Exception as e:
            return f"Lỗi khi trả lời câu hỏi: {e}"

    def get_available_models(self) -> list:
        """
        Get list of available Gemini models
        """
        try:
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    models.append(model.name)
            return models
        except Exception as e:
            print(f"Error getting models: {e}")
            return []