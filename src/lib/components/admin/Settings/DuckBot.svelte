<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { GatewayDiscovery } from '$lib/components/admin/Settings/OpenClaw';

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
	let socialEnabled = false;

	// Agent Registration State
	let agentName = 'DuckBot';
	let agentEndpoint = 'http://localhost:18789';
	let agentCapabilities = ['messaging', 'task_execution', 'orchestration', 'social-media', 'research'];
	let registering = false;
	let registerStatus = '';
	
	const registerAgent = async () => {
		registering = true;
		registerStatus = 'Registering agent...';
		try {
			// Register with Agent Mesh
			const response = await fetch('http://localhost:4000/api/agents', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'X-API-Key': 'openclaw-mesh-default-key'
				},
				body: JSON.stringify({
					name: agentName,
					endpoint: agentEndpoint,
					capabilities: agentCapabilities
				})
			});
			if (response.ok) {
				registerStatus = '✅ Agent registered successfully!';
				toast.success('OpenClaw Agent registered!');
			} else {
				registerStatus = '❌ Registration failed';
				toast.error('Failed to register agent');
			}
		} catch (e) {
			registerStatus = '❌ Error: ' + e;
			toast.error('Registration error');
		}
		registering = false;
	};

	const testAgentConnection = async () => {
		toast.loading('Testing connection...');
		try {
			const response = await fetch('http://localhost:18789/api/health');
			if (response.ok) {
				toast.success('✅ Gateway connected!');
			} else {
				toast.error('❌ Gateway not responding');
			}
		} catch (e) {
			toast.error('❌ Cannot reach gateway');
		}
	};

	// Test Chat
	let testMessage = '';
	let chatResponse = '';
	let chatting = false;
	
	const sendTestMessage = async () => {
		if (!testMessage.trim()) return;
		chatting = true;
		chatResponse = '...';
		try {
			const response = await fetch('http://localhost:18789/v1/chat/completions', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					model: 'gpt-4',
					messages: [{ role: 'user', content: testMessage }]
				})
			});
			const data = await response.json();
			chatResponse = data.choices?.[0]?.message?.content || 'No response';
		} catch (e) {
			chatResponse = 'Error: ' + e;
		}
		chatting = false;
	};

	// Model Presets - OpenClaw uses WebSocket for control, HTTP for API
	let presets = [
		{ name: 'OpenClaw Gateway (WebSocket)', url: 'ws://localhost:18789', type: 'websocket', desc: 'Control Plane (WS)' },
		{ name: 'OpenClaw Gateway (HTTP)', url: 'http://localhost:18789/v1', type: 'openai', desc: 'Model API' },
		{ name: 'MiniMax Portal', url: 'https://api.minimax.chat/v1', type: 'openai', desc: 'Cloud Model' },
		{ name: 'LM Studio Local', url: 'http://localhost:1234/v1', type: 'openai', desc: 'Local Models' },
		{ name: 'Ollama Local', url: 'http://localhost:11434', type: 'ollama', desc: 'Local Models' }
	];

	const save = async () => {
		toast.success('DuckBot Settings Saved!');
		if (saveHandler) {
			await saveHandler();
		}
	};

	const testConnection = async (preset: any) => {
		toast.loading(`Testing ${preset.name}...`, { duration: 3000 });
		try {
			let testUrl = '';
			if (preset.type === 'websocket') {
				// WebSocket - test the HTTP API endpoint instead
				testUrl = 'http://localhost:18789/v1/models';
			} else if (preset.url.includes('/v1')) {
				testUrl = preset.url + '/models';
			} else if (preset.type === 'ollama') {
				testUrl = preset.url + '/api/tags';
			} else {
				testUrl = preset.url + '/v1/models';
			}
			
			const response = await fetch(testUrl, {
				method: 'GET',
				signal: AbortSignal.timeout(5000)
			});
			if (response.ok) {
				toast.success(`✅ ${preset.name} connected!`);
			} else if (response.status === 401) {
				toast.success(`✅ ${preset.name} connected (auth required)`);
			} else {
				toast.error(`❌ ${preset.name} returned: ${response.status}`);
			}
		} catch (error: any) {
			toast.error(`❌ ${preset.name} failed: ${error.message || 'Connection refused'}`);
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
				🦞 OpenClaw Agent First WebUI
			</div>
			<div class="text-xs mt-1 text-gray-500">
				Built for Multi-Agent AI Orchestration with OpenClaw
			</div>
		</div>

		<!-- OpenClaw WebSocket Info -->
		<div class="border border-blue-300 dark:border-blue-700 rounded-lg p-3 bg-blue-50 dark:bg-blue-900/20">
			<div class="flex items-center gap-2 text-sm font-medium text-blue-700 dark:text-blue-300">
				🔗 OpenClaw WebSocket Connection
			</div>
			<div class="text-xs mt-1 text-blue-600 dark:text-blue-400">
				OpenClaw uses WebSocket (ws://) for control plane and HTTP for model API.
				<br/>Gateway: <code>ws://localhost:18789</code>
			</div>
		</div>

		<!-- Quick Links -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				🔗 Quick Links
			</div>
			<div class="flex flex-wrap gap-2">
				<a href="http://localhost:5000" target="_blank" class="px-3 py-1.5 rounded-full bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 text-xs hover:bg-orange-200 dark:hover:bg-orange-900/50">
					📊 Dashboard
				</a>
				<a href="http://localhost:5001" target="_blank" class="px-3 py-1.5 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs hover:bg-blue-200 dark:hover:bg-blue-900/50">
					🔧 ClawAPI
				</a>
				<a href="http://localhost:8188" target="_blank" class="px-3 py-1.5 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs hover:bg-purple-200 dark:hover:bg-purple-900/50">
					🎨 ComfyUI
				</a>
				<a href="http://localhost:18789/docs" target="_blank" class="px-3 py-1.5 rounded-full bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 text-xs hover:bg-green-200 dark:hover:bg-green-900/50">
					📚 API Docs
				</a>
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

		<!-- Model Presets -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				🧠 Model Presets
			</div>
			
			<div class="border border-gray-200 dark:border-gray-700 rounded-lg p-3 space-y-2">
				{#each presets as preset}
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-2">
							<span>{preset.type === 'websocket' ? '🔌' : preset.type === 'openai' ? '🤖' : '🦙'} {preset.name}</span>
							<span class="text-xs text-gray-500">({preset.desc})</span>
						</div>
						<div class="flex items-center gap-2">
							<input type="text" bind:value={preset.url} class="input text-xs" placeholder="Enter URL..." />
							<button type="button" class="text-xs px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600" on:click={() => testConnection(preset)}>
								Test
							</button>
						</div>
					</div>
				{/each}
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

		<!-- OpenClaw Agent Setup -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				🤖 OpenClaw Agent Registration
			</div>
			
			<div class="border border-orange-300 dark:border-orange-700 rounded-lg p-4 bg-orange-50 dark:bg-orange-900/10">
				<p class="text-xs text-gray-600 dark:text-gray-400 mb-3">
					Register this agent with Agent Mesh network
				</p>
				
				<div class="space-y-3">
					<div>
						<label class="text-xs text-gray-500">Agent Name</label>
						<input type="text" bind:value={agentName} class="input text-sm w-full" placeholder="DuckBot" />
					</div>
					
					<div>
						<label class="text-xs text-gray-500">Gateway Endpoint</label>
						<input type="text" bind:value={agentEndpoint} class="input text-sm w-full" placeholder="http://localhost:18789" />
					</div>
					
					<div class="flex gap-2">
						<button 
							class="px-3 py-1.5 bg-orange-600 text-white rounded text-sm hover:bg-orange-700"
							on:click={registerAgent}
						>
							🚀 Register
						</button>
						<button 
							class="px-3 py-1.5 bg-gray-200 dark:bg-gray-700 rounded text-sm"
							on:click={testAgentConnection}
						>
							Test
						</button>
					</div>
					
					{#if registerStatus}
						<p class="text-sm {registerStatus.includes('✅') ? 'text-green-600' : 'text-red-600'}">{registerStatus}</p>
					{/if}
				</div>
			</div>
		</div>

		<!-- Gateway Discovery -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				🔍 Gateway Discovery
			</div>
			<GatewayDiscovery />
		</div>

		<!-- Test Chat -->
		<div>
			<div class=" mb-2.5 text-sm font-medium flex items-center gap-2">
				💬 Test Chat with Agent
			</div>
			
			<div class="border border-blue-200 dark:border-blue-700 rounded-lg p-4 bg-blue-50 dark:bg-blue-900/10">
				<div class="space-y-3">
					<textarea 
						bind:value={testMessage}
						placeholder="Type a message to test the agent..."
						class="input text-sm w-full h-20 resize-none"
					></textarea>
					
					<button 
						class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
						on:click={sendTestMessage}
						disabled={chatting || !testMessage.trim()}
					>
						{chatting ? 'Sending...' : 'Send Message'}
					</button>
					
					{#if chatResponse}
						<div class="mt-3 p-3 bg-white dark:bg-gray-800 rounded border">
							<p class="text-sm font-medium text-gray-500 mb-1">Response:</p>
							<p class="text-sm">{chatResponse}</p>
						</div>
					{/if}
				</div>
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
