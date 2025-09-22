import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import api


logger = logging.basicConfig(level=logging.INFO)
app = FastAPI()

app.include_router(api.router, prefix="/rest/api")

#CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://p-l-r-ui-service-562328781960.us-east1.run.app",
                   "https://paramiguel.org",
                   "http://localhost:4200",
                   "https://www.paramiguel.org"
                   ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.get("/")
def read_root():
    return {"Message": "Ok 🪅"}

def run_uvicorn():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3000)

if __name__ == "__main__":
    from watchgod import run_process
    run_process(".", run_uvicorn)