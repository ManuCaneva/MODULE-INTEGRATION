import { obtenerReservaPorId, cancelarReserva } from "@/lib/api";
import { redirect } from "next/navigation";

export default async function ReservationDetailPage({ params }: { params: { id: string } }) {
    const idReserva = Number(params.id);
    // TODO: Get usuarioId from session
    const info = await obtenerReservaPorId(idReserva);

    return (
        <section className="space-y-4">
            <h1 className="text-xl font-semibold">Reserva #{info.idReserva}</h1>
            <p className="text-sm">Estado: <b>{info.estado}</b></p>
            <p className="text-sm">Expira: {new Date(info.expiresAt).toLocaleString()}</p>

            <form action={async () => {
                "use server";
                await cancelarReserva(idReserva, { motivo: 'Cancelado desde la UI' });
                redirect(`/reservations`);
            }}>
                <button className="border px-3 py-1 rounded">Liberar</button>
            </form>
        </section>
    );
}
