"""学生管理系统主应用"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.core.middleware import ExceptionHandlerMiddleware, RequestLogMiddleware
from app.api.v1 import auth, students, grades, statistics
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="学生管理系统API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# 添加自定义中间件
app.add_middleware(RequestLogMiddleware)
app.add_middleware(ExceptionHandlerMiddleware)

# 注册路由
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(students.router, prefix=settings.API_V1_PREFIX)
app.include_router(grades.router, prefix=settings.API_V1_PREFIX)
app.include_router(statistics.router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    logging.info("数据库表创建成功")
    logging.info(f"{settings.APP_NAME} 启动成功")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logging.info(f"{settings.APP_NAME} 已关闭")


@app.get("/", tags=["根路径"])
async def root():
    """根路径"""
    return {
        "message": f"欢迎使用{settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
