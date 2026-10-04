# -*- coding: utf-8 -*-
"""
llama.cpp WebUI 汉化补丁
- 对 bundle JS 做"精确字面量替换"，只在特定语法上下文内替换
- 不修改任何第三方库(KaTeX/Mermaid 等)的字符串
- 输出到 webui-zh，供 llama-server --path 使用
"""
import json, os, re, shutil, sys

LLAMA_TAG = 'b11344'
BASE = os.path.dirname(os.path.abspath(__file__))
_UI_ROOT = os.path.join(BASE, '_ui')
SRC = os.path.join(_UI_ROOT, 'llama-' + LLAMA_TAG)
DST = os.path.join(BASE, 'webui-zh')
BUNDLE = '_app/immutable/bundle.DvlqYeJf.js'


def ensure_ui():
    """确保原始 UI 已解压；没有就从 GitHub 拉取（升级 llama.cpp 后改 LLAMA_TAG 重跑即可）"""
    if not os.path.isdir(SRC):
        os.makedirs(_UI_ROOT, exist_ok=True)
        tgz = os.path.join(_UI_ROOT, 'ui.tar.gz')
        url = (f'https://github.com/ggml-org/llama.cpp/releases/download/'
               f'{LLAMA_TAG}/llama-{LLAMA_TAG}-ui.tar.gz')
        print('downloading UI bundle ...')
        if os.system(f'curl.exe -L -sS --retry 8 --retry-delay 4 --retry-all-errors -o "{tgz}" "{url}"') != 0:
            raise SystemExit('download failed')
        if os.system(f'tar.exe -xzf "{tgz}" -C "{_UI_ROOT}"') != 0:
            raise SystemExit('extract failed')
    if not os.path.isdir(SRC):
        raise SystemExit(f'UI not found: {SRC}')

# ---------- gr("...") 静态文本 ----------
GR = {
    "API Key": "API 密钥",
    "Add": "添加",
    "Add New MCP Server": "添加新的 MCP 服务器",
    "Add another MCP server": "再添加一个 MCP 服务器",
    "Add files, system prompt or configure MCP servers": "添加文件、系统提示词，或配置 MCP 服务器",
    "Add to chat": "添加到对话",
    "Add your first MCP server": "添加你的第一个 MCP 服务器",
    "Agentic turn limit reached. Continue?": "已达智能体轮次上限，是否继续？",
    "Allow once": "仅允许一次",
    "Browse and attach resources from connected MCP servers to your chat context.": "浏览已连接的 MCP 服务器资源，并附加到对话上下文中。",
    "Build Info": "构建信息",
    "Cancel": "取消",
    "Choose a model to use for the conversation": "选择一个模型用于本次对话",
    "Choose a new title for this conversation.": "为本次对话设置新标题。",
    "Close": "关闭",
    "Collapse System Message": "折叠系统消息",
    "Connect a remote MCP server by URL.": "通过 URL 连接远程 MCP 服务器。",
    "Context Size": "上下文长度",
    "Continue": "继续",
    "Current model details and capabilities": "当前模型的详细信息与能力",
    "Delete": "删除",
    "Delete Server": "删除服务器",
    "Deny": "拒绝",
    "Dismiss": "忽略",
    "Embedding Size": "嵌入维度",
    "Export Anyway": "仍然导出",
    "Export Without Sensitive Data": "导出（不含敏感数据）",
    "File Path": "文件路径",
    "File Upload Error": "文件上传失败",
    "Got it": "知道了",
    "Include all attachments": "包含所有附件",
    "Load model": "加载模型",
    "Loading resources...": "正在加载资源…",
    "Modalities": "模态类型",
    "Model": "模型",
    "Model Information": "模型信息",
    "Model Size": "模型大小",
    "No conversations available": "暂无对话",
    "No resources available": "暂无可用资源",
    "Not available": "不可用",
    "Parallel Slots": "并行槽位（同时处理的请求数）",
    "Parameters": "参数",
    "Preview only": "仅预览",
    "Read Resource": "读取资源",
    "Reload": "重新加载",
    "Reset Settings to Default": "将设置恢复为默认值",
    "Reset to Default": "恢复默认",
    "Save": "保存",
    "Save & Retry": "保存并重试",
    "Save settings": "保存设置",
    "Select Model": "选择模型",
    "Show full system message": "展开完整系统消息",
    "Show system message in conversations": "在对话中显示系统消息",
    "Some files cannot be uploaded with the current model.": "当前模型无法上传部分文件。",
    "Stop": "停止",
    "Success!": "成功！",
    "The following files are empty and have been removed from your attachments:": "以下文件内容为空，已从附件中移除：",
    "The requested model could not be found. Select an available model to continue.": "找不到所请求的模型，请选择一个可用模型后继续。",
    "Title": "标题",
    "Training Context": "训练上下文长度",
    "Try again": "重试",
    "Update available": "有可用更新",
    "Use Prompt": "使用提示词",
    "Vocabulary Size": "词表大小",
    "Vocabulary Type": "词表类型",
}

# ---------- placeholder ----------
PLACEHOLDER = {
    "Choose working directory": "选择工作目录",
    "Conversation title": "对话标题",
    "Edit your message...": "编辑你的消息…",
    "Enter fork name": "输入分支名称",
    "Enter your API key...": "输入你的 API 密钥…",
    "Paste token here": "在此粘贴令牌",
    "Search conversations...": "搜索对话…",
    "Search models...": "搜索模型…",
    "Search resources...": "搜索资源…",
}

