<script lang="ts">
  export let nodes: any[] = [];
  export let loading = false;
  
  function getStatusColor(status: string) {
    switch (status) {
      case 'online': return 'bg-green-500';
      case 'offline': return 'bg-red-500';
      default: return 'bg-gray-400';
    }
  }
  
  function getPlatformIcon(platform: string) {
    switch (platform) {
      case 'windows': return '🪟';
      case 'linux': return '🐧';
      case 'macos': return '🍎';
      default: return '💻';
    }
  }
</script>

<div class="nodes-panel">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold">🖥️ Nodes</h2>
    <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
      + Add Node
    </button>
  </div>
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each nodes as node}
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
          <div class="flex items-center gap-3 mb-3">
            <span class="text-2xl">{getPlatformIcon(node.platform)}</span>
            <div class="flex-1">
              <h3 class="font-semibold">{node.name}</h3>
              <span class={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full ${getStatusColor(node.status)} text-white`}>
                {node.status}
              </span>
            </div>
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400 space-y-1">
            <p>ID: {node.id}</p>
            <p>Platform: {node.platform}</p>
            <p>Last seen: {node.last_seen ? new Date(node.last_seen).toLocaleString() : 'never'}</p>
            {#if node.capabilities?.length}
              <p>Capabilities: {node.capabilities.join(', ')}</p>
            {/if}
          </div>
          <div class="mt-3 flex gap-2">
            <button class="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600">
              Details
            </button>
            <button class="px-3 py-1 text-sm bg-purple-100 dark:bg-purple-900/30 text-purple-700 rounded hover:bg-purple-200">
              Invoke
            </button>
          </div>
        </div>
      {/each}
      
      {#if nodes.length === 0}
        <div class="col-span-full text-center py-12 text-gray-500">
          <p class="text-lg">No nodes connected</p>
          <p class="text-sm">Nodes will appear here when they connect</p>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .nodes-panel {
    padding: 1rem;
  }
</style>
