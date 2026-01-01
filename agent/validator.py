# agent/validator.py

def validate_params(args, required):
    missing = [r for r in required if r not in args or not args[r]]
    if missing:
        return False, f"Missing parameters: {missing}"
    return True, None


def validate_result(result):
    if result is None:
        return False
    if isinstance(result, dict) and result.get("error"):
        return False
    if hasattr(result, "empty") and result.empty:
        return False
    return True
