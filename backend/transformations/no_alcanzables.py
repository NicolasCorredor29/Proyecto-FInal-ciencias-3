def eliminar_no_alcanzables(g):
    variables = g["variables"]
    producciones = g["producciones"]
    inicial = g["inicial"]

    alcanzables = {inicial}
    cambio = True

    while cambio:
        cambio = False
        for A in list(alcanzables):
            for prod in producciones[A]:
                for x in prod:
                    if x in variables and x not in alcanzables:
                        alcanzables.add(x)
                        cambio = True

    nuevas_vars = [v for v in variables if v in alcanzables]
    nuevas_prod = {v: producciones[v] for v in nuevas_vars}

    return {
        "variables": nuevas_vars,
        "terminales": g["terminales"],
        "inicial": inicial,
        "producciones": nuevas_prod,
    }
