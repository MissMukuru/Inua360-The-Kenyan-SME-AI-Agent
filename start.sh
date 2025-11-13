#!/bin/bash
cd inua360_the_kenyan_sme_ai_agent
uvicorn app:app --host 0.0.0.0 --port $PORT
