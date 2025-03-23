import random
import string
import sqlite3
from fastapi import FastAPI, Query
from pydantic import BaseModel, HttpUrl
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware( # type: ignore
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
conn = sqlite3.connect("urls.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_code TEXT NOT NULL UNIQUE,
    clicks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
conn.close()

class URLRequest(BaseModel):
    long_url: HttpUrl

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.post("/shorten")
def shorten_url(request: URLRequest, alias: str = Query(None)):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    
    # Check if the URL already exists
    cursor.execute("SELECT short_code FROM urls WHERE long_url = ?", (str(request.long_url),))
    existing = cursor.fetchone()
    
    if existing:
        return {"short_url": f"http://127.0.0.1:8000/{existing[0]}"}
    
    short_code = alias if alias else generate_short_code()
    
    # Ensure alias is unique
    cursor.execute("SELECT short_code FROM urls WHERE short_code = ?", (short_code,))
    if cursor.fetchone():
        conn.close()
        return {"error": "Alias already exists. Choose a different one."}
    
    cursor.execute("INSERT INTO urls (long_url, short_code) VALUES (?, ?)", (str(request.long_url), short_code))
    conn.commit()
    conn.close()
    
    return {"short_url": f"http://127.0.0.1:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT long_url, clicks FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    
    if result:
        long_url, clicks = result
        cursor.execute("UPDATE urls SET clicks = ? WHERE short_code = ?", (clicks + 1, short_code))
        conn.commit()
        conn.close()
        return RedirectResponse(url=long_url)
    
    conn.close()
    return {"error": "Short URL not found"}

@app.get("/stats/{short_code}")
def get_clicks(short_code: str):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT long_url, clicks FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {"long_url": result[0], "clicks": result[1]}
    else:
        return {"error": "Short URL not found"}
    

@app.get("/stats/{short_code}")
def get_clicks(short_code: str):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT long_url, clicks FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result:
        return {"long_url": result[0], "clicks": result[1]}
    else:
        return {"error": "Short URL not found"}