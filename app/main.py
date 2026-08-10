from fastapi import FastAPI

app = FastAPI(
    title="Learnwise API",
    version="0.1.0",
)


@app.get("/", tags=["health"])
async def read_root() -> dict[str, str]:
    """Return a basic service description."""
    return {"message": "Learnwise API"}


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    """Report whether the API is ready to receive requests."""
    return {"status": "ok"}
