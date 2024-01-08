from fastapi import FastAPI
from uvicorn import Config, Server
from app.infrastructure.line_api_connector import router as api_router


app = FastAPI()
app.include_router(api_router)

config = Config(app, host="0.0.0.0", port=8000, log_level="info")
server = Server(config)
server.run()
