<script>
  import '../app.css';
</script>

<header>
  <h1>Gestor de Papas</h1>
</header>

<main>
  <slot />
</main>

<style>
  header {
    background-color: #2a2a2a;
    padding: 1rem 2rem;
    border-bottom: 1px solid #444;
  }

  main {
    padding: 2rem;
  }
</style>