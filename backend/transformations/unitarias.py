def eliminar_unitarias(g):
    variables = g["variables"]
    producciones = g["producciones"]

    unit = {A: set() for A in variables}

    # Encontrar pares unitarios
    for A in variables:
        for prod in producciones[A]:
            if len(prod) == 1 and prod[0] in variables:
                unit[A].add(prod[0])

    cambio = True
    while cambio:
        cambio = False
        for A in variables:
            for B in list(unit[A]):
                for C in unit[B]:
                    if C not in unit[A]:
                        unit[A].add(C)
                        cambio = True

    nuevas_producciones = {A: [] for A in variables}

    for A in variables:
        for prod in producciones[A]:
            if not (len(prod) == 1 and prod[0] in variables):
                nuevas_producciones[A].append(prod)

        for B in unit[A]:
            for prod in producciones[B]:
                if not (len(prod) == 1 and prod[0] in variables):
                    nuevas_producciones[A].append(prod)

    return {
        "variables": variables,
        "terminales": g["terminales"],
        "inicial": g["inicial"],
        "producciones": nuevas_producciones,
    }
