"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/lib/api";
import { Pedido, Producto, CategoriaProducto } from "@/lib/types";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";

const categoriaLabel: Record<CategoriaProducto, string> = {
    bebidas: "Bebidas",
    comidas: "Comidas",
    postres: "Postres",
    otros: "Otros",
};

export default function PedidoPage() {
    const { id } = useParams();
    const router = useRouter();
    const [pedido, setPedido] = useState<Pedido | null>(null);
    const [productos, setProductos] = useState<Producto[]>([]);
    const [loading, setLoading] = useState(true);

    const cargarDatos = async () => {
        try {
            const [pedidosRes, productosRes] = await Promise.all([
                api.get(`/pedidos/mesa/${id}`),
                api.get("/productos/?solo_disponibles=true"),
            ]);
            setPedido(pedidosRes.data);
            setProductos(productosRes.data);
        } catch {
            router.push("/mesas");
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        cargarDatos();
    }, [id]);

    const agregarItem = async (producto_id: number) => {
        if (!pedido) return;
        try {
            const res = await api.post(`/pedidos/${pedido.id}/items`, {
                producto_id,
                cantidad: 1,
            });
            setPedido(res.data);
        } catch (e) {
            console.error("Error agregando item:", e);
        }
    }

    const quitarItem = async (item_id: number) => {
        if (!pedido) return;
        const res = await api.delete(`/pedidos/${pedido.id}/items/${item_id}`);
        setPedido(res.data);
    };

    const total = pedido?.items.reduce(
        (acc, item) => acc + item.precio_unitario * item.cantidad,
        0
    ) ?? 0;

    const productosPorCategoria = (Object.keys(categoriaLabel) as CategoriaProducto[]).map(
        (cat) => ({
            categoria: cat,
            label: categoriaLabel[cat],
            items: productos.filter((p) => p.categoria === cat),
        })
    ).filter((g) => g.items.length > 0);

    if (loading) return (
        <div className="p-8 text-muted-foreground"> Cargando pedido...</div>
    );

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <div className="border-b px-8 py-4 flex items-center justify-between">
                <div className="flex items-center gap-4">
                    <button
                        onClick={() => router.push("/mesas")}
                        className="text-muted-foreground hover:text-foreground transition-colors text-sm"
                    >
                        ← Mesas
                    </button>
                    <Separator orientation="vertical" className="h-5" />
                    <h1 className="font-medium">Mesa {id}</h1>
                </div>
                <Button
                    onClick={() => router.push(`/mesas/${id}/cobro`)}
                    disabled={!pedido?.items.length}
                >
                    Cobrar · S/ {total.toFixed(2)}
                </Button>
            </div>

            <div className="grid grid-cols-2 h-[calc(100vh-65px)]">
                {/* Pedido actual */}
                <div className="border-r flex flex-col">
                    <div className="px-6 py-4 border-b">
                        <h2 className="text-sm font-medium text-muted-foreground uppercase tracking-wide">
                            Pedido actual
                        </h2>
                    </div>
                    <ScrollArea className="flex-1">
                        <div className="px-6 py-4">
                            {!pedido?.items.length ? (
                                <p className="text-muted-foreground text-sm mt-4">
                                    Sin items — agrega desde la carta
                                </p>
                            ) : (
                                <div className="flex flex-col gap-2">
                                    {pedido.items.map((item) => (
                                        <div
                                            key={item.id}
                                            className="flex items-center justify-between py-2"
                                        >
                                            <div className="flex flex-col">
                                                <span className="text-sm font-medium">{item.nombre}</span>
                                                <span className="text-xs text-muted-foreground">
                                                    S/ {item.precio_unitario.toFixed(2)} c/u
                                                    {item.es_compartido && " · compartido"}
                                                </span>
                                            </div>
                                            <div className="flex items-center gap-3">
                                                <span className="text-sm font-medium">
                                                    S/ {(item.precio_unitario * item.cantidad).toFixed(2)}
                                                </span>
                                                <button
                                                    onClick={() => quitarItem(item.id)}
                                                    className="text-muted-foreground hover:text-red-500 transition-colors text-lg leading-none"
                                                >
                                                    ×
                                                </button>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </ScrollArea>

                    {/* Total */}
                    {!!pedido?.items.length && (
                        <div className="border-t px-6 py-4">
                            <div className="flex justify-between items-center">
                                <span className="text-sm text-muted-foreground">Total</span>
                                <span className="text-xl font-medium">S/ {total.toFixed(2)}</span>
                            </div>
                        </div>
                    )}
                </div>

                {/* Carta */}
                <ScrollArea className="h-full">
                    <div className="px-6 py-4 flex flex-col gap-6">
                        {productosPorCategoria.map(({ categoria, label, items }) => (
                            <div key={categoria}>
                                <h3 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">
                                    {label}
                                </h3>
                                <div className="grid grid-cols-2 gap-2">
                                    {items.map((producto) => (
                                        <Card
                                            key={producto.id}
                                            onClick={() => agregarItem(producto.id)}
                                            className="p-4 cursor-pointer hover:border-foreground/30 transition-colors"
                                        >
                                            <p className="text-sm font-medium">{producto.nombre}</p>
                                            <p className="text-sm text-muted-foreground mt-1">
                                                S/ {producto.precio.toFixed(2)}
                                            </p>
                                        </Card>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </ScrollArea>
            </div>
        </div>
    );
}
