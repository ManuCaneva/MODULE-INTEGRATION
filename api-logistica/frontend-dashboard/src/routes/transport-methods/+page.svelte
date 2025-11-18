<script>
    /** @type {import('./$types').PageData} */
    export let data;
</script>

<div class="container">
    <h1>Transport Methods</h1>

    {#if data.error}
        <p class="error">{data.error}</p>
    {:else if data.transportMethods && data.transportMethods.length > 0}
        <ul>
            {#each data.transportMethods as method}
                <li>
                    <strong>{method.transport_type}</strong>: {method.description} (Cost: {method.cost}, Max Weight: {method.max_weight})
                </li>
            {/each}
        </ul>
    {:else}
        <p>No transport methods found.</p>
    {/if}
</div>

<style>
    .container {
        max-width: 800px;
        margin: 20px auto;
        padding: 20px;
        border: 1px solid #eee;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #333;
        text-align: center;
    }
    ul {
        list-style: none;
        padding: 0;
    }
    li {
        background-color: #f9f9f9;
        margin-bottom: 10px;
        padding: 10px 15px;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    .error {
        color: red;
        font-weight: bold;
        text-align: center;
    }
</style>