# ---------- title（区块标题 / 提示） ----------
TITLE = {
    "Agentic": "智能体",
    "Conversations": "对话",
    "Delete All": "全部删除",
    "Delete Conversation": "删除对话",
    "Delete Message": "删除消息",
    "Delete all conversations": "删除所有对话",
    "Developer": "开发者",
    "Discard changes?": "放弃更改？",
    "Display": "显示",
    "Download content": "下载内容",
    "Export": "导出",
    "Fork Conversation": "创建对话分支",
    "General": "通用",
    "Import": "导入",
    "Import/Export": "导入/导出",
    "Refresh resources": "刷新资源",
    "Runtime info": "运行时信息",
    "Sampling & Penalties": "采样与惩罚",
    "Settings": "设置",
    "Skip reasoning": "跳过思考过程",
    "Tools": "工具",
}

# ---------- tooltip ----------
TOOLTIP = {
    "Add to favorites": "加入收藏",
    "Close Sidebar": "关闭侧边栏",
    "Continue": "继续",
    "Copy": "复制",
    "Delete selected": "删除所选",
    "Exit bulk selection mode": "退出批量选择模式",
    "Fork conversation": "创建对话分支",
    "Model information": "模型信息",
    "New chat": "新建对话",
    "Next version": "下一个版本",
    "Previous version": "上一个版本",
    "Regenerate": "重新生成",
    "Remove from favorites": "取消收藏",
    "Reset working directory": "重置工作目录",
    "Retry loading model": "重试加载模型",
    "Scroll to bottom": "滚动到底部",
    "Send immediately": "立即发送",
    "Unload model": "卸载模型",
}

# ---------- message / note / error ----------
MESSAGE = {
    "Failed to load PDF images": "PDF 图片加载失败",
    "Failed to load model": "模型加载失败",
    "Failed to load models": "模型列表加载失败",
    "Failed to unload model": "模型卸载失败",
    "Invalid Base64 string": "Base64 字符串无效",
    "Method not found": "未找到该方法",
    "Please enter a server URL first.": "请先输入服务器 URL。",
    "URL cannot use javascript:, data:, or vbscript: scheme": "URL 不能使用 javascript:、data: 或 vbscript: 协议",
    "URL must be parseable": "URL 必须可解析",
    "Unknown error": "未知错误",
    "Unknown error executing prompt": "执行提示词时发生未知错误",
    "Unknown error occurred": "发生未知错误",
    "Unknown reason": "未知原因",
}
ERROR = {
    "All MCP server connections failed": "所有 MCP 服务器连接均失败",
}
NOTE = {
    "Integers must be within the safe integer range.": "整数必须在安全整数范围内。",
    "Invalid URL format": "URL 格式无效",
    "Invalid hostname": "主机名无效",
    "Invalid protocol": "协议无效",
    "No matching discriminator": "没有匹配的判别字段",
}

# ---------- 设置项名称 label ----------
LABEL = {
    "API Key": "API 密钥",
    "Agentic turns": "智能体轮次上限",
    "Always show sidebar on desktop": "桌面上始终显示侧边栏",
    "Always show tool call content": "始终展开工具调用内容",
    "Audio": "音频",
    "Audio Files": "音频文件",
    "Avg speed": "平均速度",
    "Backend sampling": "后端采样",
    "Conversation tabs": "对话标签页",
    "Conversation title": "对话标题",
    "Copy text attachments as plain text": "将文本附件复制为纯文本",
    "Current time": "当前时间",
    "Custom CSS": "自定义 CSS",
    "Custom JSON": "自定义 JSON",
    "DRY allowed length": "DRY 允许长度",
    "DRY base": "DRY 基数",
    "DRY multiplier": "DRY 倍数",
    "DRY penalty last N": "DRY 惩罚回溯长度 N",
    "Dark": "深色",
    "Default": "默认",
    "Disable automatic scroll": "禁用自动滚动",
    "Disable reasoning content parsing": "禁用思考内容解析",
    "Dynamic temperature exponent": "动态温度指数",
    "Dynamic temperature range": "动态温度范围",
    "Edit file": "编辑文件",
    "Enable PDF as Images": "将 PDF 作为图片处理",
    "Enable raw output toggle": "启用原始输出开关",
    "Exclude reasoning from context": "从上下文中排除思考内容",
    "Frequency penalty": "频率惩罚（按出现次数压制词元）",
    "Generate title with LLM": "用 LLM 生成标题",
    "Generated": "已生成",
    "Generation": "生成",
    "High": "高",
    "Images": "图片",
    "JavaScript sandbox tool": "JavaScript 沙箱工具",
    "LLM title generation prompt": "LLM 标题生成提示词",
    "Light": "浅色",
    "Low": "低",
    "MCP request timeout (seconds)": "MCP 请求超时（秒）",
    "MCP servers": "MCP 服务器",
    "Max": "最大",
    "Max tokens": "最大生成词元数",
    "Maximum image resolution (megapixels)": "最大图片分辨率（百万像素）",
    "Medium": "中",
    "Mention search depth": "提及搜索深度",
    "Min P": "最小概率 P（相对最高概率词元的过滤阈值）",
    "Off": "关闭",
    "PDF Files": "PDF 文件",
    "Parse PDF as image": "将 PDF 解析为图片",
    "Paste long text to file length": "长文本转为文件的长度阈值",
    "Pre-fill KV cache after response": "回复后预填充 KV 缓存",
    "Presence penalty": "存在惩罚（已出现过的词元降权）",
    "Prompt": "提示词",
    "Prompt tokens evaluated": "已处理的提示词元数",
    "Read file": "读取文件",
    "Read media": "读取媒体",
    "Reading": "读取",
    "Render thinking as Markdown": "以 Markdown 渲染思考内容",
    "Render user content as Markdown": "以 Markdown 渲染用户内容",
    "Repeat last N": "重复惩罚回溯长度 N",
    "Repeat penalty": "重复惩罚（压制重复内容）",
    "Run JavaScript": "运行 JavaScript",
    "Run command": "运行命令",
    "Runtime info": "运行时信息",
    "Samplers": "采样器",
    "Search files": "搜索文件",
    "Search in files": "在文件中搜索",
    "Select": "选择",
    "Send message on Enter": "按 Enter 发送消息",
    "Show build version information": "显示构建版本信息",
    "Show full path in mentions": "在提及中显示完整路径",
    "Show message generation statistics": "显示消息生成统计",
    "Show microphone on empty input": "输入框为空时显示麦克风",
    "Show model quantization information": "显示模型量化信息",
    "Show model tags": "显示模型标签",
    "Show organization name in model selector trigger": "在模型选择按钮中显示组织名",
    "Show raw model names": "显示原始模型名称",
    "Show statistics for individual agentic turns": "显示各智能体轮次的统计",
    "Show system message": "显示系统消息",
    "Show thought in progress": "生成过程中显示思考",
    "Summary": "摘要",
    "Symbolic math (nerdamer)": "符号运算（nerdamer）",
    "System": "跟随系统",
    "System Message": "系统消息",
    "Temperature": "温度（越高越随机，越低越确定）",
    "Text Files": "文本文件",
    "Theme": "主题",
    "Tokens generated": "已生成词元数",
    "Top K": "Top K（只保留概率最高的 K 个词元）",
    "Top P": "Top P（核采样：保留累积概率达 P 的词元）",
    "Typical P": "典型采样 P（按信息量筛选词元）",
    "Use first non-empty line for the conversation title": "用首个非空行作为对话标题",
    "Use full height code blocks": "代码块使用完整高度",
    "Video": "视频",
    "Video Files": "视频文件",
    "Vision": "视觉",
    "Write file": "写入文件",
    "XTC probability": "XTC 概率（触发剔除的概率）",
    "XTC threshold": "XTC 阈值（被剔除词元的概率下限）",
}

