import geoip2.database
from geoip2.errors import AddressNotFoundError
from typing import Optional
from ..config import settings

class GeoIPService:
    """Сервис для работы с GeoIP данными"""
    
    _reader = None

    @classmethod
    def get_reader(cls):
        """Ленивая инициализация GeoIP ридера"""
        if cls._reader is None and hasattr(settings, 'geoip_path'):
            try:
                cls._reader = geoip2.database.Reader(settings.geoip_path)
            except Exception as e:
                print(f"Error loading GeoIP database: {e}")
                cls._reader = None
        return cls._reader

    @classmethod
    def get_country_code(cls, ip_address: str) -> Optional[str]:
        """
        Получает код страны по IP адресу
        
        Args:
            ip_address: IP адрес для проверки
            
        Returns:
            Код страны (2 символа) или None если не удалось определить
        """
        reader = cls.get_reader()
        if not reader:
            return None
        
        try:
            response = reader.city(ip_address)
            return response.country.iso_code
        except AddressNotFoundError:
            return None
        except Exception as e:
            print(f"GeoIP lookup error: {e}")
            return None

    @classmethod
    def close(cls):
        """Закрывает соединение с GeoIP базой"""
        if cls._reader:
            cls._reader.close()
            cls._reader = None
