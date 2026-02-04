# app/config.py
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://self_controlled:liushihao574@59.110.52.22:5432/self_controlled"
)