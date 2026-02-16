<script lang="ts">
  export let jobs: any[] = [];
  export let loading = false;
  
  function getStatusColor(status: string) {
    switch (status) {
      case 'running': return 'bg-green-500';
      case 'error': return 'bg-red-500';
      case 'idle': return 'bg-gray-400';
      default: return 'bg-gray-400';
    }
  }
</script>

<div class="cron-panel">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold">⏰ Cron Jobs</h2>
    <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
      + Add Job
    </button>
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
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Schedule</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Last Run</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">Next Run</th>
            <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 uppercase">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          {#each jobs as job}
            <tr>
              <td class="px-4 py-3 font-medium">{job.name}</td>
              <td class="px-4 py-3 text-sm font-mono">{job.schedule}</td>
              <td class="px-4 py-3">
                <span class={`inline-flex items-center gap-1 text-xs px-2 py-0.5 rounded-full ${getStatusColor(job.status)} text-white`}>
                  {job.status}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-gray-500">
                {job.last_run ? new Date(job.last_run).toLocaleString() : '—'}
              </td>
              <td class="px-4 py-3 text-sm text-gray-500">
                {job.next_run ? new Date(job.next_run).toLocaleString() : '—'}
              </td>
              <td class="px-4 py-3 text-right">
                <button class="px-2 py-1 text-sm bg-blue-100 dark:bg-blue-900/30 text-blue-700 rounded hover:bg-blue-200 mr-1">
                  Run
                </button>
                <button class="px-2 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200">
                  Edit
                </button>
              </td>
            </tr>
          {/each}
          
          {#if jobs.length === 0}
            <tr>
              <td colspan="6" class="px-4 py-12 text-center text-gray-500">
                No cron jobs configured
              </td>
            </tr>
          {/if}
        </tbody>
      </table>
    </div>
  {/if}
</div>

<style>
  .cron-panel {
    padding: 1rem;
  }
</style>
