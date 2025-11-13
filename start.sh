#!/bin/bash
uvicorn inua360_the_kenyan_sme_ai_agent.prediction.predictions_api:app --host 0.0.0.0 --port ${PORT:-8000}
