import os
import sys
import threading
import webview
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.main import app

# --- Detect running mode (source vs. frozen .exe) ---
if getattr(sys, 'frozen', False):
    # Running inside PyInstaller bundle
    BASE_DIR = sys._MEIPASS  # temp folder where PyInstaller unpacks files
else:
    # Running from source
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Frontend path (React/Vite build) ---
FRONTEND_DIR = os.path.join(BASE_DIR, "client", "dist")
assets_dir = os.path.join(FRONTEND_DIR, "assets")

# --- Mount static assets ---
app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

@app.get("/{path:path}")
async def serve_frontend(path: str):
    index_file = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_file)

# --- Run FastAPI + PyWebView ---
def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def start_gui():
    webview.create_window("KDS App", "http://127.0.0.1:8000", width=1200, height=800)
    webview.start()

if __name__ == "__main__":
    threading.Thread(target=start_server, daemon=True).start()
    start_gui()
