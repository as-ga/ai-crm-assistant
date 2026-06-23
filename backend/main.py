from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "AI Assistant Server is running. Use the /health endpoint to check the health status."
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}