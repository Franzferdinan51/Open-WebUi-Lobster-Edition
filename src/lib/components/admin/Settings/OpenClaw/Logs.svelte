<script lang="ts">
  export let logs: any[] = [];
  export let sources: string[] = [];
  export let loading = false;
  
  let selectedSource = 'all';
  let selectedLevel = 'all';
  let searchQuery = '';
  
  function getLevelColor(level: string) {
    switch (level) {
      case 'error': return 'text-red-500';
      case 'warn': return 'text-yellow-500';
      case 'info': return 'text-blue-500';
      case 'debug': return 'text-gray-500';
      default: return 'text-gray-400';
    }
  }
  
  $: filteredLogs = logs.filter(log => {
    if (selectedSource !== 'all' && !log.source.includes(selectedSource)) return false;
    if (selectedLevel !== 'all' && log.level !== selectedLevel) return false;
    if (searchQuery && !log.message.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });
</script>

<div class="logs-panel">
  <div class="flex items-center justify-between mb-4">
    <h2 class="text-2xl font-bold">📋 Logs</h2>
    <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
      🔄 Refresh
    </button>
  </div>
  
  <!-- Filters -->
  <div class="flex flex-wrap gap-3 mb-4">
    <select 
      bind:value={selectedSource}
      class="px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg"
    >
      <option value="all">All Sources</option>
      {#each sources as source}
        <option value={source}>{source}</option>
      {/each}
    </select>
    
    <select 
      bind:value={selectedLevel}
      class="px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg"
    >
      <option value="all">All Levels</option>
      <option value="error">Error</option>
      <option value="warn">Warning</option>
      <option value="info">Info</option>
      <option value="debug">Debug</option>
    </select>
    
    <input 
      type="text"
      bind:value={searchQuery}
      placeholder="Search logs..."
      class="px-3 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg flex-1 min-w-[200px]"
    />
  </div>
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <div class="bg-black rounded-lg p-4 font-mono text-sm max-h-[600px] overflow-y-auto">
      {#each filteredLogs as log}
        <div class="py-1 border-b border-gray-800 last:border-0">
          <span class="text-gray-500">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
          <span class={`ml-2 ${getLevelColor(log.level)} uppercase`}>{log.level}</span>
          <span class="ml-2 text-gray-400">[{log.source}]</span>
          <span class="ml-2 text-gray-300">{log.message}</span>
        </div>
      {/each}
      
      {#if filteredLogs.length === 0}
        <div class="text-center py-8 text-gray-500">
          No logs found
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .logs-panel {
    padding: 1rem;
  }
</style>
