<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { getDashboardShipments } from '../../services/shipmentService';
  import type { DashboardShipmentDto, FiltersState, PaginatedDashboardShipmentsResponse } from '$lib/types';

  import Filters from './Filters.svelte';
  import ShipmentList from './ShipmentList.svelte';

  let allShipments: DashboardShipmentDto[] = [];
  let filteredShipments: DashboardShipmentDto[] = [];
  let currentPage: number = 1;
  let totalPages: number = 1;
  let isLoading: boolean = false;
  let hasMore: boolean = true;
  let observer: IntersectionObserver;
  let loadMoreElement: HTMLElement;

  const PAGE_SIZE = 20; // Define a page size for infinite scrolling

  async function loadShipments() {
    if (isLoading || !hasMore) return;

    isLoading = true;
    try {
      const response: PaginatedDashboardShipmentsResponse = await getDashboardShipments(currentPage, PAGE_SIZE);
      allShipments = [...allShipments, ...response.shipments];
      totalPages = response.pagination.total_pages;
      hasMore = currentPage < totalPages;
      currentPage++;
      applyFilters(); // Re-apply filters after loading more shipments
    } catch (error) {
      console.error('Error loading shipments:', error);
      // Optionally, display an error message to the user
    } finally {
      isLoading = false;
    }
  }

  function applyFilters() {
    const { id, city, status, startDate, endDate } = currentFilters; // Use currentFilters for filtering
    
    filteredShipments = allShipments.filter(shipment => {
      // 1. Filtro por ID
      const idMatch = id ? shipment.shipping_id.toString().toUpperCase().includes(id.toUpperCase()) : true;

      // 2. Filtro por Ciudad
      const cityMatch = city ? shipment.delivery_address.locality_name.toLowerCase().includes(city.toLowerCase()) : true;

      // 3. Filtro por Estado
      const statusMatch = status ? shipment.status === status : true;

      // 4. Filtro por Rango de Fechas
      const entryDate = new Date(shipment.created_at);
      const start = startDate ? new Date(startDate) : null;
      const end = endDate ? new Date(endDate) : null;
      // Ajustamos las fechas para que la comparación sea inclusiva
      if (start) start.setHours(0, 0, 0, 0);
      if (end) end.setHours(23, 59, 59, 999);

      const dateMatch = (!start || entryDate >= start) && (!end || entryDate <= end);

      // El envío se muestra solo si todas las condiciones son verdaderas
      return idMatch && cityMatch && statusMatch && dateMatch;
    });
  }

  let currentFilters: FiltersState = {
    id: '',
    city: '',
    status: '',
    startDate: '',
    endDate: ''
  };

  function handleFilterChange(event: CustomEvent<FiltersState>) {
    currentFilters = event.detail;
    // Reset pagination and reload from scratch when filters change
    allShipments = [];
    currentPage = 1;
    hasMore = true;
    loadShipments();
  }

  onMount(async () => {
    await loadShipments();

    observer = new IntersectionObserver(
      (entries) => {
        const [entry] = entries;
        if (entry.isIntersecting && hasMore && !isLoading) {
          loadShipments();
        }
      },
      { threshold: 0.1 }
    );

    if (loadMoreElement) {
      observer.observe(loadMoreElement);
    }
  });

  onDestroy(() => {
    if (observer) {
      observer.disconnect();
    }
  });

  // Reactively apply filters whenever allShipments or currentFilters change
  $: {
    applyFilters();
  }
</script>

<h2>Dashboard de Pedidos</h2>
<p>Listado de Pedidos</p>

<Filters on:filterChange={handleFilterChange} />

<ShipmentList shipments={filteredShipments} />

{#if isLoading}
  <p>Cargando más pedidos...</p>
{:else if !hasMore && allShipments.length > 0}
  <p>No hay más pedidos para cargar.</p>
{/if}

<div bind:this={loadMoreElement} style="height: 1px; margin-top: -1px;"></div>