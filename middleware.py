from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class CustomMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 요청 로깅
        print(f"Request path: {request.url.path}")

        # 요청을 다음으로 넘기고 응답을 받음
        response = await call_next(request)

        # 응답 로깅
        print(f"Response status: {response.status_code}")

        # # 응답이 StreamingResponse 타입인지 확인
        # if hasattr(response, 'body_iterator'):
        #     # 비동기적으로 응답 본문 수집
        #     body_bytes = b''
        #     async for chunk in response.body_iterator:
        #         body_bytes += chunk
        #     # 수집된 응답 본문 로깅
        #     body_text = body_bytes.decode('utf-8')
        #     print("Response body:", body_text)

        #     # 클라이언트에게 동일한 응답 본문 전송
        #     new_response = Response(content=body_bytes, status_code=response.status_code, headers=dict(response.headers), media_type=response.media_type)
        #     return new_response
        # else:
        #     return response

        return response