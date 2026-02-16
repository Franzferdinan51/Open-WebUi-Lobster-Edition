<script lang="ts">
  export let channels: any[] = [];
  export let loading = false;
  
  const channelIcons: Record<string, string> = {
    telegram: '✈️',
    whatsapp: '💬',
    discord: '🎮',
    slack: '💼',
    signal: '🔒',
    imessage: '🍎',
    googlechat: '📱'
  };
  
  function getStatusColor(status: string) {
    switch (status) {
      case 'connected': return 'bg-green-500';
      case 'error': return 'bg-red-500';
      case 'connecting': return 'bg-yellow-500';
      default: return 'bg-gray-400';
    }
  }
</script>

<div class="channels-panel">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold">📱 Channels</h2>
    <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
      + Add Channel
    </button>
  </div>
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each channels as channel}
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
          <div class="flex items-center gap-3 mb-3">
            <span class="text-2xl">{channelIcons[channel.type] || '📱'}</span>
            <div>
              <h3 class="font-semibold capitalize">{channel.type}</h3>
              <span class={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full ${getStatusColor(channel.status)} text-white`}>
                {channel.status}
              </span>
            </div>
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400 space-y-1">
            {#if channel.name}
              <p>Name: {channel.name}</p>
            {/if}
            {#if channel.chat_id}
              <p>Chat ID: {channel.chat_id}</p>
            {/if}
          </div>
          <div class="mt-3 flex gap-2">
            <button class="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600">
              Configure
            </button>
            <button class="px-3 py-1 text-sm bg-green-100 dark:bg-green-900/30 text-green-700 rounded hover:bg-green-200">
              Test
            </button>
          </div>
        </div>
      {/each}
      
      {#if channels.length === 0}
        <div class="col-span-full text-center py-12 text-gray-500">
          <p class="text-lg">No channels configured</p>
          <p class="text-sm">Add a channel to start receiving messages</p>
        </div>
      {/if}
    </div>
    
    <!-- Available Channel Types -->
    <div class="mt-8">
      <h3 class="text-lg font-semibold mb-3">Available Channels</h3>
      <div class="flex flex-wrap gap-3">
        {#each ['telegram', 'whatsapp', 'discord', 'slack', 'signal', 'imessage', 'googlechat'] as type}
          <div class="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-gray-800 rounded-lg">
            <span>{channelIcons[type]}</span>
            <span class="capitalize">{type}</span>
          </div>
        {/each}
      </div>
    </div>
  {/if}
</div>

<style>
  .channels-panel {
    padding: 1rem;
  }
</style>
