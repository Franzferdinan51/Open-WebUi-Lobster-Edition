<script lang="ts">
  export let sessions: any[] = [];
  export let loading = false;
  
  function getStatusColor(status: string) {
    switch (status) {
      case 'active': return 'bg-green-500';
      case 'ended': return 'bg-gray-400';
      case 'error': return 'bg-red-500';
      default: return 'bg-gray-400';
    }
  }
</script>

<div class="sessions-panel">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold">💬 Sessions</h2>
  </div>
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-900">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Session ID</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Agent</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Channel</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Created</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Activity</th>
            <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          {#each sessions as session}
            <tr>
              <td class="px-4 py-3 font-mono text-sm">{session.id}</td>
              <td class="px-4 py-3">{session.agent_id}</td>
              <td class="px-4 py-3 capitalize">{session.channel}</td>
              <td class="px-4 py-3">
                <span class={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full ${getStatusColor(session.status)} text-white`}>
                  {session.status}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-500">
                {session.created_at ? new Date(session.created_at).toLocaleString() : '—'}
              </td>
              <td class="px-4 py-3 text-sm text-gray-500">
                {session.last_activity ? new Date(session.last_activity).toLocaleString() : '—'}
              </td>
              <td class="px-4 py-3 text-right">
                <button class="px-2 py-1 text-sm bg-blue-100 dark:bg-blue-900/30 text-blue-700 rounded hover:bg-blue-200 mr-1">
                  View
                </button>
                {#if session.status === 'active'}
                  <button class="px-2 py-1 text-sm bg-red-100 dark:bg-red-900/30 text-red-700 rounded hover:bg-red-200">
                    End
                  </button>
                {/if}
              </td>
            </tr>
          {/each}
          
          {#if sessions.length === 0}
            <tr>
              <td colspan="7" class="px-4 py-12 text-center text-gray-500">
                No active sessions
              </td>
            </tr>
          {/if}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  .sessions-panel {
    padding: 1rem;
  }
</style>
