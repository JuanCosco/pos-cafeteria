"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/lib/api";
import { Pedido, DivisionGrupos } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Card } from "@/components/ui/card";

export default function CobroPage() {
    const { id } = useParams();
    const router = useRouter();
    const [pedido, setPedido] = useState<Pedido | null>(null);
    const [loading, setLoading] = useState(true);

    //Estado para division de grupos
    const [numGrupos, setNumGrupos] = useState(2);
    const [nombresGrupos, setNombresGrupos] = useState<string[]>(["Grupo 1", "Grupo 2"]);
    const [gruposCreados, setGruposCreados] = useState<{ id: number; nombre: string }[]>([]);
    const [division, setDivision] = useState<DivisionGrupos | null>(null);
    const [itemSeleccionado, setItemSeleccionado] = useState<number | null>(null);

    useEffect(() => {
        api.get(`/pedidos/mesa/${id}`)
            .then((res) => setPedido(res.data))
            .catch(() => router.push("/mesas"))
            .finally(() => setLoading(false))
    }, [id]);

    const total = pedido?.items.reduce(
        (acc, item) => acc + item.precio_unitario * item.cantidad, 0
    ) ?? 0;

    const cobrarJunto = async () => {
        if (!pedido) return;
        await api.patch(`/pedidos/${pedido.id}/cerrar`);
        router.push("/mesas");
    };

    const dividirMitad = (n: number) => {
        return (total / n).toFixed(2);
    };

    const crearGrupos = async () => {
        if (!pedido) return;
        const res = await api.post(`/pedidos/${pedido.id}/grupos`, nombresGrupos);
        setGruposCreados(res.data);
        setDivision(null);
    };

    const asignarItem = async (item_id: number, grupo_pago_id: number) => {
        if (!pedido) return;
        await api.patch(`/pedidos/${pedido.id}/items/${item_id}/asignar`, null, {
            params: { grupo_pago_id },
        });
        setItemSeleccionado(null);

        if (division) calcularDivision();
    };

    const calcularDivision = async () => {
        if (!pedido) return;
        const res = await api.get(`/pedidos/${pedido.id}/grupos/dividir`);
        setDivision(res.data);
    };

    const cobrarGrupos = async () => {
        if (!pedido) return;
        await api.patch(`/pedidos/${pedido.id}/cerrar`);
        router.push("/mesas");
    };

    const actualizarNombres = (n: number) => {
        setNumGrupos(n);
        setNombresGrupos(
            Array.from({ length: n }, (_, i) => nombresGrupos[i] || `Grupo ${i + 1}`)
        );
        setGruposCreados([]);
        setDivision(null);
    };

    if (loading) return <div className="p-8 text-muted-foreground">Cargando...</div>;

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <div className="border-b px-8 py-4 flex items-center gap-4">
                <button
                    onClick={() => router.push(`/mesas/${id}/pedido`)}
                    className="text-muted-foreground hover:text-foreground transition-colors text-sm"
                >
                    ← Pedido
                </button>
                <Separator orientation="vertical" className="h-5" />
                <h1 className="font-medium">Cobro · Mesa {id}</h1>
            </div>

            <div className="max-w-3xl mx-auto px-8 py-8">
                {/* Resumen del pedido */}
                <Card className="p-6 mb-8">
                    <h2 className="text-sm font-medium text-muted-foreground uppercase tracking-wide mb-4">
                        Resumen
                    </h2>
                    <div className="flex flex-col gap-2">
                        {pedido?.items.map((item) => (
                            <div key={item.id} className="flex justify-between text-sm">
                                <span>{item.nombre} × {item.cantidad}</span>
                                <span>S/ {(item.precio_unitario * item.cantidad).toFixed(2)}</span>
                            </div>
                        ))}
                    </div>
                    <Separator className="my-4" />
                    <div className="flex justify-between font-medium">
                        <span>Total</span>
                        <span>S/ {total.toFixed(2)}</span>
                    </div>
                </Card>

                {/* Tabs de modalidad de cobro */}
                <Tabs defaultValue="junto">
                    <TabsList className="w-full mb-6">
                        <TabsTrigger value="junto" className="flex-1">Cuenta única</TabsTrigger>
                        <TabsTrigger value="mitad" className="flex-1">Dividir partes iguales</TabsTrigger>
                        <TabsTrigger value="grupos" className="flex-1">Por grupos</TabsTrigger>
                    </TabsList>

                    {/* Tab 1 — Cuenta única */}
                    <TabsContent value="junto">
                        <Card className="p-6 flex flex-col gap-4">
                            <p className="text-sm text-muted-foreground">
                                El cliente paga todo junto.
                            </p>
                            <div className="flex justify-between items-center">
                                <span className="text-2xl font-medium">S/ {total.toFixed(2)}</span>
                                <Button onClick={cobrarJunto}>Cobrar y cerrar mesa</Button>
                            </div>
                        </Card>
                    </TabsContent>

                    {/* Tab 2 — Dividir en partes iguales */}
                    <TabsContent value="mitad">
                        <Card className="p-6 flex flex-col gap-6">
                            <p className="text-sm text-muted-foreground">
                                Divide el total en partes iguales sin asignar platos.
                            </p>
                            <div className="flex items-center gap-4">
                                <span className="text-sm">¿Entre cuántos?</span>
                                <div className="flex items-center gap-2">
                                    <button
                                        onClick={() => setNumGrupos(Math.max(2, numGrupos - 1))}
                                        className="w-8 h-8 rounded-full border flex items-center justify-center hover:bg-muted"
                                    >
                                        −
                                    </button>
                                    <span className="w-8 text-center font-medium">{numGrupos}</span>
                                    <button
                                        onClick={() => setNumGrupos(numGrupos + 1)}
                                        className="w-8 h-8 rounded-full border flex items-center justify-center hover:bg-muted"
                                    >
                                        +
                                    </button>
                                </div>
                            </div>
                            <div className="flex flex-col gap-2">
                                {Array.from({ length: numGrupos }).map((_, i) => (
                                    <div key={i} className="flex justify-between text-sm py-2 border-b last:border-0">
                                        <span className="text-muted-foreground">Persona {i + 1}</span>
                                        <span className="font-medium">S/ {dividirMitad(numGrupos)}</span>
                                    </div>
                                ))}
                            </div>
                            <Button onClick={cobrarJunto} className="w-full">
                                Cobrar y cerrar mesa
                            </Button>
                        </Card>
                    </TabsContent>

                    {/* Tab 3 — Por grupos */}
                    <TabsContent value="grupos">
                        <Card className="p-6 flex flex-col gap-6">
                            {/* Paso 1 — definir grupos */}
                            {!gruposCreados.length && (
                                <>
                                    <p className="text-sm text-muted-foreground">
                                        Define los grupos y luego asigna cada plato.
                                    </p>
                                    <div className="flex items-center gap-4">
                                        <span className="text-sm">¿Cuántos grupos?</span>
                                        <div className="flex items-center gap-2">
                                            <button
                                                onClick={() => actualizarNombres(Math.max(2, numGrupos - 1))}
                                                className="w-8 h-8 rounded-full border flex items-center justify-center hover:bg-muted"
                                            >
                                                −
                                            </button>
                                            <span className="w-8 text-center font-medium">{numGrupos}</span>
                                            <button
                                                onClick={() => actualizarNombres(numGrupos + 1)}
                                                className="w-8 h-8 rounded-full border flex items-center justify-center hover:bg-muted"
                                            >
                                                +
                                            </button>
                                        </div>
                                    </div>
                                    <div className="flex flex-col gap-2">
                                        {nombresGrupos.map((nombre, i) => (
                                            <div key={i} className="flex items-center gap-3">
                                                <span className="text-sm text-muted-foreground w-20">Grupo {i + 1}</span>
                                                <input
                                                    value={nombre}
                                                    onChange={(e) => {
                                                        const nuevos = [...nombresGrupos];
                                                        nuevos[i] = e.target.value;
                                                        setNombresGrupos(nuevos);
                                                    }}
                                                    className="border rounded-md px-3 py-1.5 text-sm flex-1 bg-background"
                                                    placeholder={`Grupo ${i + 1}`}
                                                />
                                            </div>
                                        ))}
                                    </div>
                                    <Button onClick={crearGrupos}>Continuar →</Button>
                                </>
                            )}

                            {/* Paso 2 — asignar items */}
                            {gruposCreados.length > 0 && !division && (
                                <>
                                    <p className="text-sm text-muted-foreground">
                                        Toca un plato y luego el grupo al que pertenece.
                                    </p>
                                    <div className="flex flex-col gap-2">
                                        {pedido?.items.map((item) => (
                                            <div
                                                key={item.id}
                                                onClick={() => setItemSeleccionado(item.id === itemSeleccionado ? null : item.id)}
                                                className={`flex justify-between items-center p-3 rounded-lg border cursor-pointer transition-colors ${item.grupo_pago_id
                                                        ? "border-green-300 bg-green-50"
                                                        : itemSeleccionado === item.id
                                                            ? "border-foreground bg-muted"
                                                            : "hover:border-foreground/30"
                                                    }`}
                                            >
                                                <span className="text-sm">{item.nombre} × {item.cantidad}</span>
                                                <span className="text-sm text-muted-foreground">
                                                    {item.grupo_pago_id
                                                        ? gruposCreados.find((g) => g.id === item.grupo_pago_id)?.nombre ?? "Asignado"
                                                        : item.es_compartido ? "Compartido" : "Sin asignar"}
                                                </span>
                                            </div>
                                        ))}
                                    </div>

                                    {itemSeleccionado && (
                                        <div className="flex flex-col gap-2">
                                            <p className="text-xs text-muted-foreground">¿A qué grupo pertenece?</p>
                                            <div className="flex gap-2 flex-wrap">
                                                {gruposCreados.map((grupo) => (
                                                    <Button
                                                        key={grupo.id}
                                                        variant="outline"
                                                        size="sm"
                                                        onClick={() => asignarItem(itemSeleccionado, grupo.id)}
                                                    >
                                                        {grupo.nombre}
                                                    </Button>
                                                ))}
                                            </div>
                                        </div>
                                    )}

                                    <Button onClick={calcularDivision}>Ver división →</Button>
                                </>
                            )}

                            {/* Paso 3 — resultado */}
                            {division && (
                                <>
                                    <div className="flex flex-col gap-4">
                                        {division.grupos.map((grupo) => (
                                            <div key={grupo.grupo_id} className="border rounded-lg p-4">
                                                <div className="flex justify-between items-center mb-3">
                                                    <span className="font-medium">{grupo.nombre}</span>
                                                    <span className="font-medium">S/ {grupo.total_a_pagar.toFixed(2)}</span>
                                                </div>
                                                {grupo.items.map((item, i) => (
                                                    <div key={i} className="flex justify-between text-sm text-muted-foreground">
                                                        <span>{item.nombre} × {item.cantidad}</span>
                                                        <span>S/ {item.subtotal.toFixed(2)}</span>
                                                    </div>
                                                ))}
                                                {grupo.parte_compartida > 0 && (
                                                    <div className="flex justify-between text-sm text-muted-foreground mt-1">
                                                        <span>Compartido</span>
                                                        <span>S/ {grupo.parte_compartida.toFixed(2)}</span>
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                        {division.sin_asignar.length > 0 && (
                                            <p className="text-sm text-amber-600">
                                                ⚠ {division.sin_asignar.length} item(s) sin asignar
                                            </p>
                                        )}
                                    </div>
                                    <div className="flex gap-3">
                                        <Button variant="outline" onClick={() => setDivision(null)} className="flex-1">
                                            ← Ajustar
                                        </Button>
                                        <Button onClick={cobrarGrupos} className="flex-1">
                                            Cobrar y cerrar mesa
                                        </Button>
                                    </div>
                                </>
                            )}
                        </Card>
                    </TabsContent>
                </Tabs>
            </div>
        </div>
    );
}