import type { PageLoad } from './$types';
import { getShipmentById } from '$lib/services/shipmentService';

export const load: PageLoad = async ({ params, fetch }) => {
    const shipmentId = params.id;
    try {
        const shipment = await getShipmentById(shipmentId, fetch);
        return {
            shipment,
        };
    } catch (error: any) {
        return {
            shipment: undefined,
            error: error.message,
        };
    }
};