# ---------- 参数说明 help ----------
HELP = {
    "Addon for the temperature sampler. Smoothes out the probability redistribution based on the most probable token.":
        "温度采样的附加项：依据最可能的词元来平滑概率重分布。",
    "Addon for the temperature sampler. The added value to the range of dynamic temperature, which adjusts probabilities by entropy of tokens.":
        "温度采样的附加项：动态温度范围的附加值，按词元熵自动调整概率。",
    "After each response, re-submit the conversation to pre-fill the server KV cache. Makes the next turn faster since the prompt is already encoded while you read the response.":
        "每次回复后重新提交对话以预填充服务端 KV 缓存。这样你阅读回复时提示词就已编码完毕，下一轮响应更快。",
    "Always display code blocks at their full natural height, overriding any height limits.":
        "代码块始终按完整自然高度显示，不受高度限制。",
    "Always keep the sidebar visible on desktop instead of auto-hiding it.":
        "桌面上始终显示侧边栏，而不是自动隐藏。",
    "Automatically expand tool call details while executing and keep them expanded after completion.":
        "工具调用执行时自动展开详情，完成后保持展开。",
    "Automatically show microphone button instead of send button when textarea is empty for models with audio modality support.":
        "当模型支持音频模态且输入框为空时，自动显示麦克风按钮而非发送按钮。",
    "CSS injected into the page at runtime. Set it here, or ship it server side via the --ui-config customCss field.":
        "运行时注入页面的 CSS。可在此设置，也可通过服务端 --ui-config 的 customCss 字段下发。",
    "Choose how conversation titles are generated. The first non-empty line uses a fast deterministic rule; the LLM option uses a model-generated title from the first message exchange.":
        "选择对话标题的生成方式。首个非空行是快速确定性规则；LLM 选项则由模型根据首轮对话生成标题。",
    "Choose the color theme for the interface. You can choose between System (follows your device settings), Light, or Dark.":
        "选择界面配色主题：跟随系统（依设备设置）、浅色或深色。",
    "Configure MCP servers as a JSON list. Use the form in the MCP Client settings section to edit.":
        "以 JSON 列表配置 MCP 服务器。可在「MCP 客户端」设置区用表单编辑。",
    "Controls the randomness of the generated text by affecting the probability distribution of the output tokens. Higher = more random, lower = more focused.":
        "通过影响输出词元的概率分布来控制文本随机性。值越高越随机，越低越聚焦。",
    "Controls the repetition of token sequences in the generated text":
        "控制生成文本中词元序列的重复程度。",
    "Counterpart of the conversation title radio; stored and synced without a dedicated UI field.":
        "对话标题选项的对应项；会被保存和同步，但没有独立的界面字段。",
    "Custom JSON parameters to send to the API. Must be valid JSON format.":
        "发送给 API 的自定义 JSON 参数，必须是合法的 JSON 格式。",
    "DRY sampling reduces repetition in generated text even across long contexts. This parameter sets DRY penalty for the last n tokens.":
        "DRY 采样可减少长上下文中的重复内容。此参数设置回溯 n 个词元的 DRY 惩罚。",
    "DRY sampling reduces repetition in generated text even across long contexts. This parameter sets the DRY sampling base value.":
        "DRY 采样可减少长上下文中的重复内容。此参数设置 DRY 采样的基数值。",
    "DRY sampling reduces repetition in generated text even across long contexts. This parameter sets the DRY sampling multiplier.":
        "DRY 采样可减少长上下文中的重复内容。此参数设置 DRY 采样的倍数。",
    "DRY sampling reduces repetition in generated text even across long contexts. This parameter sets the allowed length for DRY sampling.":
        "DRY 采样可减少长上下文中的重复内容。此参数设置 DRY 采样允许的重复长度。",
    "Disable automatic scrolling while messages stream so you can control the viewport position manually.":
        "消息流式输出时禁用自动滚动，以便你手动控制视图位置。",
    "Display generation statistics (tokens/second, token count, duration) below each assistant message.":
        "在每条助手消息下方显示生成统计（词元/秒、词元数、耗时）。",
    "Display quantization badges (e.g. Q8_0, Q4_K_M) next to model names throughout the interface.":
        "在界面各处的模型名旁显示量化标签（如 Q8_0、Q4_K_M）。",
    "Display the current build version in the bottom-right corner of the interface.":
        "在界面右下角显示当前构建版本。",
    "Display the full file system path inside file and folder @-mention badges instead of just the file or folder name.":
        "在文件和文件夹的 @ 提及标签中显示完整路径，而非仅名称。",
    "Display the organization name in the model selector trigger button.":
        "在模型选择按钮中显示组织名称。",
    "Display the system message at the top of each conversation.":
        "在每次对话顶部显示系统消息。",
    "Enable backend-based samplers. When enabled, supported samplers run on the accelerator backend for faster sampling.":
        "启用后端采样器。开启后，受支持的采样器会在加速后端上运行，采样更快。",
    "Expand thought process by default when generating messages.":
        "生成消息时默认展开思考过程。",
    "Expose a run_javascript tool to the model. Code runs in a Web Worker inside a sandboxed iframe with an opaque origin, isolated from the WebUI and its API, with a hard timeout.":
        "向模型提供 run_javascript 工具。代码在不透明来源的沙箱 iframe 内的 Web Worker 中运行，与 WebUI 及其 API 隔离，并有强制超时。",
    "How many directory levels below the working directory the @-mention file search descends. Larger values surface deeply nested files but take longer on large trees.":
        "@ 提及文件搜索向下检索的目录层级数。值越大越能发现深层文件，但在大目录树上更慢。",
    "Images larger than this will be resized before sending to server. Set to 0 to disable.":
        "大于此尺寸的图片会在发送到服务端前被缩放。设为 0 表示不限制。",
    "Keeps only k top tokens.":
        "只保留概率最高的 k 个词元。",
    "Last n tokens to consider for penalizing repetition":
        "参与重复惩罚的回溯词元数 n。",
    "Limits tokens based on how often they appear in the output.":
        "根据词元在输出中出现的次数进行限制。",
    "Limits tokens based on the minimum probability for a token to be considered, relative to the probability of the most likely token.":
        "按「相对最高概率词元」的最小概率阈值来过滤词元。",
    "Limits tokens based on whether they appear in the output or not.":
        "根据词元是否已在输出中出现过来进行限制。",
    "Limits tokens to those that together have a cumulative probability of at least p":
        "只保留累积概率至少达到 p 的那批词元。",
    "Maximum number of tool execution cycles before stopping (prevents infinite loops).":
        "停止前允许的最大工具执行轮数（用于防止死循环）。",
    "On pasting long text, it will be converted to a file. You can control the file length by setting the value of this parameter. Value 0 means disable.":
        "粘贴长文本时会自动转为文件。此参数控制触发转换的长度阈值，0 表示禁用。",
    "Optional template for the title generation prompt. Use {{USER}} for the user message and {{ASSISTANT}} for the assistant message.":
        "标题生成提示词的模板（可选）。用 {{USER}} 代表用户消息，{{ASSISTANT}} 代表助手消息。",
    "Parse PDF as image instead of text. Automatically falls back to text processing for non-vision models.":
        "将 PDF 按图片而非文本解析。对不支持视觉的模型会自动回退为文本处理。",
    "Render the reasoning/thinking block content as formatted Markdown instead of plain text.":
        "将推理/思考块内容以 Markdown 格式渲染，而非纯文本。",
    "Render user messages using markdown formatting in the chat. Turn this off to keep a message exactly as typed; @-mention badges show either way.":
        "在对话中以 Markdown 格式渲染用户消息。关闭后消息将完全按输入原样显示；@ 提及标签两种情况都会显示。",
    "Send reasoning_format=none so the server returns thinking tokens inline instead of extracting them into a separate field.":
        "发送 reasoning_format=none，让服务端把思考词元内联返回，而不是抽取到独立字段。",
    "Show open chats as browser-style tabs above the conversation, one per open chat. When disabled, only one chat is shown at a time.":
        "在对话上方以浏览器标签页形式显示已打开的对话，每个对话一个标签。关闭后一次只显示一个对话。",
    "Show toggle button to display messages as plain text instead of Markdown-formatted content":
        "显示切换按钮，可将消息以纯文本显示，而非 Markdown 格式。",
    "Sorts and limits tokens based on the difference between log-probability and entropy.":
        "依据对数概率与信息熵之差来排序并筛选词元。",
    "Strip thinking from previous messages before sending. When off, thinking is sent back via the reasoning_content field so the model sees its own chain-of-thought across turns.":
        "发送前剔除历史消息中的思考内容。关闭后，思考内容会通过 reasoning_content 字段回传，使模型在多轮中能看到自己的思维链。",
    "The maximum number of token per output. Use -1 for infinite (no limit).":
        "单次输出的最大词元数。设为 -1 表示无限制。",
    "The starting message that defines how model should behave.":
        "定义模型行为方式的起始消息。",
    "Timeout for individual MCP tool calls.":
        "单次 MCP 工具调用的超时时间。",
    "Use Enter to send messages and Shift + Enter for new lines. When disabled, use Ctrl/Cmd + Enter.":
        "按 Enter 发送消息，Shift + Enter 换行。关闭后改用 Ctrl/Cmd + Enter 发送。",
    "When copying a message with text attachments, combine them into a single plain text string instead of a special format that can be pasted back as attachments.":
        "复制含文本附件的消息时，合并为单个纯文本字符串，而不是可回粘为附件的特殊格式。",
    "XTC sampler cuts out top tokens; this parameter controls the chance of cutting tokens at all. 0 disables XTC.":
        "XTC 采样器会剔除部分高概率词元；此参数控制剔除发生的概率，0 表示禁用 XTC。",
    "XTC sampler cuts out top tokens; this parameter controls the token probability that is required to cut that token.":
        "XTC 采样器会剔除部分高概率词元；此参数控制某词元被剔除所需的概率阈值。",
}

