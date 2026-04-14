"""langsmith_config.py — LangSmith observability setup"""
import os
from dotenv import load_dotenv

load_dotenv()

def setup_langsmith(project_name: str):
    os.environ.setdefault("LANGCHAIN_TRACING_V2", "true")
    os.environ.setdefault("LANGCHAIN_PROJECT", project_name)
    api_key = os.getenv("LANGCHAIN_API_KEY", "")
    if not api_key:
        print("Warning: LANGCHAIN_API_KEY not set — tracing disabled")
