# config/__init__.py
import memory.config_manager as config_manager

def get_config() -> dict:
    """Legacy compatibility function. Try to use config_manager directly."""
    return {
        "os_system": config_manager.get_os_system(),
        "gemini_api_key": config_manager.get_gemini_key(),
        "camera_index": config_manager.get_config_value("camera_index", 0)
    }

def get_os() -> str:
    """Returns: 'windows' | 'mac' | 'linux'"""
    return config_manager.get_os_system().lower()

def is_windows() -> bool: return get_os() == "windows"
def is_mac()     -> bool: return get_os() == "mac"
def is_linux()   -> bool: return get_os() == "linux"