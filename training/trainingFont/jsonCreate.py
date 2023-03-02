import json

datos = {
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 30,
    "dirección": {
        "calle": "Av. Siempre Viva",
        "número": 123,
        "ciudad": "Springfield"
    },
    "telefonos": [
        {
            "tipo": "casa",
            "número": "555-1234"
        },
        {
            "tipo": "trabajo",
            "número": "555-5678"
        }
    ]
}

datos_con_nombre = {"datos": datos}


datos.update({
    "nombre2": "Pedro",
    "edad2": 40,
})

datos["ciudad2"] = "Madrid"


archivos = {}

archivo_1 = {}
archivo_1.update({
    "Model": "A",
    "Reco": "HOla",
    "Real": "Hola",
})

archivo_2 = {}
archivo_2.update({
    "Model": "B",
    "Reco": "HolA",
    "Real": "HolA",
})

archivos.update({
    "archivo_1": archivo_1,
    "archivo_2": archivo_2,
})

with open("datos.json", "w") as archivo_json:
    json.dump(archivos, archivo_json, indent = 4)