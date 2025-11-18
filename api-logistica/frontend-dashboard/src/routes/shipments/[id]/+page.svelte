<script lang="ts">
  import { page } from '$app/stores';
  import { getShipmentById } from '../../../lib/services/shipmentService';
  import type { ShippingDetail, ShipmentStatus } from '$lib/types';

  const shipmentId = $page.params.id;
  let shipmentDetails: ShippingDetail | undefined;

  // Function to format date from ISO string to DD/MM/YYYY
  function formatDate(isoString: string): string {
    if (!isoString) return '';
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }

  // Function to get status display name
  const statusNames: Record<ShipmentStatus, string> = {
    'created': 'Creado',
    'reserved': 'Reservado',
    'in_transit': 'En Tránsito',
    'delivered': 'Entregado',
    'cancelled': 'Cancelado',
    'in_distribution': 'En Distribución',
    'arrived': 'Arribado',
  };

  const transportTypeNames: Record<TransportType, string> = {
    'truck': 'Camión',
    'plane': 'Avión',
    'boat': 'Barco',
  };

  getShipmentById(shipmentId).then(details => {
    shipmentDetails = details;
  });
</script>

{#if shipmentDetails}
<div class="details-container">
  <h2>Detalles del Pedido {shipmentDetails.shipping_id}</h2>

  <div class="details-section">
    <h3>Información General</h3>
    <p><strong>ID de Usuario:</strong> {shipmentDetails.user_id}</p>
    <p><strong>Origen:</strong> {shipmentDetails.departure_address.locality_name}, {shipmentDetails.departure_address.street} {shipmentDetails.departure_address.number}</p>
    <p><strong>Destino:</strong> {shipmentDetails.delivery_address.locality_name}, {shipmentDetails.delivery_address.street} {shipmentDetails.delivery_address.number}</p>
    <p><strong>Estado Actual:</strong> {statusNames[shipmentDetails.status] || shipmentDetails.status}</p>
    <p><strong>Tipo de Transporte:</strong> {transportTypeNames[shipmentDetails.transport_type] || shipmentDetails.transport_type}</p>
    <p><strong>Costo Total:</strong> {shipmentDetails.total_cost} {shipmentDetails.currency}</p>
    <p><strong>Número de Seguimiento:</strong> {shipmentDetails.tracking_number}</p>
    <p><strong>Transportista:</strong> {shipmentDetails.carrier_name}</p>
    <p><strong>Fecha de Creación:</strong> {formatDate(shipmentDetails.created_at)}</p>
    <p><strong>Última Actualización:</strong> {formatDate(shipmentDetails.updated_at)}</p>
    <p><strong>Fecha Estimada de Entrega:</strong> {formatDate(shipmentDetails.estimated_delivery_at)}</p>
  </div>

  <div class="details-section">
    <h3>Historial de Estados</h3>
    {#if shipmentDetails.logs && shipmentDetails.logs.length > 0}
      <ul>
        {#each shipmentDetails.logs as log}
          <li><strong>{formatDate(log.timestamp)}:</strong> {statusNames[log.status] || log.status} - {log.message}</li>
        {/each}
      </ul>
    {:else}
      <p>No hay historial de estados disponible.</p>
    {/if}
  </div>

  <div class="details-section">
    <h3>Productos</h3>
    {#if shipmentDetails.products && shipmentDetails.products.length > 0}
      <ul>
        {#each shipmentDetails.products as product}
          <li>ID: {product.id} (Cantidad: {product.quantity})</li>
        {/each}
      </ul>
    {:else}
      <p>No hay productos asociados a este envío.</p>
    {/if}
  </div>

  <a href="/" class="button">Volver al Listado</a>
</div>
{:else}
<p>Cargando...</p>
{/if}

<style>
  .details-container {
    padding: 2rem;
    background-color: #1e1e1e;
    border-radius: 8px;
  }

  .details-section {
    margin-bottom: 1.5rem;
  }

  h2, h3 {
    color: #f0f0f0;
  }

  p, li {
    color: #ccc;
  }

  ul {
    list-style-type: none;
    padding-left: 0;
  }

  .button {
    display: inline-block;
    background-color: #3b82f6;
    color: white;
    padding: 10px 15px;
    border-radius: 4px;
    text-decoration: none;
    margin-top: 1rem;
  }

  .button:hover {
    background-color: #2563eb;
  }
</style>
