import requests
import time

BASE_URL = "https://pokeapi.co/api/v2/"


# FUNCIONES AUXILIARES
def obtener_pokemon(nombre):
    try:
        res = requests.get(BASE_URL + f"pokemon/{nombre}")
        return res.json()
    except:
        return None

def obtener_lista(endpoint):
    try:
        res = requests.get(BASE_URL + endpoint)
        return res.json()
    except:
        return None


# 🔥 1. TIPOS
# a) Pokémon fuego en Kanto
def fuego_kanto():
    data = obtener_lista("type/fire")
    contador = 0

    for p in data["pokemon"]:
        poke = obtener_pokemon(p["pokemon"]["name"])
        if poke and poke["id"] <= 151:  # Kanto
            contador += 1
        time.sleep(0.1)

    print("🔥 Pokémon tipo fuego en Kanto:", contador)


# b) Pokémon agua con altura > 10
def agua_altos():
    data = obtener_lista("type/water")
    resultado = []

    for p in data["pokemon"]:
        poke = obtener_pokemon(p["pokemon"]["name"])
        if poke and poke["height"] > 10:
            resultado.append(poke["name"])
        time.sleep(0.1)

    print("🌊 Pokémon agua con altura > 10:", resultado)



# ⚡ 2. EVOLUCIONES
# a) Cadena evolutiva (ej: bulbasaur)
def cadena_evolutiva(nombre):
    especie = requests.get(BASE_URL + f"pokemon-species/{nombre}").json()
    evo_url = especie["evolution_chain"]["url"]

    cadena = requests.get(evo_url).json()

    def recorrer(chain):
        print(chain["species"]["name"])
        for evo in chain["evolves_to"]:
            recorrer(evo)

    print("🌱 Cadena evolutiva:")
    recorrer(cadena["chain"])


# b) Eléctricos sin evolución
def electricos_sin_evolucion():
    data = obtener_lista("type/electric")
    resultado = []

    for p in data["pokemon"]:
        especie = requests.get(BASE_URL + f"pokemon-species/{p['pokemon']['name']}").json()

        if not especie["evolves_from_species"] and not especie["evolution_chain"]:
            resultado.append(p["pokemon"]["name"])

        time.sleep(0.1)

    print("⚡ Eléctricos sin evolución:", resultado)



# ⚔️ 3. ESTADÍSTICAS
# a) Mayor ataque en Johto
def mayor_ataque_johto():
    max_ataque = 0
    mejor = ""

    for i in range(152, 252):  # Johto
        poke = obtener_pokemon(i)
        if poke:
            ataque = poke["stats"][1]["base_stat"]
            if ataque > max_ataque:
                max_ataque = ataque
                mejor = poke["name"]

    print("⚔️ Mayor ataque en Johto:", mejor, max_ataque)


# b) Mayor velocidad (no legendario)
def mayor_velocidad():
    max_speed = 0
    mejor = ""

    for i in range(1, 500):
        poke = obtener_pokemon(i)
        if poke:
            speed = poke["stats"][5]["base_stat"]

            if speed > max_speed:
                max_speed = speed
                mejor = poke["name"]

        time.sleep(0.05)

    print("⚡ Mayor velocidad:", mejor, max_speed)



# 🌿 4. EXTRAS
# a) Hábitat más común en planta
def habitat_planta():
    data = obtener_lista("type/grass")
    habitats = {}

    for p in data["pokemon"]:
        especie = requests.get(BASE_URL + f"pokemon-species/{p['pokemon']['name']}").json()
        h = especie["habitat"]

        if h:
            nombre = h["name"]
            habitats[nombre] = habitats.get(nombre, 0) + 1

        time.sleep(0.1)

    print("🌿 Hábitat más común:", max(habitats, key=habitats.get))


# b) Pokémon con menor peso
def menor_peso():
    min_peso = float("inf")
    nombre = ""

    for i in range(1, 500):
        poke = obtener_pokemon(i)
        if poke:
            if poke["weight"] < min_peso:
                min_peso = poke["weight"]
                nombre = poke["name"]

        time.sleep(0.05)

    print("⚖️ Menor peso:", nombre, min_peso)



# EJECUCIÓN
if __name__ == "__main__":
    fuego_kanto()
    agua_altos()
    cadena_evolutiva("bulbasaur")
    mayor_ataque_johto()
    mayor_velocidad()
    habitat_planta()
    menor_peso()