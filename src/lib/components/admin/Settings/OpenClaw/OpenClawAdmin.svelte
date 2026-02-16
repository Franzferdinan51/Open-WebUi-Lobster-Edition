<script lang="ts">
  import { onMount } from 'svelte';
  import { Overview, Agents, Channels, Cron, Nodes, Sessions, Logs, Usage, Skills } from './index';
  
  type TabId = 'overview' | 'agents' | 'channels' | 'cron' | 'nodes' | 'sessions' | 'logs' | 'usage' | 'skills';
  
  let activeTab: TabId = 'overview';
  let connected = false;
  let loading = true;
  
  // Data
  let agents: any[] = [];
  let channels: any[] = [];
  let cronJobs: any[] = [];
  let nodes: any[] = [];
  let sessions: any[] = [];
  let logs: any[] = [];
  let logSources: string[] = [];
  let usage: any = null;
  let skills: any[] = [];
  
  // Computed
  let sessionsCount = 0;
  let presenceCount = 0;
  let cronEnabled = false;
  let cronNext = '';
  let lastChannelsRefresh = '';
  
  const tabs: { id: TabId; label: string; icon: string }[] = [
    { id: 'overview', label: 'Overview', icon: '🖥️' },
    { id: 'agents', label: 'Agents', icon: '🤖' },
    { id: 'channels', label: 'Channels', icon: '📱' },
    { id: 'cron', label: 'Cron', icon: '⏰' },
    { id: 'nodes', label: 'Nodes', icon: '🖥️' },
    { id: 'sessions', label: 'Sessions', icon: '💬' },
    { id: 'logs', label: 'Logs', icon: '📋' },
    { id: 'usage', label: 'Usage', icon: '📊' },
    { id: 'skills', label: 'Skills', icon: '🧩' },
  ];
  
  async function fetchData() {
    loading = true;
    try {
      const baseUrl = '/openclaw-control/api';
      
      // Fetch all data in parallel
      const [agentsRes, channelsRes, cronRes, nodesRes, sessionsRes, logsRes, usageRes, skillsRes] = await Promise.allSettled([
        fetch(`${baseUrl}/agents`).then(r => r.json()).catch(() => ({ agents: [] })),
        fetch(`${baseUrl}/channels`).then(r => r.json()).catch(() => ({ channels: [] })),
        fetch(`${baseUrl}/cron/jobs`).then(r => r.json()).catch(() => ({ jobs: [] })),
        fetch(`${baseUrl}/nodes`).then(r => r.json()).catch(() => ({ nodes: [] })),
        fetch(`${baseUrl}/sessions`).then(r => r.json()).catch(() => ({ sessions: [] })),
        fetch(`${baseUrl}/logs`).then(r => r.json()).catch(() => ({ logs: [], sources: [] })),
        fetch(`${baseUrl}/usage`).then(r => r.json()).catch(() => ({})),
        fetch(`${baseUrl}/skills`).then(r => r.json()).catch(() => ({ skills: [] })),
      ]);
      
      agents = agentsRes.status === 'fulfilled' ? agentsRes.value.agents || [] : [];
      channels = channelsRes.status === 'fulfilled' ? channelsRes.value.channels || [] : [];
      cronJobs = cronRes.status === 'fulfilled' ? cronRes.value.jobs || [] : [];
      nodes = nodesRes.status === 'fulfilled' ? nodesRes.value.nodes || [] : [];
      sessions = sessionsRes.status === 'fulfilled' ? sessionsRes.value.sessions || [] : [];
      logs = logsRes.status === 'fulfilled' ? logsRes.value.logs || [] : [];
      logSources = logsRes.status === 'fulfilled' ? logsRes.value.sources || [] : [];
      usage = usageRes.status === 'fulfilled' ? usageRes.value : null;
      skills = skillsRes.status === 'fulfilled' ? skillsRes.value.skills || [] : [];
      
      // Compute derived values
      sessionsCount = sessions.length;
      presenceCount = agents.filter((a: any) => a.status === 'online').length;
      cronEnabled = cronJobs.filter((j: any) => j.enabled).length > 0;
      cronNext = cronJobs.length > 0 ? cronJobs[0].nextRun || 'N/A' : 'N/A';
      lastChannelsRefresh = channels.length > 0 ? 'Active' : 'No channels';
      
      connected = true;
    } catch (e) {
      console.error('Failed to fetch OpenClaw data:', e);
      connected = false;
    } finally {
      loading = false;
    }
  }
  
  onMount(() => {
    fetchData();
  });
</script>

<div class="openclaw-admin">
  <!-- Header -->
  <div class="flex items-center justify-between mb-6 px-4 pt-4">
    <div class="flex items-center gap-3">
      <span class={`w-3 h-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`}></span>
      <h1 class="text-2xl font-bold">🦞 OpenClaw Admin</h1>
    </div>
    <button 
      on:click={fetchData}
      class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition flex items-center gap-2"
    >
      🔄 Refresh
    </button>
  </div>
  
  <!-- Tabs -->
  <div class="flex gap-2 px-4 mb-4 overflow-x-auto">
    {#each tabs as tab}
      <button 
        on:click={() => activeTab = tab.id}
        class="px-4 py-2 rounded-lg transition whitespace-nowrap flex items-center gap-2 {activeTab === tab.id 
          ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-medium' 
          : 'hover:bg-gray-100 dark:hover:bg-gray-800'}"
      >
        <span>{tab.icon}</span>
        <span>{tab.label}</span>
      </button>
    {/each}
  </div>
  
  <!-- Content -->
  <div class="border-t border-gray-200 dark:border-gray-700">
    {#if activeTab === 'overview'}
      <Overview {connected} hello={null} {sessionsCount} {presenceCount} {cronEnabled} {cronNext} {lastChannelsRefresh} />
    {:else if activeTab === 'agents'}
      <Agents {agents} {loading} />
    {:else if activeTab === 'channels'}
      <Channels {channels} {loading} />
    {:else if activeTab === 'cron'}
      <Cron jobs={cronJobs} {loading} />
    {:else if activeTab === 'nodes'}
      <Nodes {nodes} {loading} />
    {:else if activeTab === 'sessions'}
      <Sessions {sessions} {loading} />
    {:else if activeTab === 'logs'}
      <Logs logs={logs} sources={logSources} {loading} />
    {:else if activeTab === 'usage'}
      <Usage {usage} {loading} />
    {:else if activeTab === 'skills'}
      <Skills {skills} {loading} />
    {/if}
  </div>
</div>

<style>
  .openclaw-admin {
    min-height: 100%;
    background: var(--bg-secondary);
  }
</style>
