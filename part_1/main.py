from fastapi import FastAPI
import uvicorn
from src.routes import contacts, auth

app = FastAPI()

app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello User!!!"}

if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)