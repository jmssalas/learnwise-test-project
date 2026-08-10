from fastapi import FastAPI

app = FastAPI(
    title="Learnwise API",
    version="0.1.0",
)


@app.post("/sms", tags=["sms"])
async def sms() -> dict[str, str]:
    """Receive incoming SMS messages from the SMS Provider."""
    # @TODO: Implement SMS receiving logic here
    return {"status": "@TODO"}


@app.post("/feedback", tags=["sms"])
async def feedback() -> dict[str, str]:
    """Receive feedback of the most recent conversation."""
    # @TODO: Implement SMS receiving logic here
    return {"status": "@TODO"}


@app.get("/admin/conversations", tags=["admin"])
async def conversations(phoneNumber: str) -> list[dict]:
    """Retrieve a list of all conversations of the phone number provided."""
    # @TODO: Implement SMS receiving logic here
    return [{"status": "@TODO"}]