# ---------- description（仅应用自身 UI，跳过第三方库） ----------
DESCRIPTION = {
    "Are you sure you want to delete all conversations? This action cannot be undone and will permanently remove all your conversations and messages.":
        "确定要删除所有对话吗？此操作无法撤销，将永久删除你的全部对话和消息。",
    "Are you sure you want to delete this conversation? This action cannot be undone and will permanently remove all messages in this conversation.":
        "确定要删除该对话吗？此操作无法撤销，将永久删除该对话中的所有消息。",
    "You have unsaved changes. Are you sure you want to discard them?":
        "有未保存的更改，确定要放弃吗？",
    "Create a new conversation branching from this message.":
        "从该消息创建一条新的对话分支。",
    "Download your conversations as a ZIP of JSONL files. This includes all messages, attachments, and conversation history.":
        "将对话导出为 ZIP（内含 JSONL 文件），包含所有消息、附件和对话历史。",
    "Export your chat settings and preferences as a JSON file.":
        "将聊天设置与偏好导出为 JSON 文件。",
    "Import chat settings from a previously exported JSON file. This will merge with your existing settings.":
        "从之前导出的 JSON 文件导入聊天设置，将与现有设置合并。",
    "Import one or more conversations from a previously exported ZIP or JSONL file. This will merge with your existing conversations.":
        "从之前导出的 ZIP 或 JSONL 文件导入一个或多个对话，将与现有对话合并。",
    "Get runtime info (OS name), may call when user asks about local files or shell commands":
        "获取运行时信息（操作系统名称）。当用户询问本地文件或 shell 命令时可能被调用。",
    "JavaScript source to execute": "要执行的 JavaScript 源码",
    "Determines the markup language of the output.": "决定输出所用的标记语言。",
    "Browse up-to-date documentation and code examples for libraries and frameworks.":
        "浏览库和框架的最新文档与代码示例。",
    "Insert an MCP prompt": "插入一个 MCP 提示词",
    "Communication link": "通信链路",
    "Adds a comment": "添加注释",
}

