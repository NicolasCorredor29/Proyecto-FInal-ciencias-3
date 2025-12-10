"use client";

import { useState } from "react";

export default function FormularioGramatica() {
  const [variables, setVariables] = useState<string[]>(["S"]);
  const [terminales, setTerminales] = useState<string[]>([]);
  const [producciones, setProducciones] = useState<Record<string, string>>({
    S: "",
  });
  const [resultado, setResultado] = useState<any>(null);

  const agregarVariable = () => {
    const nueva = prompt("Ingrese nueva variable:");
    if (!nueva) return;
    if (variables.includes(nueva)) {
      alert("La variable ya existe");
      return;
    }
    setVariables([...variables, nueva]);
    setProducciones((prev) => ({ ...prev, [nueva]: "" }));
  };

  const agregarTerminal = () => {
    const nueva = prompt("Ingrese nuevo terminal:");
    if (!nueva) return;
    if (terminales.includes(nueva)) {
      alert("El terminal ya existe");
      return;
    }
    setTerminales([...terminales, nueva]);
  };

  const actualizarProduccion = (variable: string, valor: string) => {
    setProducciones((prev) => ({
      ...prev,
      [variable]: valor,
    }));
  };

  const formatearProducciones = (prods: Record<string, string[][]>) => {
    return Object.entries(prods)
      .map(([variable, alternativas]) => {
        const ladoDerecho = alternativas
          .map((prod) => prod.join("")) // ["A","B"] → "AB"
          .join(" | ");
        return `${variable} → ${ladoDerecho}`;
      })
      .join("\n");
  };

  const enviarOperacion = async (tipo: string) => {
    const json = {
      variables,
      terminales,
      inicial: "S",
      producciones,
      operacion: tipo,
    };

    try {
      const res = await fetch(
        "https://proyecto-final-ciencias-3.onrender.com/api/procesar-gramatica",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(json),
        }
      );

      const data = await res.json();
      console.log("Respuesta del backend:", data);

      setResultado(data);
    } catch (error) {
      console.error("Error al enviar:", error);
      alert("Error al conectar con el backend");
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4 border rounded-md shadow mt-6">
      <h1 className="text-xl font-bold mb-4 text-center">Proyecto Final</h1>

      <div className="mb-4">
        <h2 className="font-semibold mb-1">Variables:</h2>
        <p>{variables.join(", ")}</p>

        <button
          onClick={agregarVariable}
          className="bg-blue-500 text-white px-3 py-1 rounded mt-2"
        >
          Agregar variable
        </button>
      </div>

      <div className="mb-4">
        <h2 className="font-semibold mb-1">Terminales:</h2>
        <p>{terminales.length ? terminales.join(", ") : "(ninguno)"}</p>

        <button
          onClick={agregarTerminal}
          className="bg-blue-500 text-white px-3 py-1 rounded mt-2"
        >
          Agregar terminal
        </button>
      </div>
      <div>
        <h2 className="font-semibold mb-2">Producciones:</h2>

        {variables.map((v) => (
          <div key={v} className="mb-3">
            <label className="block font-medium mb-1">{v} →</label>
            <input
              type="text"
              value={producciones[v]}
              onChange={(e) => actualizarProduccion(v, e.target.value)}
              placeholder="Ej: AB|a"
              className="w-full border px-2 py-1 rounded"
            />
          </div>
        ))}
      </div>

      <div className="space-y-3 mt-6">
        <button
          onClick={() => enviarOperacion("inutiles")}
          className="w-full bg-blue-500 text-white px-3 py-2 rounded"
        >
          1. Eliminar variables no terminales
        </button>

        <button
          onClick={() => enviarOperacion("no-alcanzables")}
          className="w-full bg-blue-500 text-white px-3 py-2 rounded"
        >
          2. Eliminar de variables no alcanzables
        </button>

        <button
          onClick={() => enviarOperacion("lambda")}
          className="w-full bg-blue-500 text-white px-3 py-2 rounded"
        >
          3. Eliminar producciones λ
        </button>

        <button
          onClick={() => enviarOperacion("unitarias")}
          className="w-full bg-blue-500 text-white px-3 py-2 rounded"
        >
          4. Eliminar producciones unitarias
        </button>
        <button
          onClick={() => enviarOperacion("todas")}
          className="bg-blue-500 text-white px-3 py-2 rounded w-full mt-2"
        >
          Aplicar todas
        </button>
      </div>
      {resultado && (
        <div className="mt-6 p-4 border rounded bg-gray-100">
          <h2 className="font-semibold mb-2">Resultado:</h2>
          <pre className="whitespace-pre-wrap text-sm">
            {formatearProducciones(resultado.producciones)}
          </pre>
        </div>
      )}
    </div>
  );
}
