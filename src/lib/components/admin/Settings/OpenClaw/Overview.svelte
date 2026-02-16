<script lang="ts">
  import { onMount } from 'svelte';
  
  export let connected = false;
  export let hello: any = null;
  export let settings: any = {};
  export let password = '';
  export let lastError: string | null = null;
  export let presenceCount = 0;
  export let sessionsCount: number | null = null;
  export let cronEnabled: boolean | null = null;
  export let cronNext: number | null = null;
  export let lastChannelsRefresh: number | null = null;
  
  let gatewayUrl = 'http://localhost:18789';
  let token = '';
  
  function formatUptime(ms: number): string {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    if (days > 0) return `${days}d ${hours % 24}h`;
    if (hours > 0) return `${hours}h ${minutes % 60}m`;
    if (minutes > 0) return `${minutes}m ${seconds % 60}s`;
    return `${seconds}s`;
  }
  
  function formatRelative(ts: number): string {
    const diff = Date.now() - ts;
    const minutes = Math.floor(diff / 60000);
    if (minutes < 1) return 'just now';
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    return new Date(ts).toLocaleDateString();
  }
  
  $: snapshot = hello?.snapshot || {};
  $: uptime = snapshot?.uptimeMs ? formatUptime(snapshot.uptimeMs) : 'n/a';
  $: tick = snapshot?.policy?.tickIntervalMs ? `${snapshot.policy.tickIntervalMs}ms` : 'n/a';
  $: authMode = snapshot?.authMode;
</script>

<div class="overview-panel">
  <h2 class="text-2xl font-bold mb-6">🖥️ Gateway Overview</h2>
  
  {#if !connected}
    <div class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mb-4">
      <p class="text-yellow-800 dark:text-yellow-200">Not connected to gateway</p>
      {#if lastError}
        <p class="text-red-600 dark:text-red-400 mt-2 text-sm">{lastError}</p>
      {/if}
    </div>
  {/if}
  
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- Connection Status -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
      <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Connection</h3>
      <div class="flex items-center gap-2">
        <span class={`w-3 h-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`}></span>
        <span class="font-medium">{connected ? 'Connected' : 'Disconnected'}</span>
      </div>
      {#if authMode}
        <p class="text-xs text-gray-500 mt-2">Auth: {authMode}</p>
      {/if}
    </div>
    
    <!-- Uptime -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
      <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Uptime</h3>
      <p class="text-2xl font-bold">{uptime}</p>
      <p class="text-xs text-gray-500 mt-2">Tick: {tick}</p>
    </div>
    
    <!-- Active Sessions -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
      <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Sessions</h3>
      <p class="text-2xl font-bold">{sessionsCount ?? '—'}</p>
      <p class="text-xs text-gray-500 mt-2">Active</p>
    </div>
    
    <!-- Agents -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
      <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Agents</h3>
      <p class="text-2xl font-bold">{presenceCount}</p>
      <p class="text-xs text-gray-500 mt-2">Online</p>
    </div>
    
    <!-- Cron Status -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
      <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Cron Jobs</h3>
      <div class="flex items-center gap-2">
        <span class={`w-3 h-3 rounded-full ${cronEnabled ? 'bg-green-500' : 'bg-gray-400'}`}></span>
        <span class="font-medium">{cronEnabled ? 'Enabled' : 'Disabled'}</span>
      </div>
      {#if cronNext}
        <p class="text-xs text-gray-500 mt-2">Next: {new Date(cronNext).toLocaleString()}</p>
      {/if}
    </div>
    
    <!-- Channels -->
    <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
      <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">Channels</h3>
      <div class="flex items-center gap-2">
        <span class="w-3 h-3 rounded-full bg-green-500"></span>
        <span class="font-medium">Active</span>
      </div>
      {#if lastChannelsRefresh}
        <p class="text-xs text-gray-500 mt-2">Last: {formatRelative(lastChannelsRefresh)}</p>
      {/if}
    </div>
  </div>
  
  <!-- Quick Actions -->
  <div class="mt-6">
    <h3 class="text-lg font-semibold mb-3">Quick Actions</h3>
    <div class="flex flex-wrap gap-2">
      <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        🔄 Refresh
      </button>
      <button class="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition">
        ⚙️ Settings
      </button>
      <button class="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition">
        📊 View Logs
      </button>
    </div>
  </div>
</div>

<style>
  .overview-panel {
    padding: 1rem;
  }
</style>
