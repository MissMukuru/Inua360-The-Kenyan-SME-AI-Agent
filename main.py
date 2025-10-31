from fastapi import FastAPI
from inua360_the_kenyan_sme_ai_agent.endpoint import growth

app = FastAPI(title="SME Growth Prediction API")
app.include_router(growth.router)
