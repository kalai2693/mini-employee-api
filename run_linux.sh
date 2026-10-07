#!/usr/bin/env bash
source .venv/bin/activate
uvicorn employee_api.main:app --reload
