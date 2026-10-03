from fastapi import FastAPI
from app.api.routes import vehicles, reservations, auth, availability, customers, company, extras, analytics, assistant, whatsapp, payments
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend for Marrakech Drive Premium Car Rental",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
async def root():
    return {"message": "Welcome to Marrakech Drive API", "version": "1.0.0"}
