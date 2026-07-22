"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { Mesa } from "@/lib/types";
import { Badge } from "@/components/ui/badge";

const estadoConfig: Record<string, { label: string, badge: string, card: string }> = {
    libre: {
        label: "Libre",
        badge: "bg-green-100 text-green-800 border-green-300",
        card: "border-green-200 hover:border-green-400 hover:shadow-green-100",
    },
    ocupada: {
        label: "Ocupada",
        badge: "bg-amber-100 text-amber-800 border-amber-300",
        card: "border-amber-200 hover:border-amber-400 hover:shadow-amber-100",
    },
    pidio_cuenta: {
        label: "Pidió cuenta",
        badge: "bg-red-100 text-red-800 border-red-300",
        card: "border-red-200 hover:border-red-400 hover:shadow-red-100",
    },
};

export default function MesasPage() {
    const router = useRouter();
    const [mesas, setMesas] = useState<Mesa[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const cargarMesas = () => {
        api
            .get("/mesas/")
            .then((res) => setMesas(res.data))
            .catch(() => setError("No se pudo conectar con la API"))
            .finally(() => setLoading(false));
    };

    useEffect(() => {
        cargarMesas();
        const interval = setInterval(cargarMesas, 15000);
        return () => clearInterval(interval);
    }, []);

    const handleMesa = async (mesa: Mesa) => {
        if (mesa.estado === "libre") {
            await api.post("/pedidos/", { mesa_id: mesa.id });
        }
        router.push(`/mesas/${mesa.id}/pedido`);
    };

    const mesasOrdenadas = [...mesas].sort((a, b) => a.numero - b.numero);

    if (loading) return (
        <div className="p-8 text-muted-foreground">Cargando mesas...</div>
    );

    if (error) return (
        <div className="p-8 text-red-500">{error}</div>
    );
    return (
        <div className="min-h-screen bg-background p-8">
            <div className="max-w-4xl mx-auto">
                <div className="flex items-center justify-between mb-8">
                    <h1 className="text-2xl font-medium">Mesas</h1>
                    <span className="text-sm text-muted-foreground">
                        {mesas.filter((m) => m.estado === "libre").length} libres ·{" "}
                        {mesas.filter((m) => m.estado === "ocupada").length} ocupadas
                    </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
                    {mesasOrdenadas.map((mesa) => {
                        const config = estadoConfig[mesa.estado];
                        return (
                            <button
                                key={mesa.id}
                                onClick={() => handleMesa(mesa)}
                                className={`border-2 rounded-xl p-6 flex flex-col gap-3 text-left transition-all hover:shadow-md cursor-pointer bg-background ${config.card}`}
                            >
                                <span className="text-xl font-medium">Mesa {mesa.numero}</span>
                                <Badge className={`w-fit text-xs font-normal border ${config.badge}`}>
                                    {config.label}
                                </Badge>
                            </button>
                        );
                    })}
                </div>
            </div>
        </div>
    );

}