<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  
  export let meshUrl = 'http://100.74.88.40:4000';
  export let apiKey = 'openclaw-mesh-default-key';
  
  let agents: any[] = [];
  let loading = true;
  let error = '';
  let refreshInterval: any;
  
  async function fetchAgents() {
    try {
      const res = await fetch(`${meshUrl}/api/agents`, {
        headers: { 'X-API-Key': apiKey }
      });
      if (!res.ok) throw new Error('Failed to fetch');
      agents = await res.json();
      error = '';
    } catch (e) {
      error = 'Failed to connect to Agent Mesh';
      agents = [];
    } finally {
      loading = false;
    }
  }
  
  function getTimeSince(timestamp: string) {
    const diff = Date.now() - new Date(timestamp).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    return `${Math.floor(hours / 24)}d ago`;
  }
  
  function isOnline(lastSeen: string) {
    const diff = Date.now() - new Date(lastSeen).getTime();
    return diff < 5 * 60 * 1000; // 5 minutes
  }
  
  onMount(() => {
    fetchAgents();
    refreshInterval = setInterval(fetchAgents, 30000); // Refresh every 30s
  });
  
  onDestroy(() => {
    if (refreshInterval) clearInterval(refreshInterval);
  });
</script>

<div class="mesh-dashboard">
  <div class="flex items-center justify-between mb-6">
    <div class="flex items-center gap-3">
      <h2 class="text-2xl font-bold">🤝 Agent Mesh Dashboard</h2>
      <span class="px-2 py-1 text-xs bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full">
        {agents.length} Agents
      </span>
    </div>
    <button 
      on:click={fetchAgents}
      class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
    >
      <span>🔄</span> Refresh
    </button>
  </div>
  
  {#if error}
    <div class="bg-red-100 dark:bg-red-900 border border-red-400 text-red-700 dark:text-red-200 px-4 py-3 rounded-lg mb-4">
      {error}
    </div>
  {/if}
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each agents as agent}
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow border-l-4 {isOnline(agent.last_seen) ? 'border-green-500' : 'border-gray-400'}">
          <div class="flex items-start justify-between mb-3">
            <div>
              <h3 class="font-semibold text-lg">{agent.name}</h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">{agent.id}</p>
            </div>
            <span class="px-2 py-1 text-xs rounded-full {isOnline(agent.last_seen) ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200' : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300'}">
              {isOnline(agent.last_seen) ? '🟢 Online' : '⚪ Offline'}
            </span>
          </div>
          
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-500 dark:text-gray-400">Endpoint:</span>
              <span class="font-mono text-xs">{agent.endpoint || 'N/A'}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-500 dark:text-gray-400">Last Seen:</span>
              <span>{getTimeSince(agent.last_seen)}</span>
            </div>
          </div>
          
          {#if agent.capabilities && agent.capabilities.length > 0}
            <div class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
              <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">Capabilities:</p>
              <div class="flex flex-wrap gap-1">
                {#each agent.capabilities as cap}
                  <span class="px-2 py-0.5 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded">
                    {cap}
                  </span>
                {/each}
              </div>
            </div>
          {/if}
        </div>
      {/each}
    </div>
    
    {#if agents.length === 0}
      <div class="text-center py-12 text-gray-500 dark:text-gray-400">
        <p class="text-xl mb-2">🤖</p>
        <p>No agents registered on the mesh</p>
      </div>
    {/if}
  {/if}
</div>
