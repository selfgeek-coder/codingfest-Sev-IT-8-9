import trimesh
from config import Settings

class CalcService:

    @staticmethod
    def calc_price(file_path: str, material: str, speed: float):
        """
        Возвращает словарь:
        {
            "volume_cm3": ...,
            "weight_g": ...,
            "print_time_h": ...,
            "price_rub": ...
        }
        """

        if material not in Settings.materials:
            raise ValueError("Unknown material")

        # --- Загружаем STL ---
        mesh = trimesh.load(file_path, force='mesh')

        mesh.remove_infinite_values()
        mesh.merge_vertices()
        mesh.process(validate=True)

        if not mesh.is_watertight:
            mesh = mesh.fill_holes()

        mesh.process(validate=True)

        volume_mm3 = mesh.volume
        volume_cm3 = volume_mm3 / 1000

        density = Settings.materials[material]["density"]  # г/см³
        weight_g = volume_cm3 * density

        # speed = скорость печати в см3/час или аналог (твоя же логика)
        time_h = volume_cm3 / speed

        price_per_kg = Settings.materials[material]["price"]
        material_cost = (weight_g / 1000) * price_per_kg

        hour_rate = Settings.hour_rate        # ₽/ч
        time_cost = time_h * hour_rate

        electricity = getattr(Settings, "electricity_rub_h", 0)
        electricity_cost = time_h * electricity

        total_price = material_cost + time_cost + electricity_cost

        min_price = Settings.min_price
        total_price = max(total_price, min_price)

        return {
            "volume_cm3": round(volume_cm3, 2),
            "weight_g": round(weight_g, 2),
            "print_time_h": round(time_h, 2),
            "price_rub": round(total_price, 2)
        }
