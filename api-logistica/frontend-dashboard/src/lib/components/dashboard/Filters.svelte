<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { FiltersState, ShipmentStatus } from '$lib/types';

  let id: string = '';
  let city: string = '';
  let status: ShipmentStatus | '' = '';
  // Estas variables siempre almacenarán la fecha en formato 'YYYY-MM-DD'
  let startDate: string = '';
  let endDate: string = '';

  const dispatch = createEventDispatcher<{ filterChange: FiltersState }>();

  function applyFilters() {
    dispatch('filterChange', {
      id: id.toUpperCase(),
      city: city.toLowerCase(),
      status: status,
      startDate: startDate,
      endDate: endDate
    });
  }
</script>

<div class="filter-grid">
  <input
    type="text"
    placeholder="Buscar por ID..."
    bind:value={id}
    on:input={applyFilters}
  />
  
  <input
    type="text"
    placeholder="Filtrar por destino..."
    bind:value={city}
    on:input={applyFilters}
  />

  <select bind:value={status} on:change={applyFilters}>
    <option value="">Todos los estados</option>
    <option value="in_transit">En Tránsito</option>
    <option value="created">Creado</option>
    <option value="delivered">Entregado</option>
    <option value="cancelled">Cancelado</option>
    <option value="in_distribution">En Distribución</option>
    <option value="arrived">Arribado</option>
    <option value="reserved">Reservado</option>
  </select>

  <div class="date-filter">
    <label for="start-date">Desde:</label>
    <input
      type="date"
      id="start-date"
      bind:value={startDate}
      on:change={applyFilters}
    />
  </div>
  <div class="date-filter">
    <label for="end-date">Hasta:</label>
    <input
      type="date"
      id="end-date"
      bind:value={endDate}
      on:change={applyFilters}
    />
  </div>
</div>

<style>
  .filter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
    align-items: center;
  }
  input, select {
    padding: 0.5rem;
    background-color: #2a2a2a;
    color: #f0f0f0;
    border: 1px solid #444;
    border-radius: 4px;
    font-size: 14px;
    width: 100%;
    box-sizing: border-box;
  }
  .date-filter {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  .date-filter label {
    white-space: nowrap;
  }
  /* Estilo para que el calendario del date picker sea visible en tema oscuro */
  input[type="date"]::-webkit-calendar-picker-indicator {
    filter: invert(1);
  }
</style>