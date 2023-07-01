from dotenv import load_dotenv
import os
import logging


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    # change handler name
    handlers=[logging.FileHandler("/tmp/crm_logger.log"), logging.StreamHandler()],
)

LOGGER = logging.getLogger(__name__)

if os.path.isfile(".env"):
    load_dotenv()
else:
    raise Exception("No .env file found")

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
SECRET_JWT = os.environ.get('SECRET_JWT')