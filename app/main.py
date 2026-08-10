from fastapi import FastAPI

from app.controllers import sms

app = FastAPI(
    title="Learnwise API",
    version="0.1.0",
)

app.include_router(sms.router)

@app.get("/admin/conversations", tags=["admin"])
async def conversations(phoneNumber: str) -> list[dict]:
    """Retrieve a list of all conversations of the phone number provided."""
    # @TODO: Implement SMS receiving logic here
    return [{"status": "@TODO"}]
