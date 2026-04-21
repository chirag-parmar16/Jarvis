import json
import sys
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv, set_key

def get_base_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent.parent

BASE_DIR    = get_base_dir()
CONFIG_DIR  = BASE_DIR / "config"
CONFIG_FILE = CONFIG_DIR / "api_keys.json"
DOTENV_PATH = BASE_DIR / ".env"

# Load environment variables from .env file
load_dotenv(DOTENV_PATH)

def ensure_config_dir() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def config_exists() -> bool:
    """Check if the system is configured (either .env or legacy JSON exists)."""
    return is_configured() or CONFIG_FILE.exists()

def save_api_keys(gemini_api_key: str) -> None:
    """Save Gemini API key to .env and remove from legacy JSON."""
    ensure_config_dir()
    
    # Save to .env
    set_key(str(DOTENV_PATH), "GEMINI_API_KEY", gemini_api_key.strip())
    
    # Reload environment
    load_dotenv(DOTENV_PATH)

    # Clean up from legacy api_keys.json
    _cleanup_legacy_json("gemini_api_key")

def save_os_system(os_system: str) -> None:
    """Save OS system preference to .env."""
    ensure_config_dir()
    set_key(str(DOTENV_PATH), "OS_SYSTEM", os_system.strip().lower())
    load_dotenv(DOTENV_PATH)
    _cleanup_legacy_json("os_system")

def _cleanup_legacy_json(key: str) -> None:
    """Remove a specific key from api_keys.json if it exists."""
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            if key in data:
                del data[key]
                if not data:
                    CONFIG_FILE.unlink()
                else:
                    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass

def get_config_value(key: str, default=None):
    """Get a value from legacy config or environment."""
    # 1. Check environment
    env_val = os.getenv(key.upper())
    if env_val:
        return env_val
        
    # 2. Check legacy JSON
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            return data.get(key, default)
        except Exception:
            pass
    return default

def save_config_value(key: str, value) -> None:
    """Save a value to legacy config (non-secret)."""
    ensure_config_dir()
    data = {}
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    data[key] = value
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def get_gemini_key() -> str | None:
    """Centralized getter for Gemini API Key."""
    # 1. Check environment variable (highest priority)
    env_key = os.getenv("GEMINI_API_KEY")
    if env_key:
        return env_key.strip()
    
    # 2. Check legacy config file (fallback during migration)
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            key = data.get("gemini_api_key")
            if key:
                # Migrate to .env automatically
                save_api_keys(key)
                return key.strip()
        except Exception:
            pass
    
    return None

def get_os_system() -> str:
    """Centralized getter for OS system preference."""
    # 1. Check environment variable
    env_os = os.getenv("OS_SYSTEM")
    if env_os:
        return env_os.strip().lower()
    
    # 2. Check legacy config
    if CONFIG_FILE.exists():
        try:
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            os_name = data.get("os_system")
            if os_name:
                save_os_system(os_name)
                return os_name.strip().lower()
        except Exception:
            pass
            
    return "windows" # Default

def is_configured() -> bool:
    """Determine if the core configuration is complete."""
    key = get_gemini_key()
    return bool(key and len(key) > 5)