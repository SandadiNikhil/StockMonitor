"""Module for loading and providing configuration settings."""

from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='env/key.env')  # load .env here 

API_KEY = os.environ.get("apikey")
BASE_URL = os.environ.get("base_url")

def get_api_key():
    """Returns the Financial Modeling Prep API key from environment variables."""
    return os.environ.get("apikey")

def get_base_url():
    """Returns the base URL for the Financial Modeling Prep API from environment variables."""
    return os.environ.get("base_url")
