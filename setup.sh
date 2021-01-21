#!/bin/sh
source .venv/bin/activate
pip install -r requirements.txt
python3 pipeline.py techstars_source.csv