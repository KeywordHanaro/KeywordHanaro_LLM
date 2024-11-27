from pydantic import BaseModel
# 요청 데이터 모델 정의
class QueryRequest(BaseModel):
    query: str  # 클라이언트로부터 받을 'query' 필드

# 응답 데이터 모델 정의
class QueryResponse(BaseModel):
    query: str  # 클라이언트가 보낸 쿼리
    answer: str  # 서버에서 생성한 답변