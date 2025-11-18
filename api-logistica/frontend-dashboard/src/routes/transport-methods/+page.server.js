/** @type {import('./$types').PageServerLoad} */
export async function load({ fetch }) {
    const response = await fetch('/api/shipping/transport-methods');
    const data = await response.json();

    if (response.ok) {
        return {
            transportMethods: data.transport_methods // Assuming the response has a 'transport_methods' key
        };
    } else {
        return {
            error: data.message || 'Failed to fetch transport methods'
        };
    }
}