<script lang="ts">
  import { onMount } from 'svelte';
  
  let deviceName = '';
  let pairingCode = '';
  let status = 'idle';
  let message = '';
  
  async function generatePairingCode() {
    status = 'generating';
    message = '';
    
    try {
      // Generate a simple pairing code
      pairingCode = Math.random().toString(36).substring(2, 8).toUpperCase();
      status = 'ready';
      message = `Pairing code: ${pairingCode}`;
    } catch (e) {
      status = 'error';
      message = 'Failed to generate code';
    }
  }
  
  async function pairDevice() {
    if (!deviceName.trim()) {
      message = 'Please enter a device name';
      return;
    }
    
    status = 'pairing';
    message = '';
    
    try {
      // Simulate pairing (would call actual API)
      await new Promise(r => setTimeout(r, 1500));
      status = 'paired';
      message = `Device "${deviceName}" paired successfully!`;
      deviceName = '';
    } catch (e) {
      status = 'error';
      message = 'Pairing failed';
    }
  }
  
  let devices = [
    { name: 'DuckBot-Linux', status: 'online', lastSeen: 'now' },
    { name: 'AgentSmith-Windows', status: 'online', lastSeen: '2m ago' },
  ];
</script>

<div class="device-auth-panel">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold">🔐 Device Authentication</h2>
  </div>
  
  <!-- Pair New Device -->
  <div class="bg-white dark:bg-gray-800 rounded-lg p-4 mb-6">
    <h3 class="font-semibold mb-3">Pair New Device</h3>
    
    <div class="space-y-3">
      <div>
        <label class="text-sm font-medium">Device Name</label>
        <input 
          bind:value={deviceName}
          type="text" 
          class="w-full px-3 py-2 border rounded-lg bg-white dark:bg-gray-700"
          placeholder="e.g., My Laptop"
        />
      </div>
      
      <button 
        on:click={pairDevice}
        disabled={status === 'pairing'}
        class="w-full px-4 py-2 bg-blue-600 text-white rounded-lg disabled:opacity-50"
      >
        {status === 'pairing' ? 'Pairing...' : 'Pair Device'}
      </button>
      
      {#if message}
        <p class="text-sm {status === 'error' ? 'text-red-500' : status === 'paired' ? 'text-green-500' : 'text-yellow-500'}">
          {message}
        </p>
      {/if}
    </div>
  </div>
  
  <!-- Generate Code -->
  <div class="bg-white dark:bg-gray-800 rounded-lg p-4 mb-6">
    <h3 class="font-semibold mb-3">Quick Pairing Code</h3>
    <button 
      on:click={generatePairingCode}
      class="px-4 py-2 bg-green-600 text-white rounded-lg"
    >
      Generate Code
    </button>
    {#if pairingCode}
      <p class="mt-2 text-2xl font-mono font-bold text-green-600">{pairingCode}</p>
    {/if}
  </div>
  
  <!-- Paired Devices -->
  <div class="bg-white dark:bg-gray-800 rounded-lg p-4">
    <h3 class="font-semibold mb-3">Paired Devices</h3>
    <div class="space-y-2">
      {#each devices as device}
        <div class="flex items-center justify-between p-2 bg-gray-100 dark:bg-gray-700 rounded">
          <div>
            <p class="font-medium">{device.name}</p>
            <p class="text-xs text-gray-500">Last seen: {device.lastSeen}</p>
          </div>
          <span class="px-2 py-1 text-xs rounded-full {device.status === 'online' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">
            {device.status}
          </span>
        </div>
      {/each}
    </div>
  </div>
</div>
