"""中间件模块"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.exceptions import BusinessException
import time
import logging

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    """异常处理中间件"""
    
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except BusinessException as e:
            return JSONResponse(
                status_code=e.code,
                content={
                    "code": e.code,
                    "message": e.message
                }
            )
        except Exception as e:
            logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "code": 500,
                    "message": "服务器内部错误"
                }
            )


class RequestLogMiddleware(BaseHTTPMiddleware):
    """请求日志中间件"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 记录请求信息
        logger.info(f"Request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # 记录响应信息
        process_time = time.time() - start_time
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"status={response.status_code} duration={process_time:.3f}s"
        )
        
        return response