# ============ 第二阶段：模板字面量 / 普通字符串常量 / 单引号属性 ============

# se('...>文本<...') 里的界面文本
TEMPLATE = {
    "(failed)": "（失败）",
    "(not available)": "（不可用）",
    "(optional)": "（可选）",
    "(with line numbers)": "（含行号）",
    "A new version is available. Reload to update.": "有新版本可用，重新加载以更新。",
    "Across all turns": "所有轮次合计",
    "Add files": "添加文件",
    "Always allow": "始终允许",
    "Applies to new conversations. Tool picks inside a chat only affect that chat.":
        "仅对新对话生效。在某个对话内选择的工具只影响该对话。",
    "Attach a file": "附加文件",
    "Audio": "音频",
    "Audio preview not available": "音频预览不可用",
    "Authorization": "授权",
    "Available context size is only visible once the model is loaded.": "上下文可用长度仅在模型加载后才可见。",
    "Available models": "可用模型",
    "Available resources": "可用资源",
    "Branch conversation after edit": "编辑后创建对话分支",
    "Browse": "浏览",
    "Build Info": "构建信息",
    "Chat Template": "对话模板",
    "Check server logs for any error messages": "查看服务器日志中的错误信息",
    "Check that the server is accessible at the correct URL": "确认服务器可访问且 URL 正确",
    "Close": "关闭",
    "Close preview": "关闭预览",
    "Close tab": "关闭标签页",
    "Configure Server": "配置服务器",
    "Connecting to Server": "正在连接服务器",
    "Console": "控制台",
    "Context": "上下文",
    "Context size:": "上下文长度：",
    "Conversation Name": "对话名称",
    "Conversation title": "对话标题",
    "Converting PDF to images...": "正在将 PDF 转换为图片…",
    "Current model does not support audio": "当前模型不支持音频",
    "Current time": "当前时间",
    "Display name": "显示名称",
    "Drop your files here to upload": "将文件拖到此处上传",
    "Edit file": "编辑文件",
    "Empty Files:": "空文件：",
    "Empty files cannot be processed or sent to the AI model": "空文件无法处理，也不会发送给 AI 模型",
    "Enabled": "已启用",
    "Failed to load PDF images": "PDF 图片加载失败",
    "Failed to load tools": "工具加载失败",
    "Favorite models": "收藏的模型",
    "File Path": "文件路径",
    "File type not supported": "不支持的文件类型",
    "Generating diagram...": "正在生成图表…",
    "Go Home": "回到主页",
    "Hello there": "你好",
    "Include sensitive data": "包含敏感数据",
    "Include sensitive data (not recommended)": "包含敏感数据（不推荐）",
    "Input": "输入",
    "KV cache total": "KV 缓存总量",
    "Loaded models": "已加载模型",
    "Loading model information...": "正在加载模型信息…",
    "Loading model...": "正在加载模型…",
    "Loading models…": "正在加载模型…",
    "Loading tools...": "正在加载工具…",
    "MCP Resources": "MCP 资源",
    "MCP Servers": "MCP 服务器",
    "MCP Tools": "MCP 工具",
    "Maximum reasoning effort with extended context usage": "最高推理强度，占用更多上下文",
    "Media attachment not found in message extras": "在该消息的附加数据中找不到媒体附件",
    "Messages": "消息",
    "Modalities": "模态类型",
    "Model": "模型",
    "New chat": "新建对话",
    "No PDF pages available": "没有可用的 PDF 页面",
    "No content available": "暂无内容",
    "No context info available": "暂无可用的上下文信息",
    "No edits": "没有修改",
    "No matches": "没有匹配项",
    "No matching folders": "没有匹配的文件夹",
    "No model": "无模型",
    "No model information available": "暂无可用的模型信息",
    "No models available.": "没有可用模型。",
    "No models found.": "未找到模型。",
    "No output": "无输出",
    "No resources": "无资源",
    "No results": "无结果",
    "No tools available": "没有可用工具",
    "Open file mention picker": "打开文件提及选择器",
    "Open working directory picker": "打开工作目录选择器",
    "Output": "输出",
    "Pinned": "已置顶",
    "Preview not available for this file type": "该文件类型不支持预览",
    "Prompt tokens:": "提示词元数：",
    "Read file": "读取文件",
    "Read media": "读取媒体",
    "Reasoning": "思考过程",
    "Receiving arguments...": "正在接收参数…",
    "Recent conversations": "最近的对话",
    "Recommended Servers": "推荐的服务器",
    "Reconnecting to the stream...": "正在重新连接数据流…",
    "Rendering svg...": "正在渲染 SVG…",
    "Requested:": "请求：",
    "Resolved URI:": "解析后的 URI：",
    "Resources": "资源",
    "Response was truncated": "回复被截断",
    "Run llama-server with": "使用以下命令运行 llama-server",
    "Running...": "运行中…",
    "Search results": "搜索结果",
    "Searching in:": "搜索范围：",
    "Searching...": "正在搜索…",
    "See parent conversation": "查看父对话",
    "Select a resource to preview": "选择一个资源进行预览",
    "Select an available model:": "选择一个可用模型：",
    "Select model": "选择模型",
    "Send": "发送",
    "Server Connection Error": "服务器连接错误",
    "Server Tools": "服务器工具",
    "Server URL": "服务器 URL",
    "Server instructions": "服务器说明",
    "Settings": "设置",
    "Show raw output": "显示原始输出",
    "Skip reasoning": "跳过思考过程",
    "Start the llama-server:": "启动 llama-server：",
    "Stop": "停止",
    "Stop generation": "停止生成",
    "System Message": "系统消息",
    "Templates": "模板",
    "The selected model does not support vision. Only the extracted": "所选模型不支持视觉，仅提取的",
    "These files have been automatically removed from your attachments": "以下文件已自动从附件中移除",
    "This model supports:": "该模型支持：",
    "This turn · KV cache": "本轮 · KV 缓存",
    "Toggle content": "展开/折叠内容",
    "Token usage details": "词元用量详情",
    "Tool": "工具",
    "Tool use": "工具调用",
    "Tools": "工具",
    "Total matches:": "匹配总数：",
    "Troubleshooting": "故障排查",
    "Unsupported File Types": "不支持的文件类型",
    "Update without re-sending": "更新且不重新发送",
    "Use llama-server proxy": "使用 llama-server 代理",
    "Verify your network connection": "检查网络连接",
    "Video": "视频",
    "Video preview not available": "视频预览不可用",
    "Vision": "视觉",
    "Waiting for file content...": "正在等待文件内容…",
    "Waiting for media data...": "正在等待媒体数据…",
    "Waiting for result...": "正在等待结果…",
    "Waiting for runtime info...": "正在等待运行时信息…",
    "What happened:": "发生了什么：",
    "Working directory cleared": "工作目录已清空",
    "Write file": "写入文件",
    "You can try uploading files with content instead": "你可以改为上传有内容的文件",
    "Your browser does not support the audio element.": "你的浏览器不支持音频播放。",
    "Your browser does not support the video element.": "你的浏览器不支持视频播放。",
    "timed out": "已超时",
    "will be sent to the model.": "将发送给模型。",
    "✓ API key validated successfully! Connecting...": "✓ API 密钥验证成功，正在连接…",
}

