class SecureLogger:
    def __init__(self, key=None): pass
    def log(self, msg): print(f"[LOG] {msg}")
def load_vault():
    return {"log_key": None, "ntfy_url": "https://ntfy.sh/keith_04901_vault"}
