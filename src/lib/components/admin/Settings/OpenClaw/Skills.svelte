<script lang="ts">
  export let skills: any[] = [];
  export let loading = false;
  
  let searchQuery = '';
  
  function getStatusColor(enabled: boolean) {
    return enabled ? 'bg-green-500' : 'bg-gray-400';
  }
  
  $: filteredSkills = skills.filter(skill => 
    skill.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    skill.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );
</script>

<div class="skills-panel">
  <div class="flex items-center justify-between mb-6">
    <h2 class="text-2xl font-bold">🧩 Skills</h2>
    <button class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
      + Add Skill
    </button>
  </div>
  
  <!-- Search -->
  <div class="mb-4">
    <input 
      type="text"
      bind:value={searchQuery}
      placeholder="Search skills..."
      class="w-full px-4 py-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg"
    />
  </div>
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
    </div>
  {:else}
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {#each filteredSkills as skill}
        <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow">
          <div class="flex items-start justify-between mb-2">
            <h3 class="font-semibold">{skill.name}</h3>
            <button 
              class="relative w-10 h-5 rounded-full transition-colors {getStatusColor(skill.enabled)}"
              on:click={() => skill.enabled = !skill.enabled}
            >
              <span class={`absolute top-0.5 w-4 h-4 bg-white rounded-full transition-transform ${skill.enabled ? 'left-5' : 'left-0.5'}`}></span>
            </button>
          </div>
          {#if skill.description}
            <p class="text-sm text-gray-500 dark:text-gray-400 mb-3">{skill.description}</p>
          {/if}
          <div class="flex flex-wrap gap-1 mb-3">
            {#each skill.tags || [] as tag}
              <span class="px-2 py-0.5 text-xs bg-gray-100 dark:bg-gray-700 rounded">{tag}</span>
            {/each}
          </div>
          <div class="flex gap-2">
            <button class="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600">
              Configure
            </button>
          </div>
        </div>
      {/each}
      
      {#if filteredSkills.length === 0}
        <div class="col-span-full text-center py-12 text-gray-500">
          <p class="text-lg">No skills found</p>
          <p class="text-sm">Add a skill to get started</p>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .skills-panel {
    padding: 1rem;
  }
</style>