# 单引号写法下的属性（内容含双引号，故源码用单引号包裹）
SINGLE = [
    ('label', {
        'Enable "Continue" button': '启用「继续」按钮',
    }),
    ('help', {
        'Display full raw model identifiers (e.g. "ggml-org/GLM-4.7-Flash-GGUF:Q8_0") instead of parsed names with badges.':
            '显示完整的原始模型标识符（例如 "ggml-org/GLM-4.7-Flash-GGUF:Q8_0"），而不是解析后的名称加标签。',
        'Display model tags (e.g. "vision", "reasoning") next to model names throughout the interface.':
            '在界面各处的模型名旁显示模型标签（如 "vision"、"reasoning"）。',
        'Display per-turn statistics (tokens, duration) under each turn in agentic responses. Shown only when "Show message generation statistics" is enabled.':
            '在智能体回复的每一轮下方显示该轮统计（词元数、耗时）。仅在开启「显示消息生成统计」时生效。',
        'Enable "Continue" button for assistant messages, including reasoning models.':
            '为助手消息（含推理模型）启用「继续」按钮。',
        'Pre-load nerdamer in the sandbox for symbolic computation: simplify, diff, integrate, solve, and more. Requires "JavaScript sandbox tool" to be enabled.':
            '在沙箱中预加载 nerdamer 以进行符号运算：化简、求导、积分、求解等。需先启用「JavaScript 沙箱工具」。',
        'The order at which samplers are applied, in simplified way. Default is "top_k;typ_p;top_p;min_p;temperature": top_k->typ_p->top_p->min_p->temperature':
            '采样器的应用顺序（简化表示）。默认为 "top_k;typ_p;top_p;min_p;temperature"，即 top_k → typ_p → top_p → min_p → temperature。',
    }),
]

