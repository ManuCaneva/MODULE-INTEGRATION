<script lang="ts">
  import type { DashboardShipmentDto, ShipmentStatus } from '$lib/types';

  export let shipments: DashboardShipmentDto[] = [];

  const statusNames: Record<ShipmentStatus, string> = {
    'created': 'Creado',
    'reserved': 'Reservado',
    'in_transit': 'En Tránsito',
    'delivered': 'Entregado',
    'cancelled': 'Cancelado',
    'in_distribution': 'En Distribución',
    'arrived': 'Arribado',
  };

  const statusColors: Record<ShipmentStatus, string> = {
    'created': '#f0e68c',
    'reserved': '#ffa07a',
    'in_transit': '#add8e6',
    'delivered': '#98fb98',
    'cancelled': '#f08080',
    'in_distribution': '#dda0dd',
    'arrived': '#8fbc8f',
  };

  function getColorForStatus(status: ShipmentStatus): string {
    return statusColors[status] || '#ccc'; // Color por defecto
  }

  /**
   * TOMA UNA FECHA ISO STRING Y LA DEVUELVE COMO 'DD/MM/YYYY'.
   */
  function formatDate(dateString: string): string {
    if (!dateString) return '';
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are 0-indexed
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }
</script>

<table>
  <thead>
    <tr>
      <th>ID Pedido</th>
      <th>Destino</th>
      <th>Estado</th>
      <th>Fecha Ingreso</th>
      <th>Acciones</th>
    </tr>
  </thead>
  <tbody>
    {#each shipments as shipment}
      <tr>
        <td>{shipment.shipping_id}</td>
        <td>{shipment.delivery_address.locality_name}</td>
        <td>
          <span class="status-circle" style="background-color: {getColorForStatus(shipment.status)}"></span>
          {statusNames[shipment.status] || shipment.status}
        </td>
        <td>{formatDate(shipment.created_at)}</td>
        <td><a href="/shipments/{shipment.shipping_id}" class="button">Ver Detalles</a></td>
      </tr>
    {:else}
      <tr>
        <td colspan="5">No se encontraron pedidos con los filtros seleccionados.</td>
      </tr>
    {/each}
  </tbody>
</table>

<style>
  /* ... tus estilos de la tabla aquí ... */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }
  th, td {
    border: 1px solid #444;
    padding: 8px;
    text-align: left;
  }
  th {
    background-color: #2a2a2a;
  }
  .status-circle {
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-right: 8px;
  }
  a.button {
    background-color: #3b82f6;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    text-decoration: none;
  }
  a.button:hover {
    background-color: #2563eb;
  }
</style>