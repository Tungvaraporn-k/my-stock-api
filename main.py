import os, requests
from fastapi import FastAPI, HTTPException

app = FastAPI(title="Stock Analysis API")
API_KEY = os.environ.get("API_KEY")

@app.get("/stock/{symbol}")
def get_stock_info(symbol: str):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY is not configured.")
        
    symbol = symbol.upper()
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    res = requests.get(url).json()
    
    # ดัก Error: ถ้าไม่มีข้อมูล (c=0) หรือ API Key ผิด (มีคำว่า error)
    if "error" in res or res.get('c', 0) == 0:
        raise HTTPException(status_code=404, detail="Stock not found or API Error")
    
    # คำนวณและส่งผลลัพธ์กลับทันที
    return {
        "symbol": symbol,
        "current_price": res['c'],
        "support_level": round(res['l'] * 0.95, 2),
        "resistance_level": round(res['h'] * 1.05, 2)
    }