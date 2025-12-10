def eliminar_inutiles(g):
    variables = g["variables"]
    terminales = g["terminales"]
    producciones = g["producciones"]

    generativas = set()
    cambio = True

    # 1. Encontrar generativas
    while cambio:
        cambio = False
        for A in variables:
            for prod in producciones[A]:
                if all(x in terminales or x in generativas for x in prod):
                    if A not in generativas:
                        generativas.add(A)
                        cambio = True

    # 2. Filtrar
    nuevas_vars = [v for v in variables if v in generativas]
    nuevas_producciones = {
        v: [p for p in producciones[v] if all(x in terminales or x in generativas for x in p)]
        for v in nuevas_vars
    }

    return {
        "variables": nuevas_vars,
        "terminales": terminales,
        "inicial": g["inicial"],
        "producciones": nuevas_producciones,
    }
