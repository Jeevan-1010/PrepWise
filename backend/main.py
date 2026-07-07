from fastapi import FastAPI

app = FastAPI(
    title="PrepWise API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to PrepWise API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }