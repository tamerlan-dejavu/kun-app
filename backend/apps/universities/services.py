"""Значок «Студент»: почта -> письмо с кодом -> значок. Повтор раз в 12 месяцев."""


def request_student_code(user, email: str) -> None:
    raise NotImplementedError


def verify_student_code(user, code: str) -> None:
    raise NotImplementedError
