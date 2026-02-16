<script lang="ts">
  export let usage: any = null;
  export let loading = false;
  
  $: totalRequests = usage?.total_requests || 0;
  $: totalTokens = usage?.total_tokens || 0;
  $: totalCost = usage?.total_cost || 0;
  $: byModel = usage?.by_model || {};
  $: byChannel = usage?.by_channel || {};
</script>

<div class="usage-panel">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold">📊 Usage Metrics</h2>
    <select class="px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg">
      <option value="day">Today</option>
      <option value="week">This Week</option>
      <option value="month">This Month</option>
      <option value="year">This Year</option>
    </select>
  </div>
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <!-- Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
        <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Total Requests</h3>
        <p class="text-3xl font-bold">{totalRequests.toLocaleString()}</p>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
        <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Total Tokens</h3>
        <p class="text-3xl font-bold">{totalTokens.toLocaleString()}</p>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
        <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Total Cost</h3>
        <p class="text-3xl font-bold">${totalCost.toFixed(2)}</p>
      </div>
    </div>
    
    <!-- By Model -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
        <h3 class="text-lg font-semibold mb-4">By Model</h3>
        <div class="space-y-3">
          {#each Object.entries(byModel) as [model, data]}
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="font-medium truncate">{model}</span>
                <span class="text-gray-500">{data.requests} reqs</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div class="bg-blue-600 h-2 rounded-full" style="width: {data.percentage || 50}%"></div>
              </div>
              <p class="text-xs text-gray-500 mt-1">{data.tokens?.toLocaleString()} tokens</p>
            </div>
          {/each}
          
          {#if Object.keys(byModel).length === 0}
            <p class="text-gray-500 text-center py-4">No model usage data</p>
          {/if}
        </div>
      </div>
      
      <!-- By Channel -->
      <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
        <h3 class="text-lg font-semibold mb-4">By Channel</h3>
        <div class="space-y-3">
          {#each Object.entries(byChannel) as [channel, count]}
            <div>
              <div class="flex justify-between text-sm mb-1">
                <span class="font-medium capitalize">{channel}</span>
                <span class="text-gray-500">{count} requests</span>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div class="bg-green-600 h-2 rounded-full" style="width: {Math.min(100, (count / totalRequests) * 100)}%"></div>
              </div>
            </div>
          {/each}
          
          {#if Object.keys(byChannel).length === 0}
            <p class="text-gray-500 text-center py-4">No channel usage data</p>
          {/if}
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .usage-panel {
    padding: 1rem;
  }
</style>
