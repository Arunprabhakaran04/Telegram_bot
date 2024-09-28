import requests
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("serpAPI_API_TOKEN")
