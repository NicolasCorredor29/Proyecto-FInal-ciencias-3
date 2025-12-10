def eliminar_lambda(g):
    variables = g["variables"]
    producciones = g["producciones"]

    # Encontrar anulables
    anulables = set()
    cambio = True

    while cambio:
        cambio = False
        for A in variables:
            for prod in producciones[A]:
                # λ puede venir como "0" o como "ε"
                if prod == ["0"] or prod == ["ε"] or all(x in anulables for x in prod):
                    if A not in anulables:
                        anulables.add(A)
                        cambio = True

    nuevas_producciones = {A: [] for A in variables}

    # Generar nuevas reglas sin λ
    for A in variables:
        for prod in producciones[A]:
            # Saltar λ explícito
            if prod == ["0"] or prod == ["ε"]:
                continue

            nuevas_producciones[A].append(prod)

            # Subconjuntos removiendo anulables
            for i in range(len(prod)):
                if prod[i] in anulables:
                    nueva = prod[:i] + prod[i+1:]
                    if nueva and nueva not in nuevas_producciones[A]:
                        nuevas_producciones[A].append(nueva)

    # Si el inicial era anulable → agregar lambda como "0"
    if g["inicial"] in anulables:
        nuevas_producciones[g["inicial"]].append(["0"])

    return {
        "variables": variables,
        "terminales": g["terminales"],
        "inicial": g["inicial"],
        "producciones": nuevas_producciones,
    }
