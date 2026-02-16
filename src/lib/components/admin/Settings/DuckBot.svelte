<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';

	const i18n = getContext('i18n');

	export let saveHandler: Function;

	// DuckBot Features
	let agentSmithConnected = true;
	let minimaxEnabled = true;
	let lmStudioEnabled = true;
	let comfyuiEnabled = true;
	let ttsEnabled = true;
	let cryptoEnabled = true;
	let polymarketEnabled = true;
	let socialEnabled = false; // Disabled due to X ban risk

	// Connection Status
	let agentSmithStatus = 'Connected';
	let openclawGateway = 'http://localhost:18789';
	let agentMeshUrl = 'http://100.74.88.40:4000';
	let comfyuiUrl = 'http://100.74.88.40:8188';

	const save = async () => {
		toast.success('DuckBot Settings Saved!');
		if (saveHandler) {
			await saveHandler();
		}
	};

	onMount(() => {
		// Load settings from config
	});
</script>

<form
	on:submit|preventDefault={() => {
		save();
	}}
	class="flex flex-col h-full justify-between space-y-3 text-sm mb-6"
>
	<div class=" space-y-3 overflow-y-scroll max-h-[28rem] md:max-h-full">
		<!-- DuckBot Lobster Edition Header -->
		<div class="lobster-card p-4">
			<div class="flex items-center gap-2 text-lg font-bold lobster-gradient-text">
				🦞 DuckBot Lobster Edition
			</div>
			<div class="text-xs mt-1 text-gray-500">
				OpenWebUI with full OpenClaw Integration
			</div>
		</div>

		<!-- Agent Connections -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				🤖 Agent Connections
			</div>
			
			<div class="border border-gray-200 dark:border-gray-700 rounded-lg p-3 space-y-3">
				<!-- Agent Smith -->
				<div class="flex items-center justify-between">
					<div class="flex items-center gap-2">
						<span>Agent Smith</span>
						<span class="text-xs px-2 py-0.5 rounded-full" class:bg-green-500={agentSmithConnected} class:bg-red-500={!agentSmithConnected} class:text-white={true}>
							{agentSmithConnected ? 'Connected' : 'Disconnected'}
						</span>
					</div>
					<input type="text" bind:value={agentSmithStatus} class="input" disabled />
				</div>

				<!-- Agent Mesh -->
				<div class="flex items-center justify-between">
					<div class="flex items-center gap-2">
						<span>🌐 Agent Mesh</span>
					</div>
					<input type="text" bind:value={agentMeshUrl} class="input" />
				</div>

				<!-- OpenClaw Gateway -->
				<div class="flex items-center justify-between">
					<div class="flex items-center gap-2">
						<span>🔗 OpenClaw Gateway</span>
					</div>
					<input type="text" bind:value={openclawGateway} class="input" />
				</div>

				<!-- ComfyUI -->
				<div class="flex items-center justify-between">
					<div class="flex items-center gap-2">
						<span>🎨 ComfyUI</span>
					</div>
					<input type="text" bind:value={comfyuiUrl} class="input" />
				</div>
			</div>
		</div>

		<!-- Model Providers -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				🧠 AI Models
			</div>
			
			<div class="border border-gray-200 dark:border-gray-700 rounded-lg p-3 space-y-2">
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={minimaxEnabled} class="checkbox" />
					<span>MiniMax M2.5</span>
				</label>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={lmStudioEnabled} class="checkbox" />
					<span>LM Studio (Local)</span>
				</label>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={comfyuiEnabled} class="checkbox" />
					<span>ComfyUI (Image Gen)</span>
				</label>
			</div>
		</div>

		<!-- Tools & Features -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				🛠️ Tools & Features
			</div>
			
			<div class="border border-gray-200 dark:border-gray-700 rounded-lg p-3 space-y-2">
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={ttsEnabled} class="checkbox" />
					<span>🔊 Text-to-Speech (KaniTTS)</span>
				</label>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={cryptoEnabled} class="checkbox" />
					<span>₿ Crypto Tracking</span>
				</label>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={polymarketEnabled} class="checkbox" />
					<span>📈 Polymarket Integration</span>
				</label>
				<label class="flex items-center gap-2">
					<input type="checkbox" bind:checked={socialEnabled} class="checkbox" />
					<span>📱 Social Media (Disabled)</span>
				</label>
			</div>
		</div>

		<!-- Theme -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				🎨 Theme
			</div>
			
			<div class="border border-gray-200 dark:border-gray-700 rounded-lg p-3">
				<label class="flex items-center gap-2">
					<input type="checkbox" checked class="checkbox" />
					<span class="lobster-gradient-text font-bold">🦞 Lobster Theme</span>
					<span class="text-xs text-gray-500">(Active)</span>
				</label>
			</div>
		</div>

		<!-- Links -->
		<div>
			<div class=" mb-2.5 text-sm font-medium">
				🔗 Links
			</div>
			
			<div class="flex gap-2 flex-wrap">
				<a href="https://github.com/Franzferdinan51/Open-WebUi-Lobster-Edition" target="_blank" class="text-xs px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700">
					🐙 GitHub
				</a>
				<a href="https://clawhub.com" target="_blank" class="text-xs px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700">
					🦆 ClawHub
				</a>
				<a href="https://discord.gg/openwebui" target="_blank" class="text-xs px-3 py-1 rounded-full bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700">
					💬 Discord
				</a>
			</div>
		</div>
	</div>

	<div class="flex justify-end pt-4">
		<button class="btn-lobster" type="submit">
			{$i18n.t('Save')}
		</button>
	</div>
</form>

<style>
	.lobster-card {
		background: linear-gradient(135deg, rgba(255, 107, 53, 0.1) 0%, rgba(201, 42, 42, 0.1) 100%);
		border: 1px solid rgba(255, 107, 53, 0.3);
		border-radius: 1rem;
	}
	
	.lobster-gradient-text {
		background: linear-gradient(135deg, #ff6b35 0%, #ffd166 100%);
		-webkit-background-clip: text;
		-webkit-text-fill-color: transparent;
		background-clip: text;
	}
	
	.input {
		background: var(--color-bg-secondary);
		border: 1px solid var(--color-border);
		border-radius: 0.5rem;
		padding: 0.25rem 0.5rem;
		font-size: 0.75rem;
		width: 150px;
	}
	
	.checkbox {
		width: 1rem;
		height: 1rem;
		accent-color: #ff6b35;
	}
	
	.btn-lobster {
		background: linear-gradient(135deg, #ff6b35 0%, #c92a2a 100%);
		color: white;
		border: none;
		padding: 0.5rem 1.5rem;
		border-radius: 0.5rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.3s ease;
	}
	
	.btn-lobster:hover {
		box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
	}
</style>
