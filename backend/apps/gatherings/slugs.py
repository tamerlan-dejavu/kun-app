import secrets

# Без похожих символов (0/O, 1/l/I) — ссылку могут продиктовать голосом
ALPHABET = "abcdefghjkmnpqrstuvwxyz23456789"
SLUG_LENGTH = 10


def generate_slug() -> str:
    """Короткий неугадываемый slug для /g/<slug>: 31^10 ≈ 8·10^14 вариантов."""
    return "".join(secrets.choice(ALPHABET) for _ in range(SLUG_LENGTH))
