def read_kl(filename: str) -> dict | None:
    try:
        with open(filename, "+r") as file:
            pass
        return {}
    except Exception:
        return None