# 独立双引号字符串常量
PLAIN = {
    "Search": "搜索",
    "Add files, prompts, tools or MCP Servers": "添加文件、提示词、工具或 MCP 服务器",
    "Type a message...": "输入消息…",
    "Reset to default": "恢复默认",
    "Enable \"Continue\" button": "启用「继续」按钮",
}

# ============ 第三阶段：按钮文字 / 无障碍标签 / 动态拼接 ============
BTN = {
    "Export conversations": "导出对话",
    "Import conversations": "导入对话",
    "Delete all conversations": "删除所有对话",
    "Export settings": "导出设置",
    "Import settings": "导入设置",
    "Delete conversation": "删除对话",
}

SR = {
    "Open command picker": "打开命令选择器",
    "Open prompt picker": "打开提示词选择器",
}

ARIA = {
    "Scroll left": "向左滚动",
    "Scroll right": "向右滚动",
    "Settings": "设置",
    "Notifications alt+T": "通知",
}

DESCRIPTION.update({
    "Permanently delete all conversations and their messages. This action cannot be undone. Consider exporting your conversations first if you want to keep a backup.":
        "永久删除所有对话及其消息。此操作无法撤销。如果想保留备份，建议先导出对话。",
})

PLAIN.update({
    "Go to start": "回到开头",
    "Expand navigation": "展开导航",
})

TOOLTIP.update({
    "Settings": "设置",
})

# 长且唯一的原文，任意位置直接替换
RAW = [
    ("Settings are saved in browser's localStorage", "设置保存在浏览器的 localStorage 中"),
    ("Record audio, type a message ", "录制音频、输入消息"),
    ("Type a message", "输入消息"),
    ("<!> Reload app", "<!> 重新加载应用"),
    ("Set the API Key if you are using ", "若你使用了服务端的 "),
    ("</code> option for the server.", "</code> 选项，请在此设置 API 密钥。"),
    ('"Disable":"Enable"', '"禁用":"启用"'),
    ('tool${d.totalToolCount!==1?"s":""}', '个工具'),
    ('tool${l().tools.length!==1?"s":""}', '个工具'),
    ('tool${E(p).tools.length!==1?"s":""}', '个工具'),
    ('[bn.BROWSER]:"Browser"', '[bn.BROWSER]:"浏览器"'),
    ('[bn.BROWSER]:"Browser Tools"', '[bn.BROWSER]:"浏览器工具"'),
    ('[bn.CUSTOM]:"Custom Tools"', '[bn.CUSTOM]:"自定义工具"'),
    ('[bn.SERVER]:"Server Tools"', '[bn.SERVER]:"服务器工具"'),
    ('[bn.SERVER]:"Server"', '[bn.SERVER]:"服务器"'),
    ('"containerAriaLabel",3,"Notifications"', '"containerAriaLabel",3,"通知"'),
    ('"closeButtonAriaLabel",3,"Close toast"', '"closeButtonAriaLabel",3,"关闭提示"'),
    ("Reset to default", "恢复默认"),
]

# 正则替换（处理不定空白等）
REGEX = [
    (r'\s+or upload\s+files to get started', '，或上传文件即可开始'),
]

CTX = [
    ('gr', GR, 'call'),
    ('placeholder', PLACEHOLDER, 'attr'),
    ('title', TITLE, 'attr'),
    ('tooltip', TOOLTIP, 'attr'),
    ('label', LABEL, 'attr'),
    ('help', HELP, 'attr'),
    ('message', MESSAGE, 'attr'),
    ('error', ERROR, 'attr'),
    ('note', NOTE, 'attr'),
    ('description', DESCRIPTION, 'attr'),
    ('buttonText', BTN, 'attr'),
    ('srLabel', SR, 'attr'),
    ('"aria-label"', ARIA, 'attr'),
]


