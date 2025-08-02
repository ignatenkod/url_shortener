import geoip2.database
from geoip2.errors import AddressNotFoundError
from ..config import settings

_geoip_reader = None

def get_geoip_reader():
    """Ленивая инициализация GeoIP ридера"""
    global _geoip_reader
    if _geoip_reader is None and settings.geoip_path:
        try:
            _geoip_reader = geoip2.database.Reader(settings.geoip_path)
        except Exception as e:
            print(f"Error loading GeoIP database: {e}")
            _geoip_reader = None
    return _geoip_reader

def get_geoip_data(ip_address: str):
    """
    Получает геоданные по IP адресу
    
    Args:
        ip_address: IP адрес для поиска
        
    Returns:
        geoip2.models.City или None
    """
    reader = get_geoip_reader()
    if not reader:
        return None
    
    try:
        return reader.city(ip_address)
    except AddressNotFoundError:
        return None
