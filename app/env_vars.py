from dotenv import load_dotenv
import os
from os.path import join, dirname

enviornment = os.environ.get("APP_ENV")
if enviornment not in ["production", "development", "test"]:
    raise RuntimeError(f"Invalid app enviornment {enviornment} - should be production, development or test.")

dotenv_path = join(dirname(__file__), '..', f'.env.{enviornment}')
loaded = load_dotenv(dotenv_path=dotenv_path, override=True)
ENV_VARS = os.environ

print(f"Loading env variables from {dotenv_path}")
