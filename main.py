from fastapi import FastAPI
#실행
#python -m uvicorn main:app --host 172.16.20.209 --port 81

# FastAPI 애플리케이션 생성
app = FastAPI()

# /getInfo 경로에 대한 GET 요청 처리
@app.get("/getInfo")
async def get_info():
    # 반환할 JSON 데이터
    return {
        "status": "success",
        "message": "This is your JSON response!",
        "data": {"key1": "value1", "key2": "value2"}
    }