from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import vehicles, reservations, auth, availability, customers, company, extras, analytics, assistant, whatsapp, payments, locations
from app.core.config import settings
from app.core.logging import logger
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import create_async_engine
import redis.asyncio as redis

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend for Marrakech Drive Premium Car Rental",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception occurred: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": "An unexpected error occurred on the server."},
    )

@app.get("/health", tags=["System"])
async def health_check():
    health_status = {"status": "ok", "checks": {}}

    # Check Database
    try:
        engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        health_status["checks"]["database"] = "ok"
        await engine.dispose()
    except Exception as e:
        logger.error(f"Health check failed for database: {str(e)}")
        health_status["checks"]["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check Redis
    try:
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.aclose()
        health_status["checks"]["redis"] = "ok"
    except Exception as e:
        logger.error(f"Health check failed for redis: {str(e)}")
        health_status["checks"]["redis"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    return health_status

app.include_router(vehicles.router, prefix=f"{settings.API_V1_STR}/vehicles", tags=["Vehicles"])
app.include_router(availability.router, prefix=f"{settings.API_V1_STR}/availability", tags=["Availability & Pricing"])
app.include_router(reservations.router, prefix=f"{settings.API_V1_STR}/reservations", tags=["Reservations"])
app.include_router(customers.router, prefix=f"{settings.API_V1_STR}/customers", tags=["Customers"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(company.router, prefix=f"{settings.API_V1_STR}/company", tags=["Company Settings"])
app.include_router(extras.router, prefix=f"{settings.API_V1_STR}/extras", tags=["Extras"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Analytics"])
app.include_router(assistant.router, prefix=f"{settings.API_V1_STR}/assistant", tags=["AI Assistant"])
app.include_router(whatsapp.router, prefix=f"/webhooks/twilio", tags=["WhatsApp Webhook"])
app.include_router(payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["Payments"])
app.include_router(locations.router, prefix=f"{settings.API_V1_STR}/locations", tags=["Locations"])

@app.get("/")
async def root():
    return {"message": "Welcome to Marrakech Drive API", "version": "1.0.0"}
