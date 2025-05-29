from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = FastAPI()

# スプレッドシート認証
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)
spreadsheet = client.open("RDI")  # ← 固定のスプレッドシート名

# POST用のデータ構造
class WriteRequest(BaseModel):
    sheet_name: str  # ← ここを追加：ワークシート名（タブ名）
    row: int
    col: int
    value: str

@app.post("/write_cell")
def write_cell(data: WriteRequest):
    try:
        worksheet = spreadsheet.worksheet(data.sheet_name)  # ← ワークシート名で取得
        worksheet.update_cell(data.row, data.col, data.value)
        return {
            "message": f"Wrote '{data.value}' to cell ({data.row}, {data.col}) in sheet '{data.sheet_name}'"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
