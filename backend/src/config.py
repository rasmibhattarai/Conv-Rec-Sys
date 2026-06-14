import os
import logging
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from openai import AsyncOpenAI

# Set up logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

model_name = os.getenv("OPENAI_MODEL", "qwen-3.5-397b")
base_url = os.getenv("OPENAI_BASE_URL")
api_key = os.getenv("OPENAI_API_KEY")

# Provider for the main agent
provider = OpenAIProvider(base_url=base_url, api_key=api_key)
model = OpenAIChatModel(model_name, provider=provider)

# Standard AsyncOpenAI client for the SQL Sub-Agent
oai_client = AsyncOpenAI(
    api_key=api_key, base_url=base_url.rstrip("/") if base_url else None
)
