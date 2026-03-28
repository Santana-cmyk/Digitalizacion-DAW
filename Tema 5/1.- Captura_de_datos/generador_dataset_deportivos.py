import csv
import random
import math

# Semilla para reproducibilidad (puedes cambiarla o comentarla)
random.seed(42)

# Modelos deportivos reales con especificaciones base (aprox. reales)
MODELOS = [
    # Marca, Modelo, HP, 0-100 km/h (s), Precio base (€), Año lanzamiento, País
    {"marca": "Ferrari", "modelo": "488 GTB", "hp": 670, "aceleracion": 3.0, "precio": 240000, "lanzamiento": 2015, "pais": "Italia"},
    {"marca": "Ferrari", "modelo": "F8 Tributo", "hp": 720, "aceleracion": 2.9, "precio": 260000, "lanzamiento": 2019, "pais": "Italia"},
    {"marca": "Lamborghini", "modelo": "Huracán EVO", "hp": 640, "aceleracion": 2.9, "precio": 230000, "lanzamiento": 2019, "pais": "Italia"},
    {"marca": "Lamborghini", "modelo": "Aventador S", "hp": 740, "aceleracion": 2.9, "precio": 350000, "lanzamiento": 2017, "pais": "Italia"},
    {"marca": "Porsche", "modelo": "911 GT3 (992)", "hp": 510, "aceleracion": 3.4, "precio": 190000, "lanzamiento": 2021, "pais": "Alemania"},
    {"marca": "Porsche", "modelo": "911 Turbo S (992)", "hp": 650, "aceleracion": 2.7, "precio": 230000, "lanzamiento": 2020, "pais": "Alemania"},
    {"marca": "McLaren", "modelo": "720S", "hp": 720, "aceleracion": 2.9, "precio": 260000, "lanzamiento": 2017, "pais": "Reino Unido"},
    {"marca": "McLaren", "modelo": "570S", "hp": 570, "aceleracion": 3.2, "precio": 190000, "lanzamiento": 2015, "pais": "Reino Unido"},
    {"marca": "Bugatti", "modelo": "Chiron", "hp": 1500, "aceleracion": 2.4, "precio": 2500000, "lanzamiento": 2016, "pais": "Francia"},
    {"marca": "Aston Martin", "modelo": "Vantage", "hp": 510, "aceleracion": 3.6, "precio": 160000, "lanzamiento": 2018, "pais": "Reino Unido"},
    {"marca": "Aston Martin", "modelo": "DBS Superleggera", "hp": 725, "aceleracion": 3.4, "precio": 280000, "lanzamiento": 2018, "pais": "Reino Unido"},
    {"marca": "Chevrolet", "modelo": "Corvette C8 Stingray", "hp": 495, "aceleracion": 3.0, "precio": 90000, "lanzamiento": 2020, "pais": "EE.UU."},
    {"marca": "Chevrolet", "modelo": "Corvette C8 Z06", "hp": 670, "aceleracion": 2.7, "precio": 140000, "lanzamiento": 2023, "pais": "EE.UU."},
    {"marca": "Nissan", "modelo": "GT-R Nismo", "hp": 600, "aceleracion": 2.8, "precio": 190000, "lanzamiento": 2014, "pais": "Japón"},
    {"marca": "BMW", "modelo": "M4 Competition (G82)", "hp": 510, "aceleracion": 3.9, "precio": 100000, "lanzamiento": 2021, "pais": "Alemania"},
    {"marca": "Audi", "modelo": "R8 V10 Performance", "hp": 620, "aceleracion": 3.1, "precio": 210000, "lanzamiento": 2019, "pais": "Alemania"},
]

# Colores típicos de coches deportivos
COLORES = [
    "Rojo", "Amarillo", "Naranja", "Azul", "Negro", "Blanco",
    "Gris", "Verde lima", "Azul eléctrico", "Rojo burdeos", "Gris mate"
]

