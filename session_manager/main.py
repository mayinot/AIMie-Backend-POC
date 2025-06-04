from fastapi import FastAPI
from session_manager.router import router
from session_manager.config import PORT


app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("session_manager.main:app", host="0.0.0.0", port=PORT, reload=True)
