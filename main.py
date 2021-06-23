# endpoints are updated in the readme
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def root():
    detail = {
        "name": "Symetry API",
        "description" : "Symertry SSO general API",
        "version": "0.0.1",
        "origin" : "Float Business Accelerator",
        "team" : "Monsoon '21 Batch"
        }

    return detail
