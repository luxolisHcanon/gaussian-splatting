#!/bin/sh

# Start Server
conda run -n gaussian-splatting uvicorn main:app --host 0.0.0.0 --port 8080 --log-level debug --reload
