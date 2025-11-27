from stl import mesh
from config import Settings

class CalcService:

    @staticmethod
    def calc_price(file_path: str, material: str, speed: float):
        """
        считает цену за модель,
        возвращает словарь:
        {
            "volume_cm3": ...,
            "weight_g": ...,
            "print_time_h": ...,
            "price_rub": ...
        }
        """

        if material not in Settings.densities:
            raise ValueError("Unknown material")

        m = mesh.Mesh.from_file(file_path)

        # объем модели
        volume_mm3, _, _ = m.get_mass_properties()
        volume_cm3 = volume_mm3 / 1000

        # масса
        density = Settings.densities[material]
        weight_g = volume_cm3 * density

        # время печати
        time_h = volume_cm3 / speed

        # цена
        price_rub = (weight_g / 1000) * Settings.prices[material]

        return {
            "volume_cm3": round(volume_cm3, 2),
            "weight_g": round(weight_g, 2),
            "print_time_h": round(time_h, 2),
            "price_rub": round(price_rub, 2)
        }
