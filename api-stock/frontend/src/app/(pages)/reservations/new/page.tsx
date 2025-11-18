"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { listarProductos, crearReserva } from "@/lib/api";
import type { Product } from "@/lib/definitions";

import Link from "next/link";

export default function NewReservationPage() {
    const router = useRouter();
    const [idCompra, setIdCompra] = useState("");
    const [products, setProducts] = useState<Product[]>([]);
    const [qty, setQty] = useState<Record<number, number>>({});

    useEffect(() => {
        listarProductos(1, 100).then(p => setProducts(p.items));
    }, []);

    const submit = async () => {
        const productos = Object.entries(qty)
            .filter(([, c]) => Number(c) > 0)
            .map(([id, c]) => ({ idProducto: Number(id), cantidad: Number(c) }));

        if (!idCompra) return alert("Ingrese idCompra");
        if (productos.length === 0) return alert("Agregue al menos un producto");

        // TODO: Get usuarioId from session
        const usuarioId = 123;

        const r = await crearReserva({ idCompra, usuarioId, productos });
        router.push(`/reservations/${r.idReserva}`);
    };

    return (
        <section className="space-y-4">
            <h1 className="text-xl font-semibold">Nueva reserva</h1>

            <div>
                <label className="text-sm">ID de compra</label>
                <input value={idCompra} onChange={e => setIdCompra(e.target.value)} className="border rounded px-2 py-1 ml-2" />
            </div>

            <table className="w-full border rounded">
                <thead className="bg-gray-50">
                    <tr>
                        <th className="p-2 text-left">Producto</th>
                        <th className="p-2 text-right">Stock</th>
                        <th className="p-2 text-right">Cantidad</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map(p => (
                        <tr key={p.id} className="border-t">
                            <td className="p-2">{p.nombre}</td>
                            <td className="p-2 text-right">{p.stockDisponible}</td>
                            <td className="p-2 text-right">
                                <input
                                    type="number"
                                    min={0}
                                    max={p.stockDisponible}
                                    className="border rounded px-2 py-1 w-24 text-right"
                                    value={qty[p.id] ?? 0}
                                    onChange={(e) => setQty(q => ({ ...q, [p.id]: Number(e.target.value) }))}
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div>
                <button className="border px-3 py-1 rounded" onClick={submit}>Reservar</button>
                <Link className="ml-2 border px-3 py-1 rounded" href="/reservations">Cancelar</Link>
            </div>
        </section>
    );
}