def main():
    ensure_ui()
    bundle_path = os.path.join(SRC, BUNDLE)
    t = open(bundle_path, encoding='utf-8').read()
    orig_len = len(t)

    report = []
    for ctx, mapping, kind in CTX:
        for en, zh in mapping.items():
            key = f'{ctx}("{en}")' if kind == 'call' else f'{ctx}:"{en}"'
            if key not in t:
                report.append(('MISS', ctx, en))
                continue
            n = t.count(key)
            new = (f'{ctx}(' + json.dumps(zh, ensure_ascii=False) + ')') if kind == 'call' \
                else (f'{ctx}:' + json.dumps(zh, ensure_ascii=False))
            t = t.replace(key, new)
            report.append(('OK', ctx, f'{n}x  {en} -> {zh}'))

    # ---- 第二阶段 ----
    # 单引号属性
    for attr, mapping in SINGLE:
        for en, zh in mapping.items():
            key = f"{attr}:'{en}'"
            if key not in t:
                report.append(('MISS', attr + "'", en))
                continue
            t = t.replace(key, f"{attr}:'{zh}'")
            report.append(('OK', attr + "'", en))

    # 独立双引号常量（先于 RAW，避免 "Type a message..." 被 RAW 截断）
    for en, zh in PLAIN.items():
        key = json.dumps(en, ensure_ascii=False)
        if key not in t:
            report.append(('MISS', 'plain', en))
            continue
        n = t.count(key)
        t = t.replace(key, json.dumps(zh, ensure_ascii=False))
        report.append(('OK', 'plain', f'{n}x  {en}'))

    # 模板中的 >文本<（容忍前后空白）
    for en, zh in TEMPLATE.items():
        pat = re.compile(r'>(\s*)' + re.escape(en) + r'(\s*)<')
        m = pat.search(t)
        if not m:
            report.append(('MISS', 'template', en))
            continue
        n = len(pat.findall(t))
        t = pat.sub(lambda mm: '>' + mm.group(1) + zh + mm.group(2) + '<', t)
        report.append(('OK', 'template', f'{n}x  {en}'))

    # 长且唯一的原文，任意位置替换
    for en, zh in RAW:
        if en not in t:
            report.append(('MISS', 'raw', en))
            continue
        n = t.count(en)
        t = t.replace(en, zh)
        report.append(('OK', 'raw', f'{n}x  {en}'))

    # 正则替换
    for pat, zh in REGEX:
        m = re.search(pat, t)
        if not m:
            report.append(('MISS', 'regex', pat))
            continue
        t = re.sub(pat, zh, t)
        report.append(('OK', 'regex', f'{pat} -> {zh}'))

    if os.path.exists(DST):
        shutil.rmtree(DST)
    shutil.copytree(SRC, DST)
    open(os.path.join(DST, BUNDLE), 'w', encoding='utf-8').write(t)

    # ---- 处理 Service Worker：它会把旧版 bundle 一直缓存住，导致看不到汉化 ----
    # 不改变 bundle 文件名（避免旧缓存 HTML 引用到已删除文件而白屏），
    # 改为用"自我注销"的 sw.js 把已有 SW 顶掉，并在页面里禁止再次注册。
    idx_path = os.path.join(DST, 'index.html')
    html = open(idx_path, encoding='utf-8').read()

    disable_sw = (
        "<script>"
        "(function(){"
        "if('serviceWorker' in navigator){"
        "navigator.serviceWorker.getRegistrations().then(function(rs){"
        "rs.forEach(function(r){r.unregister();});});"
        "navigator.serviceWorker.register=function(){"
        "return Promise.reject(new Error('sw disabled'));};}"
        "if(window.caches){caches.keys().then(function(ks){"
        "ks.forEach(function(k){caches.delete(k);});});}"
        "})();"
        "</script>\n"
    )
    html = html.replace('<head>', '<head>\n' + disable_sw, 1)
    html = html.replace('<html lang="en">', '<html lang="zh-CN">')
    open(idx_path, 'w', encoding='utf-8').write(html)

    # 自我注销的 SW：安装即 skipWaiting，激活时注销自己、清空缓存并刷新页面
    self_destruct_sw = (
        "self.addEventListener('install',function(){self.skipWaiting();});\n"
        "self.addEventListener('activate',function(e){e.waitUntil((async function(){\n"
        "try{await self.registration.unregister();}catch(err){}\n"
        "try{var ks=await caches.keys();await Promise.all(ks.map(function(k){return caches.delete(k);}));}catch(err){}\n"
        "try{var cs=await self.clients.matchAll({type:'window'});cs.forEach(function(c){c.navigate(c.url);});}catch(err){}\n"
        "})());});\n"
    )
    open(os.path.join(DST, 'sw.js'), 'w', encoding='utf-8', newline='\n').write(self_destruct_sw)
    wb = os.path.join(DST, 'workbox-b3c04f83.js')
    if os.path.exists(wb):
        os.remove(wb)
    print('service worker neutralized (self-unregistering sw.js written)')

    ok = sum(1 for r in report if r[0] == 'OK')
    miss = [r for r in report if r[0] == 'MISS']
    print(f'replaced groups: {ok}, missing: {len(miss)}')
    print(f'bundle {orig_len} -> {len(t)} chars')
    if miss:
        print('\n--- MISSING (未找到，需检查) ---')
        for _, ctx, en in miss:
            print(f'  [{ctx}] {en}')


if __name__ == '__main__':
    main()