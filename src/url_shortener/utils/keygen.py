from crc32c import crc32c
from nanoid import generate

def generate_short_key(url: str = None) -> str:
    """
    Генерирует короткий ключ для URL
    
    Args:
        url: Оригинальный URL (опционально)
        
    Returns:
        str: Короткий ключ (6-8 символов)
    """
    if url:
        # Используем CRC32 если передан URL
        checksum = crc32c(url.encode())
        return f"{checksum:08x}"[:8]
    else:
        # Иначе используем nanoid
        return generate(size=6)
