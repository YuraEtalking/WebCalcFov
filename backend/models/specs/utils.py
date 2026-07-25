from sqlalchemy import CheckConstraint


def positive_checks(table: str, *fields: str) -> tuple[CheckConstraint, ...]:
    return tuple(
        CheckConstraint(
            f'{field} IS NULL OR {field} > 0',
            name=f'ck_{table}_{field}_positive',
        )
        for field in fields
    )
