import argparse
import datetime as dt
import sys
from pathlib import Path

from libs.environment import env
from libs.tokens.config import TokenConfig
from libs.tokens.exceptions import TokenSecretError
from libs.tokens.export import issue_export_token

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def _positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("Значение должно быть больше 0")
    return number


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m libs.tokens",
    )
    parser.add_argument(
        "--days",
        type=_positive_int,
        default=30,
        help="срок действия токена в днях (по умолчанию 30)",
    )
    args = parser.parse_args()

    env.load(BASE_DIR / ".env")
    try:
        token = issue_export_token(
            env.get(TokenConfig.SECRET_ENV),
            dt.timedelta(days=args.days),
        )
    except TokenSecretError as e:
        sys.exit(f"Ошибка: {e}")

    print(token)


if __name__ == "__main__":
    main()
