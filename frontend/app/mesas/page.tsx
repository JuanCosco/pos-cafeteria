"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Mesa } from "@/lib/types";

const estadoColor: Record<string, string> = {
    libre: "bg-green-100 text-green-800 border-green-300",
    ocupada: "bg-amber-100 text-amber-800 border-amber-300",
    pidio_cuenta: "bg-red-100 text-red-800 border-red-300",
}

const estadoLabel: Record<string, string> = {
    libre: "Libre",
    ocupada: "Ocupada",
    pidio_cuenta: "Pidió cuenta",
}

export default function MesasPage() {
    const [mesas, setMesas] = useState<Mesa[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        api
            .get("/mesas/")
            .then((res) => setMesas(res.data))
            .catch(() => setError("No se pudo conectar con la API"))
            .finally(() => setLoading(false));
    }, []);

    if (loading) return <p className="p-8 text-muted-foreground">Cargando mesas...</p>;
    if (error) return <p className="p-8 text-red-500">{error}</p>;

    return (
        <div className="p-8">
            <h1 className="text-2xl font-medium mb-6">Mesas</h1>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                {mesas.map((mesa) => (
                    <div
                        key={mesa.id}
                        className={`border rounded-xl p-6 flex flex-col gap-2 cursor-pointer hover:shadow-md transition-shadow ${estadoColor[mesa.estado]}`}
                    >
                        <span className="text-lg font-medium">Mesa {mesa.numero}</span>
                        <span className="text-sm">{estadoLabel[mesa.estado]}</span>
                    </div>
                ))}
            </div>
        </div>
    );

}