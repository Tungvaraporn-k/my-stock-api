import os
from fastapi import FastAPI
import requests

app = FastAPI(
    title="Stock Analysis API for Custom GPT",
    description="API สำหรับดูราคาหุ้น วิเคราะห์แนวรับ-แนวต้าน และข่าวหุ้น",
    version="1.0.0"
)

# ดึง API_KEY มาจากตัวแปร Environment (ที่เราตั้งค่าใน Render)
API_KEY = os.environ.get("API_KEY")

@app.get("/stock/{symbol}")
def get_stock_info(symbol: str):
    """
    ดึงข้อมูลราคาปัจจุบัน ข่าวล่าสุด และประเมินแนวรับแนวต้านของหุ้น (ตัวย่อ)
    """
    # 1. ดึงราคาปัจจุบันจาก Finnhub
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    response = requests.get(url).json()
    
    current_price = response.get('c', 0)
    high_price = response.get('h', 0)
    low_price = response.get('l', 0)
    
    # 2. วิเคราะห์แนวรับแนวต้าน (Basic)
    resistance = high_price * 1.05 
    support = low_price * 0.95    
    
    # 3. ดึงข่าวหุ้น (จำลอง)
    # news_url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2023-01-01&to=2023-01-02&token={API_KEY}"
    
    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "support_level": round(support, 2),
        "resistance_level": round(resistance, 2),
        "latest_news": "นี่คือข่าวที่ดึงมาจาก API..." 
    }