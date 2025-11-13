#!/bin/bash
cd inua360_the_kenyan_sme_ai_agent
uvicorn inua360_the_kenyan_sme_ai_agent.modeling.predictions_api:app --host 0.0.0.0 --port $PORT
