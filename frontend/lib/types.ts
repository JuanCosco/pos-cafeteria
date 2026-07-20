export type EstadoMesa = "libre" | "ocupada" | "pidio_cuenta";
export type EstadoPedido = "abierto" | "cerrado";
export type CategoriaProducto = "bebidas" | "comidas" | "postres" | "otros";

export interface Mesa {
    id: number;
    numero: number;
    estado: EstadoMesa;
}

export interface Producto {
    id: number;
    nombre: string;
    precio: number;
    categoria: CategoriaProducto;
    disponible: boolean;
}

export interface Item {
    id: number;
    pedido_id: number;
    nombre: string;
    precio_unitario: number;
    cantidad: number;
    es_compartido: boolean;
    grupo_pago_id: number | null;
}

export interface Pedido {
    id: number;
    mesa_id: number;
    estado: EstadoPedido;
    items: Item[];
}

export interface GrupoPago {
    grupo_id: number;
    nombre: string;
    items: { nombre: string; cantidad: number; subtotal: number }[];
    total_propio: number;
    parte_compartida: number;
    total_a_pagar: number;
}

export interface DivisionGrupos {
    pedido_id: number;
    grupos: GrupoPago[];
    compartido: {
        items: { nombre: string; cantidad: number; subtotal: number }[];
        total: number;
        dividido_entre: number;
    };
    sin_asignar: { id: number; nombre: string; cantidad: number }[];
}
