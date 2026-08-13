from fastapi import Request


def parse_ids(raw: str | None) -> list[int]:
    if not raw:
        return []

    return [int(x) for x in raw.split(',') if x.isdigit()]


def get_ids(request: Request, key: str) -> list[int]:
    return parse_ids(request.cookies.get(key))