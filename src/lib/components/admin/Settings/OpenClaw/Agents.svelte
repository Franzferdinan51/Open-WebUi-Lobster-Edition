<script lang="ts">
  export let agents: any[] = [];
  export let selectedAgent: string | null = null;
  export let loading = false;
  
  let activePanel: 'overview' | 'files' | 'tools' | 'skills' | 'channels' | 'cron' = 'overview';
  
  function getStatusColor(status: string) {
    switch (status) {
      case 'online': return 'bg-green-500';
      case 'offline': return 'bg-red-500';
      case 'busy': return 'bg-yellow-500';
      default: return 'bg-gray-400';
    }
  }
</script>

<div class="agents-panel">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold">🤖 Agents</h2>
    <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
      + Add Agent
    </button>
  </div>
  
  <!-- Tabs -->
  <div class="flex gap-2 mb-4 border-b border-gray-200 dark:border-gray-700 pb-2">
    <button 
      class="px-3 py-1.5 rounded-lg transition {activePanel === 'overview' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}"
      on:click={() => activePanel = 'overview'}
    >
      Overview
    </button>
    <button 
      class="px-3 py-1.5 rounded-lg transition {activePanel === 'tools' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}"
      on:click={() => activePanel = 'tools'}
    >
      Tools
    </button>
    <button 
      class="px-3 py-1.5 rounded-lg transition {activePanel === 'skills' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}"
      on:click={() => activePanel = 'skills'}
    >
      Skills
    </button>
    <button 
      class="px-3 py-1.5 rounded-lg transition {activePanel === 'channels' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}"
      on:click={() => activePanel = 'channels'}
    >
      Channels
    </button>
    <button 
      class="px-3 py-1.5 rounded-lg transition {activePanel === 'cron' ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300' : 'hover:bg-gray-100 dark:hover:bg-gray-800'}"
      on:click={() => activePanel = 'cron'}
    >
      Cron
    </button>
  </div>
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <!-- Agents Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each agents as agent}
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow border-2 {selectedAgent === agent.id ? 'border-blue-500' : 'border-transparent'}">
          <div class="flex items-center gap-3 mb-3">
            <span class={`w-3 h-3 rounded-full ${getStatusColor(agent.status)}`}></span>
            <span class="font-semibold">{agent.name}</span>
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400 space-y-1">
            <p>ID: {agent.id}</p>
            <p>Platform: {agent.platform || 'unknown'}</p>
            <p>Last seen: {agent.last_seen ? new Date(agent.last_seen).toLocaleString() : 'never'}</p>
          </div>
          <div class="mt-3 flex gap-2">
            <button class="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600">
              Configure
            </button>
            <button class="px-3 py-1 text-sm bg-blue-100 dark:bg-blue-900/30 text-blue-700 rounded hover:bg-blue-200">
              Chat
            </button>
          </div>
        </div>
      {/each}
      
      {#if agents.length === 0}
        <div class="col-span-full text-center py-12 text-gray-500">
          <p class="text-lg">No agents found</p>
          <p class="text-sm">Connect an agent to get started</p>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .agents-panel {
    padding: 1rem;
  }
</style>
