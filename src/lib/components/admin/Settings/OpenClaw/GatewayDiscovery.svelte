<script lang="ts">
  // Gateway Discovery from ClawTabs
  const GATEWAY_PORTS = [18789, 8080, 3000];
  const SUBNET_PATTERNS = ['192.168.1', '192.168.0', '10.0.0', '100.106.80'];
  
  interface DiscoveredGateway {
    url: string;
    ip: string;
    port: number;
    latency: number;
    lastSeen: number;
  }
  
  let scanning = false;
  let discovered: DiscoveredGateway[] = [];
  let scanStatus = '';
  
  // Gateway form
  let gatewayUrl = 'ws://100.106.80.61:18789';
  let gatewayToken = '';
  let testing = false;
  let testResult: { success: boolean; error?: string } | null = null;
  
  async function probeGateway(ip: string, port: number, timeoutMs = 500): Promise<DiscoveredGateway | null> {
    const url = `ws://${ip}:${port}`;
    const startTime = Date.now();
    
    return new Promise((resolve) => {
      try {
        const ws = new WebSocket(url);
        const timeout = setTimeout(() => { ws.close(); resolve(null); }, timeoutMs);
        ws.onopen = () => {
          clearTimeout(timeout);
          ws.close();
          resolve({ url, ip, port, latency: Date.now() - startTime, lastSeen: Date.now() });
        };
        ws.onerror = () => { clearTimeout(timeout); resolve(null); };
        ws.onclose = () => { clearTimeout(timeout); resolve(null); };
      } catch { resolve(null); }
    });
  }
  
  function generateIPs(): string[] {
    const ips: string[] = ['127.0.0.1', 'localhost'];
    for (const subnet of SUBNET_PATTERNS) {
      for (let i = 1; i <= 254; i++) {
        ips.push(`${subnet}.${i}`);
      }
    }
    return ips;
  }
  
  async function scanNetwork() {
    scanning = true;
    scanStatus = 'Scanning local network...';
    discovered = [];
    
    const ips = generateIPs();
    const probes: Promise<DiscoveredGateway | null>[] = [];
    
    for (const ip of ips) {
      for (const port of GATEWAY_PORTS) {
        probes.push(probeGateway(ip, port, 300));
        if (probes.length >= 50) break;
      }
      if (probes.length >= 50) break;
    }
    
    const results = await Promise.all(probes);
    discovered = results.filter(r => r !== null) as DiscoveredGateway[];
    scanning = false;
    scanStatus = `Found ${discovered.length} gateway(s)`;
  }
  
  async function testConnection() {
    testing = true;
    testResult = null;
    try {
      const wsUrl = gatewayUrl.replace('http', 'ws') + '/ws';
      const ws = new WebSocket(wsUrl);
      await new Promise((resolve, reject) => {
        ws.onopen = () => { ws.close(); resolve(true); };
        ws.onerror = () => reject(new Error('Connection failed'));
        ws.onclose = () => reject(new Error('Connection closed'));
        setTimeout(() => reject(new Error('Timeout')), 5000);
      });
      testResult = { success: true };
    } catch (e: any) {
      testResult = { success: false, error: e.message };
    }
    testing = false;
  }
  
  function selectGateway(gw: DiscoveredGateway) {
    gatewayUrl = gw.url;
  }
</script>

<div class="gateway-discovery">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-semibold">🔍 Gateway Discovery</h3>
    <button 
      class="btn-lobster px-4 py-2 text-sm"
      on:click={scanNetwork}
      disabled={scanning}
    >
      {scanning ? '🔄 Scanning...' : '🔍 Scan Network'}
    </button>
  </div>
  
  {#if scanStatus}
    <p class="text-sm text-gray-500 mb-3">{scanStatus}</p>
  {/if}
  
  {#if discovered.length > 0}
    <div class="mb-4 max-h-40 overflow-y-auto border rounded">
      {#each discovered as gw}
        <button 
          class="w-full text-left px-3 py-2 hover:bg-gray-100 dark:hover:bg-gray-800 border-b last:border-0"
          on:click={() => selectGateway(gw)}
        >
          <span class="font-mono text-sm">{gw.ip}:{gw.port}</span>
          <span class="text-xs text-gray-500 ml-2">{gw.latency}ms</span>
        </button>
      {/each}
    </div>
  {/if}
  
  <!-- Manual Entry -->
  <div class="space-y-3 mt-4">
    <div>
      <label class="text-xs text-gray-500">Gateway URL</label>
      <input 
        type="text" 
        bind:value={gatewayUrl}
        class="input text-sm w-full"
        placeholder="ws://100.106.80.61:18789"
      />
    </div>
    <div>
      <label class="text-xs text-gray-500">Gateway Token</label>
      <input 
        type="password" 
        bind:value={gatewayToken}
        class="input text-sm w-full"
        placeholder="Enter token..."
      />
    </div>
    <div class="flex gap-2 mt-3">
      <button 
        class="btn-lobster px-4 py-2 text-sm"
        on:click={testConnection}
        disabled={testing}
      >
        {testing ? 'Testing...' : '✅ Connect'}
      </button>
    </div>
    {#if testResult}
      <p class="text-sm {testResult.success ? 'text-green-600' : 'text-red-600'}">
        {testResult.success ? '✅ Connected!' : '❌ ' + (testResult.error || 'Failed')}
      </p>
    {/if}
  </div>
</div>

<style>
	.btn-lobster {
		background: linear-gradient(135deg, #ff6b35 0%, #ff8c42 25%, #c92a2a 75%, #ff6b35 100%);
		background-size: 200% 200%;
		color: white;
		border: none;
		border-radius: 0.5rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s ease;
	}
	
	.btn-lobster:hover {
		background-position: 100% 100%;
		box-shadow: 0 4px 20px rgba(255, 107, 53, 0.6);
	}
	
	.btn-lobster:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
</style>
