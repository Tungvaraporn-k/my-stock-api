from fastapi import FastAPI
import requests

app = FastAPI(
    title="Stock Analysis API for Custom GPT",
    description="API สำหรับดูราคาหุ้น วิเคราะห์แนวรับ-แนวต้าน และข่าวหุ้น",
    version="1.0.0",
    servers=[
        {"url": "https://a1b2-c3d4-e5f6.ngrok-free.app"} # ใส่ URL ngrok ของคุณตรงนี้
    ]
)

API_KEY = "ใส่_API_KEY_ของคุณที่นี่"

@app.get("/stock/{symbol}")
def get_stock_info(symbol: str):
    """
    ดึงข้อมูลราคาปัจจุบัน ข่าวล่าสุด และประเมินแนวรับแนวต้านของหุ้น (ตัวย่อ)
    """
    # 1. ดึงราคาปัจจุบัน (จำลองการดึงจาก Finnhub)
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    response = requests.get(url).json()
    
    current_price = response.get('c', 0)
    high_price = response.get('h', 0)
    low_price = response.get('l', 0)
    
    # 2. วิเคราะห์แนวรับแนวต้าน (แบบ Basic: ใช้จุดสูงสุด/ต่ำสุดของวัน หรือคุณจะใช้สูตร Pivot Point ก็ได้)
    resistance = high_price * 1.05 # สมมติว่าแนวต้านคือ High + 5%
    support = low_price * 0.95    # สมมติว่าแนวรับคือ Low - 5%
    
    # 3. ดึงข่าวหุ้น (จำลอง)
    news_url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2023-01-01&to=2023-01-02&token={API_KEY}"
    # news_response = requests.get(news_url).json() # ของจริง uncomment บรรทัดนี้
    
    return {
        "symbol": symbol.upper(),
        "current_price": current_price,
        "support_level": support,
        "resistance_level": resistance,
        "latest_news": "นี่คือข่าวที่ดึงมาจาก API..." # ใส่ news_response ที่ดึงมา
    }