# Prefijos WMI aproximados por marca para VIN sintético
WMI_POR_MARCA = {
    "Ferrari": "ZFF",
    "Lamborghini": "ZHW",
    "Porsche": "WP0",
    "McLaren": "SBM",
    "Bugatti": "VF9",
    "Aston Martin": "SCF",
    "Chevrolet": "1G1",
    "Nissan": "JN1",
    "BMW": "WBS",
    "Audi": "WUA",
}

# Caracteres válidos para VIN (sin I, O, Q)
VIN_CHARS = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"


def generar_vin(marca: str) -> str:
    """
    Genera un VIN sintético de 17 caracteres.
    Usa un WMI aproximado según la marca y completa con caracteres válidos.
    No calcula el dígito de control real, pero respeta longitud y alfabeto.
    """
    wmi = WMI_POR_MARCA.get(marca, "XXX")
    resto = "".join(random.choice(VIN_CHARS) for _ in range(17 - len(wmi)))
    return (wmi + resto)[:17]


def variar_precio(precio_base: float) -> float:
    """
    Aplica una variación realista al precio (distribución normal).
    Se limita a un rango razonable (±30%).
    """
    factor = random.gauss(1.0, 0.15)
    factor = max(0.7, min(1.3, factor))
    return round(precio_base * factor, -2)  # redondeo a centenas


def variar_aceleracion(acel_base: float) -> float:
    """
    Aplica una ligera variación a la aceleración 0-100 km/h.
    Se mantiene en un rango plausible.
    """
    delta = random.gauss(0.0, 0.12)
    valor = acel_base + delta
    # No menos de 2.0 s y no más de 4.5 s para estos modelos
    valor = max(2.0, min(4.5, valor))
    return round(valor, 2)


def variar_hp(hp_base: int) -> int:
    """
    Pequeña variación en la potencia, simulando unidades distintas o preparación ligera.
    """
    delta = int(round(random.gauss(0.0, 15.0)))
    valor = hp_base + delta
    # No menos del 90% ni más del 115% de la potencia base
    minimo = int(hp_base * 0.9)
    maximo = int(hp_base * 1.15)
    return max(minimo, min(maximo, valor))


def generar_anio(lanzamiento: int) -> int:
    """
    Genera un año de fabricación entre el año de lanzamiento y 2024.
    """
    return random.randint(lanzamiento, 2024)


def generar_color() -> str:
    """
    Devuelve un color típico de coche deportivo.
    """
    return random.choice(COLORES)


def generar_registro() -> dict:
    """
    Genera un registro coherente de coche deportivo.
    """
    base = random.choice(MODELOS)

    marca = base["marca"]
    modelo = base["modelo"]
    hp = variar_hp(base["hp"])
    aceleracion = variar_aceleracion(base["aceleracion"])
    precio = variar_precio(base["precio"])
    anio = generar_anio(base["lanzamiento"])
    color = generar_color()
    pais = base["pais"]
    vin = generar_vin(marca)

    return {
        "Marca": marca,
        "Modelo": modelo,
        "Año": anio,
        "Color": color,
        "Precio_EUR": precio,
        "Potencia_HP": hp,
        "Aceleracion_0_100_s": aceleracion,
        "Pais_fabricacion": pais,
        "VIN": vin,
    }


def generar_dataset_csv(nombre_archivo: str, n_registros: int = 1000):
    """
    Genera un dataset de n_registros coches deportivos y lo guarda en un CSV.
    """
    campos = [
        "Marca",
        "Modelo",
        "Año",
        "Color",
        "Precio_EUR",
        "Potencia_HP",
        "Aceleracion_0_100_s",
        "Pais_fabricacion",
        "VIN",
    ]

    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for _ in range(n_registros):
            registro = generar_registro()
            writer.writerow(registro)


if __name__ == "__main__":
    nombre = "coches_deportivos_realistas_1000.csv"
    generar_dataset_csv(nombre_archivo=nombre, n_registros=1000)
    print(f"Dataset generado y guardado en: {nombre}")
