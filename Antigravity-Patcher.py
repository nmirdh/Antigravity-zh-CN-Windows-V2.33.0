# coding: utf-8
import os
import json
import struct
import subprocess
import shutil
import sys

if sys.platform == "win32":
    APP_DIR = os.path.join(os.getenv('LOCALAPPDATA', ''), 'Programs', 'antigravity')
    RESOURCES_DIR = os.path.join(APP_DIR, "resources")
elif sys.platform == "darwin":
    APP_DIR = "/Applications/Antigravity.app"
    RESOURCES_DIR = os.path.join(APP_DIR, "Contents", "Resources")
else:
    print("[错误] 当前仅支持 Windows 和 macOS 系统。")
    sys.exit(1)

ASAR_PATH = os.path.join(RESOURCES_DIR, "app.asar")
UNPACKED_APP_DIR = os.path.join(RESOURCES_DIR, "app")

DOM_TRANSLATOR_INJECTION = r"""
// Antigravity Chinese Localization Engine
(function() {
  const dictionary = {
    // Top Bar & Global Navigation
    "Goals": "目标", "Tasks": "任务", "Artifacts": "产物", "Artifact": "产物", "Scratch": "草稿", "Chat": "对话",
    "No artifacts generated": "暂无生成的产物", "No artifacts": "暂无产物",
    "Active": "进行中", "Inactive": "未激活", "Completed": "已完成", "Failed": "已失败",
    "History": "历史记录", "Settings": "设置", "System": "系统", "Network": "网络",
    "Model": "模型", "Memory": "记忆", "Tools": "工具", "Agents": "智能体",
    "Overview": "概览", "Logs": "日志", "Clear": "清除", "Save": "保存",
    "Cancel": "取消", "Submit": "提交", "Run": "运行", "Stop": "停止",
    "Edit": "编辑", "Delete": "删除", "Add": "添加", "Remove": "移除", "Download": "下载",
    "Monthly Limit": "每月限额", "Weekly Limit": "每周限额", "Five Hour Limit": "五小时限额",
    "Weekly Limit Remaining": "每周限额剩余", "Five Hour Limit Remaining": "五小时限额剩余",
    "limit": "限额", "limits": "限额", "weekly": "每周", "hourly": "每小时",
    "Sidebar": "侧边栏", "Display Options": "显示选项", "Message input": "消息输入框", "Record voice memo": "录制语音备忘",
    "Typeahead menu": "预输入菜单", "Group By": "分组方式", "Last Updated": "最后更新", "Last Prompt": "最新提示词", "Last prompt": "最新提示词",
    "Alphabetical (A-Z)": "字母顺序 (A-Z)", "Alphabetical (Z-A)": "字母倒序 (Z-A)", "Date Added": "添加日期", "Creation Date": "创建日期", "Created Date": "创建日期", "Subtitles": "副标题", "No Subtitle": "无副标题",
    "Filter": "筛选", "Scheduled": "已计划", "Environment": "环境", "None": "无", "Fast": "快速",
    "Last 7 days": "最近 7 天", "Last 24 hours": "最近 24 小时", "Last 30 days": "最近 30 天", "Last 3 months": "最近 3 个月",
    "Today": "今天", "Yesterday": "昨天", "This week": "本周", "This month": "本月", "All time": "全部时间",
    "Project": "项目", "project": "项目", "projects": "项目", "Conversation": "对话", "conversation": "对话",
    "No Project": "无项目", "No project": "无项目", "no project": "无项目",
    "No projects found": "暂无项目", "No projects found.": "暂无项目",
    "No project found": "暂无项目", "No project found.": "暂无项目",
    "found": "找到", "not found": "未找到", "Not found": "未找到",
    "Search projects": "搜索项目", "Search projects...": "搜索项目...",
    "Workspace": "工作区", "workspace": "工作区", "Minimize": "最小化", "Maximize": "最大化", "Back": "返回",
    "Folders": "文件夹", "folders": "文件夹", "including": "包括",
    "Rename": "重命名", "Mark Unread": "标记为未读", "Mark Read": "标记为已读", "Duplicate": "制作副本",
    "Export": "导出", "Import": "导入", "Pin": "置顶", "Archive": "归档",
    "Split": "分屏", "Split Right": "向右分屏", "Split Down": "向下分屏", "Split Left": "向左分屏", "Split Up": "向上分屏",
    "Replace With New": "替换为新建", "Replace with New": "替换为新建", "Replace with new": "替换为新建",
    "Copy Link": "复制链接", "Copy link": "复制链接", "Copy ID": "复制 ID", "Copy id": "复制 ID",
    "Copy Conversation ID": "复制对话 ID", "Copy Conversation Link": "复制对话链接", "Duplicate Conversation": "复制对话",
    "Close Others": "关闭其他", "Close All": "全部关闭", "Close to the Right": "关闭右侧", "Close Saved": "关闭已保存",
    "Create New Project": "创建新项目", "Archive Conversation": "归档对话", "now": "刚刚",
    "Conversation Name": "对话名称", "Conversation ID": "对话 ID", "Project Name": "项目名称",
    "Toggle Auxiliary Pane": "切换辅助面板", "Maximize Pane": "最大化面板", "Minimize Pane": "最小化面板", "Restore Pane": "还原面板",
    "Files Changed": "已修改文件", "Files changed": "已修改文件", "File Changed": "已修改文件",
    "Uploads": "已上传文件", "uploads": "已上传文件", "See all": "查看全部", "See All": "查看全部",
    "Background Tasks": "后台任务", "Background tasks": "后台任务", "Background Task": "后台任务",
    "Terminals": "终端", "terminals": "终端", "Delete Terminal": "删除终端", "Split Terminal": "拆分终端",
    "Add Terminal": "添加终端", "Add terminal": "添加终端",
    "No subagents": "暂无子智能体", "No subagents running": "暂无运行中的子智能体", "No subagent": "暂无子智能体",
    "Select Model": "选择模型", "Select model": "选择模型", "Select a model": "选择一个模型",
    "User cancelled agent execution.": "用户取消了智能体执行。",
    "Open Antigravity IDE": "打开 Antigravity IDE", "Create Project": "创建项目", 
    "Command Palette": "命令面板", "Zoom In": "放大", "Zoom Out": "缩小", "Reset Zoom": "重置缩放",
    "Delete Conversation": "删除对话", "Are you sure you want to delete this conversation? This action cannot be undone.": "您确定要删除此对话吗？此操作无法撤销。",
    "Confirm Undo": "确认撤销", "This undo action will not make any code changes.": "此撤销操作不会对代码做出任何更改。",
    "Confirm Redo": "确认重做", "This redo action will not make any code changes.": "此重做操作不会对代码做出任何更改。",
    "Undo changes up to this point": "撤销更改至此处", "Redo changes up to this point": "重做更改至此处",
    "Confirming this undo action will make the following changes:": "确认此撤销操作将做出以下更改：",
    "Confirming this undo action will not make any code changes.": "确认此撤销操作不会做出任何代码更改。",
    "Confirming this redo action will make the following changes:": "确认此重做操作将做出以下更改：",
    "Confirming this redo action will not make any code changes.": "确认此重做操作不会做出任何代码更改。",
    "Undo changes": "撤销更改", "Redo changes": "重做更改",
    "Record Audio": "录制音频", "Record Audio Ctrl+M": "录制音频 Ctrl+M",
    "Send message": "发送消息", "Send message Enter": "发送消息 Enter",
    "Getting started with a Project": "开始使用项目",
    "Now that you've created a project, configure your project's agent settings or start a conversation.": "现在您已经创建了一个项目，接下来请配置该项目的智能体设置，或者直接开始对话。",
    "Open Settings": "打开设置", "Start first conversation": "开始首次对话",
    "Main Agent": "主智能体", "Add Context": "添加上下文",
    "Loading Antigravity": "正在加载 Antigravity", "Loading": "正在加载",
    "+ New Conversation": "+ 新建对话", "New Conversation": "新建对话", "Conversation History": "历史对话", "Scheduled Tasks": "计划任务",
    "Automations": "自动化", "Automation": "自动化",
    "Open File": "打开文件", "New Terminal": "新建终端", "just now": "刚刚", "Just now": "刚刚",
    "No conversations yet": "暂无对话", "Open IDE": "打开 IDE", "Window": "窗口",
    "Review": "审阅", "Email": "电子邮箱", "Upgrade": "升级", "Not in Project": "未分组项目",
    "Ask anything, @ to mention, / for actions": "输入任何问题，使用 @ 提及，使用 / 执行操作",
    "Ask anything, @ to mention": "输入任何问题，使用 @ 提及",
    "Message subagent, @ to mention": "向子智能体发送消息，使用 @ 提及",
    "Message subagent, @ to mention, / for actions": "向子智能体发送消息，使用 @ 提及，使用 / 执行操作",
    "Message this chat": "在此对话中发送消息",
    "Ask a side question without interrupting the main conversation": "在不打断主对话的情况下提出旁支问题",
    "Ask a quick question without interrupting the main conversation.": "在不打断主对话的情况下快速提问。",
    "Stop Side Question": "停止旁支提问", "Promote to conversation": "升级为独立对话",
    "Status": "状态", "Sort Conversations": "对话排序", "Worktree": "工作区树",
    "New Project": "新建项目", "Quick Start": "快速开始",
    "Good response": "好的回答", "Bad response": "差的回答",
    "Fork": "分支对话", "Fork Conversation": "创建分支对话", "Fork in Shared Workspace": "在共享工作区中分支",
    "Fork in New Workspace": "在新工作区中分支", "Fork conversation in this folder": "在此文件夹中创建分支对话",
    "Keeps working in this folder. Nothing is copied.": "继续在此文件夹中工作，不会复制任何文件。",
    "Manifest Changes": "清单更改", "Agent Edits": "智能体编辑", "Staged Changes": "已暂存更改", "Branch Changes": "分支更改",
    "Documents": "文档", "Subagents": "子智能体", "Standalone Terminals": "独立终端", "Web Preview": "网页预览",
    "Commit": "提交", "Amend": "修正提交", "Push": "推送", "Stage change": "暂存更改", "Unstage change": "取消暂存更改",
    "Discard unstaged changes": "放弃未暂存的更改", "Include unstaged changes": "包含未暂存的更改",
    "Stage All": "全部暂存", "Unstage All": "全部取消暂存", "Commit Message": "提交信息",
    "Enter commit message...": "输入提交信息...", "Generate commit message": "生成提交信息",
    "Chief of Staff": "幕僚长", "Chief of Staff Dashboard": "幕僚长看板", "Welcome to your Chief of Staff": "欢迎使用您的幕僚长",
    "What should the agent do on each run?": "每次运行时智能体应该做什么？",
    "Where should it run?": "应该在哪里运行？", "When should it run?": "应该在何时运行？",
    "On a schedule": "按计划定时运行", "When something happens": "当特定事件发生时",
    "Every hour": "每小时", "Every day": "每天", "Every weekday": "每个工作日", "Every week": "每周",
    "Refresh all credentials": "刷新所有凭据",
    "Background tasks and terminals agents left running, across all conversations.": "跨所有对话中智能体保持运行的后台任务和终端。",
    "Nothing is running right now": "当前没有正在运行的任务",

    // General Settings Page & v2.29.0 Settings
    "General": "常规", "Appearance": "外观", "Theme": "主题", "Light": "浅色", "Dark": "深色",
    "Language": "语言", "Version": "版本", "Check for Updates": "检查更新", "About": "关于",
    "Advanced": "高级", "API Key": "API 密钥", "Account": "账号", "Profile": "个人资料",
    "Logout": "退出登录", "Sign Out": "退出登录", "Feedback": "反馈", "Privacy": "隐私",
    "Terms": "条款", "Auto-start": "开机自启", "Launch on startup": "开机时启动",
    "Notifications": "通知", "Shortcuts": "快捷键", "Keyboard Shortcuts": "键盘快捷键",
    "Global Shortcut": "全局快捷键", "Toggle Visibility": "切换显示/隐藏", "Proxy": "代理",
    "Update": "更新", "Updates": "更新", "Check for update": "检查更新",
    "Models": "模型", "Customizations": "自定义", "Browser": "浏览器", "App": "应用", "Application": "应用", "Applications": "应用",
    "Projects": "项目", "Conversations": "对话", "Workspaces": "工作区", "Provide Feedback": "提供反馈",
    "Manage your plan, credentials, and general preferences.": "管理您的套餐、凭据和常规偏好设置。",
    "Enable Telemetry": "启用遥测",
    "When toggled on, Antigravity collects usage data to help Google enhance performance and features.": "开启后，Antigravity 将收集使用数据，以帮助 Google 提升性能和功能。",
    "Marketing Emails": "营销邮件",
    "Receive product updates, tips, and promotions from Google Antigravity via email.": "通过电子邮件接收来自 Google Antigravity 的产品更新、提示和促销信息。",
    "Your Plan: Google AI Pro": "当前计划：Google AI Pro", "Your Plan: Google AI Ultra": "当前计划：Google AI Ultra", "Your Plan:": "当前计划：",
    "You can upgrade to a Google AI Ultra plan to receive higher rate limits.": "您可以升级至 Google AI Ultra 套餐以获得更高的使用限额。",
    "By using this app, you agree to its": "使用本应用即表示您同意其",
    "Terms of Service": "服务条款",
    "Remote Agents Data": "远程智能体数据", "Delete All Remote Agents Data": "删除所有远程智能体数据",
    "Delete All Data": "删除所有数据", "Delete All Remote Agents Data?": "确定删除所有远程智能体数据？",
    "Permanently delete your remote conversations, projects, scheduled tasks, connected plugins and settings. Data in the desktop app and your Google account are not affected.": "永久删除您的远程对话、项目、计划任务、已连接插件和设置。桌面应用中的数据和您的 Google 账号不受影响。",
    "Managed by Enterprise Gateway": "由企业网关管理", "Authenticated via Enterprise Gateway": "已通过企业网关认证",
    "Configure agent execution, queued message delivery, and permissions.": "配置智能体执行、排队消息发送以及权限。",
    "Execution": "执行", "Agent Settings": "智能体设置", "Agent Behavior": "智能体行为",
    "File Permissions": "文件权限", "Network Permissions": "网络权限",
    "Queued Messages": "排队消息", "Configure when follow-up messages are sent.": "配置发送后续消息的时机。",
    "Interrupt the agent and send immediately.": "打断智能体并立即发送。",
    "Queue until after the current turn.": "排队等待至当前轮次结束后发送。",
    "Enter to Send": "按 Enter 键发送", "Send messages with the keyboard's Enter key instead of starting a new line.": "使用键盘的 Enter 键发送消息，而不是换行。",
    "Queue": "排队", "Send Immediately": "立即发送", "Keyboard shortcuts": "键盘快捷键",
    "New Conversation Button": "新建对话按钮", "Which workspace the New Conversation button and keyboard shortcut start you in.": "设置点击“新建对话”按钮或使用快捷键时默认进入的工作区。",
    "New Workspace": "新建工作区", "Create a new workspace from your first message.": "根据您的第一条消息创建一个新工作区。",
    "Start without a workspace, for general questions.": "在不使用工作区的情况下开始，适用于常规提问。",
    "Last Workspace": "上次使用的工作区", "Reuse your last workspace.": "重用您上次使用的工作区。",
    "Command Setup Script": "命令初始化脚本", "A shell setup script run before every command the agent executes.": "在智能体执行每条命令之前运行的 Shell 初始化脚本。",
    "Validate": "验证", "Validating setup script…": "正在验证初始化脚本…", "Setup script ran successfully.": "初始化脚本运行成功。", "Setup script failed.": "初始化脚本运行失败。",
    "Permission Preset": "权限预设", "Permission Settings": "权限设置", "Permissions": "权限",
    "Cloud Permissions": "云端权限", "Permission Details": "权限详情",
    "This Computer": "此电脑", "Remote": "远程",
    "Every command requires approval.": "每条命令都需要批准。",
    "Ask before sensitive operations.": "在执行敏感操作前询问。",
    "Auto (Preview)": "自动 (预览版)", "Automatically decide if commands run.": "自动决定是否运行命令。",
    "Turbo": "极速 (Turbo)", "Run all commands without restrictions.": "无限制地运行所有命令。",
    "Terminal Command Auto Execution": "终端命令自动执行",
    "Require Review": "需要审阅", "Proceed in Sandbox": "在沙盒中自动执行", "Auto": "自动",
    "Controls whether terminal commands require your approval before running.": "控制终端命令在运行前是否需要您的批准。",
    "Note: A change to this setting will only apply to new messages sent to the agent. In-progress responses will use the previous setting value.": "注意：对此设置的更改仅适用于发送给智能体的新消息。正在进行的回复将继续使用之前的设置值。",
    "The agent never asks for confirmation before executing terminal commands (except those in the Deny list). This provides the agent with the maximum ability to operate over long periods without intervention, but also has the highest risk of the agent executing an unsafe terminal command.": "智能体在执行终端命令前从不请求确认（拒绝列表中的命令除外）。这赋予了智能体在无需人工干预的情况下长时间运行的最大能力，但也存在执行不安全终端命令的最高风险。",
    "Terminal commands automatically proceed inside the sandbox. A command that needs to leave the sandbox proceeds only if an agent judges it reversible, and otherwise requests review.": "终端命令在沙盒内会自动执行。需要脱离沙盒运行的命令仅在智能体判断其可逆时才会自动执行，否则将请求审阅。",
    "The agent always asks for confirmation before executing terminal commands (except those in the Allow list).": "智能体在执行终端命令前总是请求确认（允许列表中的命令除外）。",
    "Terminal command automatically proceeds if the command runs inside the sandbox. Otherwise, it requests review.": "如果终端命令在沙盒内运行则自动执行，否则将请求审阅。",
    "Enable Sandbox Mode": "启用沙盒模式", "Restricts agent tools to a secure, isolated local sandbox.": "将智能体工具限制在安全、隔离的本地沙盒中运行。",
    "Enable Terminal Sandbox": "启用终端沙盒", "Run terminal commands with sandbox restrictions.": "在沙盒限制下运行终端命令。",
    "Sandbox Allow Network": "允许沙盒访问网络", "Allow sandboxed commands to make network requests.": "允许沙盒中的命令发起网络请求。",
    "Agent Non-Workspace File Access": "智能体非工作区文件访问", "Outside of folders file access policy": "工作文件夹外的文件访问策略",
    "Configures how the agent tries to access files outside of its working folders.": "配置智能体尝试访问其工作文件夹之外的文件时的策略。",
    "Modify permissions for file and terminal tools.": "修改文件和终端工具的权限。",
    "Configure what the agent can do in local and remote conversations.": "配置智能体在本地和远程对话中可以执行的操作。",
    "Configure global allowed and denied resource permissions.": "配置全局允许和拒绝的资源权限。",
    "Controls permissions for remote conversations.": "控制远程对话的权限。",
    "Security Preset": "安全预设", 
    "Choose a predefined security preset for the agent. This controls terminal auto-execution policy, and file access policy.": "为智能体选择一个预定义的安全预设。这将控制终端自动执行策略和文件访问策略。",
    "Controls the actions the agent can take.": "控制智能体可以执行的操作。",
    "Controls the actions the agent can take": "控制智能体可以执行的操作",
    "Global Permissions": "全局权限", "Global permissions": "全局权限",
    "Tool Permissions": "工具权限", "Tool permissions": "工具权限",
    "Modify permissions for file, terminal, and MCP tools.": "修改文件、终端和 MCP 工具的权限。",
    "Modify permissions for file, terminal, and MCP tools": "修改文件、终端和 MCP 工具的权限",
    "Default": "默认", "Always Ask": "总是询问", "Always Proceed": "自动执行",
    "Inherit Global": "继承全局", "Inherits Global": "继承全局", "inherit global": "继承全局",
    "Inherits your Global Permissions when working in this project.": "在此项目中工作时继承您的全局权限。",
    "Inherits your Global Permissions when working in this project": "在此项目中工作时继承您的全局权限",
    "Inherits your Global Permissions": "继承您的全局权限",
    "Plan Review Policy": "计划审阅策略",
    "Whether the agent asks you to review its documents.": "智能体是否要求您审阅其文档。",
    "Whether the agent asks you to review its documents": "智能体是否要求您审阅其文档",
    "Type / and select plan to have the agent generate a plan.": "输入 / 并选择 plan 即可让智能体生成计划。",
    "Type / and select plan to have the agent generate a plan": "输入 / 并选择 plan 即可让智能体生成计划",
    "to have the agent generate a plan.": "即可让智能体生成计划。",
    "to have the agent generate a plan": "即可让智能体生成计划",
    "and select": "并选择",
    "Artifact Review Policy": "产物审阅策略",
    "Specifies Agent's behavior when asking for review on artifacts, which are documents it creates to enable a richer conversation experience.": "指定智能体在请求审阅产物时的行为。产物是指其为提供更丰富对话体验而创建的各类文档与生成物。",
    "File Access Rules": "文件访问规则", "Configure allowed and denied paths for file reads and writes.": "配置允许和拒绝的文件读取和写入路径。",
    "Network Access Rules": "网络访问规则", "Configure allowed and denied URLs for reading.": "配置允许和拒绝读取的 URL。",
    "File Reads": "文件读取", "Allow/deny agent read access to specific files or directories.": "允许/拒绝智能体对特定文件或目录的读取权限。",
    "File Writes": "文件写入", "Allow/deny agent write access to specific files or directories.": "允许/拒绝智能体对特定文件或目录的写入权限。",
    "Network Reads": "网络读取", "Allow/deny agent read access to specific URLs.": "允许/拒绝智能体对特定 URL 的读取权限。",
    "Read URLs": "URL 读取", "Allow/deny agent read access to specific URLs or domains.": "允许/拒绝智能体对特定 URL 或域名的读取权限。",
    "Allow/deny specific terminal commands.": "允许/拒绝特定的终端命令。", "e.g., npm test": "例如：npm test",
    "External tools the agent can call via Model Context Protocol.": "智能体可通过模型上下文协议 (MCP) 调用的外部工具。", "Enter tool name or server...": "输入工具名称或服务器...",
    "Allow/deny agent command execution outside the sandbox.": "允许/拒绝智能体在沙盒外部执行命令。", "e.g., curl": "例如：curl",
    "Allow": "允许", "Deny": "拒绝", "There are no customizations enabled.": "当前未启用任何自定义项。",
    "Manage Antigravity app settings.": "管理 Antigravity 应用设置。",
    "Inherits your General settings when working in this project.": "在此项目中工作时继承您的全局设置。",
    "No MCP servers installed": "未安装任何 MCP 服务器", "Use Add MCP to browse the store, or add a custom server via the MCP config.": "使用“添加 MCP”浏览商店，或通过 MCP 配置添加自定义服务器。",
    "Plugins": "插件", "Browse and enable plugins from the Build With Google catalog.": "浏览并启用“使用 Google 构建”目录中的插件。",
    "Cloud CLI MCP Server provides tools to run gcloud and bq CLIcommands in a remote sandbox environment": "Cloud CLI MCP 服务器提供了在远程沙盒环境中运行 gcloud 和 bq CLI 命令的工具。",
    "Browser Actuation Permissions": "浏览器操作权限", "Execute URLs": "URL 执行", "Allow/deny agent browser actuation access to specific URLs.": "允许/拒绝智能体对特定 URL 的浏览器操作权限。",
    "Media": "媒体", "Mentions": "提及", "Actions": "操作",
    "Enable Remote Control": "启用远程控制", "Work with local agents from another device.": "在其他设备上与本地智能体协同工作。",
    "Enter Queues after the turn": "Enter 键：在当前轮次后排队",
    "Alt+Enter Sends immediately": "Alt+Enter 键：立即发送",
    "Alt+Enter On empty prompt, sends next in queue": "Alt+Enter 键：在输入为空时，发送队列中的下一条",
    "Useful for typical development with an emphasis on security. It prioritizes safety over speed by requiring manual approval for all terminal commands and files outside the project directory.": "适用于注重安全的典型开发场景。它将安全性置于速度之上，要求对所有终端命令和项目目录之外的文件访问进行手动批准。",
    "Requires manual review for all terminal commands and file accesses outside of the working folders.": "要求对所有终端命令和工作文件夹之外的文件访问进行手动审阅。",
    "Full machine": "完整机器访问",
    "All terminal commands require review. The agent can read or write to any file in the machine.": "所有终端命令均需审阅。智能体可以读取或写入机器上的任何文件。",
    "Turbo mode": "极速模式",
    "Disables all safety barriers for maximal iteration velocity.": "禁用所有安全屏障，以获得最快的迭代速度。",
    "Custom": "自定义配置", "Manually customize individual settings.": "手动自定义各项设置。",
    "System Default": "跟随系统", "Zoom Level": "缩放比例", "Font Size": "字体大小",
    "Small": "小", "Medium": "中", "Large": "大", "Code Font": "代码字体", "Editor Font": "编辑器字体",
    "Default Model": "默认模型", "Temperature": "温度", "System Prompt": "系统提示词",
    "Search Engine": "搜索引擎", "Web Search": "网络搜索", "Enable Web Access": "启用网络访问",
    "Startup": "启动", "Launch at login": "登录时自动启动", "Hardware Acceleration": "硬件加速",
    "Current Version": "当前版本", "Up to date": "已是最新版本", "Downloading": "下载中...",
    "Restart to update": "重启以更新", "Danger Zone": "危险区域", "Clear History": "清除历史记录",
    "Delete All": "全部删除", "Reset to Default": "恢复默认设置", "Restore Defaults": "恢复默认设置", "Reset to default": "恢复默认", "Restore defaults": "恢复默认设置",
    "Keybindings": "快捷键绑定", "Command": "命令", "Shortcut": "快捷键", "Action": "操作",
    "Advanced Settings": "高级设置", "Developer Tools": "开发者工具", "Toggle Developer Tools": "切换开发者工具",
    "Open Logs": "打开日志", "Proxy Server": "代理服务器", "Enable Proxy": "启用代理",
    "Auto-Updater": "自动更新程序", "Always": "始终", "Never": "从不", "Ask": "询问",
    "Contrast": "对比度", "contrast": "对比度", "Strong": "强", "strong": "强",
    "Windows Subsystem for Linux": "适用于 Linux 的 Windows 子系统 (WSL)",
    "Run the app against a Linux environment. Connecting relaunches the app into the selected WSL distro.": "在 Linux 环境中运行应用。连接后将重启应用并切换至所选的 WSL 分发版。",
    "Connect": "连接", "connect": "连接",
    "App version": "应用版本", "App Version": "应用版本",
    "Automatic Check for Updates": "自动检查更新",
    "Automatically prompt you to restart the app when a new update is available. When disabled, you can check for updates manually from the app menu.": "当有新更新可用时自动提示您重启应用。禁用后，您可以从应用菜单中手动检查更新。",
    "Invalid Media": "无效媒体", "invalid media": "无效媒体",
    "Maximum number of attachments reached": "已达到附件数量上限",
    "Maximum number of attachments reached.": "已达到附件数量上限。",
    "Save changes": "保存更改", "Apply": "应用", "OK": "确定", "Features": "功能",
    "Experimental Features": "实验性功能", "Enable": "启用", "Disable": "禁用",
    "API Configuration": "API 配置", "Account Settings": "账号设置", "Profile Settings": "个人资料",
    "Workspace Settings": "工作区设置", "Manage Projects": "管理项目",
    "Terminal & Tooling Permissions": "终端与工具权限",
    "Terminal Commands": "终端命令", "Configure allowed terminal commands.": "配置允许执行的终端命令。",
    "Commands Outside Sandbox": "沙盒外命令", "Configure allowed commands outside the sandbox.": "配置允许在沙盒外执行的命令。",
    "MCP Tools": "MCP 工具", "Configure external tools via Model Context Protocol.": "通过模型上下文协议配置外部工具。",
    "Yes, and always allow": "是，始终允许", "No (tell the agent what to do instead)": "否 (告诉智能体改做什么)",
    "Skip": "跳过", "Submit": "提交",

    // Models & Usage Tab
    "Models & Usage": "模型与用量", "Manage your model quota and credits.": "管理您的模型配额和积分额度。",
    "Usage": "用量", "Model Quota": "模型配额", "No quota information available.": "暂无配额信息。",
    "Refresh quota and credits data": "刷新配额和积分数据",
    "Daily limit": "每日限额", "Weekly limit": "每周限额", "5h limit": "五小时限额",
    "Daily Limit": "每日限额", "5-Hour Limit": "五小时限额", "5h Limit": "五小时限额",
    "Gemini 4 Argon Weekly Limit": "Gemini 4 Argon 每周限额",
    "Gemini 4 Argon Five Hour Limit": "Gemini 4 Argon 五小时限额",
    "% left": "% 剩余",
    "Plan": "订阅计划", "Model Credits": "模型积分", "Enable AI Credit Overages": "启用 AI 积分超额使用",
    "When toggled on, Antigravity will use your AI credits to fulfill model requests once you're out of model quota. Antigravity will always use your model quota first before using AI credits.": "启用后，当您的模型配额用尽时，Antigravity 将使用您的 AI 积分来完成模型请求。Antigravity 将始终优先使用模型配额。",
    "See Activity": "查看活动", "Get More AI Credits": "获取更多 AI 积分", "View plans": "查看套餐",
    "Available AI Credits:": "可用 AI 积分：",
    "Gemini Models": "Gemini 模型", "Claude and GPT models": "Claude 和 GPT 模型",
    "Limited time": "限时", "Low": "低", "Medium": "中", "High": "高", "XHigh": "超高", "Extra": "超高", "Max": "最高", "View Usage": "查看用量",
    "Best of N Models": "Best of N 多模型对比", "No models available": "暂无可用模型", "Loading models...": "正在加载模型...",
    "Add Model": "添加模型", "Custom models are only supported on Linux machines.": "自定义模型仅在 Linux 设备上受支持。",
    "Notice": "提示", "notice": "提示", "Leaving Soon": "即将下线", "Leaving soon": "即将下线",
    "Start using Gemini 3.8 Flash, our best Flash model.": "开始使用 Gemini 3.8 Flash，我们最强大的 Flash 模型。",
    "Sonnet 5.5 is now available on paid Pro and Ultra plans. Third-party model access will no longer be available on your current plan starting on November 2, 2026.": "Sonnet 5.5 现已在付费的 Pro 和 Ultra 方案中提供。从 2026 年 11 月 2 日起，您当前的方案将不再支持访问第三方模型。",
    "GPT-OSS will be removed from Antigravity on November 18, 2026.": "GPT-OSS 将于 2026 年 11 月 18 日从 Antigravity 中移除。",
    "Give Feedback": "提供反馈", "New Remote Project": "新建远程项目",
    "Create a project whose conversations run remotely.": "创建一个对话在远程运行的项目。",
    "Create a new project from one or more folders.": "从一个或多个文件夹创建新项目。",
    "What can we get done today?": "今天想完成什么工作？",
    "To continue using this model now, enable AI Credit overages.": "若要立即继续使用此模型，请启用 AI 积分超额使用。",
    "Change...": "更改...", "Voice mode": "语音模式", "Not set": "未设置", "System default": "跟随系统",
    "Start Voice mode": "开启语音模式", "End Voice mode": "结束语音模式", "Voice mode in progress": "语音模式进行中",
    "Start Live Chat": "开启实时对话", "End Live chat": "结束实时对话", "Live chat in progress": "实时对话进行中",
    "Mute mic": "麦克风静音", "Unmute mic": "取消麦克风静音", "Back to chat": "返回对话", "Choose a voice": "选择音色",
    "Extensions": "扩展", "No extensions available": "暂无可用扩展",
    "Customize Sections": "自定义模块", "Links": "链接", "Modified Files": "已修改文件",
    "Hide Whitespace Changes": "隐藏空白字符更改", "Show Whitespace Changes": "显示空白字符更改",
    "View Stacked Diff": "上下分栏查看差异", "View Split Diff": "分屏查看差异",
    "Collapse Diffs": "折叠差异", "Expand Diffs": "展开差异", "Expand All": "全部展开", "Collapse All": "全部折叠",
    "View Diff": "查看差异", "Viewing Diff": "正在查看差异", "View File": "查看文件",
    "Copy Content": "复制内容", "Download File": "下载文件", "Copy Path": "复制路径", "Export as PDF": "导出为 PDF",
    "Copy code": "复制代码", "Copy Code": "复制代码", "Copied": "已复制",
    "At mention code block": "@ 提及代码块", "At Mention Code Block": "@ 提及代码块",
    "Insert in terminal": "插入到终端", "Insert in Terminal": "插入到终端", "Markdown view mode": "Markdown 视图模式",
    "Ran": "已运行", "Running": "正在运行", "Running command": "运行命令",
    "Analyzing": "正在分析", "Analyzing Task Log": "正在分析任务日志", "Analyzed Task Log": "已分析任务日志",
    "Analyzing content": "正在分析内容", "Analyzed content": "已分析内容",
    "Editing": "正在编辑", "Creating": "正在创建", "Deleting": "正在删除",
    "Searching": "正在搜索", "Searched": "已搜索", "Semantic searching": "正在语义搜索", "Semantic searched": "已语义搜索",
    "Rejected": "已拒绝", "Canceled": "已取消", "Interrupted": "已中断", "Errored": "执行出错",
    "Exploring": "正在浏览", "Explored": "已浏览", "Done": "已完成",
    "Checking command status": "正在检查命令状态", "Checked command status": "已检查命令状态",
    "This command ran in the sandbox.": "此命令在沙盒中运行。", "Show more": "显示更多", "Show less": "收起",
    "Read URL rejected": "已拒绝读取 URL",

    // Customizations & Plugins
    "Configure default behaviors, skills, and MCP servers.": "配置默认行为、技能和 MCP 服务器。",
    "Learn more.": "了解更多。", "Learn more": "了解更多",
    "Token Usage": "Token 使用量",
    "The breakdown below shows token usage from customizations like rules, skills, and MCP. If a budget is exceeded, large rules are demoted to path pointers and large customizations are excluded automatically.": "下方的明细展示了来自规则、技能和 MCP 等自定义项的 Token 使用情况。如果超出预算，大型规则将降级为路径指针，大型自定义项将被自动排除。",
    "The breakdown below shows token usage from customizations like skills, rules, and MCP. If the budget is exceeded, large customizations will be truncated automatically.": "下方的明细展示了来自技能、规则和 MCP 等自定义项的 Token 使用情况。如果超出预算，大型规则将降级为路径指针，大型自定义项将被自动排除。",
    "Skills": "技能", "Rules": "规则",
    "Installed MCP Servers": "已安装的 MCP 服务器",
    "Add MCP +": "添加 MCP +", "Add MCP": "添加 MCP", "Add MCP Servers": "添加 MCP 服务器", "Add MCP Server": "添加 MCP 服务器",
    "Copy Config File Path": "复制配置文件路径",
    "Search MCP servers by name": "按名称搜索 MCP 服务器",
    "Refresh": "刷新", "Refreshing...": "刷新中...", "Refreshing": "刷新中",
    "Analyzed": "已分析", "analyzed": "已分析",
    "Exploring file, editing file": "浏览文件、编辑文件",
    "Open MCP Config": "打开 MCP 配置",
    "No MCP Servers": "无 MCP 服务器",
    "You currently don't have any MCP Servers installed. Add an MCP server above or add a custom one via the MCP Config.": "您目前尚未安装任何 MCP 服务器。请在上方添加 MCP 服务器，或通过 MCP 配置添加自定义服务器。",
    "Build With Google Plugins": "使用 Google 插件构建", "Build with Antigravity Plugins": "使用 Antigravity 插件构建",
    "Customize": "自定义", "Hide breakdown": "隐藏明细",
    "coding agent": "编程智能体",
    "Search customizations...": "搜索自定义项...",
    "Google Workspace": "Google Workspace",
    "Build with Google": "使用 Google 构建",
    "Design, Creative & Media": "设计、创意与媒体",
    "Design, creative, and media tools.": "设计、创意和媒体工具。",
    "Productivity & Project Management": "效率与项目管理",
    "Plan work, track issues, sign documents, and manage your notes and files.": "规划工作、跟踪议题、签署文档，并管理您的笔记和文件。",
    "Cloud Hosting & Deployment": "云托管与部署",
    "Deploy and host your apps, sites, and their backends.": "部署并托管您的应用、网站及其后端。",
    "Developer Tools": "开发者工具",
    "APIs, services, and tools to build, test, secure, and run your apps.": "用于构建、测试、保护和运行应用的 API、服务和工具。",
    "Business": "商业与企业服务",
    "Payments, CRM, accounting, data, identity, customer support, marketing, and workflow automation.": "支付、CRM、财务、数据、身份认证、客户支持、营销和工作流自动化。",
    "More Plugins": "更多插件",
    "Explore other marketplace customizations": "探索插件市场中的其他自定义扩展",
    "Explore other marketplace customizations.": "探索插件市场中的其他自定义扩展。",
    "Marketplace": "插件市场",
    "Installed": "已安装",
    "Find skills, agents, and more in the Marketplace.": "在插件市场中发现技能、智能体及更多内容。",
    "Browse the Marketplace": "浏览插件市场",
    "Skills & Rules": "技能与规则",
    "Built In": "内置",
    "Custom Agents": "自定义智能体",
    "No custom agents yet.": "暂无自定义智能体。",
    "MCP Servers": "MCP 服务器",
    "No MCP servers yet. Use Add to browse the store.": "暂无 MCP 服务器。请使用“添加”浏览商店。",
    "Create a Plugin with the Agent": "使用智能体创建插件",
    "Hooks": "钩子 (Hooks)", "Manage Hooks": "管理钩子", "Configure hooks that run on agent lifecycle events.": "配置在智能体生命周期事件上运行的钩子。",
    "Agent Hooks Configuration": "智能体钩子配置", "+ Add Hook": "+ 添加钩子", "Add Hook Card": "添加钩子卡片",
    "Add Handler": "添加处理器", "Delete Hook": "删除钩子", "Delete Handler": "删除处理器",
    "Pre Tool Use": "工具使用前", "Post Tool Use": "工具使用后", "Pre Invocation": "调用前", "Post Invocation": "调用后",
    "Default Customizations": "默认自定义项", "Include Jetski Default Customizations": "包含默认自定义项",
    "Include default customizations, such as default skills.": "包含默认自定义项（例如默认技能）。",
    "When enabled, the agent will include default customizations, including default skills.": "启用后，智能体将包含默认自定义项（包括默认技能）。",
    "Accounts": "已关联账号", "Connections": "连接", "Bundles": "捆绑包", "UI Extensions": "UI 扩展", "Context Providers": "上下文提供程序", "Themes": "主题",
    "Signed-in accounts": "已登录账号", "Apps connected to your account": "已连接到您账号的应用",
    "Sign in to an app once and your agent can use it on any device. Open an app to see the account it uses or to disconnect it.": "登录一次应用，您的智能体即可在任何设备上使用它。打开应用即可查看其使用的账号或断开连接。",
    "Services this plugin connects to on your behalf. Credentials stay on this machine and are only sent to the domains listed.": "此插件代表您连接的服务。凭据仅保存在本机，且仅发送至列出的域名。",
    "See less": "收起",
    "Google Docs": "Google 文档",
    "Google Sheets": "Google 表格",
    "Google Slides": "Google 幻灯片",
    "Google Drive": "Google 云端硬盘",
    "Google Calendar": "Google 日历",
    "Gemini API": "Gemini API",
    "Android CLI": "Android CLI",
    "Data Agent Kit": "Data Agent Kit",
    "Dart and Flutter": "Dart 和 Flutter",
    "Google Maps Platform": "Google Maps Platform",
    "Core tools and knowledge required to develop for Android": "开发 Android 所需的核心工具和知识",
    "Core tools and knowledge required to develop for Android.": "开发 Android 所需的核心工具和知识。",
    "Modern Web Guidance": "现代 Web 开发指南",
    "Keep your coding agent up to date with the latest web best practices.": "让您的编程智能体掌握最新的 Web 最佳实践。",
    "Google Antigravity SDK": "Google Antigravity SDK",
    "Using the Antigravity Python SDK to build AI agents": "使用 Antigravity Python SDK 构建 AI 智能体",
    "Science": "科学", "Curated collection of agent skills for science.": "精选的科学领域智能体技能集合。",
    "Firebase": "Firebase",
    "Prototype, build & run modern apps users love with Firebase's backend, AI, and operational infrastructure.": "借助 Firebase 的后端、AI 和运营基础设施，设计原型、构建并运行深受用户喜爱的现代应用。",
    "Chrome DevTools": "Chrome 开发者工具",
    "Reliable automation, in-depth debugging, and performance analysis in Chrome using Chrome DevTools and Puppeteer": "使用 Chrome DevTools 和 Puppeteer 在 Chrome 中实现可靠的自动化、深度调试和性能分析",
    "Google Kubernetes Engine (Remote)": "Google Kubernetes Engine (远程)",

    // Shortcuts Panel
    "Configure keyboard shortcuts.": "配置键盘快捷键。",
    "Keyboard shortcuts for quick navigation and control.": "用于快速导航和控制的键盘快捷键。",
    "Search shortcuts...": "搜索快捷键...", "Search shortcuts": "搜索快捷键", "Clear search": "清除搜索",
    "RECOMMENDED": "推荐", "NAVIGATION": "导航", "Recommended": "推荐", "Navigation": "导航",
    "Open Conversation Picker": "打开对话选择器", "Open File Search": "打开文件搜索",
    "Go Back": "后退", "Go Forward": "前进", "Go Back in Pane": "在面板中后退", "Go Forward in Pane": "在面板中前进",
    "Reopen Closed Tab": "重新打开关闭的标签页",
    "Move Conversation Up": "向上移动对话", "Move Conversation Down": "向下移动对话",
    "Open Conversation in New Tab": "在新标签页中打开对话", "Middle Click": "鼠标中键点击",
    "Start Voice Recording": "开始语音录制", "Stop Voice Recording": "停止语音录制",
    "Mute Voice Mic": "语音麦克风静音", "Mute Voice Speaker": "语音扬声器静音",
    "Open in Code Search": "在代码搜索中打开", "Code Search": "代码搜索",
    "Add Shortcut": "添加快捷键", "Edit Shortcut": "编辑快捷键", "Remove Shortcut": "移除快捷键",
    "Focus Input": "聚焦输入框", "File Picker": "文件选择器",
    "Select Previous Conversation": "选择上一个对话", "Select Next Conversation": "选择下一个对话",
    "Previous Pane Tab": "上一个面板标签", "Next Pane Tab": "下一个面板标签",
    "Previous Side Panel Tab": "上一个侧边面板标签", "Next Side Panel Tab": "下一个侧边面板标签",
    "Toggle Model Selector": "切换模型选择器", "Toggle Voice Recording": "切换语音录制",
    "Find in Pane": "在面板中查找", "Find in Conversation": "在对话中查找", "Add to Chat/Quote": "添加到对话/引用",
    "LAYOUT CONTROLS": "布局控制", "Layout Controls": "布局控制", "Layout controls": "布局控制",
    "App Shortcuts": "应用快捷键", "Editor Shortcuts": "编辑器快捷键", 
    "Global Shortcuts": "全局快捷键", "Terminal Shortcuts": "终端快捷键", 
    "Chat Shortcuts": "对话快捷键", "Press desired key combination": "按下所需的组合键",
    "Open Command Palette": "打开命令面板", "Open Keyboard Shortcuts": "打开键盘快捷键", "Open Preferences": "打开偏好设置",
    "Toggle Side Panel": "切换侧边面板", "Toggle Maximize Side Panel": "切换最大化侧边面板",
    "Toggle Terminal": "切换终端", "Toggle File Viewer": "切换文件查看器", "Toggle Overview Panel": "切换概览面板",
    "Toggle Project Selector": "切换项目选择器", "Open Workspace Selector": "打开工作区选择器",
    "Toggle Environment Selector": "切换环境选择器", "Toggle Between Light/Dark Themes": "切换浅色/深色主题",

    // Feedback Panel
    "Feedback Type": "反馈类型", "Auth and Billing": "认证与计费", "Description": "描述",
    "Please describe the issue in detail. The more actionable your feedback, the quicker our team can address your request. Some helpful information includes:": "请详细描述您的问题。您的反馈越具体，我们的团队就能越快处理您的请求。一些有用的信息包括：",
    "Steps to reproduce the issue": "重现问题的步骤", "Expected behavior": "预期行为",
    "Actual behavior": "实际行为", "Any error messages": "任何错误消息", "Any relevant information": "任何相关信息",
    "Describe the bug you encountered...": "描述您遇到的错误...",
    "Steps to Reproduce": "重现步骤", "Please list the steps to reproduce the issue...": "请列出重现问题的步骤...",
    "Please list the steps to reproduce the issue": "请列出重现问题的步骤",
    "Attach a screenshot (optional)": "附加截图（可选）", "Attach Antigravity server logs": "附加 Antigravity 服务器日志",
    "We'd love to hear from you.": "我们期待您的反馈。", "How can we improve?": "我们该如何改进？",
    "Thinking...": "思考中...", "Thought": "思考过程", "Agent is thinking...": "智能体正在思考...",
    "Show thought process": "显示思考过程", "Hide thought process": "隐藏思考过程",
    "Generating...": "生成中...", "Planning...": "计划中...",
    "Issue Type": "问题类型", "Bug Report": "错误报告", "Feature Request": "功能请求",
    "Remote Control Issue": "远程控制问题", "Remote control issue": "远程控制问题",
    "Legal Help": "法律帮助", "legal help": "法律帮助",
    "Visit Legal Help to ask for content changes for legal reasons.": "访问法律帮助以出于法律原因请求更改内容。",
    "Visit Legal Help to ask for content changes for legal reasons": "访问法律帮助以出于法律原因请求更改内容",
    "to ask for content changes for legal reasons.": "以出于法律原因请求更改内容。",
    "to ask for content changes for legal reasons": "以出于法律原因请求更改内容",
    "General Feedback": "常规反馈", "Describe your issue or idea...": "描述您的问题或想法...",
    "Please provide details...": "请提供详细信息...", "Include diagnostic data": "包含诊断数据",
    "Include app logs": "包含应用日志", "Send Feedback": "发送反馈",

    // Browser Tab & Built-in Browser (v2.29.0)
    "Browser Settings": "浏览器设置", "Built-in Browser": "内置浏览器", "Browser Subagent": "浏览器子智能体",
    "Configure the browser subagent. It requires": "配置浏览器子智能体。需要安装",
    "to be installed. The browser subagent can be invoked by typing /browser in the conversation input box.": "。您可以在对话输入框中输入 /browser 来调用浏览器子智能体。",
    "Browser Javascript Execution Policy": "浏览器 JavaScript 执行策略",
    "Controls whether the agent can run custom JavaScript to automate complex browser actions.": "控制智能体是否可以运行自定义 JavaScript 来自动化复杂的浏览器操作。",
    "Disabled": "已禁用", "Block all browser JavaScript execution.": "阻止所有浏览器 JavaScript 执行。",
    "Request Review": "请求审阅", "Prompt for approval before running browser scripts.": "在运行浏览器脚本前提示批准。",
    "Allow full browser script execution without prompting.": "允许执行完整的浏览器脚本而不提示。",
    "Actuation Permissions": "操作权限", "Browser Actuation Rules": "浏览器操作规则",
    "Configure allowed and denied URLs for browser actuation.": "配置允许和拒绝进行浏览器操作的 URL。",
    "Download Location": "下载位置", "Folder where files downloaded in the built-in browser are saved.": "内置浏览器中下载文件的保存文件夹。",
    "Reset": "重置", "Change": "更改",
    "Browsing History": "浏览历史记录",
    "Clear visited URLs and autocomplete suggestions from the built-in browser.": "清除内置浏览器中的已访问 URL 和自动补全建议。",
    "Clear visited URLs and autocomplete suggestions from side panel preview.": "清除侧边面板预览中的已访问 URL 和自动补全建议。",
    "Enable Browser Tools": "启用浏览器工具",
    "The browser subagent has been disabled by your administrator. Contact your administrator to enable browser use.": "浏览器子智能体已被您的管理员禁用。请联系管理员以启用浏览器功能。",
    "Open Links In": "链接打开方式", "Choose where links open by default when clicked.": "选择点击链接时的默认打开位置。",
    "New Tab": "新标签页", "External Browser": "外部浏览器", "Side Panel Preview": "侧边面板预览",
    "Configure link opening and built-in browser preferences.": "配置链接打开方式和内置浏览器偏好设置。",

    // App, Notifications, Sound & Voice Tab (v2.29.0)
    "App Settings": "应用设置", "Manage application settings.": "管理应用设置。",
    "Prevent Sleep": "阻止睡眠", "Prevent the computer from sleeping while the app is running.": "在应用运行时阻止计算机进入睡眠状态。",
    "Keep In Menu Bar": "保留在系统托盘", 
    "The app will be accessible from the menu bar and will keep running in the background when all windows are closed.": "应用将可以从系统托盘访问，并在所有窗口关闭时继续在后台运行。",
    "Keep the app accessible from the menu bar and running in the background when all windows are closed.": "应用将可以从系统托盘访问，并在所有窗口关闭时继续在后台运行。",
    "Notification Settings": "通知设置", "To modify notification settings, open your operating system's system preferences.": "要修改通知设置，请打开操作系统的系统偏好设置。",
    "Open System Preferences": "打开系统偏好设置",
    "Manage your notification preferences.": "管理您的通知偏好设置。",
    "Enable Notifications for Agent": "启用智能体通知",
    "Show system notifications when your action is needed or the agent finishes.": "当需要您操作或智能体完成任务时显示系统通知。",
    "Sound": "声音", "Enable Sounds for Agent": "启用智能体提示音",
    "Play a sound when your action is needed or the agent finishes.": "当需要您操作或智能体完成任务时播放提示音。",
    "Volume": "音量", "Set the volume of agent sounds.": "设置智能体提示音的音量。", "Chime volume": "提示音音量",
    "Voice": "语音", "Voices": "语音音色", "Voice Mode": "语音模式",
    "The voice used in Voice mode. Powered by Gemini Live.": "语音模式中使用的音色，由 Gemini Live 提供支持。",
    "How loud Antigravity's voice is.": "设置 Antigravity 语音的音量大小。", "Voice volume": "语音音量",
    "Microphone": "麦克风", "Input device for voice mode and dictation.": "用于语音模式和听写的输入设备。",
    "Save audio recordings": "保存录音", "Only stored on your machine.": "仅保存在您的本机设备上。",
    "Recordings": "录音记录", "No recordings": "暂无录音", "Delete all": "全部删除", "Delete all recordings?": "确定删除所有录音吗？",

    // Conversations Tab, Appearance & Permissions (v2.29.0)
    "Agent settings and permissions for conversations outside of projects.": "针对项目外对话的智能体设置和权限。",
    "Agent settings and permissions for conversations outside of workspaces.": "针对工作区外对话的智能体设置和权限。",
    "Settings and permissions for conversations outside of workspaces.": "针对工作区外对话的设置和权限。",
    "Inherit General": "继承全局设置", "Local Permissions": "本地权限",
    "Also includes": "还包括", "global settings": "全局设置",
    "when working in this project.": "（当在此项目中工作时）。",
    "when working in this workspace.": "（当在此工作区中工作时）。",
    "Toggle Sidebar": "切换侧边栏", "View Split Diff": "分屏查看差异", "Collapse All": "全部折叠",
    "Learn more about": "了解更多关于",
    "Configure the agent's visual theme and display preferences.": "配置智能体的视觉主题和显示偏好。",
    "Chat Settings": "聊天设置", "Verbose Agent Chat": "详细的智能体对话",
    "Conversation Steps": "对话步骤展示", "Choose how much detail is shown during a conversation.": "选择对话过程中显示的详细程度。", "Verbose": "详细",
    "Display and preserve intermediate thinking steps.": "显示并保留中间思考过程。",
    "Conversation Width": "对话宽度", "Chat Width": "聊天宽度", "Configure the maximum width of the conversation panel.": "配置对话面板的最大宽度。",
    "Narrow": "较窄", "Wide": "较宽", "Fill": "铺满",
    "Markdown Artifact Width": "Markdown 产物宽度", "Configure the default width of markdown artifacts.": "配置 Markdown 产物的默认宽度。",
    "Context and Quota Indicator": "上下文与配额指示器",
    "Show how full the context window is next to the send button. Click it for a breakdown and to see your model quota.": "在发送按钮旁显示上下文窗口的占用比例。点击可查看详细占用分布及模型配额。",
    "Custom Context Menus": "自定义右键菜单", "Replace the default browser right-click menu with quick actions.": "使用快捷操作菜单替换默认的浏览器右键菜单。",
    "Screen Reader Mode": "屏幕阅读器模式", "Optimize the interface and terminal output for screen readers.": "针对屏幕阅读器优化界面和终端输出。", "Accessibility": "无障碍功能",
    "Terminal Placement": "终端位置", "Choose where terminal sessions appear.": "选择终端会话的显示位置。",
    "Side Panel": "侧边面板", "Bottom Panel": "底部面板",
    "Select light, dark, or inherit system settings.": "选择浅色、深色，或跟随系统设置。",
    "Light Theme": "浅色主题", "Preset": "预设", "Default Light": "默认浅色",
    "Background": "背景颜色", "Foreground": "前景颜色", "Accent": "强调色",
    "Dark Theme": "深色主题", "Default Dark": "默认深色",
    "Allow write access to this path?": "允许写入此路径吗？",
    "Allow read access to this path?": "允许读取此路径吗？",
    "Allow execution of this command?": "允许执行此命令吗？",
    "Allow running this command?": "允许运行此命令吗？",
    "Allow running this command outside the sandbox?": "允许在沙盒外部运行此命令吗？",
    "Allow reading this URL?": "允许读取此 URL 吗？",
    "Allow executing actions on this URL?": "允许在此 URL 上执行操作吗？",
    "Allow using this MCP tool?": "允许使用此 MCP 工具吗？",
    "Allow a one-time administrator (UAC) elevation?": "允许一次性管理员 (UAC) 提权吗？",
    "Allow access to this resource?": "允许访问此资源吗？",
    "Yes, allow": "是，允许",
    "Yes, allow this time": "是，仅本次允许",
    "Yes, and always allow in this conversation": "是，在本次对话中始终允许",
    "Yes, and always allow when not in a project": "是，在未分组项目中始终允许",
    "Yes, and always allow": "是，始终允许",
    "Confirm the command is safe to run outside of the sandbox with full network and disk access.": "请确认该命令在沙盒外以完整网络和磁盘权限运行是安全的。",
    "Show details": "显示详情", "Hide details": "隐藏详情",
    "tell the agent what to do instead": "告诉智能体接下来该做什么",
    "(tell the agent what to do instead)": "(告诉智能体接下来该做什么)",
    "Skip": "跳过", "Working.": "运行中。", "Working...": "运行中...",
    "Edited": "已编辑", "Viewed": "已查看", "Created": "已创建", "Deleted": "已删除", "Executed": "已执行",
    "Save rule to always allow write access to this path?": "保存规则以始终允许写入此路径吗？",
    "Save rule to always allow read access to this path?": "保存规则以始终允许读取此路径吗？",
    "Save rule to always allow execution of this command?": "保存规则以始终允许执行此命令吗？",
    "Save rule to always allow running this command?": "保存规则以始终允许运行此命令吗？",
    "Save rule to always allow running this command outside the sandbox?": "保存规则以始终允许在沙盒外运行此命令吗？",
    "Save rule to always allow reading this URL?": "保存规则以始终允许读取此 URL 吗？",
    "Save rule to always allow executing actions on this URL?": "保存规则以始终允许在此 URL 上执行操作吗？",
    "Save rule to always allow using this MCP tool?": "保存规则以始终允许使用此 MCP 工具吗？",
    "Save rule to always allow a one-time administrator (UAC) elevation?": "保存规则以始终允许一次性管理员 (UAC) 提权吗？",
    "Save rule to always allow access to this resource?": "保存规则以始终允许访问此资源吗？",
    "Yes, save rule in this conversation": "是，在本次对话中保存规则",
    "Yes, save rule when not in a project": "是，在未分组项目中保存规则",
    "Yes, save rule globally": "是，全局保存规则",

    // Error & Diagnostics UI
    "Our servers are experiencing high traffic right now, please try again in a minute.": "我们的服务器当前负载较高，请稍后重试。",
    "Error ID:": "错误 ID：",
    "Agent terminated due to error": "智能体因错误而终止",
    "Agent execution terminated due to error.": "智能体执行因错误而终止。",
    "Agent execution terminated due to error": "智能体执行因错误而终止",
    "You can prompt the model to try again or start a new conversation if the error persists.": "您可以提示模型重试，或者如果错误仍然存在，可以开启新的对话。",
    "See our troubleshooting guide for more help.": "查看我们的排查指南以获取更多帮助。",
    "See our troubleshooting guide for more help": "查看我们的排查指南以获取更多帮助",
    "troubleshooting guide": "排查指南", "troubleshooting_guide": "排查指南",
    "See our": "查看我们的",
    "for more help.": "以获取更多帮助。", "for more help": "以获取更多帮助",
    "Dismiss": "忽略", "Copy debug info": "复制调试信息", "Download Diagnostics": "下载诊断信息",

    // Remote Control & WSL Feature & Context Menus (v2.29.0)
    "Try Remote Control": "尝试远程控制",
    "Remote Control": "远程控制",
    "Device Name": "设备名称", "Enter device name...": "输入设备名称...",
    "A label for this computer when you connect from another device. Changing it reconnects.": "从其他设备连接时显示的本电脑名称。修改后将重新连接。",
    "Show Remote Control QR code": "显示远程控制二维码",
    "Scan the code to open this device in Remote Control, or": "扫描二维码以在远程控制中打开此设备，或者",
    "Open in Remote Control": "在远程控制中打开",
    "Continue your work from another device with Remote Control. Scan the QR code or open the link below.": "使用远程控制在另一台设备上继续您的工作。请扫描二维码或打开下方链接。",
    "These settings can only be changed on the computer running the app, not from a remote session.": "这些设置只能在运行该应用的电脑本机上更改，无法在远程会话中修改。",
    "Connected": "已连接", "Local Windows environment": "本地 Windows 环境",
    "The app is currently connected to a WSL distro. Reopening locally relaunches it directly on Windows.": "当前应用已连接到 WSL 分发版。选择“在本地重新打开”将直接在 Windows 上重启应用。",
    "Reopen Locally": "在本地重新打开", "Connect to WSL": "连接到 WSL",
    "Open in Side Panel": "在侧边面板中打开", "Open in Built-in Browser": "在内置浏览器中打开",
    "Open in External Browser": "在外部浏览器中打开", "Open in New Tab": "在新标签页中打开",
    "Open Link in New Tab": "在新标签页中打开链接", "Open Link in External Browser": "在外部浏览器中打开链接",
    "Copy Link Address": "复制链接地址", "Open Image in New Tab": "在新标签页中打开图片", "Copy Image Address": "复制图片地址",
    "Open In": "打开方式", "Side Panel (Default)": "侧边面板 (默认)", "Built-in Browser (Default)": "内置浏览器 (默认)",
    "External Browser (Default)": "外部浏览器 (默认)", "New Tab (Default)": "新标签页 (默认)",
    "Kick off work on your computer and continue working with your agents from your phone or another device. Turn on Remote Control in app settings.": "在电脑上启动工作，并可以通过手机或其他设备继续与智能体协同工作。请在应用设置中开启“远程控制”。",
    "Kick off work on your computer and continue working with your agents from your phone or another device.": "在电脑上启动工作，并可以通过手机或其他设备继续与智能体协同工作。",
    "Turn on Remote Control in app settings.": "请在应用设置中开启“远程控制”。",
    "Turn on Remote Control in app settings": "请在应用设置中开启“远程控制”",
    "Unavailable": "不可用",
    "The original Gemini 4 model for advanced workflows": "适用于高级工作流的经典 Gemini 4 模型",
    "Knowledge Work": "知识工作",
    "Simplified interface for research, writing, and everyday tasks.": "专为研究、写作和日常任务设计的简化界面。",
    "Software Engineering": "软件工程",
    "Full interface for coding, developer tools, and managing agents.": "面向编程、开发工具与智能体管理的完整界面。",
    "For most deep reasoning and complex problems": "适用于大多数深度推理与复杂问题",
    "Your This Computer setting": "您的“此电脑”设置",
    "Your Remote setting": "您的“远程”设置",
    "Project setting": "项目设置",
    "Workspace setting": "工作区设置",
    "Default and Auto": "默认与自动",
    "Create with Prompt": "通过提示词创建",
    "Run a prompt on a schedule, like a morning summary of yesterday's changes. Runs show up here.": "按计划定时运行提示词，例如每天早上汇总昨天的更改。运行记录将显示在此处。",
    "SSH Host…": "SSH 主机…",
    "SSH Host...": "SSH 主机...",
    "Create a project on a machine you reach over SSH. It opens in that host's own window.": "在可通过 SSH 访问的机器上创建项目。它将在该主机的独立窗口中打开。",
    "Google does not control the availability or functionality of third party developer tools. Your data from third party developer tools connected to your Antigravity instance may be shared with Google. Google will protect any such data in accordance with the Google Privacy Policy, found here:": "Google 不控制第三方开发者工具的可用性或功能。连接到您的 Antigravity 实例的第三方开发者工具中的数据可能会与 Google 共享。Google 将按照以下链接中的 Google 隐私权政策保护此类数据：",
    "Undo to this point": "撤销至此处",
    "Redo to this point": "重做至此处",
    "Revert file changes": "还原文件更改",
    "Cannot revert this message": "无法撤销此消息",
    "Cannot revert to a message that was cleared to save space": "无法撤销到已清理以节省空间的消息",
    "Cannot revert a message sent while the agent was running": "无法撤销在智能体运行期间发送的消息",
    "For paid Pro plans, Argon quota is separate. Higher Argon quota (included as part of the larger Gemini quota bucket) is available on Ultra plans.": "对于付费 Pro 套餐，Argon 配额单独计算。Ultra 套餐提供更高的 Argon 配额（包含在更大的 Gemini 配额池中）。",
    "Outside of Project": "未分组项目",
    "Outside of Workspace": "工作区外",
    "For speed and efficiency in execution tasks": "适用于追求速度与效率的执行任务",
    "Models within this group:": "此分组包含的模型：",
    "Argon that may offload routine steps to Hydrogen. Same Argon-level quality, fewer tokens used.": "可将常规步骤分流至 Hydrogen 的 Argon 模型。保持 Argon 级别质量，同时消耗更少 Token。",
    "Neon that may offload routine steps to Hydrogen. Same Neon-level quality, fewer tokens used.": "可将常规步骤分流至 Hydrogen 的 Neon 模型。保持 Neon 级别质量，同时消耗更少 Token。",
    "Workspace Name": "工作区名称",
    "Worktree Name": "工作树名称",
    "Edit Conversation Title": "编辑对话标题",
    "Run until the specified goal is completely finished.": "持续运行直至指定目标完全完成。",
    "Compact the conversation now (summarize history to free up the context window).": "立即压缩对话（总结历史记录以释放上下文窗口）。",
    "Run an instruction on a recurring schedule or as a one-time timer.": "按周期性计划或一次性定时器执行指令。",
    "Invoke a browser agent for web tasks.": "调用浏览器智能体执行网页任务。",
    "Plan carefully before executing a task.": "在执行任务前进行周密规划。",
    "Interview me to align on a plan.": "通过交互式访谈与我对齐方案。",
    "Invoke a team of agents to autonomously tackle large projects.": "调用智能体团队自主协作处理大型项目。",
    "Reflect on recent successes or corrections to capture reusable skills or rules.": "总结近期的成功经验或纠错记录，沉淀为可复用的技能或规则。",
    "Experimental. Deep reasoning agent for complex coding and research projects that need planning and rigorous verification.": "实验性功能。面向需要深度规划与严格验证的复杂编程及研究项目的深度推理智能体。",
    "Bundled With the App": "随应用内置",
    "Unlock the power of agent swarms": "解锁智能体蜂群（Swarm）的强大能力",
    "View Debug": "查看调试",
    "MCP servers": "MCP 服务器",
    "Developer": "开发者",
    "Website": "网站",
    "Repository": "代码库",
    "Loading plugin...": "正在加载插件...",
    "Loading plugin…": "正在加载插件…",
    "UI extensions": "UI 扩展",
    "Untitled": "无标题",
    "Trigger": "触发器",
    "Uses your local files and tools.": "使用您的本地文件和工具。",
    "Uses your local files and tools. Schedules only.": "使用您的本地文件和工具。仅限按计划运行。",
    "What should the agent do on each run? For example: summarize new bugs assigned to me and anything that changed overnight.": "每次运行时智能体应该做什么？例如：汇总分配给我的新 Bug 以及夜间发生的所有更改。",
    "Inter": "Inter 字体",
    "Catppuccin": "猫布奇诺",
    "Everforest": "常青森林",
    "Gruvbox Material": "复古质感",
    "One Light": "一号浅色",
    "Solarized Light": "日光浅色",
    "One Dark Pro": "一号深色专业版",
    "Solarized Dark": "日光深色",
    "Dracula": "德古拉",
    "Monokai": "莫诺凯",
    "Nord": "北欧冷灰",
    "Tokyo Night": "东京夜色",
    "SSH Host": "SSH 主机",
    "Search Hosts...": "搜索主机...",
    "Search Hosts…": "搜索主机…",

    // v2.33.0 Comprehensive UI Localization Additions
    "(excluding product analytics data)": "（不包括产品分析数据）",
    "(no title)": "（无标题）",
    "(not set)": "（未设置）",
    "(still loading…)": "（仍在加载…）",
    "+ Add Organization policy": "+ 添加组织策略",
    "+ Add Repository policy": "+ 添加仓库策略",
    "+ Add branch policy": "+ 添加分支策略",
    "+ Add issue policy": "+ 添加议题策略",
    "+ Add pull request policy": "+ 添加拉取请求策略",
    "+ Add workflow run policy": "+ 添加工作流运行策略",
    "1 Comment": "1 条评论",
    "1 Draft": "1 条草稿",
    "1 active conversation": "1 个活跃对话",
    "1 archived conversation": "1 个已归档对话",
    "1 browser step": "1 个浏览器步骤",
    "1 comment": "1 条评论",
    "1 day": "1 天",
    "1 hidden host": "1 个已隐藏的主机",
    "1 hour": "1 小时",
    "1 minute": "1 分钟",
    "1 month": "1 个月",
    "1 second": "1 秒",
    "1 week": "1 周",
    "1 year": "1 年",
    "12:00 AM": "上午 12:00",
    "12:00 PM": "下午 12:00",
    "A Google Cloud project is required to use Antigravity.": "使用 Antigravity 需要提供 Google Cloud 项目。",
    "A bash script run in your cloud environment after cloning repositories (or configure interactively in chat with /env-setup).": "克隆代码库后在您的云环境中运行的 bash 脚本（或在对话中使用 /env-setup 进行交互式配置）。",
    "A chunk is a section of the page. Long pages are chunked so that only the sections that are relevant to your query are read.": "分块是页面中的一个片段。较长的页面会被划分为多个分块，以便仅读取与您的查询相关的部分。",
    "A comma-separated list like org-a, org-b, or * for all.": "以逗号分隔的列表，例如 org-a, org-b，或使用 * 表示全部。",
    "A comma-separated list like repo-a, repo-b, or * for all.": "以逗号分隔的列表，例如 repo-a, repo-b，或使用 * 表示全部。",
    "A copy of the workspace snapshot recorded at this step.": "此步骤记录的工作区快照副本。",
    "A few things to know, and a couple settings to review.": "了解一些注意事项，并检查几项设置。",
    "A folder in this project could not be loaded because its location is invalid.": "此项目中的一个文件夹因位置无效而无法加载。",
    "A full copy of this workspace, uncommitted changes included.": "此工作区的完整副本，包含未提交的更改。",
    "A high-risk mode that disables all safety barriers. The agent operates with full system access, auto-executes all terminal commands, and reads or writes to all local files without review prompts.": "禁用所有安全屏障的高风险模式。智能体拥有完整的系统访问权限，会自动执行所有终端命令，并在不提示审阅的情况下读写所有本地文件。",
    "A host can't contain spaces.": "主机名不能包含空格。",
    "A license or project selection is required to use Antigravity.": "使用 Antigravity 需要选择许可或项目。",
    "A new version is available.": "有新版本可用。",
    "A nickname for identifying this application in the companion website. Changing this will restart the connection.": "用于在配套网站中标识此应用的昵称。更改此项将重启连接。",
    "A password or secure field is on screen.": "屏幕上包含密码或安全输入框。",
    "A project with this name already exists.": "已存在同名项目。",
    "A shell setup script run before every command the agent executes in this project. Overrides the global script.": "在智能体于此项目中执行每条命令前运行的 shell 配置脚本。将覆盖全局脚本。",
    "A similar": "一个类似的",
    "A snapshot was saved before running. To restore your previous output:": "运行前已保存快照。要恢复之前的输出：",
    "AI Credits Used to Generate Response": "已使用 AI 积分生成回复",
    "AI Credits are used when you've exceeded your model quota. Keep track of your current AI Credits in the": "当您超出模型配额时将使用 AI 积分。您可以在以下位置查看当前的 AI 积分：",
    "AI coding agents are known to have certain security risks, including autonomous code execution, data exfiltration, prompt injection and supply chain risks. Ensure that you monitor and verify all actions taken by the agent.": "AI 编程智能体存在一定的安全风险，包括自主代码执行、数据泄露、提示词注入和供应链风险。请确保您监控并验证智能体执行的所有操作。",
    "API key": "API 密钥",
    "About embedding": "关于嵌入",
    "Accept Step": "接受步骤",
    "Accept all": "全部接受",
    "Access grants": "访问授权",
    "Access restricted": "访问受限",
    "Access rules": "访问规则",
    "Account connected.": "账号已连接。",
    "Accumulated Item": "累计项",
    "Accumulated State": "累积状态",
    "Action required": "需要操作",
    "Action requires your attention": "操作需要您关注",
    "Active Tasks & Conversations:": "进行中的任务与对话：",
    "Add Comment": "添加评论",
    "Add Folder": "添加文件夹",
    "Add New Handler to": "添加新处理程序到",
    "Add Resource": "添加资源",
    "Add Workspace": "添加工作区",
    "Add a message...": "添加消息...",
    "Add account": "添加账户",
    "Add an optional message, ⏎ to submit comments": "添加可选消息，按 ⏎ 提交评论",
    "Add anyway": "仍然添加",
    "Add bundle": "添加插件包",
    "Add context": "添加上下文",
    "Add files": "添加文件",
    "Add label": "添加标签",
    "Add screenshot to conversation": "将截图添加到对话",
    "Add to Chat": "添加到对话",
    "Added": "已添加",
    "Added (Staged)": "已添加（已暂存）",
    "Adding...": "正在添加...",
    "Address bar": "地址栏",
    "Address bar suggestions": "地址栏建议",
    "Admin escalation": "管理员提权",
    "Agent Script": "智能体脚本",
    "Agent can": "智能体可以",
    "Agent can retrieve console logs from the browser and return it for further processing.": "智能体可以从浏览器获取控制台日志并返回以进行进一步处理。",
    "Agent can run": "智能体可以运行",
    "Agent data is not available": "智能体数据不可用",
    "Agent encountered an internal error.": "智能体遇到内部错误。",
    "Agent finished": "智能体已完成",
    "Agent options": "智能体选项",
    "Agent:": "智能体：",
    "Agents created by": "由",
    "All": "全部",
    "All Files": "所有文件",
    "All Workspaces": "所有工作区",
    "All active Antigravity shortcuts and user keybinding overrides are managed directly by VS Code.": "所有生效的 Antigravity 快捷键和用户按键绑定覆盖项均由 VS Code 直接管理。",
    "All agents": "所有智能体",
    "All changes since the branch point": "自分支点以来的所有更改",
    "All runs": "所有运行",
    "All tools (*)": "所有工具 (*)",
    "Allow Gemini to notify you when the agent needs your attention or completes a task.": "允许 Gemini 在智能体需要您关注或完成任务时通知您。",
    "Allow Google to collect and use your Interactions data, subject to the": "允许 Google 收集和使用您的交互数据，但须遵守",
    "Allow creating issues and grant access to specific issues.": "允许创建议题并授予对特定议题的访问权限。",
    "Allow microphone access to start Voice": "允许访问麦克风以启动语音模式",
    "Allow opening pull requests and grant access to specific PRs.": "允许发起拉取请求并授予对特定 PR 的访问权限。",
    "Allow reading workflow runs (list, view, watch) across the whole repository.": "允许在整个仓库中读取工作流运行（列出、查看、监视）。",
    "Allow/deny agent browser file downloads from specific sites.": "允许/拒绝智能体浏览器从特定网站下载文件。",
    "Allowed Domains": "允许的域名",
    "Alt text:": "替代文本：",
    "Always open": "始终直接打开",
    "Amend staged changes into the current commit": "将已暂存的更改修补到当前提交",
    "Amend succeeded": "修改提交成功",
    "Amending...": "正在修补提交...",
    "An agent is using the built-in browser. Clearing its data signs the agent out of sites and may interrupt its task.": "有智能体正在使用内置浏览器。清除其数据会使智能体退出网站登录状态，并可能中断其任务。",
    "An embedded page on this page says": "此页面上的嵌入页面显示",
    "An error occurred while checking the port. Please try again.": "检查端口时出错。请重试。",
    "An error occurred while submitting your feedback. Please try again.": "提交反馈时出错，请重试。",
    "An error was thrown.": "发生错误。",
    "Annotate": "批注",
    "Announcements and tips": "公告与提示",
    "Antigravity (AGY) Style": "Antigravity (AGY) 风格",
    "Antigravity Interactive HTML": "Antigravity 交互式 HTML",
    "Antigravity would like to use the browser.": "Antigravity 想要使用浏览器。",
    "Any error messages seen when trying to log in": "尝试登录时看到的任何错误信息",
    "Appears larger on mobile": "在移动设备上显示更大",
    "Approve": "批准",
    "Apps": "应用",
    "Archive Project": "归档项目",
    "Archive This Conversation": "归档此对话",
    "Archive Workspace": "归档工作区",
    "Archive project": "归档项目",
    "Archived Only": "仅已归档",
    "Are you sure you want to delete": "您确定要删除",
    "Are you sure you want to delete the": "确定要删除此",
    "Are you sure you want to delete this handler?": "确定要删除此处理程序吗？",
    "Are you sure you want to delete this hook card?": "确定要删除此钩子卡片吗？",
    "Are you sure you want to delete this side question? This action cannot be undone.": "确定要删除此旁支提问吗？此操作无法撤销。",
    "Artifact Viewer": "产物查看器",
    "Artifact image": "产物图片",
    "Artifact not found": "未找到产物",
    "Artifact updated by agent": "智能体已更新产物",
    "Artifacts like Google Docs, PDFs, Office documents (Word, Excel, PowerPoint), etc. Everything else the agent creates is under Artifacts.": "Google 文档、PDF、Office 文档（Word、Excel、PowerPoint）等产物。智能体创建的其他所有内容都归类在“产物”下。",
    "Ask about your code or any topic, get clear answers.": "询问代码或任何主题，获得清晰解答。",
    "Ask questions, report issues, and discuss features": "提问、报告问题和讨论功能",
    "Asked": "已询问",
    "Asking": "正在询问",
    "Attach terminal output": "附加终端输出",
    "Attaching logs requires an email address": "附加日志需要提供电子邮件地址",
    "Attackers might be able to see the images you're looking at on this site and trick you by modifying them.": "攻击者可能会看到您在此网站上查看的图片，并通过修改图片来欺骗您。",
    "Audio File": "音频文件",
    "Audio attachment": "音频附件",
    "Audio clip": "音频片段",
    "Audio file size exceeds 20MB limit": "音频文件大小超过 20MB 限制",
    "Audio streaming transcription not available": "音频流式转录不可用",
    "Authenticate": "进行身份验证",
    "Authenticated as": "已验证身份为",
    "Authenticating...": "正在验证身份...",
    "Authentication Required": "需要身份验证",
    "Authentication expired": "身份验证已过期",
    "Authentication failed": "身份验证失败",
    "Authentication required": "需要身份验证",
    "Author": "作者",
    "Authorization code": "授权码",
    "Authorization code sign-in is unavailable in this version.": "此版本不支持授权码登录。",
    "Authorization code was rejected. Paste a fresh code and try again.": "授权码被拒绝。请粘贴新的授权码并重试。",
    "Auto Pin": "自动固定",
    "Auto-Captured": "自动捕获",
    "Auto-assignment not configured": "未配置自动分配",
    "Automated safeguards help to protect your conversations from insecure or unsafe content. That being said, users should be aware of potential agentic risks, including data exfiltration.": "自动化安全防护有助于保护您的对话免受不安全内容的影响。尽管如此，用户仍应注意潜在的智能体风险，包括数据泄露。",
    "Automatically reproduce bugs, trace causes, test fixes.": "自动复现 Bug、追踪根因并测试修复方案。",
    "Automation credentials expired": "自动化凭据已过期",
    "Automation credentials expiring soon": "自动化凭据即将过期",
    "Automation saved": "自动化已保存",
    "Available for": "适用于",
    "Available licenses": "可用许可",
    "Avoid uploading highly sensitive data and verify actions taken by your agent. Make sure you have the": "请避免上传高度敏感的数据，并核实智能体执行的操作。请确保您拥有",
    "Back to all agents": "返回所有智能体",
    "Back to home": "返回主页",
    "Background Task Output": "后台任务输出",
    "Background task": "后台任务",
    "Bad Response": "回复不佳",
    "Base branch for new worktree": "新工作树的基础分支",
    "Baseline model quota reached": "已达到基础模型配额上限",
    "Basic auth": "基本身份验证",
    "Best of N mode is not available": "Best of N 模式不可用",
    "Billing model": "计费模式",
    "Binary file not shown": "不显示二进制文件",
    "Blocked": "已阻止",
    "Blocked by organization policy": "已被组织策略阻止",
    "Blocked, needs input": "已阻塞，需要输入",
    "Blocked: file type not allowed": "已阻止：不允许的文件类型",
    "Bookmarked": "已添加书签",
    "Bookmarking": "正在添加书签",
    "Branch": "分支",
    "Branch actions": "分支操作",
    "Branch names": "分支名称",
    "Browse": "浏览",
    "Browse MCP resources": "浏览 MCP 资源",
    "Browse rules": "浏览规则",
    "Browser Subagent Viewer": "浏览器子智能体查看器",
    "Browser Task": "浏览器任务",
    "Browser Use": "浏览器使用",
    "Browser actions": "浏览器操作",
    "Browser downloads": "浏览器下载",
    "Browser is currently being operated by this conversation in another Hub window": "此对话当前正在另一个 Hub 窗口中操作浏览器",
    "Browser screenshot": "浏览器截图",
    "Browser steps": "浏览器步骤",
    "Browser task": "浏览器任务",
    "Browser task still running…": "浏览器任务仍在运行中…",
    "Browser tools are disabled in the Antigravity Android desktop app.": "浏览器工具已在 Antigravity Android 桌面应用中禁用。",
    "Browser tools are not available in the Antigravity Android desktop app.": "浏览器工具在 Antigravity Android 桌面应用中不可用。",
    "Browser: you took over": "浏览器：您已接管",
    "Browsing Data": "浏览数据",
    "Browsing history": "浏览历史记录",
    "Build new features": "构建新功能",
    "Build with one agent or a team": "使用单个智能体或智能体团队进行构建",
    "Built to help, not hurt": "以助人为本，安全可靠",
    "Business Account Sign In": "企业账号登录",
    "By default, agents work in folders you choose and ask before sensitive changes. Adjust this anytime in Settings.": "默认情况下，智能体仅在您选择的文件夹中工作，并在进行敏感更改前询问您。您随时可以在设置中调整此项。",
    "By using this app, you agree to its": "使用本应用即表示您同意其",
    "CSV spreadsheet attachment": "CSV 电子表格附件",
    "Cache:": "缓存：",
    "Cancel (Ctrl+D)": "取消 (Ctrl+D)",
    "Cancel (⌃C)": "取消 (⌃C)",
    "Cancel All Tasks": "取消所有任务",
    "Cancel Generation": "取消生成",
    "Cancel Questionnaire and Stop the Agent": "取消问卷并停止智能体",
    "Cancel Step": "取消步骤",
    "Cancel Task": "取消任务",
    "Cancel download": "取消下载",
    "Cancel questionnaire": "取消问卷",
    "Cancel recording": "取消录制",
    "Cancel step": "取消步骤",
    "Canceled bookmark of": "已取消添加书签",
    "Canceled creation of": "已取消创建",
    "Canceled deletion of": "已取消删除",
    "Canceled deletion of setup routine": "已取消删除设置例程",
    "Canceled edit to": "已取消编辑",
    "Canceled removal of bookmark": "已取消移除书签",
    "Canceled saving setup routine": "已取消保存设置例程",
    "Cancelled": "已取消",
    "Canvas page · display only": "画布页面 · 仅供展示",
    "Canvas · written by your Chief of Staff · display only": "画布 · 由您的幕僚长撰写 · 仅供展示",
    "Card": "卡片",
    "Certificate details": "证书详情",
    "Certificate is not valid": "证书无效",
    "Certificate is valid": "证书有效",
    "Change model": "更改模型",
    "Change schedule": "更改计划",
    "Changes": "更改",
    "Change…": "更改…",
    "Chat Input": "对话输入",
    "Chat Layout": "对话布局",
    "Chat anyways": "仍然对话",
    "Check that the microphone is unmuted and the right input device is selected.": "请检查麦克风是否已取消静音，并确认已选择正确的输入设备。",
    "Checking access...": "正在检查访问权限...",
    "Checking availability…": "正在检查可用性…",
    "Checking…": "正在检查…",
    "Chief of Staff canvas": "幕僚长画布",
    "Chief of Staff voice mode is active": "幕僚长语音模式已开启",
    "Choose Antigravity's Voice": "选择 Antigravity 的语音",
    "Choose File…": "选择文件…",
    "Choose Region": "选择区域",
    "Choose a Subscription": "选择订阅",
    "Choose between non-colliding VS Code defaults or standalone Antigravity chords.": "在无冲突的 VS Code 默认快捷键或独立的 Antigravity 组合快捷键之间进行选择。",
    "Choose what to clear from the built-in browser. It can't be undone.": "选择要从内置浏览器中清除的数据。此操作无法撤销。",
    "Choose whether to be notified when the agent needs your attention or completes a task.": "选择当智能体需要您关注或完成任务时是否发送通知。",
    "Clear Browsing Data?": "清除浏览数据？",
    "Clear and friendly": "清晰友好",
    "Clear cookies and site data": "清除 Cookie 和网站数据",
    "Clear file filter": "清除文件筛选",
    "Clear filter": "清除筛选",
    "Clear history, cookies and site data from the built-in browser, or manage cookies for each site.": "清除内置浏览器的历史记录、Cookie 和网站数据，或按网站管理 Cookie。",
    "Clear row filter": "清除行筛选",
    "Cleared built-in browser data": "已清除内置浏览器数据",
    "Cleared built-in browser history": "已清除内置浏览器历史记录",
    "Clearing cookies and site data for": "清除",
    "Click to Open Docs": "点击打开文档",
    "Click to disable tool": "点击以禁用工具",
    "Click to enable tool": "点击以启用工具",
    "Click to learn more about sources": "点击了解更多关于来源的信息",
    "Click to open docs": "点击打开文档",
    "Click to respond to the question.": "点击回答此问题。",
    "Click to respond to the questions.": "点击回答这些问题。",
    "Click to view more": "点击查看更多",
    "Click to view or edit comment": "点击查看或编辑评论",
    "Clicked": "已点击",
    "Clicked in Browser": "已在浏览器中点击",
    "Clicking": "正在点击",
    "Clicking in Browser": "正在浏览器中点击",
    "Close Other Tabs": "关闭其他标签页",
    "Close Panel": "关闭面板",
    "Close Sidebar": "关闭侧边栏",
    "Close Tab": "关闭标签页",
    "Close Tabs to the Left": "关闭左侧标签页",
    "Close Tabs to the Right": "关闭右侧标签页",
    "Close downloads": "关闭下载列表",
    "Close message": "关闭消息",
    "Close references": "关闭引用",
    "Close split view and go to forked conversation": "关闭分屏视图并前往分支对话",
    "Cloud": "云端",
    "Code Change Summary": "代码变更摘要",
    "Code Preview": "代码预览",
    "Code block": "代码块",
    "Code search": "代码搜索",
    "Code snippet": "代码片段",
    "Collapse All Folders": "折叠所有文件夹",
    "Collapse Questionnaire": "收起问卷",
    "Collapse command": "折叠命令",
    "Collapse questionnaire": "收起问卷",
    "Collapse queued messages": "折叠排队中的消息",
    "Collapse subagents": "折叠子智能体",
    "Command execution": "命令执行",
    "Command is required": "必须填写命令",
    "Command prompt": "命令提示符",
    "Command:": "命令：",
    "Commands and files these agents can use.": "这些智能体可使用的命令和文件。",
    "Comment": "评论",
    "Comment on Selection": "评论所选内容",
    "Comment on the plan before your agent starts, and get a walkthrough when it finishes.": "在智能体开始前对计划发表评论，并在完成后查看演练说明。",
    "Commit staged changes": "提交已暂存的更改",
    "Commit succeeded": "提交成功",
    "Committing...": "正在提交...",
    "Compacting": "正在压缩",
    "Complete verification": "完成验证",
    "Confident and clear": "自信清晰",
    "Configuration saved successfully!": "配置保存成功！",
    "Configure": "配置",
    "Configure Branches": "配置分支",
    "Configure GitHub access policies.": "配置 GitHub 访问策略。",
    "Configure MCP Server": "配置 MCP 服务器",
    "Configure allowed and denied URLs for the browser subagent (invoked with /browser). Requires": "为浏览器子智能体（通过 /browser 调用）配置允许和拒绝的 URL。需要",
    "Configure allowed and denied URLs for the browser subagent. It runs in the built-in browser, so no separate browser install is needed.": "为浏览器子智能体配置允许和拒绝的 URL。它在内置浏览器中运行，因此无需单独安装浏览器。",
    "Configure built-in browser, link opening, and browser subagent preferences.": "配置内置浏览器、链接打开方式和浏览器子智能体偏好设置。",
    "Configure workspace-specific permissions, resources, and customizations.": "配置工作区专属的权限、资源和自定义项。",
    "Confirm & Save": "确认并保存",
    "Confirm Selection": "确认选择",
    "Conflict": "冲突",
    "Connect GitHub: Run gh auth login in a terminal": "连接 GitHub：在终端中运行 gh auth login",
    "Connect an account so the agent can use this app.": "连接账号，以便智能体使用此应用。",
    "Connect to SSH Host": "连接到 SSH 主机",
    "Connect to SSH Host…": "连接到 SSH 主机…",
    "Connect your account to browse": "连接您的账户以浏览",
    "Connected Google Drive and GitHub resources": "已连接的 Google Drive 和 GitHub 资源",
    "Connecting to language server...": "正在连接到语言服务器...",
    "Connecting to terminal...": "正在连接到终端...",
    "Connecting…": "正在连接…",
    "Connection is secure": "连接安全",
    "Connection security information is not available for this page": "此页面没有可用的连接安全信息",
    "Connectors": "连接器",
    "Contact your administrator to set up Gemini Enterprise for this project": "请联系您的管理员为此项目设置 Gemini Enterprise",
    "Contents": "内容",
    "Continue": "继续",
    "Continue with Google": "使用 Google 账号继续",
    "Continue with Google Cloud": "使用 Google Cloud 继续",
    "Continue with SSO": "使用 SSO 继续",
    "Continue with different account": "使用其他账号继续",
    "Controls whether terminal commands require your approval before running.\n\nNote: A change to this setting will only apply to new messages sent to the agent. In-progress responses will use the previous setting value.": "控制终端命令在运行前是否需要您的批准。\n\n注意：更改此设置仅对发送给智能体的新消息生效。正在进行中的回复将使用之前的设置值。",
    "Conversation Archived": "对话已归档",
    "Conversation Unarchived": "对话已取消归档",
    "Conversation copied as Markdown to clipboard": "已将对话复制为 Markdown 到剪贴板",
    "Conversation limit reached": "已达到对话上限",
    "Conversation link": "对话链接",
    "Conversation turns": "对话轮次",
    "Conversation unavailable": "对话不可用",
    "Cookies and other site data": "Cookie 及其他网站数据",
    "Cookies and site data": "Cookie 和网站数据",
    "Cookies by Site": "按网站管理 Cookie",
    "Cookies the built-in browser stores for each site. Deleting a site's cookies usually signs you out of it. Other site data (local storage, IndexedDB, cache) is cleared only by Browsing Data → Clear.": "内置浏览器为每个网站存储的 Cookie。删除某个网站的 Cookie 通常会使您退出该网站的登录状态。其他网站数据（本地存储、IndexedDB、缓存）仅通过“浏览数据 → 清除”进行清除。",
    "Cookies, site storage and cache. Signs you out of all sites in the built-in browser and reloads its open tabs.": "Cookie、网站存储和缓存。这会使您退出内置浏览器中所有网站的登录状态，并重新加载已打开的标签页。",
    "Coordinator goal": "协调器目标",
    "Coordinator name": "协调器名称",
    "Coordinator settings": "协调器设置",
    "Copied sign-in link to clipboard": "已将登录链接复制到剪贴板",
    "Copied to clipboard": "已复制到剪贴板",
    "Copied transcript": "已复制转录内容",
    "Copied version details": "已复制版本详情",
    "Copied!": "已复制！",
    "Copy Command": "复制命令",
    "Copy Conversation Markdown": "复制对话 Markdown",
    "Copy File Name": "复制文件名",
    "Copy File Path": "复制文件路径",
    "Copy Image": "复制图片",
    "Copy Project Name": "复制项目名称",
    "Copy Workspace Name": "复制工作区名称",
    "Copy as Markdown": "复制为 Markdown",
    "Copy command": "复制命令",
    "Copy error messages": "复制错误消息",
    "Copy full URL to clipboard": "复制完整 URL 到剪贴板",
    "Copy gh auth login command": "复制 gh auth login 命令",
    "Copy output": "复制输出",
    "Copy path": "复制路径",
    "Copy sign-in link": "复制登录链接",
    "Copy the folder elsewhere first if you might want it back.": "如果日后可能需要恢复，请先将文件夹复制到其他位置。",
    "Copy to clipboard": "复制到剪贴板",
    "Copy transcript": "复制转录内容",
    "Copy version details": "复制版本详情",
    "Couldn't archive conversation": "无法归档对话",
    "Couldn't clear browsing data. Try again.": "无法清除浏览数据。请重试。",
    "Couldn't connect": "无法连接",
    "Couldn't connect to": "无法连接到",
    "Couldn't create the coordinator. Try again.": "无法创建协调器，请重试。",
    "Couldn't delete cookies for": "无法删除以下网站的 Cookie：",
    "Couldn't delete your data. Try again.": "无法删除您的数据。请重试。",
    "Couldn't edit queued message": "无法编辑排队消息",
    "Couldn't fetch the Google Drive file's title. The link was kept as-is.": "无法获取 Google Drive 文件标题。链接已保持原样。",
    "Couldn't load Google Drive link title": "无法加载 Google Drive 链接标题",
    "Couldn't load cookies.": "无法加载 Cookie。",
    "Couldn't load message": "无法加载消息",
    "Couldn't load your SSH hosts. You can still type one.": "无法加载您的 SSH 主机。您仍可以手动输入。",
    "Couldn't mark as unread conversation": "无法将对话标记为未读",
    "Couldn't mark conversations as read": "无法将对话标记为已读",
    "Couldn't move conversation": "无法移动对话",
    "Couldn't restore conversation": "无法恢复对话",
    "Couldn't search files": "无法搜索文件",
    "Couldn't set permissions for conversation": "无法设置对话权限",
    "Couldn't start the coordinator:": "无法启动协调器：",
    "Couldn’t send. Try again.": "发送失败，请重试。",
    "Create Coordinator": "创建协调器",
    "Create New": "新建",
    "Create a Project": "创建项目",
    "Create a token": "创建令牌",
    "Create plugin": "创建插件",
    "Created a new branch on Origin.": "已在 Origin 上创建新分支。",
    "Created outline": "已创建大纲",
    "Creating Fork...": "正在创建分支...",
    "Creating environment...": "正在创建环境...",
    "Creating projects for your conversations": "正在为您的对话创建项目",
    "Creating the forked conversation...": "正在创建分支对话...",
    "Creating workspace for the forked conversation...": "正在为分支对话创建工作区...",
    "Creating worktree for the forked conversation...": "正在为分支对话创建工作树...",
    "Creating...": "正在创建...",
    "Creating…": "正在创建…",
    "Credentials are only sent to the domains listed.": "凭据仅会发送至列出的域名。",
    "Credentials expired. This automation will not run until credentials are refreshed": "凭据已过期。刷新凭据后此自动化才会运行",
    "Credentials expiring soon. Refresh credentials to keep this automation running": "凭据即将过期。请刷新凭据以保持此自动化运行",
    "Credentials for one or more automations expire in less than a week.": "一个或多个自动化的凭据将在不到一周内过期。",
    "Credentials for one or more automations have expired.": "一个或多个自动化的凭据已过期。",
    "Credentials stay on this machine and are only sent to the domains listed.": "凭据仅保留在本机，且仅会发送至列出的域名。",
    "Cumulative Total": "累计总计",
    "Curated sets of plugins for common workflows and roles.": "面向常见工作流和角色的精选插件合集。",
    "Current parameter:": "当前参数：",
    "Current workspace": "当前工作区",
    "Custom Agent Error:": "自定义智能体错误：",
    "Custom Order": "自定义排序",
    "Custom View": "自定义视图",
    "Custom schedule": "自定义计划",
    "Customization token budget exceeded. Large customizations are excluded from context.": "已超出自定义项 Token 预算。较大的自定义项已从上下文中排除。",
    "Customizations views": "自定义项视图",
    "Customize Global Skills": "自定义全局技能",
    "Customize Shortcuts": "自定义快捷键",
    "Customize your experience across the agent, plugins, and product from the settings and marketplace. We won’t show you ads or let advertisers influence what": "您可以在设置和插件市场中自定义智能体、插件和产品的使用体验。我们不会向您展示广告，也不会让广告商影响",
    "Daily": "每天",
    "Daily conversation limit reached": "已达到每日对话上限",
    "Daily environment time used": "每日环境时长已用尽",
    "Dark preview": "深色预览",
    "Day of the month": "每月日期",
    "Day of the week": "星期几",
    "Days": "星期",
    "Debug and fix": "调试与修复",
    "Decline": "拒绝",
    "Decorations": "装饰标记",
    "Deep and velvety": "低沉柔和",
    "Delete Group": "删除分组",
    "Delete MCP Server": "删除 MCP 服务器",
    "Delete Project": "删除项目",
    "Delete Side Question": "删除旁支提问",
    "Delete Skill": "删除技能",
    "Delete Task": "删除任务",
    "Delete Workspace": "删除工作区",
    "Delete agent": "删除智能体",
    "Delete comment": "删除评论",
    "Delete organization policy": "删除组织策略",
    "Delete plugin": "删除插件",
    "Delete repository policy": "删除仓库策略",
    "Delete server": "删除服务器",
    "Delete side question": "删除旁支提问",
    "Deleted setup routine": "已删除设置例程",
    "Deleting setup routine": "正在删除设置例程",
    "Deleting...": "正在删除...",
    "Demoted": "已降级",
    "Denied Sites": "已拒绝的网站",
    "Deny setting up browser": "拒绝设置浏览器",
    "Describe the feature you would like to see...": "描述您希望看到的功能...",
    "Describe what you want. Your agent plans and builds it, and brings in other agents when needed.": "描述您的需求。您的智能体将进行规划和构建，并在需要时引入其他智能体。",
    "Describe your Remote Control issue...": "描述您的远程控制问题...",
    "Describe your auth or billing issue...": "描述您的身份验证或计费问题...",
    "Describe your changes, or leave empty to auto-generate": "描述您的更改，或留空以自动生成",
    "Desktop": "桌面",
    "Details": "详情",
    "Did restarting the desktop app help?": "重启桌面应用是否有帮助？",
    "Diff contents are no longer available.": "差异内容已不可用。",
    "Directory Viewer": "目录查看器",
    "Directory not shown": "不显示目录",
    "Disabled by organization policy": "已由组织策略禁用",
    "Disabled. Open Details to finish setup or enable.": "已禁用。打开详情以完成配置或启用。",
    "Disabling or removing this bundle doesn't affect it.": "禁用或移除此插件包不会影响它。",
    "Discard": "丢弃",
    "Discard comment draft": "丢弃评论草稿",
    "Disconnect": "断开连接",
    "Disconnected": "已断开连接",
    "Disk is full. Search will no longer match in conversation bodies until you clear up space and restart.": "磁盘空间已满。在您清理空间并重启之前，搜索将不再匹配对话正文内容。",
    "Dismiss Tip": "关闭提示",
    "Dismiss artifact update notice": "忽略产物更新通知",
    "Dismiss error": "关闭错误提示",
    "Dismiss microphone warning": "关闭麦克风警告",
    "Dismiss notification": "忽略通知",
    "Dismiss service announcement": "关闭服务公告",
    "Dismiss suggestion": "忽略建议",
    "Display": "显示",
    "Docs, Sheets, Slides, and folders": "文档、表格、幻灯片和文件夹",
    "Document": "文档",
    "Document Answers": "文档回答",
    "Document attachment": "文档附件",
    "Document file size exceeds 10MB limit": "文档文件大小超过 10MB 限制",
    "Domains:": "域名：",
    "Download files": "下载文件",
    "Download from": "下载自",
    "Download this site as an app to get notified when the agent needs your attention or completes a task.": "将此网站下载为应用，以便在智能体需要您关注或完成任务时收到通知。",
    "Downloading Update": "正在下载更新",
    "Downloading...": "正在下载...",
    "Downloads": "下载",
    "Downloads, in progress": "下载，正在进行中",
    "Draft documents, emails, and notes that sound like you.": "起草符合您风格的文档、邮件和笔记。",
    "Drag to move": "拖动以移动",
    "Drag to select a region to comment": "拖动以选择要评论的区域",
    "Dragged in Browser": "已在浏览器中拖动",
    "Dragging in Browser": "正在浏览器中拖动",
    "Drop to attach": "拖放以添加附件",
    "Each rule lets the agent run the listed workflow files on the listed refs — each a comma-separated list like ci.yml, deploy.yml and main, dev (glob patterns like fix-* allowed), or * for all. Both fields must be set for a rule to grant anything.": "每条规则允许智能体在列出的引用上运行列出的工作流文件——每项均为逗号分隔的列表，例如 ci.yml, deploy.yml 和 main, dev（支持 fix-* 等通配符模式），或使用 * 表示全部。必须同时设置两个字段，规则才会授予权限。",
    "Edit Comment": "编辑评论",
    "Edit Model": "编辑模型",
    "Edit comment": "编辑评论",
    "Edit permission target": "编辑权限目标",
    "Edit project name": "编辑项目名称",
    "Edit title": "编辑标题",
    "Edit workspace name": "编辑工作区名称",
    "Embedded web preview": "嵌入式网页预览",
    "Embedding Limitations": "嵌入限制",
    "Empty \"in []\" list literal is not allowed": "不允许使用空的 \"in []\" 列表字面量",
    "Empty directory": "空目录",
    "Empty log": "空日志",
    "Empty message": "空消息",
    "Empty table": "空表格",
    "Enable Browser Agent": "启用浏览器智能体",
    "Enable Notifications": "启用通知",
    "Enable Overages": "启用超额用量",
    "Enable Recommended Skills": "启用推荐技能",
    "Enable fine-grained GitHub permissions and define the org, repository, and resource-level access the agent is allowed to use.": "启用细粒度 GitHub 权限，并定义允许智能体使用的组织、仓库和资源级访问权限。",
    "Enable the plugin to sign in.": "启用插件以登录。",
    "Enable this plugin to manage its accounts.": "启用此插件以管理其账户。",
    "Enabled": "已启用",
    "Enabling...": "正在启用...",
    "Enter Google Cloud Project Details": "输入 Google Cloud 项目详情",
    "Enter [user@]host[:port], or pick a host from your SSH config.": "输入 [user@]host[:port]，或从您的 SSH 配置中选择一个主机。",
    "Enter always submits. This adds a second shortcut.": "Enter 始终用于提交。此操作会添加第二个快捷键。",
    "Enter project name...": "输入项目名称...",
    "Enter target...": "输入目标...",
    "Enter the required configuration values to install this MCP server.": "输入所需的配置值以安装此 MCP 服务器。",
    "Enter your feedback here...": "在此输入您的反馈...",
    "Enterprise": "企业版",
    "Enterprise Gateway": "企业网关",
    "Environments": "环境",
    "Equalize Split Panes": "等分拆分窗格",
    "Error Details:": "错误详情：",
    "Error Loading Models": "加载模型出错",
    "Error fetching MCP prompt": "获取 MCP 提示词时出错",
    "Error loading Browser recording": "加载浏览器录制时出错",
    "Error occurred during import.": "导入过程中出错。",
    "Error sending input to command": "向命令发送输入时出错",
    "Error sending termination request to command": "向命令发送终止请求时出错",
    "Error:": "错误：",
    "Error: Artifacts from remote conversations are not available here.": "错误：此处无法查看远程对话中的产物。",
    "Error: No artifact URI provided in URL parameters.": "错误：URL 参数中未提供产物 URI。",
    "Errors": "错误",
    "Europe": "欧洲",
    "Excluded": "已排除",
    "Executed notebook": "已执行 Notebook",
    "Executed notebook cells": "已执行 Notebook 单元格",
    "Executing notebook": "正在执行 Notebook",
    "Executing notebook cells": "正在执行 Notebook 单元格",
    "Exit inspect element mode (Esc)": "退出检查元素模式 (Esc)",
    "Expand": "展开",
    "Expand All Folders": "展开所有文件夹",
    "Expand Questionnaire": "展开问卷",
    "Expand questionnaire": "展开问卷",
    "Expand queued messages": "展开排队中的消息",
    "Expand subagents": "展开子智能体",
    "Experimental": "实验性",
    "Explore the plugin marketplace": "探索插件市场",
    "Export Artifact": "导出产物",
    "Export artifact": "导出产物",
    "Extracted DOM elements": "已提取 DOM 元素",
    "Extracting DOM elements": "正在提取 DOM 元素",
    "Failed to execute notebook": "执行 Notebook 失败",
    "Failed to execute notebook cells": "执行 Notebook 单元格失败",
    "Fallback Summary Used": "已使用备用摘要",
    "Featured": "精选",
    "Fetched network request": "已获取网络请求",
    "Fetched network requests": "已获取网络请求",
    "Fetching network request": "正在获取网络请求",
    "Fetching network requests": "正在获取网络请求",
    "File Explorer": "文件资源管理器",
    "File Tree Component is not loaded.": "文件树组件未加载。",
    "File Viewer": "文件查看器",
    "File attachment": "文件附件",
    "File exceeds 512 KB table preview limit.": "文件超过 512 KB 表格预览限制。",
    "File explorer": "文件资源管理器",
    "File not found": "未找到文件",
    "File path breadcrumbs": "文件路径面包屑",
    "File size exceeds 20MB limit": "文件大小超过 20MB 限制",
    "Files and resources in cloud workspaces": "云工作区中的文件和资源",
    "Files modified by the agent in this conversation": "智能体在此对话中修改的文件",
    "Files to edit:": "要编辑的文件：",
    "Files, folders, and repositories you connect are accessible to your agent in this project, including during background or scheduled runs.": "您连接的文件、文件夹和代码库可供智能体在此项目中访问，包括在后台运行或计划运行期间。",
    "Filter agents": "筛选智能体",
    "Filter files": "筛选文件",
    "Filter files...": "筛选文件...",
    "Filter resources...": "筛选资源...",
    "Filter rows": "筛选行",
    "Filter rows...": "筛选行...",
    "Finalizing transcription...": "正在完成转录...",
    "Finalizing...": "正在完成...",
    "Find References": "查找引用",
    "Find plugins - bundles of skills, agents, MCP servers, UI extensions and more, and install them in one click.": "发现各类插件（包含技能、智能体、MCP 服务器、UI 扩展等），并支持一键安装。",
    "Finder": "访达",
    "Finish signing in in your browser.": "请在浏览器中完成登录。",
    "Fires after a tool step completes.": "在工具步骤完成后触发。",
    "Fires after tool calls finish.": "在工具调用结束后触发。",
    "Fires before a tool step executes.": "在工具步骤执行前触发。",
    "Fires before the model is called.": "在调用模型前触发。",
    "Fires when the execution loop terminates.": "在执行循环终止时触发。",
    "Fit": "适应",
    "Flask": "烧瓶",
    "Focus this tile": "聚焦此窗格",
    "Fold code block": "折叠代码块",
    "Folder doesn't exist": "文件夹不存在",
    "Folders these agents can access.": "这些智能体可访问的文件夹。",
    "Font": "字体",
    "Footnotes": "脚注",
    "For Antigravity Business consumption options, see": "有关 Antigravity Business 用量选项，请参阅",
    "For Turn": "针对轮次",
    "For any feedback that does not fit into the above categories.": "用于不属于上述类别的任何反馈。",
    "Fork Environment Notice": "分支环境通知",
    "Fork in Current Workspace": "在当前工作区创建分支",
    "Fork warning": "创建分支警告",
    "Forked from": "分支自",
    "Forward": "前进",
    "Found references to": "已找到以下引用",
    "Friday": "星期五",
    "Full View": "完整视图",
    "Full output written to": "完整输出已写入",
    "Gauge": "仪表盘",
    "Generated image": "已生成图像",
    "Generated image preview": "生成的图片预览",
    "Generated media": "生成的媒体",
    "Generating commit message...": "正在生成提交信息...",
    "Generation Steps (": "生成步骤（",
    "Generations": "生成次数",
    "Generic Tool": "通用工具",
    "Get API key": "获取 API 密钥",
    "Get Anything Done with": "轻松搞定一切，尽在",
    "Get Started": "开始使用",
    "Get notified when the agent needs your attention or completes a task.": "在智能体需要您关注或完成任务时收到通知。",
    "Get started": "开始使用",
    "Getting scripts...": "正在获取脚本...",
    "Getting started with Google Antigravity": "开始使用 Google Antigravity",
    "Git commit": "Git 提交",
    "GitHub Personal Access Token": "GitHub 个人访问令牌",
    "GitHub: not signed in": "GitHub：未登录",
    "Go to": "前往",
    "Go to Home": "返回主页",
    "Go to the machine you are controlling and quit Antigravity. It installs pending updates the next time it starts.": "前往您正在控制的计算机并退出 Antigravity。下次启动时将自动安装待处理的更新。",
    "Goal": "目标",
    "Goal Verification": "目标验证",
    "Going back": "正在返回",
    "Going forward": "正在前进",
    "Good Response": "回复不错",
    "Good to see you. What's next?": "很高兴见到您。接下来做什么？",
    "Google Antigravity Terms of Service": "《Google Antigravity 服务条款》",
    "Google Cloud Project ID": "Google Cloud 项目 ID",
    "Google One Referral": "Google One 推荐",
    "Google Privacy Policy": "《Google 隐私权政策》",
    "Google Search": "Google 搜索",
    "Got it": "知道了",
    "Grand Total": "总计",
    "Grant administrator access for": "授予管理员权限以执行",
    "Grant create, update, or delete access to specific branches.": "授予对特定分支的创建、更新或删除权限。",
    "Grant read access to workflow runs and allow dispatching workflows on specific files and refs.": "授予工作流运行的读取权限，并允许在特定文件和引用上触发工作流。",
    "Grant repository access": "授予代码仓库访问权限",
    "Grant the selected actions on the listed branch names — a comma-separated list like main, dev, prod (glob patterns like fix-* allowed), or * for all.": "对列出的分支名称授予所选操作权限——以逗号分隔的列表，例如 main, dev, prod（支持 fix-* 等通配符模式），或使用 * 表示全部。",
    "Grant the selected actions on the listed issue numbers — a comma-separated list like 1, 2, 3, or * for all.": "对列出的议题编号授予所选操作权限——以逗号分隔的列表，例如 1, 2, 3，或使用 * 表示全部。",
    "Grant the selected actions on the listed pull request numbers — a comma-separated list like 1, 2, 3, or * for all.": "对列出的拉取请求编号授予所选操作权限——以逗号分隔的列表，例如 1, 2, 3，或使用 * 表示全部。",
    "Grid": "网格",
    "Group Actions": "分组操作",
    "Hand off a feature and come back to working code.": "交出功能需求，坐等可用代码完成。",
    "Handler #": "处理程序 #",
    "Having trouble signing in?": "登录遇到问题？",
    "Here's how uploaded files, attachments, and connected resources work in your cloud environment": "以下是上传的文件、附件和已连接资源在您的云环境中的工作方式",
    "Here's how you and your agents work together": "以下是您与智能体协同工作的方式",
    "Hey there!": "您好！",
    "Hey there, what should we build today?": "你好，今天我们来构建点什么？",
    "Hidden by policy": "已根据策略隐藏",
    "Hidden by the preview policy.": "已根据预览策略隐藏。",
    "Hidden hosts": "已隐藏的主机",
    "Hide Error": "隐藏错误",
    "Hide earlier steps": "隐藏较早的步骤",
    "Hide from this list": "从此列表中隐藏",
    "Hide token": "隐藏令牌",
    "Hide tools": "隐藏工具",
    "Hold": "按住",
    "Honors standard VS Code shortcuts without collisions (e.g. Ctrl+L Focus Input, Ctrl+Shift+L New Conversation, Ctrl+Shift+A Picker, Ctrl+Shift+, Settings).": "遵循标准 VS Code 快捷键且不产生冲突（例如 Ctrl+L 聚焦输入框、Ctrl+Shift+L 新建对话、Ctrl+Shift+A 选择器、Ctrl+Shift+, 设置）。",
    "Honors standard VS Code shortcuts without collisions (e.g. ⌘L Focus Input, ⌘⇧L New Conversation, ⌘⇧A Picker, ⌘⇧, Settings).": "遵循标准 VS Code 快捷键且不产生冲突（例如 ⌘L 聚焦输入框、⌘⇧L 新建对话、⌘⇧A 选择器、⌘⇧, 设置）。",
    "Hook will only trigger if the tool name matches run_command or view_file.": "仅当工具名称匹配 run_command 或 view_file 时才会触发钩子。",
    "Hook will only trigger if the tool name matches run_command.": "仅当工具名称匹配 run_command 时才会触发钩子。",
    "Hook will only trigger if the tool name starts with browser_.": "仅当工具名称以 browser_ 开头时才会触发钩子。",
    "Hook will trigger if any tool is executed.": "执行任何工具时都会触发钩子。",
    "Hook with this name already exists": "已存在同名的钩子",
    "Host": "主机",
    "Hourly": "每小时",
    "Hovering": "正在悬停",
    "How often": "重复频率",
    "How this feature would help you and other users": "此功能将如何帮助您和其他用户",
    "Idle": "空闲",
    "Idle Guard Warning": "空闲保护警告",
    "If you add multiple accounts, MCP servers use the one marked Default.": "如果您添加了多个账户，MCP 服务器将使用标记为“默认”的账户。",
    "Image": "图像",
    "Image Answers": "图片回答",
    "Image URL:": "图片 URL：",
    "Image attachment": "图像附件",
    "Image preview not available": "图像预览不可用",
    "Image rendering blocked (strict mode enabled)": "已阻止图片渲染（已启用严格模式）",
    "Import AI Studio Project": "导入 AI Studio 项目",
    "Importing shared conversation...": "正在导入共享对话...",
    "In Progress": "进行中",
    "In progress": "进行中",
    "In this case,": "在此情况下，共有",
    "Incomplete operator at end of expression": "表达式末尾的运算符不完整",
    "Inherits your Global Permissions when working in these conversations.": "在这些对话中工作时继承您的全局权限。",
    "Inline PDF preview is not available in this environment.": "当前环境不支持内联 PDF 预览。",
    "Input:": "输入：",
    "Insert into main conversation": "插入到主对话",
    "Inspect element to comment": "检查元素以添加评论",
    "Inspect live bindings or record custom key chords filtered to": "查看实时按键绑定，或录制自定义组合快捷键，筛选条件为",
    "Inspected commit": "已检查提交",
    "Install": "安装",
    "Install Update": "安装更新",
    "Install or enable the Google Drive plugin in Customizations to search files with @drive: or paste Drive links": "在自定义项中安装或启用 Google Drive 插件，即可使用 @drive: 搜索文件或粘贴 Drive 链接",
    "Installed separately": "已单独安装",
    "Installing": "正在安装",
    "Installing Update": "正在安装更新",
    "Installing...": "正在安装...",
    "Instructions": "指令",
    "Insufficient AI Credits": "AI 积分不足",
    "Intended primarily for previewing local development servers (e.g.,": "主要用于预览本地开发服务器（例如",
    "Interface Layout": "界面布局",
    "Internal search": "内部搜索",
    "Interrupt Agent": "中断智能体",
    "Invite a Friend": "邀请好友",
    "Invite now": "立即邀请",
    "Invoked subagent": "已调用子智能体",
    "Issue actions": "议题操作",
    "Issue creation": "创建议题",
    "Issue numbers": "议题编号",
    "Issued by": "颁发者",
    "Issued to": "颁发给",
    "Issues": "议题",
    "It was already sent or couldn't be removed from the queue.": "该消息已发送或无法从队列中移除。",
    "Join the Google Chat space": "加入 Google Chat 聊天室",
    "Jump to Next Prompt": "跳转到下一条提示词",
    "Jump to Previous Prompt": "跳转到上一条提示词",
    "Keep Open": "保持打开",
    "Keeps working in this workspace. Nothing is copied.": "继续在此工作区中工作。不会复制任何内容。",
    "Keeps your checkout untouched": "保持当前检出内容不变",
    "Keybinding Scheme": "按键绑定方案",
    "Kill Terminal": "终止终端",
    "Killed": "已终止",
    "Knowledge Generation": "知识生成",
    "Labs": "实验室",
    "Last Used": "上次使用",
    "Launching the browser...": "正在启动浏览器...",
    "Leave a comment": "添加评论",
    "Legacy Dark": "经典深色",
    "Legacy Light": "经典浅色",
    "Let the agent open URLs, read web pages, and interact with browser content. This gives the agent access to important (and often critical) knowledge and methods of validation, but any browser integration does increase exposure to external malicious parties for security exploits.": "允许智能体打开 URL、读取网页并与浏览器内容交互。这使智能体能够获取重要（且往往关键）的知识和验证方式，但任何浏览器集成都会增加暴露于外部恶意攻击和安全漏洞的风险。",
    "Let's tailor the experience for you. What best describes your work?": "让我们为您量身定制体验。以下哪项最符合您的工作？",
    "License Required": "需要许可",
    "License:": "许可：",
    "Light and precise": "轻快精准",
    "Light preview": "浅色预览",
    "Link copied to clipboard.": "链接已复制到剪贴板。",
    "List resources:": "列出资源：",
    "Listening. Ask anything.": "正在聆听，请随时提问。",
    "Live": "实时",
    "Live chat": "实时对话",
    "Live transcript": "实时转录",
    "Load older messages": "加载更早的消息",
    "Loading Browser recording...": "正在加载浏览器录制...",
    "Loading MCP servers...": "正在加载 MCP 服务器...",
    "Loading Notebook View...": "正在加载 Notebook 视图...",
    "Loading apps...": "正在加载应用...",
    "Loading available plugins...": "正在加载可用插件...",
    "Loading browser steps…": "正在加载浏览器步骤…",
    "Loading bundles...": "正在加载插件包...",
    "Loading conversations...": "正在加载对话...",
    "Loading cookies…": "正在加载 Cookie…",
    "Loading customizations...": "正在加载自定义项...",
    "Loading hooks...": "正在加载钩子...",
    "Loading hosts…": "正在加载主机…",
    "Loading installed plugins...": "正在加载已安装的插件...",
    "Loading licenses...": "正在加载许可...",
    "Loading plugins...": "正在加载插件...",
    "Loading preview…": "正在加载预览…",
    "Loading resources...": "正在加载资源...",
    "Loading runs…": "正在加载运行记录…",
    "Loading subagent...": "正在加载子智能体...",
    "Loading token usage...": "正在加载 Token 用量...",
    "Loading workspace customizations...": "正在加载工作区自定义项...",
    "Loading worktrees...": "正在加载工作树...",
    "Loading...": "正在加载...",
    "Loading…": "正在加载…",
    "Local": "本地",
    "Local Checkout": "本地检出",
    "Location:": "位置：",
    "Log back in": "重新登录",
    "Log in": "登录",
    "Log in to use the agent": "登录以使用智能体",
    "Long pages like this one will be broken down into outlines and read as needed. Read more at our": "像这样的长页面将被拆分为大纲并按需阅读。更多信息请参阅我们的",
    "Lost connection to the language server. Agent features may not work.": "与语言服务器的连接已断开。智能体功能可能无法正常工作。",
    "Lost connection to the remote instance. Please wait a minute or refresh the page.": "与远程实例的连接已断开。请稍候片刻或刷新页面。",
    "MCP App": "MCP 应用",
    "MCP Configuration Error:": "MCP 配置错误：",
    "MCP Install Error:": "MCP 安装错误：",
    "MCP Servers Disabled": "MCP 服务器已禁用",
    "MCP error": "MCP 错误",
    "MCP tools": "MCP 工具",
    "Machine": "整机",
    "Make default": "设为默认",
    "Manage": "管理",
    "Manage License": "管理许可",
    "Manage Permissions": "管理权限",
    "Manage and delete your data anytime": "随时管理和删除您的数据",
    "Manage fine-grained permissions for GitHub.": "管理 GitHub 的细粒度权限。",
    "Manage project folders and settings.": "管理项目文件夹和设置。",
    "Manage project folders, agent settings, and permissions.": "管理项目文件夹、智能体设置和权限。",
    "Manage project resources and settings.": "管理项目资源和设置。",
    "Manage project resources, agent settings, and permissions.": "管理项目资源、智能体设置和权限。",
    "Manage workspace folders and settings.": "管理工作区文件夹和设置。",
    "Manage workspace folders, agent settings, and permissions.": "管理工作区文件夹、智能体设置和权限。",
    "Manage workspace resources and settings.": "管理工作区资源和设置。",
    "Manage workspace resources, agent settings, and permissions.": "管理工作区资源、智能体设置和权限。",
    "Manage your conversations from the companion website.": "通过配套网站管理您的对话。",
    "Manage your keybinding scheme and customize shortcuts in VS Code.": "在 VS Code 中管理您的按键绑定方案并自定义快捷键。",
    "Managed by application menu": "由应用菜单管理",
    "Manually Captured": "手动捕获",
    "Manually Rejected": "手动拒绝",
    "Many external websites (such as Google Search, GitHub, or Wikipedia) restrict iframe embedding via": "许多外部网站（例如 Google 搜索、GitHub 或维基百科）会通过",
    "Mark All as Read": "全部标记为已读",
    "Mark This Conversation as Read": "将此对话标记为已读",
    "Mark This Conversation as Unread": "将此对话标记为未读",
    "Markdown attachment": "Markdown 附件",
    "Marked 1 conversation as read": "已将 1 个对话标记为已读",
    "Marketplace notice": "插件市场通知",
    "Matcher:": "匹配器：",
    "Maximize Width": "最大化宽度",
    "Media actions": "媒体操作",
    "Merge Conflict": "合并冲突",
    "Mermaid diagram": "Mermaid 图表",
    "Messaging subagents isn't supported in remote conversations yet.": "远程对话暂不支持向子智能体发送消息。",
    "Microphone access is blocked by your operating system. Grant microphone permission in System Settings and try again.": "您的操作系统已阻止麦克风访问权限。请在系统设置中授予麦克风权限，然后重试。",
    "Microphone blocked in browser site settings.": "麦克风已在浏览器网站设置中被阻止。",
    "Microphone blocked in system settings.": "麦克风已在系统设置中被阻止。",
    "Microphone blocked. Allow in": "麦克风已被阻止。请允许访问：",
    "Microphone capture ended unexpectedly.": "麦克风采集意外结束。",
    "Microphone capture failed.": "麦克风采集失败。",
    "Microphone capture is not supported in this environment.": "当前环境不支持麦克风采集。",
    "Microphone didn't respond.": "麦克风未响应。",
    "Microphone is already in use by another recording session.": "麦克风正被另一个录制会话占用。",
    "Microphone is in use or unavailable.": "麦克风正在使用中或不可用。",
    "Microphone problem": "麦克风问题",
    "Microphone silent": "麦克风无声音",
    "Minimize Width": "最小化宽度",
    "Minimized": "已最小化",
    "Model Summarization Failed": "模型摘要生成失败",
    "Model quota reached": "已达到模型配额上限",
    "Models Tab": "模型标签页",
    "Modified": "已修改",
    "Modified in": "修改于",
    "Monday": "星期一",
    "More actions": "更多操作",
    "More options": "更多选项",
    "Mouse button pressed": "已按下鼠标按键",
    "Mouse button released": "已释放鼠标按键",
    "Move Down": "下移",
    "Move Up": "上移",
    "Move to New Group": "移动到新分组",
    "Moved Mouse in Browser": "已在浏览器中移动鼠标",
    "Moving Mouse in Browser": "正在浏览器中移动鼠标",
    "Must be positive": "必须为正数",
    "Mute Antigravity": "静音 Antigravity",
    "Name": "名称",
    "Needs Attention": "需要注意",
    "Needs attention": "需要关注",
    "Needs your approval": "需要您的批准",
    "Network error. Check your connection and try again.": "网络错误。请检查您的网络连接并重试。",
    "New Agent Script": "新建智能体脚本",
    "New Browser": "新建浏览器",
    "New Conversation in Project": "在项目中新建对话",
    "New Conversation in Workspace": "在工作区中新建对话",
    "New Coordinator": "新建协调器",
    "New Preview": "新建预览",
    "New Side Question": "新建旁支提问",
    "New Terminal Tab": "新建终端标签页",
    "New Window": "新建窗口",
    "New Worktree": "新建工作树",
    "New chats will be grouped by workspace.": "新对话将按工作区进行分组。",
    "New conversation": "新建对话",
    "New coordinator": "新建协调器",
    "New hook name": "新钩子名称",
    "New models have been enabled for you!": "已为您启用新模型！",
    "New tab": "新建标签页",
    "Next": "下一个",
    "Next card": "下一张卡片",
    "Next question": "下一题",
    "Next voice": "下一个语音",
    "Next: Review Permissions": "下一步：审阅权限",
    "Nickname": "昵称",
    "No MCP servers found for \"": "未找到匹配的 MCP 服务器：\"",
    "No Model Selected": "未选择模型",
    "No Models Available": "无可用模型",
    "No Plugins Available": "暂无可用插件",
    "No access": "无访问权限",
    "No active terminals": "无活动终端",
    "No agent is working right now.": "当前没有正在工作的智能体。",
    "No answer provided": "未提供回答",
    "No apps available.": "暂无可用应用。",
    "No apps connected yet. Connect one from Marketplace.": "尚未连接任何应用。请前往插件市场连接。",
    "No background tasks": "无后台任务",
    "No branches": "无分支",
    "No browser pages open": "未打开浏览器页面",
    "No browser steps recorded": "未记录浏览器步骤",
    "No bundles available.": "暂无可用插件包。",
    "No changes to amend": "没有可修补的更改",
    "No changes to review": "没有可审阅的更改",
    "No commit to amend": "没有可修补的提交",
    "No commits to push": "没有可推送的提交",
    "No compatible devices found.": "未找到兼容的设备。",
    "No content available for this resource": "此资源无可用内容",
    "No customizations match your search.": "没有符合您搜索条件的自定义项。",
    "No description available.": "暂无描述。",
    "No documents": "无文档",
    "No environments found": "未找到环境",
    "No file changes": "无文件更改",
    "No files or folders found": "未找到文件或文件夹",
    "No folder selected": "未选择文件夹",
    "No folders added yet.": "尚未添加任何文件夹。",
    "No handlers configured for": "未配置处理程序：",
    "No hosts in": "以下配置中没有主机：",
    "No instructions.": "暂无指令。",
    "No internet. Agent features may not work.": "无网络连接。智能体功能可能无法正常工作。",
    "No keyboard shortcuts found matching your filter.": "未找到符合筛选条件的键盘快捷键。",
    "No license available for this project and location": "此项目和位置没有可用的许可",
    "No links": "暂无链接",
    "No longer available": "已不再可用",
    "No matching files": "无匹配文件",
    "No matching items": "没有匹配项",
    "No matching plugins found.": "未找到匹配的插件。",
    "No matching project folders. Apply to use the custom URI.": "没有匹配的项目文件夹。点击应用以使用自定义 URI。",
    "No matching resources found.": "未找到匹配的资源。",
    "No message text": "无消息文本",
    "No method available to open MCP config file": "没有可用于打开 MCP 配置文件的方法",
    "No mic audio detected": "未检测到麦克风音频",
    "No microphone found. Connect one.": "未找到麦克风。请连接一个麦克风。",
    "No microphone was found on this machine. Connect or enable an input device and try again.": "此设备上未找到麦克风。请连接或启用输入设备，然后重试。",
    "No model specified for Battle Mode, falling back to use current selected model": "未为对战模式指定模型，将回退使用当前选定的模型",
    "No models are available for your current project or account. Please check your project settings and IAM permissions.": "您当前的项目或账号没有可用的模型。请检查您的项目设置和 IAM 权限。",
    "No more older messages": "没有更多历史消息",
    "No notebook cells were found.": "未找到 Notebook 单元格。",
    "No pinned conversations": "暂无固定对话",
    "No plugins available in the marketplace.": "插件市场中暂无可用插件。",
    "No plugins available.": "暂无可用插件。",
    "No plugins match your search.": "没有与您的搜索匹配的插件。",
    "No previous worktrees": "无先前的工作树",
    "No project selected": "未选择项目",
    "No project selected or project management not available.": "未选择项目，或项目管理不可用。",
    "No recent downloads": "最近没有下载记录",
    "No remote configured": "未配置远程仓库",
    "No resources added yet.": "尚未添加任何资源。",
    "No resources available": "无可用资源",
    "No results": "无结果",
    "No results found": "未找到结果",
    "No runs yet": "暂无运行记录",
    "No shared path provided": "未提供共享路径",
    "No sign-in needed": "无需登录",
    "No sites have cookies in the built-in browser.": "内置浏览器中没有保存任何网站的 Cookie。",
    "No sites match “": "没有网站匹配“",
    "No skills or rules match this filter.": "没有符合此筛选条件的技能或规则。",
    "No skills or rules yet.": "暂无技能或规则。",
    "No token data available.": "暂无可用的 Token 数据。",
    "No upcoming run.": "暂无即将进行的运行。",
    "No uploads": "无上传内容",
    "No workspaces open.": "未打开任何工作区。",
    "Not Found": "未找到",
    "Not Signed In": "未登录",
    "Not configured": "未配置",
    "Not connected": "未连接",
    "Not now": "暂不",
    "Not on a branch": "当前不在任何分支上",
    "Not scheduled": "未计划",
    "Not secure": "不安全",
    "Not signed in": "未登录",
    "Not started": "未开始",
    "Notebook": "笔记本",
    "Notebook cell output": "Notebook 单元格输出",
    "Nothing said yet": "尚未发言",
    "Notification": "通知",
    "Notification Preferences": "通知偏好设置",
    "Number of hours": "小时数",
    "One last thing before getting started…": "开始使用前的最后一步…",
    "Only Archived": "仅已归档",
    "Only Automations": "仅自动化",
    "Only Scheduled": "仅计划任务",
    "Only Unread": "仅未读",
    "Open Browser Setup": "打开浏览器设置",
    "Open Folder": "打开文件夹",
    "Open Folder (Interactive)": "打开文件夹（交互式）",
    "Open Mermaid diagram preview": "打开 Mermaid 图表预览",
    "Open Project Picker": "打开项目选择器",
    "Open Remote Control": "打开远程控制",
    "Open SSH Host": "打开 SSH 主机",
    "Open System Browser": "打开系统浏览器",
    "Open Tabs": "已打开的标签页",
    "Open Terminal": "打开终端",
    "Open URL": "打开 URL",
    "Open a merge request": "发起合并请求",
    "Open a pull request": "发起拉取请求",
    "Open browser screenshot": "打开浏览器截图",
    "Open extracted DOM in editor": "在编辑器中打开提取的 DOM",
    "Open image preview": "打开图片预览",
    "Open in Antigravity IDE": "在 Antigravity IDE 中打开",
    "Open in Hub": "在 Hub 中打开",
    "Open in New Window": "在新窗口中打开",
    "Open in Notebook View": "在 Notebook 视图中打开",
    "Open in Tab": "在新标签页中打开",
    "Open in external browser": "在外部浏览器中打开",
    "Open in new tab": "在新标签页中打开",
    "Open in settings": "在设置中打开",
    "Open in side pane": "在侧边面板中打开",
    "Open link": "打开链接",
    "Open on another device": "在其他设备上打开",
    "Open on phone": "在手机上打开",
    "Open project settings": "打开项目设置",
    "Open search in external browser": "在外部浏览器中打开搜索",
    "Open settings menu": "打开设置菜单",
    "Open side-by-side view": "打开并排视图",
    "Open the change": "打开变更",
    "Open video preview": "打开视频预览",
    "Opened URL in Browser": "已在浏览器中打开 URL",
    "Opened browser": "已打开浏览器",
    "Opening URL in Browser": "正在浏览器中打开 URL",
    "Opening page": "正在打开页面",
    "Optimized for you": "为您优化",
    "Options": "选项",
    "Organization Allowed Domains (Read-Only)": "组织允许的域名（只读）",
    "Organization MCP Allowlist (Read-Only)": "组织 MCP 允许列表（只读）",
    "Organizations": "组织",
    "Other": "其他",
    "Other (write your answer)": "其他（填写您的回答）",
    "Other Customizations": "其他自定义项",
    "Other License": "其他许可",
    "Other credentials stay on this machine.": "其他凭据保留在本机。",
    "Other sign-in options": "其他登录方式",
    "Output:": "输出：",
    "PDF attachment": "PDF 附件",
    "PDF file size exceeds 10MB limit": "PDF 文件大小超过 10MB 限制",
    "PR details unavailable": "无法获取 PR 详情",
    "Page contents": "页面内容",
    "Page title:": "页面标题：",
    "Page was short enough to be read as a single document.": "页面较短，已作为单个文档完整阅读。",
    "Pan": "平移",
    "Parent workspace not found for this battle.": "未找到此次对比的父工作区。",
    "Paste a code instead": "改为粘贴授权码",
    "Paste auth code": "粘贴授权码",
    "Paste authorization code": "粘贴授权码",
    "Paste code": "粘贴授权码",
    "Paste key": "粘贴密钥",
    "Paste new key": "粘贴新密钥",
    "Paste the code shown after you sign in.": "粘贴登录后显示的授权码。",
    "Path copied!": "已复制路径！",
    "Paused": "已暂停",
    "Paused. Resume it to schedule the next run.": "已暂停。请恢复以安排下次运行。",
    "Pay As You Go": "按量付费",
    "Pay only for the tokens you use, billed through Gemini platform.": "仅为您使用的 Token 付费，通过 Gemini 平台计费。",
    "Permanently delete": "永久删除",
    "Pick a model to change it.": "选择一个模型以进行更改。",
    "Pick up this remote conversation on your phone or in any browser. Scan the QR code or open the link below.": "在手机或任意浏览器中继续此远程对话。请扫描下方二维码或打开链接。",
    "Pin / Unpin Conversation": "置顶 / 取消置顶对话",
    "Pin Tab": "固定标签页",
    "Pin This Conversation": "置顶此对话",
    "Pinned Actions": "固定项操作",
    "Plan upgrade required": "需要升级套餐",
    "Playback available": "支持回放",
    "Please describe the feature you'd like to see. The more detailed the requirements, the easier it will be for our team to incorporate your ideas. Some helpful information includes:": "请描述您希望看到的功能。需求越详细，我们的团队就越容易采纳您的想法。有帮助的信息包括：",
    "Please describe your auth or billing issue. More details will help our support team resolve your issue quicker. Some helpful information includes:": "请描述您的身份验证或计费问题。提供更多详细信息有助于我们的支持团队更快解决您的问题。有帮助的信息包括：",
    "Please fill out all required argument values before continuing.": "请填写所有必填参数值后再继续。",
    "Please fill out all required values to continue.": "请填写所有必填值以继续。",
    "Please provide a more detailed description (at least 10 characters).": "请提供更详细的描述（至少 10 个字符）。",
    "Please provide more detailed steps to reproduce (at least 5 characters).": "请提供更详细的复现步骤（至少 5 个字符）。",
    "Please sign in using the Antigravity sidebar panel to view this page.": "请使用 Antigravity 侧边栏面板登录以查看此页面。",
    "Please verify your account to continue using": "请验证您的账号以继续使用",
    "Please verify your account, then sign in again to continue. Learn more by visiting our": "请验证您的账号，然后重新登录以继续。如需了解更多信息，请访问我们的",
    "Plugin": "插件",
    "Plugin Operation Error:": "插件操作错误：",
    "Plugin operations are not supported in this environment.": "此环境不支持插件操作。",
    "Plugin:": "插件：",
    "Powered by Gemini Live ·": "由 Gemini Live 提供支持 ·",
    "Press": "按下",
    "Press keys...": "请按键...",
    "Pressed": "已按下",
    "Pressing": "正在按下",
    "Pressing key": "正在按键",
    "Preview": "预览",
    "Preview is not available for this file type.": "此文件类型不支持预览。",
    "Preview unavailable": "预览不可用",
    "Previous": "上一个",
    "Previous Worktrees": "先前的工作树",
    "Previous card": "上一张卡片",
    "Previous question": "上一题",
    "Previous voice": "上一个语音",
    "Pricing is based on public API pricing": "价格基于公开 API 定价",
    "Privacy Notice": "隐私声明",
    "Privacy Settings": "隐私设置",
    "Proceed": "继续",
    "Proceed with implementation plan": "继续执行实施计划",
    "Processing": "正在处理",
    "Prohibited Use Policy": "《禁止使用政策》",
    "Project + Worktree": "项目 + 工作树",
    "Project Agent": "项目智能体",
    "Project Folders": "项目文件夹",
    "Project General": "项目常规",
    "Project ID:": "项目 ID：",
    "Project Required": "需要项目",
    "Project Settings": "项目设置",
    "Project already exists": "项目已存在",
    "Project archived": "项目已归档",
    "Project deleted": "项目已删除",
    "Project location": "项目位置",
    "Project options": "项目选项",
    "Promote to Conversation": "转为正式对话",
    "Protocol": "协议",
    "Prototype": "原型",
    "Provide Google Cloud Project": "提供 Google Cloud 项目",
    "Pull Requests": "拉取请求",
    "Pull request actions": "拉取请求操作",
    "Pull request creation": "创建拉取请求",
    "Pull request numbers": "拉取请求编号",
    "Pull requests": "拉取请求",
    "Purchase Credits": "购买积分",
    "Push succeeded": "推送成功",
    "Pushing...": "正在推送...",
    "QR code": "二维码",
    "Queue Message": "排队发送消息",
    "Queued message deleted": "已删除排队消息",
    "Queued message loaded into editor": "已将排队消息加载到编辑器",
    "Queued message sent": "已发送排队消息",
    "Queued messages": "排队中的消息",
    "Quota": "配额",
    "Quote Selection": "引用所选内容",
    "Rate limited": "请求频率受限",
    "Raw": "源码",
    "Read": "已读取",
    "Read Browser Page in Browser": "已在浏览器中阅读页面",
    "Read URL": "已读取 URL",
    "Read access": "读取权限",
    "Read access to code, refs, commits, and other repository contents.": "对代码、引用、提交及其他仓库内容的读取权限。",
    "Read files": "读取文件",
    "Read page": "已阅读页面",
    "Read resource:": "读取资源：",
    "Read terminal:": "已读取终端：",
    "Reading": "正在读取",
    "Reading terminal:": "正在读取终端：",
    "Reads": "读取",
    "Recent": "最近",
    "Recent Conversations": "最近的对话",
    "Recent Files": "最近的文件",
    "Recent files": "最近的文件",
    "Reconnect": "重新连接",
    "Reconnecting…": "正在重新连接…",
    "Recording": "正在录制",
    "Redirected from": "重定向自",
    "References": "引用",
    "Refresh MCP servers": "刷新 MCP 服务器",
    "Refreshed Browser page": "已刷新浏览器页面",
    "Refreshed credentials for all automations.": "已刷新所有自动化的凭据。",
    "Refreshing Browser page": "正在刷新浏览器页面",
    "Refreshing credentials...": "正在刷新凭据...",
    "Reject": "拒绝",
    "Reject Step": "拒绝步骤",
    "Reject all": "全部拒绝",
    "Rejected sending input to command": "已拒绝向命令发送输入",
    "Rejected sending termination request to command": "已拒绝向命令发送终止请求",
    "Reload": "重新加载",
    "Reload app": "重新加载应用",
    "Reload this window.": "重新加载此窗口。",
    "Reloading page": "正在重新加载页面",
    "Remote Control isn't active on this instance. Enable it in": "此实例尚未启用远程控制。请前往",
    "Remote Control link": "远程控制链接",
    "Remote agents are busy": "远程智能体正忙",
    "Remote branch": "远程分支",
    "Remote branches": "远程分支",
    "Remove From Split": "从分屏中移除",
    "Remove bundle": "移除插件包",
    "Remove from Group": "从分组中移除",
    "Remove from Recent": "从最近列表中移除",
    "Remove from Split": "从分屏中移除",
    "Remove from history": "从历史记录中移除",
    "Remove from history (Shift+Delete)": "从历史记录中移除 (Shift+Delete)",
    "Remove from list": "从列表中移除",
    "Remove individual uploaded files or connected resources in Project Settings, or delete a project or conversation to remove its stored files.": "您可以在项目设置中移除单个上传的文件或已连接的资源，或删除项目或对话以移除其存储的文件。",
    "Remove policy": "移除策略",
    "Remove resource": "移除资源",
    "Removed bookmark": "已移除书签",
    "Removed from the marketplace. Stays installed until you uninstall it.": "已从插件市场下架。在您卸载前仍会保持安装状态。",
    "Removing bookmark": "正在移除书签",
    "Removing the message from the queue…": "正在从队列中移除消息…",
    "Removing...": "正在移除...",
    "Rename Group": "重命名分组",
    "Rename This Conversation": "重命名此对话",
    "Renamed": "已重命名",
    "Repeat every": "重复间隔",
    "Repeat unit": "重复单位",
    "Repo": "仓库",
    "Repositories": "仓库",
    "Repository access required": "需要仓库访问权限",
    "Request failed": "请求失败",
    "Requesting a one-time administrator (UAC) elevation": "正在请求一次性管理员 (UAC) 权限提升",
    "Requesting your permission in Terminal:": "正在终端中请求您的权限：",
    "Requesting your permission to open URL:": "正在请求您的权限以打开 URL：",
    "Requesting your permission:": "正在请求您的权限：",
    "Requires manual confirmation.": "需要手动确认。",
    "Research anything": "调研任何主题",
    "Reset All to Defaults": "全部重置为默认",
    "Reset all shortcuts to defaults": "将所有快捷键重置为默认",
    "Reset to preset": "重置为预设",
    "Resized Browser window": "已调整浏览器窗口大小",
    "Resizing Browser window": "正在调整浏览器窗口大小",
    "Resolve conflicts first": "请先解决冲突",
    "Resolving link…": "正在解析链接…",
    "Resolving permissions...": "正在解析权限...",
    "Resolving...": "正在解析...",
    "Resources": "资源",
    "Response (incl. tool calls)": "回复（含工具调用）",
    "Restart": "重启",
    "Restart to Update": "重启以更新",
    "Restore": "恢复",
    "Results": "结果",
    "Resume 1 comment draft": "恢复 1 条评论草稿",
    "Resume comment draft": "恢复评论草稿",
    "Resume environment": "恢复环境",
    "Resume it to load this file.": "恢复环境以加载此文件。",
    "Resume it to open a new terminal. Anything that was running in this one has stopped.": "恢复以打开新终端。此前在此终端中运行的所有进程均已停止。",
    "Resume this agent where it paused": "从暂停处继续此智能体",
    "Resuming environment…": "正在恢复环境…",
    "Retrieved Browser Pages": "已获取浏览器页面",
    "Retrieved Console Logs from Browser": "已从浏览器获取控制台日志",
    "Retrieving Browser Pages": "正在获取浏览器页面",
    "Retrieving Console Logs from Browser": "正在从浏览器获取控制台日志",
    "Reveal in Finder": "在访达中显示",
    "Review Changes": "审阅更改",
    "Review bundle before adding": "添加前审阅插件包",
    "Review contents": "审阅内容",
    "Review permissions": "审阅权限",
    "Review plans and walkthroughs": "审阅计划与演练",
    "Rewinds the conversation only. Files in this folder stay as they are now.": "仅回退对话。此文件夹中的文件将保持当前状态不变。",
    "Rewinds the conversation only. Files in this workspace stay as they are now.": "仅回退对话。此工作区中的文件将保持现状。",
    "Robot": "机器人",
    "Rule": "规则",
    "Rules and customization token budgets exceeded. Large rules are demoted to path pointers and large customizations are excluded from context.": "已超出规则和自定义项 Token 预算。较大的规则已降级为路径指针，较大的自定义项已从上下文中排除。",
    "Rules token budget exceeded. Large rules are demoted to path pointers.": "已超出规则 Token 预算。较大的规则已降级为路径指针。",
    "Run (unsandboxed)": "运行（无沙盒）",
    "Run Now": "立即运行",
    "Run in a new git worktree": "在新 Git 工作树中运行",
    "Run in a new worktree": "在新工作树中运行",
    "Run in your current workspace": "在当前工作区中运行",
    "Run visibility": "运行可见性",
    "Running processes are killed. This cannot be undone.": "正在运行的进程将被终止。此操作无法撤销。",
    "Runs": "运行记录",
    "Runs on this computer": "在此计算机上运行",
    "Runs remotely": "远程运行",
    "SSH Config": "SSH 配置",
    "SSH config:": "SSH 配置：",
    "SSH host": "SSH 主机",
    "Sample GDoc": "示例 Google 文档",
    "Saturday": "星期六",
    "Save Comment": "保存评论",
    "Save Configuration": "保存配置",
    "Save Image": "保存图片",
    "Save Video": "保存视频",
    "Save to": "保存到",
    "Saved": "已保存",
    "Saved setup routine": "已保存设置例程",
    "Saved!": "已保存！",
    "Saving setup routine": "正在保存设置例程",
    "Saving...": "正在保存...",
    "Saving…": "正在保存…",
    "Schedule": "计划",
    "Schedules and events.": "计划和事件。",
    "Schedules only.": "仅限计划。",
    "Scopes:": "权限范围：",
    "Screen Recording": "屏幕录制",
    "Screenshot must be under 10 MB": "截图大小不能超过 10 MB",
    "Scroll turns down": "向下滚动轮次",
    "Scroll turns up": "向上滚动轮次",
    "Scrollable table": "可滚动表格",
    "Scrolled": "已滚动",
    "Scrolled down in Browser": "已在浏览器中向下滚动",
    "Scrolled in Browser": "已在浏览器中滚动",
    "Scrolled up in Browser": "已在浏览器中向上滚动",
    "Scrolling down": "正在向下滚动",
    "Scrolling down in Browser": "正在浏览器中向下滚动",
    "Scrolling in Browser": "正在浏览器中滚动",
    "Scrolling left": "正在向左滚动",
    "Scrolling right": "正在向右滚动",
    "Scrolling up": "正在向上滚动",
    "Scrolling up in Browser": "正在浏览器中向上滚动",
    "Search Conversations": "搜索对话",
    "Search Google Drive": "搜索 Google Drive",
    "Search Projects": "搜索项目",
    "Search Recent Workspaces": "搜索最近的工作区",
    "Search automations...": "搜索自动化...",
    "Search branches": "搜索分支",
    "Search conversations": "搜索对话",
    "Search conversations, commands, and code...": "搜索对话、命令和代码...",
    "Search conversations...": "搜索对话...",
    "Search file contents...": "搜索文件内容...",
    "Search files...": "搜索文件...",
    "Search for MCP servers to add to your configuration": "搜索要添加到配置中的 MCP 服务器",
    "Search for commands...": "搜索命令...",
    "Search for content to open": "搜索要打开的内容",
    "Search for conversations...": "搜索对话...",
    "Search for files in the project...": "搜索项目中的文件...",
    "Search or enter a URL": "搜索或输入 URL",
    "Search past workspaces...": "搜索过往工作区...",
    "Search past worktrees...": "搜索过往工作树...",
    "Search results": "搜索结果",
    "Search sites": "搜索网站",
    "Search sites...": "搜索网站...",
    "Search tabs, files and more": "搜索标签页、文件及更多内容",
    "Search tasks...": "搜索任务...",
    "Search...": "搜索...",
    "Searched files": "已搜索文件",
    "Searched for files": "已搜索文件",
    "Searched web": "已搜索网络",
    "Searching...": "正在搜索...",
    "Secondary action": "次要操作",
    "Section header:": "章节标题：",
    "Security": "安全性",
    "See Plans": "查看套餐",
    "See all (": "查看全部 (",
    "See less in Plugins": "在插件中收起",
    "See more": "查看更多",
    "See more in Plugins": "在插件中查看更多",
    "See more results": "查看更多结果",
    "See plans": "查看套餐",
    "Select All": "全选",
    "Select Billing Model": "选择计费模式",
    "Select Environment": "选择环境",
    "Select Folder(s)": "选择文件夹",
    "Select Google Drive files or folders": "选择 Google Drive 文件或文件夹",
    "Select License": "选择许可",
    "Select Model to Send Message": "选择模型以发送消息",
    "Select Project": "选择项目",
    "Select Resource(s)": "选择资源",
    "Select Theme": "选择主题",
    "Select Worktree": "选择工作树",
    "Select a model in the model selector": "在模型选择器中选择一个模型",
    "Select a model using the model selector in the input box": "请使用输入框中的模型选择器选择一个模型",
    "Select all in": "全选：",
    "Select an option": "选择一个选项",
    "Select an option...": "请选择一个选项...",
    "Select another model": "选择其他模型",
    "Select branch": "选择分支",
    "Select category to search...": "选择要搜索的类别...",
    "Select text in the artifact to add a comment": "在产物中选中文本以添加评论",
    "Select the latest snapshot from the": "从以下位置选择最新快照：",
    "Select your license": "选择您的许可",
    "Select...": "请选择...",
    "Selected Option in Browser": "已在浏览器中选择选项",
    "Selected element preview": "已选元素预览",
    "Selected region": "已选区域",
    "Selecting Option in Browser": "正在浏览器中选择选项",
    "Selecting option": "正在选择选项",
    "Send": "发送",
    "Send Message": "发送消息",
    "Send Now": "立即发送",
    "Send a message in the main conversation first to start a side question": "请先在主对话中发送一条消息，然后再发起旁支提问",
    "Send command input?": "是否发送命令输入？",
    "Send feedback as": "发送反馈身份：",
    "Sending input to command": "正在向命令发送输入",
    "Sending termination request to command": "正在向命令发送终止请求",
    "Sending transcribed message...": "正在发送转录消息...",
    "Sends after agent finishes working": "将在智能体完成工作后发送",
    "Sent input to command": "已向命令发送输入",
    "Sent termination request to command": "已向命令发送终止请求",
    "Services this plugin connects to on your behalf.": "此插件代表您连接的服务。",
    "Session Summary": "会话摘要",
    "Set Project Name": "设置项目名称",
    "Set the rules, define the boundaries.": "制定规则，明确边界。",
    "Set up": "配置",
    "Settings -": "设置 -",
    "Settings Unavailable": "设置不可用",
    "Settings for conversations outside of projects.": "项目之外的对话设置。",
    "Settings for conversations outside of workspaces.": "工作区之外的对话设置。",
    "Setup": "设置",
    "Setup Script": "配置脚本",
    "Setup required": "需要配置",
    "Share": "分享",
    "Share your referral link with friends": "与好友分享您的推荐链接",
    "Shares this repository, with a working copy of its own. Uncommitted changes stay behind.": "共享此代码仓库，并拥有独立的工作副本。未提交的更改不会带入。",
    "Show 1 earlier step": "显示 1 个较早的步骤",
    "Show All": "显示全部",
    "Show Details": "显示详情",
    "Show Error": "显示错误",
    "Show Less": "收起",
    "Show all": "显示全部",
    "Show all resources": "显示全部资源",
    "Show fewer resources": "收起部分资源",
    "Show full command": "显示完整命令",
    "Show in File Explorer": "在文件资源管理器中显示",
    "Show in File Manager": "在文件管理器中显示",
    "Show in Sidebar": "在侧边栏中显示",
    "Show in folder": "在文件夹中显示",
    "Show in the list again": "重新在列表中显示",
    "Show more (": "显示更多（",
    "Show or Hide Extensions": "显示或隐藏扩展",
    "Show submitted (": "显示已提交（",
    "Show token": "显示令牌",
    "Side Question": "旁支提问",
    "Side Question Selection": "对所选内容发起旁支提问",
    "Side Question:": "旁支提问：",
    "Side Questions": "旁支提问",
    "Sidecar View": "Sidecar 视图",
    "Sidecar error": "Sidecar 错误",
    "Sign In": "登录",
    "Sign In with SSO": "使用 SSO 登录",
    "Sign in": "登录",
    "Sign in again": "重新登录",
    "Sign in in your browser, then paste the authorization code shown on the callback page.": "请在浏览器中登录，然后粘贴回调页面上显示的授权码。",
    "Sign in required": "需要登录",
    "Sign in with a different account": "使用其他账号登录",
    "Sign out": "退出登录",
    "Sign out of this server?": "确定要退出登录此服务器吗？",
    "Sign up for newsletters, tips and tricks, and other notifications about": "订阅新闻简报、使用技巧以及有关以下内容的其他通知：",
    "Signed in": "已登录",
    "Signing Out...": "正在退出登录...",
    "Simulated Key Press in Browser": "已在浏览器中模拟按键",
    "Simulating Key Press in Browser": "正在浏览器中模拟按键",
    "Site data cleared for": "已清除以下网站的网站数据：",
    "Sites with cookies": "保存了 Cookie 的网站",
    "Skill": "技能",
    "Skill deletion is not available.": "技能删除功能不可用。",
    "Skipping...": "正在跳过...",
    "Sliders": "滑块",
    "Some non-image binary content was truncated.": "部分非图片二进制内容已被截断。",
    "Some sites block embedding (via X-Frame-Options or CSP) and will show a fallback message. Blocked-page detection is best-effort (based on a load timeout), so it may occasionally be wrong. Use \"Open in new tab\" if a page doesn't load.": "部分网站会阻止嵌入（通过 X-Frame-Options 或 CSP）并显示回退提示。阻止页面检测基于加载超时尽最大努力判断，因此偶尔可能会误判。如果页面无法加载，请使用“在新标签页中打开”。",
    "Something went wrong": "出错了",
    "Something went wrong!": "出错了！",
    "Sorry, this account is ineligible to use": "抱歉，此账号无法使用",
    "Sort By": "排序方式",
    "Sort Projects": "排序项目",
    "Sort Workspaces": "排序工作区",
    "Sort and filter conversations": "排序和筛选对话",
    "Source": "来源",
    "Source:": "来源：",
    "Sources": "来源",
    "Sparkles": "星光",
    "Speech recognition service is failing, and the current model doesn't support direct audio file input.": "语音识别服务出现故障，且当前模型不支持直接输入音频文件。",
    "Speedometer": "速度表",
    "Split Conversation Horizontally": "水平拆分对话",
    "Split Conversation Vertically": "垂直拆分对话",
    "Stage": "暂存",
    "Stage and amend all changes into the current commit": "暂存并将所有更改修补到当前提交",
    "Stage and commit all changes": "暂存并提交所有更改",
    "Staged": "已暂存",
    "Staged index changes and working tree changes": "已暂存的索引更改和工作树更改",
    "Standalone": "独立",
    "Standalone terminals": "独立终端",
    "Start it again.": "重新启动。",
    "Started": "已启动",
    "Started during": "发起于",
    "Started from": "发起自",
    "Starting": "正在启动",
    "Starting preview…": "正在启动预览…",
    "Starting terminal…": "正在启动终端…",
    "Starting the conversation…": "正在启动对话…",
    "Stay up to date.": "随时了解最新动态。",
    "Still connecting…": "仍在连接…",
    "Still running": "仍在运行",
    "Stop All Subagents": "停止所有子智能体",
    "Stop Editing": "停止编辑",
    "Stop Recording": "停止录制",
    "Stop Recording and Send": "停止录制并发送",
    "Stop SSH Server…": "停止 SSH 服务器…",
    "Stop Subagent": "停止子智能体",
    "Stop Task": "停止任务",
    "Stop all agents": "停止所有智能体",
    "Stop side question": "停止旁支提问",
    "Stop subagent": "停止子智能体",
    "Stop this agent": "停止此智能体",
    "Stop transcription": "停止转录",
    "Stopping…": "正在停止…",
    "Stored and mounted in your cloud environment": "存储并挂载在您的云环境中",
    "Stream ended": "流已结束",
    "Subagent Conversation": "子智能体对话",
    "Subagent ended": "子智能体已结束",
    "Submit Appeal": "提交申诉",
    "Submit Prompt (Alternate to Enter)": "提交提示词（替代 Enter）",
    "Submit code": "提交授权码",
    "Submit comment": "提交评论",
    "Submitting...": "正在提交...",
    "Subscription": "订阅",
    "Successfully imported project:": "已成功导入项目：",
    "Suggested sending input to command": "建议向命令发送输入",
    "Suggested sending termination request to command": "建议向命令发送终止请求",
    "Summarizing call…": "正在总结通话…",
    "Sunday": "星期日",
    "Switch Roles": "切换角色",
    "Switch To": "切换到",
    "Switch branch": "切换分支",
    "Switch mic": "切换麦克风",
    "Switch to This Computer": "切换到此计算机",
    "Switched to authorization code sign-in": "已切换为授权码登录",
    "Switching tabs": "正在切换标签页",
    "System Message": "系统消息",
    "System Settings": "系统设置",
    "System UI": "系统默认字体",
    "System default app": "系统默认应用",
    "Table exceeds 100 columns.": "表格超过 100 列。",
    "Table of contents": "目录",
    "Table options": "表格选项",
    "Taking Screenshot": "正在截屏",
    "Taking longer than usual to load": "加载时间比平时更长",
    "Task not found": "未找到任务",
    "Terminal input": "终端输入",
    "Terminal sandbox is not supported in this environment": "此环境不支持终端沙盒",
    "Terminal window": "终端窗口",
    "Terminal: Add to Chat": "终端：添加到对话",
    "Terminal: Select All": "终端：全选",
    "Terms and Privacy:": "条款与隐私：",
    "Terms of Service & Data Use": "服务条款与数据使用",
    "Text attachment": "文本附件",
    "Text file size exceeds 1MB limit": "文本文件大小超过 1MB 限制",
    "Thank you! Your feedback has been submitted successfully.": "感谢您！您的反馈已成功提交。",
    "Thanks for helping make Gemini better! This is a critical part of evaluating and improving our models.": "感谢您帮助改进 Gemini！这对评估和提升我们的模型至关重要。",
    "Thanks for your feedback!": "感谢您的反馈！",
    "The Hub sent an unexpected response.": "Hub 返回了意外响应。",
    "The agent has a question for you:": "智能体有一个问题想问您：",
    "The agent has encountered an internal error.": "智能体遇到内部错误。",
    "The agent has questions for you:": "智能体有几个问题想问您：",
    "The agent is waiting for your input.": "智能体正在等待您的输入。",
    "The agent was prevented from accessing some sites": "智能体被阻止访问部分网站",
    "The agent will wait for you to install the browser extension.": "智能体将等待您安装浏览器扩展程序。",
    "The branch was pushed to GitLab.": "分支已推送至 GitLab。",
    "The certificate has been revoked.": "此证书已被吊销。",
    "The certificate has expired or is not yet valid.": "此证书已过期或尚未生效。",
    "The certificate is not issued by a trusted authority.": "此证书并非由受信任的机构颁发。",
    "The certificate is not valid for this site.": "此证书对此网站无效。",
    "The conversation could not be loaded because its data was not found.": "无法加载该对话，因为未找到其数据。",
    "The full developer experience.": "完整的开发者体验。",
    "The main conversation's input isn't available right now.": "主对话的输入框当前不可用。",
    "The remote shared a link for this push.": "远程仓库为此推送共享了一个链接。",
    "The remote workspace is not running": "远程工作区未运行",
    "The window title matches a privacy rule.": "窗口标题匹配隐私规则。",
    "Then create the project in its window.": "然后在其窗口中创建项目。",
    "There are currently no Build with": "当前没有可用的 Build with",
    "There was an error with your authentication. To log in, click": "身份验证出错。如需登录，请点击",
    "There was an unexpected issue setting up your account.": "设置您的账号时出现意外问题。",
    "These MCP allowlist rules are enforced by your organization's administrator.": "这些 MCP 允许列表规则由您组织的管理员强制执行。",
    "These allowed domain rules are set by your organization's administrator and cannot be removed.": "这些允许的域名规则由您组织的管理员设置，无法移除。",
    "Thinking": "思考",
    "Thinking…": "思考中…",
    "This Google Cloud project is not supported. Input a different project, or sign in with another account.": "不支持此 Google Cloud 项目。请输入其他项目，或使用其他账号登录。",
    "This app is not allowed in previews.": "此应用不允许在预览中显示。",
    "This bundle has no plugins yet.": "此插件包暂无插件。",
    "This cannot be undone.": "此操作无法撤销。",
    "This chat is archived.": "此对话已归档。",
    "This chat's environment is paused": "此对话的环境已暂停",
    "This computer": "此电脑",
    "This conversation is not on disk. Delete it to remove it from your sidebar.": "此对话不在磁盘上。删除它以将其从侧边栏中移除。",
    "This extension has no declared permissions requiring user input.": "此扩展没有需要用户输入的声明权限。",
    "This field is required": "此字段为必填项",
    "This file type is not currently supported in remote mode": "远程模式暂不支持此文件类型",
    "This link wants to open an app on your device.": "此链接想要打开您设备上的应用。",
    "This may take a few minutes": "这可能需要几分钟",
    "This notebook has no renderable cells.": "此 Notebook 没有可渲染的单元格。",
    "This page is not allowed in previews.": "此页面不允许在预览中显示。",
    "This page is taking longer than expected to load, or it may be blocking embedded views (via X-Frame-Options or CSP).": "此页面加载时间超出预期，或者可能阻止了嵌入式视图（通过 X-Frame-Options 或 CSP）。",
    "This page isn’t working": "此网页无法正常工作",
    "This page says": "此页面显示",
    "This permanently deletes all of your Remote Agents conversations, projects, scheduled tasks, connected plugins and settings, and stops any running remote agents. It can't be undone. Data in the desktop app and your Google account are not affected, and you can keep using Remote Agents afterwards.": "此操作将永久删除您所有的远程智能体对话、项目、计划任务、已连接的插件和设置，并停止所有正在运行的远程智能体。此操作无法撤销。桌面应用中的数据和您的 Google 账户不受影响，之后您仍可继续使用远程智能体。",
    "This project uses Firebase. Do you want to download the Firebase skill?": "此项目使用了 Firebase。您要下载 Firebase 技能吗？",
    "This project was created for": "此项目创建用于",
    "This shortcut is reserved by browser tabs and may not trigger in Web mode. It works in the Desktop Hub or installed PWA.": "此快捷键由浏览器标签页保留，在网页模式下可能无法触发。它在桌面端或已安装的 PWA 中可用。",
    "This side question isn't available in this conversation.": "此对话中无法使用该旁支提问。",
    "This sidecar failed to start.": "此 Sidecar 启动失败。",
    "This site cannot provide a secure connection.": "此网站无法提供安全连接。",
    "This site can’t be reached": "无法访问此网站",
    "This site uses an unsupported TLS protocol or cipher suite.": "此网站使用了不受支持的 TLS 协议或加密套件。",
    "This skill came from the marketplace, so you can add it again whenever you need it.": "此技能来自插件市场，您随时可以重新添加。",
    "This subagent was killed and can no longer be messaged.": "此子智能体已终止，无法再发送消息。",
    "This will permanently delete": "此操作将永久删除",
    "Thought Process": "思考过程",
    "Thursday": "星期四",
    "Time": "时间",
    "Timed out fetching the Google Drive file's title. The link was kept as-is.": "获取 Google Drive 文件标题超时。链接已保持原样。",
    "Timed out waiting for commit message generation": "等待生成提交信息超时",
    "Timeout:": "超时时间：",
    "Tip:": "提示：",
    "Title:": "标题：",
    "To update:": "更新步骤：",
    "To use the agent, please login": "如需使用智能体，请登录",
    "Toggle Google Cloud projects": "切换 Google Cloud 项目列表",
    "Toggle Terminal Panel": "切换终端面板",
    "Toggle Virtual Machine": "切换虚拟机",
    "Toggle Word Wrap": "切换自动换行",
    "Toggle checkerboard background": "切换棋盘格背景",
    "Toggle file diff": "切换文件差异",
    "Toggle sidebar": "切换侧边栏",
    "Toggle this on to allow creating new issues.": "开启此项以允许创建新议题。",
    "Toggle this on to allow creating new pull requests.": "开启此项以允许创建新的拉取请求。",
    "Toggle this on to enable read access on contents.": "开启此项以启用内容的读取权限。",
    "Token rejected": "令牌被拒绝",
    "Too many environments running": "运行中的环境过多",
    "Too many requests, please try again in a bit!": "请求过多，请稍后再试！",
    "Too much output to announce, navigate to rows manually to read": "输出内容过多，无法自动播报，请手动导航至各行阅读",
    "Took Screenshot": "已截屏",
    "Tool Output": "工具输出",
    "Tool arguments": "工具参数",
    "Transcribing audio…": "正在转录音频…",
    "Trouble signing in? Enter authorization code": "登录遇到问题？输入授权码",
    "True changes vs the parent workspace": "与父工作区相比的实际更改",
    "Try again": "重试",
    "Try out early-stage features before they ship. These may be changed or removed at any time. These features are experimental, and we make no guarantees about performance or functionality.": "在正式发布前抢先体验早期功能。这些功能随时可能更改或移除。这些功能属于实验性质，我们不对其性能或功能做任何保证。",
    "Tuesday": "星期二",
    "Turn": "轮次",
    "Type absolute path or navigate folders...": "输入绝对路径或浏览文件夹...",
    "Type to search file contents": "输入以搜索文件内容",
    "Typed into Browser": "已在浏览器中输入",
    "Typing": "正在输入",
    "Typing into Browser": "正在浏览器中输入",
    "Unarchive": "取消归档",
    "Unarchive the main conversation to insert": "取消归档主对话后即可插入",
    "Unbalanced parentheses or brackets": "括号不匹配",
    "Unclosed string literal": "字符串字面量未闭合",
    "Uncommitted": "未提交",
    "Unfold code block": "展开代码块",
    "United States": "美国",
    "Unmute Antigravity": "取消静音 Antigravity",
    "Unnamed": "未命名",
    "Unnamed resource": "未命名资源",
    "Unnamed rule": "未命名规则",
    "Unpin": "取消置顶",
    "Unpin Tab": "取消固定标签页",
    "Unpin This Conversation": "取消置顶此对话",
    "Unsandboxed commands": "非沙盒命令",
    "Untitled Conversation": "未命名对话",
    "Untitled project": "未命名项目",
    "Untracked": "未跟踪",
    "Untracked (Unstaged)": "未跟踪（未暂存）",
    "Update Anyway": "仍然更新",
    "Update Available": "有可用更新",
    "Updater": "更新程序",
    "Updating will restart the server and apply the latest changes.": "更新将会重启服务器并应用最新更改。",
    "Updating…": "正在更新…",
    "Upload Files": "上传文件",
    "Upload to Agent": "上传到智能体",
    "Upload to Google Drive": "上传至 Google 云端硬盘",
    "Uploaded files and connected resources are mounted in your cloud environment.": "上传的文件和已连接的资源已挂载在您的云环境中。",
    "Uploaded project files and in-chat attachments are stored on Google servers and mounted into your cloud sandbox so your agent can read and work with them.": "上传的项目文件和对话中的附件会存储在 Google 服务器上，并挂载到您的云沙盒中，以便您的智能体读取和处理。",
    "Uploaded to Google Drive": "已上传至 Google 云端硬盘",
    "Uploading to Drive…": "正在上传至云端硬盘…",
    "Uploading to Google Drive…": "正在上传至 Google 云端硬盘…",
    "Use Add MCP to browse the store.": "使用“添加 MCP”浏览商店。",
    "Use Advanced SSO Config": "使用高级 SSO 配置",
    "Use Antigravity through your Gemini subscription.": "通过您的 Gemini 订阅使用 Antigravity。",
    "Use Business Account": "使用企业账号",
    "Use Google Cloud project instead": "改用 Google Cloud 项目",
    "Use full Git clones for Best of N": "为 Best of N 使用完整 Git 克隆",
    "Use theme to be imported with settings": "使用随设置导入的主题",
    "Use this form if you cannot connect to Remote Control. If your instance is already connected and you are experiencing issues in the browser, report directly from the Remote Control web page so that relevant logs are included. Some helpful information includes:": "如果您无法连接到远程控制，请使用此表单。如果您的实例已连接但在浏览器中遇到问题，请直接从远程控制网页报告，以便包含相关日志。有帮助的信息包括：",
    "Use this if your admin gave you a WIF config. Paste it below to sign in.": "如果管理员向您提供了 WIF 配置，请使用此方式。在下方粘贴配置即可登录。",
    "Used MCP tool": "已使用 MCP 工具",
    "Used for:": "用途：",
    "Used tool": "已使用工具",
    "Useful for tasks that require file access across your full machine. The agent has full read and write access to all local files, but all proposed terminal commands require manual review and approval before running.": "适用于需要访问整台机器文件的任务。智能体对所有本地文件拥有完整的读写权限，但所有建议的终端命令在运行前都需要人工审阅和批准。",
    "User Intent": "用户意图",
    "User uploaded image": "用户上传的图片",
    "Uses standalone Antigravity chords (e.g. Ctrl+I Focus Input, Ctrl+Shift+O New Conversation, Ctrl+K Picker in chat, Ctrl+, Settings, Ctrl+[/] History). Replaces Go to Symbol (Ctrl+Shift+O) and Trigger Suggest (Ctrl+I), and rebinds VS Code Settings to Ctrl+Alt+,.": "使用独立的 Antigravity 组合快捷键（例如 Ctrl+I 聚焦输入框、Ctrl+Shift+O 新建对话、Ctrl+K 对话内选择器、Ctrl+, 设置、Ctrl+[/] 历史记录）。将替换“转到符号”(Ctrl+Shift+O) 和“触发建议”(Ctrl+I)，并将 VS Code 设置重新绑定至 Ctrl+Alt+,。",
    "Uses standalone Antigravity chords (e.g. ⌘I Focus Input, ⌘⇧O New Conversation, ⌘K Picker in chat, ⌘, Settings, ⌘[/] History). Replaces Go to Symbol (⌘⇧O) and Trigger Suggest (⌘I), and rebinds VS Code Settings to ⌘⌥,.": "使用独立的 Antigravity 组合快捷键（例如 ⌘I 聚焦输入框、⌘⇧O 新建对话、⌘K 对话内选择器、⌘, 设置、⌘[/] 历史记录）。将替换“转到符号”(⌘⇧O) 和“触发建议”(⌘I)，并将 VS Code 设置重新绑定至 ⌘⌥,。",
    "Using browser": "正在使用浏览器",
    "Using browser · Thinking…": "正在使用浏览器 · 思考中…",
    "Using system default microphone": "正在使用系统默认麦克风",
    "VS Code Default": "VS Code 默认",
    "VS Code Keyboard Shortcuts": "VS Code 键盘快捷键",
    "Valid until": "有效期至",
    "Validated with GitHub and stored in": "经 GitHub 验证并存储于",
    "Validation failed. Please verify requirements and try again.": "验证失败。请检查是否满足要求，然后重试。",
    "Validation timed out.": "验证超时。",
    "Verification required": "需要验证",
    "Verify": "验证",
    "Verify that these licenses were provided by your administrator and that you trust the project ID before proceeding. Account activity and data may be logged by your organization.": "在继续之前，请确认这些许可由您的管理员提供，并且您信任该项目 ID。您的组织可能会记录账户活动和数据。",
    "Video": "视频",
    "Video attachment": "视频附件",
    "Videos must be at least 1 second long": "视频时长必须至少为 1 秒",
    "View Branches": "查看分支",
    "View Logs": "查看日志",
    "View Page": "查看页面",
    "View archived in the sidebar (": "在侧边栏中查看已归档对话（",
    "View archived in the sidebar (![filter](icon://filter_list) menu).": "在侧边栏中查看已归档对话（![filter](icon://filter_list) 菜单）。",
    "View archived in the sidebar (Display options menu).": "在侧边栏中查看已归档对话（显示选项菜单）。",
    "View comments": "查看评论",
    "View could not be opened": "无法打开视图",
    "View network request": "查看网络请求",
    "View network requests": "查看网络请求",
    "View or edit comment": "查看或编辑评论",
    "View site information": "查看网站信息",
    "Virtual File": "虚拟文件",
    "Virtual File Viewer": "虚拟文件查看器",
    "Visited URLs and autocomplete suggestions.": "已访问的 URL 和自动补全建议。",
    "Voice Speed": "语速",
    "Voice dictation unavailable": "语音听写不可用",
    "Voice recording is unavailable while the Chief of Staff mic is on": "幕僚长麦克风开启时无法进行语音录制",
    "Voice speed": "语速",
    "Voice transcript": "语音转录",
    "WIF Config": "WIF 配置",
    "Wait for": "等待",
    "Waiting": "正在等待",
    "Waiting for subagent": "正在等待子智能体",
    "Waiting for the agents’ windows…": "正在等待智能体窗口…",
    "Waiting for video…": "正在等待视频…",
    "Waiting for you to finish signing in…": "正在等待您完成登录…",
    "Waiting for your approval": "正在等待您的批准",
    "Warm and approachable": "温暖亲切",
    "Warm and engaging": "温暖迷人",
    "We apologize for the inconvenience. Please try again later.": "对于造成的不便，我们深表歉意。请稍后重试。",
    "We recommend attaching logs. Attaching logs will help the Antigravity team act on and prioritize your feedback.": "建议您附加日志。附加日志有助于 Antigravity 团队处理您的反馈并确定优先级。",
    "We'll keep waiting, or you can open it directly in a new tab.": "我们将继续等待，或者您也可以直接在新标签页中打开它。",
    "Web search prioritized results from": "网络搜索已优先显示以下来源的结果：",
    "Wednesday": "星期三",
    "Weekly": "每周",
    "Welcome back. Where should we pick up?": "欢迎回来。我们从哪里继续？",
    "Welcome to": "欢迎使用",
    "What counts as a document": "哪些内容算作文档",
    "What functionality you expect your account tier to have available that is missing": "您的账户等级预期应具备但目前缺失的功能",
    "What is missing in your workflow": "您的工作流中缺少什么",
    "What quota or feature is being incorrectly limited": "哪些配额或功能受到了错误限制",
    "What should this coordinator accomplish?": "此协调器需要完成什么目标？",
    "What you would like to see to address this gap in your workflow": "您希望看到什么功能来弥补工作流中的这一缺口",
    "What's in this bundle": "此插件包包含的内容",
    "When Turbo mode is on, the agent will automatically capture screenshots in the Browser without explicit user input. You can toggle this setting in Antigravity's settings.": "开启 Turbo 模式后，智能体将在浏览器中自动捕获屏幕截图，无需您手动确认。您可以在 Antigravity 的设置中切换此选项。",
    "Whether it never connects or is intermittent/flaky": "是完全无法连接，还是间歇性不稳定",
    "Work in a New Worktree": "在新工作树中工作",
    "Worked": "已工作",
    "Workflow files": "工作流文件",
    "Workflow refs": "工作流引用",
    "Workflow runs": "工作流运行",
    "Workspace + Worktree": "工作区 + 工作树",
    "Workspace File Explorer": "工作区文件资源管理器",
    "Workspace URI not found": "未找到工作区 URI",
    "Workspace URI to switch to": "要切换到的工作区 URI",
    "Workspace archived": "工作区已归档",
    "Workspace deleted": "工作区已删除",
    "Workspace folder suggestions": "工作区文件夹建议",
    "Workspace setup warning": "工作区设置警告",
    "Workspaces are not available for this project": "此项目不支持工作区",
    "Worktree Branches": "工作树分支",
    "Worktree branch": "工作树分支",
    "Worktrees are a git feature. This folder is shared as is.": "工作树是 Git 的一项功能。此文件夹将按原样共享。",
    "Worktrees are available for Git repositories": "工作树仅适用于 Git 仓库",
    "Worktrees are not available for this project": "此项目不支持工作树",
    "Wrench": "扳手",
    "Write": "写入",
    "Write a message": "输入消息",
    "Write and edit docs": "撰写与编辑文档",
    "Write files": "写入文件",
    "Yes, allow this download": "是的，允许此次下载",
    "You are in control": "一切尽在您的掌控",
    "You are logged in using environment credentials and cannot sign out from the application.": "您当前使用的是环境凭据登录，无法从应用中退出登录。",
    "You can change this in": "您可以在以下位置更改：",
    "You can follow the workers in the Dashboard, and I'll post an update when something finishes or needs you.": "您可以在仪表盘中跟踪工作智能体的进度，当有任务完成或需要您介入时，我会向您同步更新。",
    "You cannot sign out from Remote Control. Please sign out on your local application.": "您无法从远程控制退出登录。请在本地应用中退出登录。",
    "You don't have access to this Google Drive file, so its title couldn't be added. The link was kept as-is.": "您没有此 Google Drive 文件的访问权限，因此无法添加其标题。链接已保持原样。",
    "You have a conversation in progress. Updating will cancel it and you'll need to manually restart it.": "您有 1 个对话正在进行中。更新将会取消该对话，您需要手动重新启动它。",
    "You have a conversation in progress. Updating will interrupt it, and it will automatically resume once the update completes.": "您有 1 个对话正在进行中。更新将会中断该对话，并在更新完成后自动恢复。",
    "You should not enter any sensitive information on this site (for example, passwords or credit cards), because it could be stolen by attackers.": "您不应在此网站上输入任何敏感信息（例如密码或信用卡号），因为攻击者可能会窃取这些信息。",
    "You're viewing a blank page": "您正在查看空白页",
    "You're viewing a local or shared file": "您正在查看本地或共享文件",
    "You've reached the maximum number of turns for this battle. End battle mode to continue.": "您已达到本次对战的最大轮次。请结束对战模式以继续。",
    "Your AI credits balance is too low to continue.": "您的 AI 积分余额不足，无法继续。",
    "Your Antigravity use will be associated with provided project.": "您对 Antigravity 的使用将与所提供的项目关联。",
    "Your Antigravity use will be associated with provided project. Make sure you trust the project ID before proceeding. Account activity and data may be logged by your organization.": "您对 Antigravity 的使用将与所提供的项目关联。在继续之前，请确保您信任该项目 ID。您的组织可能会记录账户活动和数据。",
    "Your Plan": "您的套餐",
    "Your administrator has disabled MCP servers for this workspace.": "您的管理员已为此工作区禁用 MCP 服务器。",
    "Your agent’s ability to execute commands is also controlled by enterprise security policies.": "您的智能体执行命令的能力还受企业安全策略控制。",
    "Your connection to this site is not fully secure": "您与此网站的连接并非完全安全",
    "Your connection to this site is not secure": "您与此网站的连接不安全",
    "Your information (for example, passwords or credit card numbers) is private when it is sent to this site.": "您的信息（例如密码或信用卡号）在发送到此网站时是私密的。",
    "Your quota for this model is running low.": "您对此模型的配额即将耗尽。",
    "Your session has expired. Please log back in to continue.": "您的会话已过期，请重新登录以继续。",
    "Your sign-in needs an update.": "您的登录状态需要更新。请",
    "Your sign-in needs an update. Sign in again to use Voice.": "您的登录状态需要更新。请重新登录以使用语音模式。",
    "Zip attachment": "Zip 附件",
    "Zip file size exceeds 20MB limit": "压缩文件大小超过 20MB 限制",
    "Zipping": "正在压缩",
    "Zoom in": "放大",
    "Zoom out": "缩小",
    "a one-time administrator (UAC) elevation": "一次性管理员 (UAC) 权限提升",
    "above hidden": "以上已隐藏",
    "above hidden)": "以上已隐藏）",
    "access to this resource": "此资源的访问权限",
    "all agent edits": "所有智能体编辑",
    "already exists for this": "已存在于此",
    "at ref": "在引用",
    "automation and can only be deleted by deleting that automation.": "（只能通过删除该自动化来删除）。",
    "branch changes": "分支更改",
    "browser downloads from this site": "从此站点进行浏览器下载",
    "chunks were collapsed into one. Chunks included in this read:": "个分块被合并为一个。本次读取包含的分块：",
    "combination of folders": "文件夹组合",
    "copy link": "复制链接",
    "cumulative total for the conversation up to this point": "截至目前本对话的累计总计",
    "custom agents": "自定义智能体",
    "does not collect any of your prompts, content, or model responses but does collect general usage patterns such as feature adoption and active user counts (“product analytics”). Telemetry data will be handled in accordance with the Google Privacy Policy.": "不会收集您的任何提示词、内容或模型回复，但会收集一般使用模式，例如功能采用情况和活跃用户数（“产品分析”）。遥测数据将按照 Google 隐私权政策进行处理。",
    "does not collect any of your prompts, content, or model responses but will still collect general usage patterns (e.g., feature adoption, active user counts).": "不会收集您的任何提示词、内容或模型回复，但仍会收集一般使用模式（例如功能采用情况、活跃用户数）。",
    "empty message": "空消息",
    "executing actions on this URL": "在此 URL 上执行操作",
    "half a minute": "半分钟",
    "icon in the URL bar.": "图标（位于地址栏中）。",
    "in a terminal": "在终端中",
    "in the top menu.": "（位于顶部菜单）。",
    "in these conversations": "在这些对话中",
    "in this project": "在此项目中",
    "is managed by the": "由以下自动化管理：",
    "learn more": "了解更多",
    "less than a minute": "不到 1 分钟",
    "less than a second": "不到 1 秒",
    "links without asking": "链接，不再询问",
    "main conversation": "主对话",
    "managed by your organization": "由您的组织管理",
    "may sign you out of this site.": "的 Cookie 和网站数据可能会导致您退出登录此网站。",
    "necessary rights": "必要权利",
    "needs a few details from you before it can run.": "需要您提供一些详细信息才能运行。",
    "new worktree": "新建工作树",
    "not connected": "未连接",
    "on the": "于",
    "on this computer.": "在此计算机上。",
    "permission grants changed": "权限授予已更改",
    "plugins available.": "插件。",
    "quick pick": "快捷选择器",
    "read access to this path": "此路径的读取权限",
    "reading this URL": "读取此 URL",
    "review comments": "审阅评论",
    "run in a dedicated": "创建的智能体将在专用的",
    "running this command": "运行此命令",
    "running this command outside the sandbox": "在沙盒外运行此命令",
    "scheduled task": "计划任务",
    "scheduled tasks": "计划任务",
    "settings page.": "设置页面中更改。",
    "single edit": "单次编辑",
    "skills and rules": "技能和规则",
    "subagent conversation": "子智能体对话",
    "text resource": "个文本资源",
    "text resources": "个文本资源",
    "the main conversation": "主对话",
    "the subagent conversation": "子智能体对话",
    "to add to Agent": "以添加到智能体",
    "to any content or files that you upload, including content of minors. Don't generate content that infringes on others' rights, including content that deceives, harasses, or harms. When using Antigravity, you must comply with Google's": "来上传任何内容或文件（包括未成年人的内容）。请勿生成侵犯他人权利的内容，包括欺骗、骚扰或伤害性内容。使用 Antigravity 时，您必须遵守 Google 的",
    "to switch to the Gemini app. Your agents keep working in the background.": "即可切换到 Gemini 应用。您的智能体将继续在后台工作。",
    "to upload": "以上传",
    "to use Voice.": "以使用语音模式。",
    "using this MCP tool": "使用此 MCP 工具",
    "view full search results": "查看完整搜索结果",
    "when working": "工作时",
    "with its own permissions, which you can change anytime in the": "中运行并拥有独立权限，您随时可以在",
    "with the same folder exists": "（包含相同文件夹）已存在",
    "with the same folders exists": "（包含相同文件夹）已存在",
    "with this name already exists.": "已存在相同名称。",
    "within it.": "（包含在其中）。",
    "write access to this path": "此路径的写入权限"
  };

  const coreWords = {
    "create": "创建", "delete": "删除", "edit": "编辑", "save": "保存", "cancel": "取消", "confirm": "确认",
    "close": "关闭", "open": "打开", "stop": "停止", "start": "启动", "run": "运行", "add": "添加", "remove": "移除", "download": "下载",
    "update": "更新", "select": "选择", "clear": "清除", "search": "搜索", "find": "查找", "view": "查看", "show": "显示", "hide": "隐藏",
    "copy": "复制", "paste": "粘贴", "cut": "剪切", "rename": "重命名", "duplicate": "制作副本",
    "agent": "智能体", "agents": "智能体", "subagent": "子智能体", "subagents": "子智能体", "task": "任务", "tasks": "任务",
    "workspace": "工作区", "workspaces": "工作区", "directory": "目录", "folder": "文件夹", "file": "文件", "files": "文件",
    "command": "命令", "commands": "命令", "terminal": "终端", "console": "控制台", "output": "输出", "input": "输入",
    "error": "错误", "warning": "警告", "info": "信息", "success": "成功", "failed": "失败", "pending": "等待中", "running": "运行中",
    "yes": "是", "true": "真", "false": "假", "on": "开", "off": "关", "enable": "启用", "disable": "禁用",
    "global": "全局", "retry": "重试", "regenerate": "重新生成", "dismiss": "忽略",
    "allow": "允许", "ask": "询问", "deny": "拒绝", "split": "分屏", "notice": "提示"
  };

  // Structured Prefix & Content Match Rules for Complex / Truncated Text
  const textPrefixRules = [
    // Plugins & Customizations
    ["Plugins are packaged collections of skills and MCPs to help the Agent in", "插件是技能和 MCP 的打包集合，用于帮助 "],
    ["Plugins are packaged collections of skills and MCPs", "插件是技能和 MCP 的打包集合，用于帮助 "],
    ["work with Google developer products. You can always change your choices in Settings.", " 中的智能体与 Google 开发者产品协同工作。您可以随时在“设置”中更改您的选择。"],
    ["Provides a comprehensive guide", "提供 Google Antigravity (AGY) 的综合指南、快速参考和站点地图，包括 Antigravity CLI、Antigravity 2.0、IDE、Python SDK、斜杠命令、快捷键和自定义项。"],
    ["How to render rich interactive HTML widgets inline in the chat or as standalone artifacts. Use this skill", "如何在对话中内联或作为独立产物渲染丰富的交互式 HTML 小部件。当您想要向用户显示图表、数据可视化或交互式控件时，请使用此技能。"],
    ["Automatically migrate legacy workflows", "自动将旧版工作流迁移到技能目录。它会扫描现有工作流，并创建目标..."],
    ["Guidelines for interacting with GitHub and request permissions", "关于与 GitHub 交互的指南，并在智能体环境中由于限制导致命令失败时向用户请求相应的权限。"],
    ["Comprehensive guide and reference for the Antigravity Customization System", "Antigravity 自定义系统的综合指南和参考。用于解释自定义项的工作原理、加载优先级、发现机制，并指导创建技能、规则、插件、钩子和 MCP 服务器。"],
    ["Skills providing tailored instructions for happy path", "提供 Dart 和 Flutter 开发主流程定制化指南的技能。"],
    ["Interactive guide to design and create a scheduled background automation", "设计和创建计划后台自动化的交互式指南。当用户想要创建自动化或周期性计划任务时（例如“总结我的邮件”），请使用此技能。"],
    ["How to manage and create plugins", "如何管理和创建插件——作为单一单元安装、启用和禁用的命名空间技能、智能体、规则、MCP 服务器和钩子捆绑包。"],
    ["Build, package, run, and debug UI extensions for Antigravity", "为 Antigravity 构建、打包、运行和调试 UI 扩展：在侧边面板中渲染的交互式 Web 面板，由使用内置 Sidecar SDK 的 Node.js sidecar 提供服务。"],
    ["Discover UI plugin panels relevant to the current task", "发现与当前任务相关的 UI 插件面板，并在对话中显示一键式快捷胶囊以在侧边面板中打开（切换）它们。"],
    ["Build and prototype location-aware applications with Google Maps Platform", "使用 Google Maps Platform 构建具有位置感知能力的应用并设计原型。"],
    ["Specialized suite of skills for data engineers and database", "专为 Google Cloud 上的数据工程师和数据库从业人员打造的专业技能套件。"],
    ["Build applications with the Gemini Interactions API and Live API", "使用 Gemini Interactions API 和 Live API 构建应用，包括文本生成、多轮对话等功能。"],
    ["Build on Google's developer platforms, including Android, Chrome, Gemini, and Google Cloud.", "基于 Google 开发者平台（包括 Android、Chrome、Gemini 和 Google Cloud）构建。"],
    ["Prototype, build & run modern apps that user", "原型设计、构建和运行现代应用程序..."],
    ["Curated collection of agent skills for science t", "为科学任务精心挑选的智能体技能集合。"],
    ["Using the Google Antigravity Python SDK to b", "使用 Google Antigravity Python SDK 构建自定义智能体..."],
    ["Search and retrieve official documentation acr", "搜索和检索官方开发者文档..."],
    ["Integration skill and tools for Google Maps Pl", "适用于 Google Maps Platform 的集成技能和工具。"],
    ["Official plugin for Dart and Flutter that installs", "Dart 和 Flutter 官方插件，提供相关工具安装和开发支持。"],
    ["This plugin provides a specialized suite of skill", "此插件提供一套专为数据处理打造的专业技能..."],
    ["Connect to Google Workspace, including Docs", "连接到 Google Workspace，包括文档、表格、幻灯片、云端硬盘、日历和 Gmail。"],
    ["Search, read, draft, and send emails in Gmail.", "在 Gmail 中搜索、阅读、起草和发送电子邮件。"],
    ["Add authentication and user management", "添加身份验证与用户管理功能。"],
    ["Real salaries and company levels from Levels.fyi", "来自 Levels.fyi 的真实薪资与公司职级数据。"],
    ["Access and clone GitHub repositories", "在远程环境中访问并克隆 GitHub 代码库。"],
    ["Google does not control the availability or functionality of third party developer tools.", "Google 不控制第三方开发者工具的可用性或功能。连接到您的 Antigravity 实例的第三方开发者工具中的数据可能会与 Google 共享。Google 将按照以下链接中的 Google 隐私权政策保护此类数据："],
    ["Read, draft, and edit docs.", "读取、起草和编辑文档。"],
    ["Read, write, and format spreadsheets.", "读取、写入和格式化电子表格。"],
    ["Read, edit, and export presentations.", "读取、编辑和导出演示文稿。"],
    ["Search, upload, download, and share files.", "搜索、上传、下载和共享文件。"],
    ["Check availability, schedule events, and RSVP.", "查看空闲时间、安排活动并回复邀请。"],
    ["Core tools and knowledge required to develop", "开发 Android 所需的核心工具和知识。"],
    ["Google Cloud guidance for coding agents", "面向编程智能体的 Google Cloud 指南：项目引导、身份认证与凭据选择，以及 gcloud CLI 命令的安全校验。"],
    ["Connect to your managed Looker MCP server", "连接到您的托管 Looker MCP 服务器，以探索数据、运行保存的 Look、构建仪表板并验证 LookML。"],
    ["Create, edit, review, resize, and brand-check", "使用 Canva MCP 服务器创建、编辑、审阅、调整尺寸并检查 Canva 设计的品牌规范。"],
    ["Turn Figma designs into production code", "将 Figma 设计转化为生产代码，使用 Code Connect 映射组件，并在 Antigravity 中创建或编辑 Figma 文件。"],
    ["Give your AI agent 600,000+ real app screens", "为您的 AI 智能体提供 600,000+ 真实应用界面及配套技能，参考真实应用模式重构界面设计。"],
    ["Teamwork Graph CLI is Atlassian's agent-first", "Teamwork Graph CLI 是 Atlassian 面向智能体的工作上下文接口：连接 Jira 议题、Confluence 页面、Bitbucket PR 及第三方数据源。"],
    ["Connect Antigravity to Dropbox to search", "将 Antigravity 连接到 Dropbox，以搜索、检查、总结、共享、收集上传、整理文件夹并清理文件。"],
    ["The product development system for teams", "面向团队和智能体的产品开发系统。在 Antigravity 中跨 Linear 工作区管理议题、项目和文档。"],
    ["Plan and track work in monday.com", "在 Antigravity 中规划和跟踪 monday.com 上的工作：创建、更新和分配事项，编写文档并构建表单。"],
    ["Connect Antigravity to your Notion workspace", "通过 Notion MCP 服务器将 Antigravity 连接到您的 Notion 工作区，提供研究、文档、会议准备和项目更新技能。"],
    ["Create and send proposals, quotes, and contracts", "创建并发送用于电子签名的提案、报价单和合同，跟踪签署进度并识别需要跟进的文档。"],
    ["Official Trello plugin with the Trello MCP", "官方 Trello 插件，包含 Trello MCP 服务器以及适用于看板、列表、卡片、清单、收件箱和计划器的技能。"],
    ["Search and read your Wispr Flow meeting notes", "搜索并读取您的 Wispr Flow 会议记录、转录文本、速记笔记和日历事件。"],
    ["Connect Zoho Projects to Antigravity", "将 Zoho Projects 连接到 Antigravity，将任务和问题转化为可用代码，调查错误并更新工作项。"],
    ["Build and deploy on Netlify", "在 Netlify 上构建和部署：函数、边缘函数、Blob、数据库、身份认证、表单、图像 CDN、缓存和 AI 网关。"],
    ["Deploy, configure, monitor, and troubleshoot", "通过 Railway 智能体技能和托管 MCP 服务器，在 Antigravity 中部署、配置、监控和排查 Railway 应用与基础设施。"],
    ["Build and deploy web apps and AI agents on Vercel", "在 Vercel 上构建和部署 Web 应用与 AI 智能体，提供 Next.js、AI SDK 和云服务技能及官方 Vercel MCP 服务器。"],
    ["Add Auth0 authentication to any app", "为任何应用添加 Auth0 身份认证：登录、MFA、SSO、组织、RBAC、自定义域名和品牌定制。"],
    ["Build and deploy Base44 full-stack apps", "构建和部署 Base44 全栈应用：CLI 项目管理、JavaScript/TypeScript SDK 开发与生产环境故障排查技能。"],
    ["Give your agent a real browser", "为您的智能体提供真实浏览器：在本地或 Browserbase 云端浏览器上导航、点击、输入、截图并提取数据。"],
    ["AI-powered code review and review-comment", "由 CodeRabbit 驱动的 AI 代码审阅与审阅意见自动修复。"],
    ["Up-to-date documentation lookup", "最新文档查询。直接从源码仓库拉取特定版本的文档和代码示例到您的 LLM 上下文中。"],
    ["Use the official CrowdStrike-hosted MCP", "使用官方 CrowdStrike 托管的 MCP 服务器操作 Falcon：检测、案件、威胁情报、SIEM、主机和云安全等。"],
    ["Databricks skills for the CLI, Apps, Lakebase", "适用于 Databricks CLI、应用、Lakebase、模型服务、Lakeflow 作业、Spark 声明式流水线等的技能套件。"],
    ["Use Datadog directly in Antigravity", "通过预配置的 Datadog MCP 服务器在 Antigravity 中直接使用 Datadog，通过自然语言查询日志、指标、追踪和仪表板。"],
    ["Investigate production issues with real Dynatrace", "使用真实 Dynatrace 数据调查生产问题：通过技能和 MCP 服务器分析问题根因、日志、指标、追踪和漏洞。"],
    ["Packaged workflows for SCA remediation", "用于 SCA 修复、AI SAST 分类、CI/CD 态势、恶意软件响应、审查结果和 Endor Labs 配置的打包工作流。"],
    ["Build and debug pipelines, manage deployments", "使用连接的工具和可复用工作流技能构建和调试流水线、管理部署、调查安全问题并运维 Harness。"],
    ["Create, run and debug Leapwork Play tests", "直接在 Antigravity 中创建、运行和调试 Leapwork Play 测试和运行列表，构建智能体并交付给 AI 工作流。"],
    ["Official Antigravity plugin for MongoDB Atlas", "MongoDB Atlas 官方插件（托管 MCP 服务器 + 技能），用于探索数据、管理集合、优化查询和生成可靠代码。"],
    ["Agent skills for Neo4j graph database", "适用于 Neo4j 图数据库的智能体技能——编写 Cypher 查询、设计图模型、使用驱动、构建 GraphRAG 流水线等。"],
    ["Agent plugin for PingOne multi-tenant", "适用于 PingOne 多租户的智能体插件，包含允许 AI 智能体配置和监控 PingOne 环境的技能和远程 MCP 服务器。"],
    ["Equip Antigravity with specialized Postman", "为 Antigravity 配备涵盖完整 API 生命周期的专业 Postman 技能：发现、设计、测试、文档化、Mock 和监控 API。"],
    ["Set up Qodo, explore code and repository", "配置 Qodo，直接在 Antigravity 中探索代码和仓库历史记录、审阅本地更改并解决 PR 问题。"],
    ["Query your SentinelOne Singularity Console", "通过自托管的只读 Purple AI MCP 服务器从 Antigravity 查询您的 SentinelOne Singularity 控制台。"],
    ["Set up Sentry monitoring, investigate", "配置 Sentry 监控，利用来自 Sentry 项目的专业技能和实时上下文调查生产错误并配置告警与发布。"],
    ["Triage Exabeam New-Scale alerts and cases", "端到端分类处理 Exabeam New-Scale 告警和案件：收集证据、映射 MITRE、得出结论并记录审批。"],
    ["Official Supabase plugin for Antigravity", "Supabase 官方插件，提供项目管理、数据库操作、身份验证、存储和 Postgres 最佳实践的技能与 MCP 访问。"],
    ["Make your coding agent a better engineer", "让您的编程智能体成为更出色的工程师。"],
    ["Unity's official plugin for Antigravity", "Unity 官方 Antigravity 插件，包含专为游戏开发、变现和性能优化精选的技能。"],
    ["Investigate files, URLs, domains and IP", "使用 VirusTotal 威胁情报、分析和提交恢复功能调查文件、URL、域名和 IP 地址。"],
    ["Accept payments and grow your business", "接受付款并拓展业务。Stripe 官方 MCP 服务器使 AI 智能体能够管理客户、产品、价格、发票、订阅和退款。"],
    ["Search Intercom conversations, contacts", "搜索 Intercom 对话、联系人和公司，发现支持趋势，并通过安全的身份验证安装 Intercom Messenger。"],
    ["Connect your agent to invideo's AI-native", "将您的智能体连接到 invideo 的 AI 原生视频编辑器，在真实时间轴上进行剪辑、调色和混音。"],
    ["Search the web and read any page as clean", "使用专为 AI 智能体打造的搜索引擎 Keenable 搜索网页并将任何页面读取为整洁的 Markdown（无需注册或 API 密钥）。"],
    ["Ask a question of the live web and get", "向实时网络提问并获取表格结果。Keenable SELECT 可在一次调用中运行多次搜索、读取页面并提取所需字段。"],
    ["Search the live web and fetch page content", "使用 Parallel 托管的 MCP 服务器搜索实时网页并获取页面内容（免费访问，无需账号或 API 密钥）。"],
    ["SEO workflows on live Semrush data", "基于实时 Semrush 数据的 SEO 工作流：关键词研究、站点审计、反向链接、竞品与流量分析、PPC 及 AI 品牌可见度。"],
    ["Build Wix apps and headless sites", "使用 Wix CLI 技能和官方 Wix MCP 服务器构建 Wix 应用和无头站点，并管理商店、预约和 CMS。"],
    ["Build, publish, and manage WordPress.com", "构建、发布和管理 WordPress.com 及 Jetpack 连接的站点：起草文章、编辑区块、查看流量统计并管理插件。"],
    ["Connect 9,000+ apps to your AI workflow", "将 9,000+ 应用连接到您的 AI 工作流，直接在客户端中发现、启用和执行 Zapier 操作与工作流。"],
    ["Manage your Bigin CRM from Antigravity", "在 Antigravity 中管理您的 Bigin CRM：查看销售管道、查找联系人和交易、记录通话、规划跟进并向客户发送邮件。"],
    ["Build on Zoho CRM v8: REST API, Deluge", "基于 Zoho CRM v8 构建：通过您的 Zoho MCP 服务器访问实时 CRM 数据，使用 REST API、Deluge 函数、小部件和 COQL。"],
    ["Zoho Desk plugin for Antigravity. Review", "适用于 Antigravity 的 Zoho Desk 插件：通过 Zoho Desk MCP 直接审阅、排定优先级并更新工单。"],
    ["Run Zoho Books from Antigravity: invoicing", "在 Antigravity 中运行 Zoho Books：管理发票、账单、银行、日记账、项目、商品、税务、自定义和自动化。"],

    // MCP Servers Descriptions
    ["Investigate and fix software issues using AI-powered root cause analysis", "使用 AI 驱动的根本原因分析来调查和修复软件问题。此 MCP 服务器连接到您的 Antimetal 账户..."],
    ["Query and act on your marketing, analytics, CRM, e-commerce", "跨 325 多个连接器查询并处理您的营销、分析、CRM、电子商务和仓库数据..."],
    ["Query your GitLab SDLC as a knowledge graph", "将您的 GitLab SDLC 作为知识图谱进行查询。Orbit 会建立相关索引..."],
    ["Enable Antigravity to deploy apps to Google Cloud Run", "使 Antigravity 能够将应用部署到 Google Cloud Run。"],
    ["Search and reference over 600,000 real-world app screens", "搜索并参考超过 600,000 个真实的应用程序屏幕、用户流程和 UI 模式..."],
    ["Build, edit, deploy, and manage full-stack web apps with Lovable", "使用自然语言，通过 Lovable 构建、编辑、部署和管理全栈 Web 应用..."],
    ["The GKE remote MCP server provides read write access to your GKE", "GKE 远程 MCP 服务器提供对您的 GKE Kubernetes 资源的读写访问权限。"],
    ["The Dart and Flutter MCP server exposes Dart (and Flutter)", "Dart 和 Flutter MCP 服务器向兼容的 AI 助手客户端公开相关开发工具操作。"],
    ["The Firebase Model Context Protocol (MCP) Server gives AI-powered", "Firebase MCP 服务器使 AI 工具能够处理您的 Firebase 项目和应用程序代码库。"],
    ["The Genkit Model Context Protocol (MCP) Server gives AI-powered", "Genkit MCP 服务器使 AI 工具能够构建、调试和检查您的 Genkit 应用。"],
    ["The gopls Model Context Protocol (MCP) server provides tools", "gopls MCP 服务器为您的 Go 代码库提供语义代码分析、实时诊断和转换工具。"],
    ["Interact with your BigQuery data using natural language", "使用自然语言与您的 BigQuery 数据交互。允许您安全地连接到您的数据集..."],
    ["The AlloyDB for PostgreSQL remote MCP server lets you access", "AlloyDB for PostgreSQL 远程 MCP 服务器允许您访问和运行 AlloyDB 工具..."],
    ["The Bigtable Admin remote MCP server lets you manage Bigtable", "Bigtable Admin 远程 MCP 服务器允许您管理 Bigtable 资源。"],
    ["The Cloud SQL remote MCP server lets you access and run Cloud SQL", "Cloud SQL 远程 MCP 服务器允许您访问和运行 Cloud SQL 工具..."],
    ["The Spanner remote MCP server lets you access and run Spanner", "Spanner 远程 MCP 服务器允许您访问和运行 Spanner 工具..."],
    ["The Apigee API hub remote MCP server lets you manage", "Apigee API hub 远程 MCP 服务器允许您管理 API、版本、规范、操作等。"],
    ["Connect your AI assistants to Looker business intelligence", "将您的 AI 助手连接到 Looker 商业智能，通过自然语言查询实现数据探索。"],
    ["Connect your AI assistants to the Knowledge Catalog", "将您的 AI 助手连接到 Knowledge Catalog，实现数据发现和治理。"],
    ["The MCP Toolbox for Databases is an open-source MCP server", "MCP Toolbox for Databases 是一个开源 MCP 服务器，旨在简化和保护用于与数据库交互的工具的开发。"],
    ["Interact with your Oracle Database data using natural language", "使用自然语言与您的 Oracle 数据库交互。此 MCP 服务器允许您安全地连接到您的数据库以执行 SQL 查询..."],
    ["The Dev Mode MCP Server brings Figma directly into your workflow", "Dev Mode MCP 服务器通过向从 Figma 生成代码的 AI 智能体提供重要的设计信息和上下文，将 Figma 直接带入您的工作流..."],
    ["The GitHub MCP Server is a Model Context Protocol (MCP) server", "GitHub MCP 服务器提供与 GitHub API 的无缝集成，从而实现高级自动化和..."],
    ["The Google Home Developer MCP server allows you to search", "Google Home Developer MCP 服务器允许您搜索 Google Home 文档、OpenThread 和 Matter 规范文档。"],
    ["Neon MCP Server is an open-source tool that lets you interact", "Neon MCP 服务器是一个开源工具，允许您使用自然语言与您的 Neon Postgres 数据库交互。"],
    ["The Stripe Model Context Protocol server allows you to integrate", "Stripe MCP 服务器允许您通过函数调用与 Stripe API 集成。该协议支持各种交互工具..."],
    ["Interact with Redis key-value stores", "与 Redis 键值存储交互。"],
    ["A Model Context Protocol server for interacting with MongoDB", "用于与 MongoDB Atlas 交互的模型上下文协议服务器。"],
    ["Official Notion MCP Server that allows interaction with Notion", "官方 Notion MCP 服务器，允许通过 Notion API 与 Notion 工作区、页面、数据库和评论进行交互。"],
    ["Official Linear.app MCP Server for interacting with Linear", "官方 Linear.app MCP 服务器，用于与 Linear 项目、议题和工作流进行交互。"],
    ["An MCP server implementation that integrates the Perplexity", "一个集成了 Perplexity Sonar API 的 MCP 服务器实现，以提供实时的、全网范围的研究能力。"],
    ["Official PayPal MCP Server that allows integration with PayPal", "官方 PayPal MCP 服务器，允许与 PayPal API 集成，用于支付处理、交易管理和账户操作。"],
    ["The Heroku Platform MCP Server enables seamless interaction", "Heroku Platform MCP 服务器可实现与 Heroku 平台资源的无缝交互，允许 LLM 读取、管理和操作应用程序..."],
    ["The Pinecone MCP Server enables AI tools to search Pinecone", "Pinecone MCP 服务器使 AI 工具能够搜索 Pinecone 文档、配置索引、根据索引配置生成代码..."],
    ["Connect your Supabase projects to AI assistants.", "将您的 Supabase 项目连接到 AI 助手。此 MCP 服务器允许管理表、获取配置、执行 SQL 查询、管理边缘函数等..."],
    ["The Prisma MCP Server enables AI tools to interact with Prisma", "Prisma MCP 服务器使 AI 工具能够与 Prisma 交互，从而轻松创建和管理 Postgres 数据库。"],
    ["The Locofy MCP Server", "Locofy MCP 服务器使 Locofy.ai 代码能够与您的 IDE 集成并进行扩展。"],
    ["Locofy MCP Server enables Locofy.ai code", "Locofy MCP 服务器使 Locofy.ai 代码能够与您的 IDE 集成并进行扩展。"],
    ["Airweave lets agents search any app.", "Airweave 允许智能体搜索任何应用程序。"],
    ["Atlassian MCP Server for interacting with Atlassian", "用于与 Atlassian 产品交互的 Atlassian MCP 服务器。"],
    ["Interact with your Harness account using natural language", "使用自然语言与您的 Harness 账户交互。此 MCP 服务器允许 AI 智能体检查和管理 CI/CD 流水线、执行、服务..."],
    ["SonarQube MCP Server enables AI assistants to interact", "SonarQube MCP 服务器使 AI 助手能够与 SonarQube 实例交互，进行代码质量分析、项目管理和质量门限操作。"],
    ["Perform searches on ingested data in Google-owned data stores", "在 Google 拥有的数据存储中，对已摄取的数据执行搜索。"],
    ["Interact with documents stored in a Firestore database", "使用自然语言与存储在 Firestore 数据库中的文档进行交互。"],
    ["Access resources in the Cloud Logging platform using natural", "使用自然语言访问 Cloud Logging 平台中的资源。"],
    ["Manage clusters for Managed Service for Apache Kafka", "使用自然语言管理 Apache Kafka 托管服务和 Kafka Connect 的集群。"],
    ["Access resources in the Cloud Monitoring platform using natural", "使用自然语言访问 Cloud Monitoring 平台中的资源。"],
    ["Manage Pub/Sub resources and publish messages. Create, list,", "管理 Pub/Sub 资源并发布消息。创建、列出、获取、更新和删除 Pub/Sub 主题、订阅和快照，以及发布消息..."],
    ["The Cloud Quotas MCP server allows you to view quota allocations", "Cloud Quotas MCP 服务器允许您查看配额分配、请求增加配额以及管理配额调整器配置。"],
    ["Enable Antigravity to control and inspect a live Chrome browser", "使 Antigravity 能够控制和检查实时 Chrome 浏览器，利用 Chrome DevTools 的强大功能进行可靠的自动化、深度调试..."],
    ["Netlify MCP Server enables AI assistants to interact", "Netlify MCP 服务器使 AI 助手能够与 Netlify 平台交互，以管理站点、部署、域名和其他 Web 开发工作流。"],
    ["A Model Context Protocol server that provides structured thinking", "一个模型上下文协议服务器，为 LLM 对话提供结构化思考和推理能力。"],
    ["Sonatype MCP server for interacting with our dependency management", "用于与我们的依赖项管理和安全情报平台交互的 Sonatype MCP 服务器。"],
    ["The Google Maps Platform Code Assist MCP server provides", "Google Maps Platform Code Assist MCP 服务器为您喜爱的 AI 编程助手提供最新、官方的 Google Maps Platform 文档、代码..."],
    ["This MCP server provides your LLM with docs and examples to instrument your AI apps with Arize AX", "此 MCP 服务器为您的 LLM 提供文档和示例，以便使用 Arize AX 检测您的 AI 应用。它还提供对 Arize 支持的访问。将其连接到您的 IDE..."],
    ["The Postman MCP Server connects Postman to AI tools", "Postman MCP 服务器将 Postman 连接到 AI 工具，使 AI 智能体和助手能够访问工作区、管理集合和环境..."],
    ["The Stitch MCP server enables AI assistants to interact with Stitch", "Stitch MCP 服务器使 AI 助手能够与 Stitch 交互以进行设计：从文本和图像生成 UI 设计，以及访问项目和屏幕..."],
    ["The ClickHouse MCP server enables agents to securely interact", "ClickHouse MCP 服务器使智能体能够安全地与 ClickHouse 数据库交互。它提供了一个通用接口来执行 SQL、探索数据和查看..."],
    ["Perform a range of infrastructure management tasks, including: manage virtual machine", "执行一系列基础设施管理任务，包括：管理虚拟机 (VM) 实例、管理实例组管理器和实例模板..."],
    ["Access enterprise mobility data using natural language queries", "使用关于设备队列的自然语言查询、策略合规性的自动审计以及设备集成来访问企业移动数据..."],
    ["Search your Google Cloud projects using natural language", "使用自然语言搜索您的 Google Cloud 项目。"],

    // Error and Fallback Links
    ["Kick off work on your computer and continue working", "在电脑上启动工作，并可以通过手机或其他设备继续与智能体协同工作。请在应用设置中开启“远程控制”。"],
    ["Turn on Remote Control in app settings", "请在应用设置中开启“远程控制”。"],
    ["Try Remote Control", "尝试远程控制"],
    ["Agent execution terminated due to error", "智能体执行因错误而终止。"],
    ["Confirming this undo action will make the following changes", "确认此撤销操作将做出以下更改："],
    ["Confirming this undo action will not make any code changes", "确认此撤销操作不会做出任何代码更改。"],
    ["Confirming this redo action will make the following changes", "确认此重做操作将做出以下更改："],
    ["Confirming this redo action will not make any code changes", "确认此重做操作不会做出任何代码更改。"],
    ["Undo changes up to this point", "撤销更改至此处"],
    ["Redo changes up to this point", "重做更改至此处"],
    ["Our servers are experiencing high traffic", "我们的服务器当前负载较高，请稍后重试。"],
    ["Agent terminated due to error", "智能体因错误而终止"],
    ["You can prompt the model to try again", "您可以提示模型重试，或者如果错误仍然存在，可以开启新的对话。"],
    ["for more help", " 以获取更多帮助。"],
    ["See our", "查看我们的 "]
  ];

  // v2.33.0 Dynamic Regex Rules
  const v233RegexRules = [
    [new RegExp("^For paid Pro plans, (.+?) quota is separate\\. Higher (.+?) quota \\(included as part of the larger Gemini quota bucket\\) is available on Ultra plans\\.$"), "对于付费 Pro 套餐，$1 配额单独计算。Ultra 套餐提供更高的 $2 配额（包含在更大的 Gemini 配额池中）。"],
    [new RegExp("^(.+?) that may offload routine steps to (.+?)\\. Same (.+?)-level quality, fewer tokens used\\.$"), "可将常规步骤分流至 $2 的 $1 模型。保持 $3 级别质量，同时消耗更少 Token。"],
    [new RegExp("^Models within this group: (.+)$"), "此分组包含的模型：$1"],
    [new RegExp("^(.+?) is currently available to (.+?) plan subscribers\\.$"), "$1 目前仅向 $2 套餐订阅用户开放。"],
    [new RegExp("^(\\d+) of (\\d+)$"), "第 $1 / $2 条"],
    [new RegExp("^\\((\\d+) image attachments?\\)$"), "（$1 张图片附件）"],
    [new RegExp("^(\\d+) image attachments?$"), "$1 张图片附件"],
    [new RegExp("^No hosts in (.+?) yet$"), "$1 中暂无主机"],
    [new RegExp("^Commit ([0-9a-fA-F]{7})$"), "提交 $1"],
    [new RegExp("^(\\d+[smhd]) limit$"), "$1 限额"],
    [new RegExp("^(.+)… Text truncated, use headings to navigate\\.$"), "$1… 文本已截断，请使用标题进行导航。"],
    [new RegExp("^File exceeds the (\\d+(?:\\.\\d+)?)MB display limit \\((\\d+(?:\\.\\d+)?)MB\\), so it can't be opened or downloaded here\\.$"), "文件超过 $1MB 的显示限制（$2MB），因此无法在此处打开或下载。"],
    [new RegExp("^(\\d+(?:s|m|h|d|w|mo|y)) ago$"), "$1 前"],
    [new RegExp("^Command: (.+)$"), "命令：$1"],
    [new RegExp("^URL: (.+)$"), "URL：$1"],
    [new RegExp("^Agent finished: (.+)$"), "智能体已完成：$1"],
    [new RegExp("^([A-Z0-9]+) file uploads are not currently supported in remote mode$"), "远程模式暂不支持上传 $1 文件"],
    [new RegExp("^Total media size exceeds (\\d+)MB limit$"), "媒体文件总大小超过 $1MB 限制"],
    [new RegExp("^Back to reference (.+)$"), "返回引用 $1"],
    [new RegExp("^Open (.+?) skill$"), "打开 $1 技能"],
    [new RegExp("^(\\d+) Comments$"), "$1 条评论"],
    [new RegExp("^Source (\\d+)$"), "来源 $1"],
    [new RegExp("^(.+?) needs? the terminal sandbox, which isn't available on this host\\.$"), "$1 需要终端沙盒，但此主机不支持终端沙盒。"],
    [new RegExp("^Thinking \\((\\d+)s\\)…$"), "思考中（$1 秒）…"],
    [new RegExp("^The preview did not respond on port (\\d+)\\.$"), "端口 $1 上的预览未响应。"],
    [new RegExp("^Nothing is running on port (\\d+)$"), "端口 $1 上没有正在运行的服务"],
    [new RegExp("^Resume the conversation to start its workspace again, then start the server on port (\\d+) and retry\\.$"), "恢复对话以重新启动其工作区，然后在端口 $1 上启动服务器并重试。"],
    [new RegExp("^No server is listening on port (\\d+) inside the remote workspace\\. Start it, or ask the agent to, then retry\\.$"), "远程工作区内的端口 $1 上没有服务器在监听。请启动该服务器（或让智能体启动），然后重试。"],
    [new RegExp("^The certificate was rejected \\((.+?)\\)\\.$"), "证书已被拒绝（$1）。"],
    [new RegExp("^An embedded page at (.+?) wants to connect to (.+)$"), "位于 $1 的嵌入页面请求连接到 $2"],
    [new RegExp("^(.+?) wants to connect to (.+)$"), "$1 请求连接到 $2"],
    [new RegExp("^An embedded page on this page wants to connect to (.+)$"), "此页面上的嵌入页面请求连接到 $1"],
    [new RegExp("^This page wants to connect to (.+)$"), "此页面请求连接到 $1"],
    [new RegExp("^An embedded page at (.+?) says$"), "位于 $1 的嵌入页面显示"],
    [new RegExp("^(https?://[^\\s]+|[a-zA-Z0-9.-]+(?::\\d+)?) says$"), "$1 显示"],
    [new RegExp("^(.+?)\\. View site information$"), "$1。查看网站信息"],
    [new RegExp("^Downloads, (\\d+)% complete$"), "下载，已完成 $1%"],
    [new RegExp("^(.+?) download progress$"), "$1 下载进度"],
    [new RegExp("^Show (.+?) in folder$"), "在文件夹中显示 $1"],
    [new RegExp("^Remove (.+?) from list$"), "从列表中移除 $1"],
    [new RegExp("^Check if there is a typo in (.+?), or open the page in your external browser\\.$"), "请检查 $1 中是否有拼写错误，或在外部浏览器中打开该页面。"],
    [new RegExp("^(.+?) could not find the requested page\\.$"), "$1 找不到请求的页面。"],
    [new RegExp("^(.+?) is currently unable to handle this request\\.$"), "$1 目前无法处理此请求。"],
    [new RegExp("^HTTP ERROR (\\d+)$"), "HTTP 错误 $1"],
    [new RegExp("^Give each Best of N fork its own clone of your Git repository instead of a copy-on-write overlay\\. Each fork is then a real repository, so commits it makes are kept when you choose it as the winner\\. Forks take longer to create, and the wait grows with the size of your repository\\.(.*)$"), "为每个 Best of N 分支提供您的 Git 仓库的独立完整克隆，而不是写时复制（copy-on-write）叠加层。这样每个分支都是一个真实的仓库，因此当您将其选为胜出方案时，它所做的提交会被保留。创建分支将花费更长时间，且等待时间会随仓库大小增加。$1"],
    [new RegExp("^([\\s\\S]*?)For (.+?), this setting is disabled\\. This means ([^ ]+) does not collect any of your prompts, content, or model responses, but will still collect general usage patterns \\(e\\.g\\., feature adoption, active user counts\\)\\.$"), "$1对于 $2，此设置已禁用。这意味着 $3 不会收集您的任何提示词、内容或模型回复，但仍会收集一般使用模式（例如功能采用率、活跃用户数）。"],
    [new RegExp("^For (.+?), telemetry is force disabled\\.$"), "对于 $1，遥测已强制禁用。"],
    [new RegExp("^For (.+?), this setting is disabled\\.$"), "对于 $1，此设置已禁用。"],
    [new RegExp("^Your Plan: (.+)$"), "您的套餐：$1"],
    [new RegExp("^Sign in from the (.+?) panel\\.$"), "从 $1 面板登录。"],
    [new RegExp("^Sign in to use (.+?)!$"), "登录以使用 $1！"],
    [new RegExp("^(.+?) \\(disabled by admin\\)$"), "$1（已由管理员禁用）"],
    [new RegExp("^(.+?) Sends immediately$"), "$1 立即发送"],
    [new RegExp("^(.+?) Queues after the turn$"), "$1 在本轮结束后排队发送"],
    [new RegExp("^(.+?) On empty prompt, sends next in queue$"), "$1 提示词为空时，发送队列中的下一条"],
    [new RegExp("^Manage (.+?) app settings\\.$"), "管理 $1 应用设置。"],
    [new RegExp("^Deleted cookies for (.+)$"), "已删除 $1 的 Cookie"],
    [new RegExp("^Delete cookies for (.+)$"), "删除 $1 的 Cookie"],
    [new RegExp("^Microphone blocked\\. Allow in (.+?)\\.$"), "麦克风已被阻止。请在$1中允许访问。"],
    [new RegExp("^Microphone access for (.+?) was denied\\. Quit and reopen the app to be asked again\\.$"), "$1 的麦克风访问权限已被拒绝。请退出并重新打开应用以重新请求权限。"],
    [new RegExp("^Microphone access for (.+?) wasn't allowed\\.$"), "未允许 $1 访问麦克风。"],
    [new RegExp("^When toggled on, (.+?) will use your AI credits to fulfill model requests once you're out of model quota\\. (.+?) will always use your model quota first before using AI credits\\.$"), "开启后，当您的模型配额用尽时，$1 将使用您的 AI 积分来完成模型请求。$2 始终会先使用您的模型配额，再使用 AI 积分。"],
    [new RegExp("^(.+?) could not be stopped: (.+)$"), "无法停止 $1：$2"],
    [new RegExp("^Stopping (\\d+) tasks?$"), "正在停止 $1 个任务"],
    [new RegExp("^Closed (\\d+) terminals?$"), "已关闭 $1 个终端"],
    [new RegExp("^Stop (\\d+) selected$"), "停止所选的 $1 项"],
    [new RegExp("^Stop (\\d+) (?:items?|tasks?|terminals?|processes?)\\?$"), "确定要停止这 $1 项吗？"],
    [new RegExp("^Conflicts with \"(.+?)\" \\(press Enter to replace\\)$"), "与“$1”冲突（按 Enter 替换）"],
    [new RegExp("^Conflicts with \"(.+?)\"$"), "与“$1”冲突"],
    [new RegExp("^Conflicts with \"(.+?)\" \\(managed by application menu\\)$"), "与“$1”冲突（由应用菜单管理）"],
    [new RegExp("^Recording shortcut for (.+?)\\. Press keys to bind, Enter to save, Escape to cancel\\.$"), "正在为 $1 录制快捷键。请按下要绑定的按键，按 Enter 保存，按 Esc 取消。"],
    [new RegExp("^Conflict: also assigned to (.+)$"), "冲突：也已分配给 $1"],
    [new RegExp("^Shortcut (.+?) for (.+)$"), "$2 的快捷键 $1"],
    [new RegExp("^Remove shortcut (.+?) for (.+)$"), "移除 $2 的快捷键 $1"],
    [new RegExp("^Add shortcut for (.+)$"), "为 $1 添加快捷键"],
    [new RegExp("^Reset (.+?) to default$"), "将 $1 重置为默认"],
    [new RegExp("^(\\d+) demoted$"), "已降级 $1 项"],
    [new RegExp("^(\\d+) excluded$"), "已排除 $1 项"],
    [new RegExp("^(\\d+) rules? exceeded the rules budget and (?:was|were) demoted from full inline content to a file-path pointer\\.$"), "$1 条规则超出规则预算，已从完整内联内容降级为文件路径指针。"],
    [new RegExp("^(\\d+) items? in (.+?) exceeded the customization budget and (?:was|were) excluded from context\\.$"), "$2 中的 $1 项超出自定义项预算，已从上下文中排除。"],
    [new RegExp("^Show (\\d+) breakdowns?$"), "显示 $1 项明细"],
    [new RegExp("^Exceeded the rules token budget\\. Full rule content \\(([\\d,]+) tokens\\) was replaced with a lightweight file-path pointer in context\\.$"), "超出规则 Token 预算。上下文中的完整规则内容（$1 个 Token）已替换为轻量级文件路径指针。"],
    [new RegExp("^All tools in this MCP server \\(([\\d,]+) tokens\\) exceeded the customization budget and were excluded from context\\.$"), "此 MCP 服务器中的所有工具（$1 个 Token）均超出自定义项预算，已从上下文中排除。"],
    [new RegExp("^(\\d+) tools? in this MCP server \\(([\\d,]+) tokens\\) exceeded the customization budget and were excluded from context\\.$"), "此 MCP 服务器中的 $1 个工具（$2 个 Token）超出自定义项预算，已从上下文中排除。"],
    [new RegExp("^Exceeded the customization token budget \\(([\\d,]+) tokens\\) and was excluded from context\\.$"), "超出自定义项 Token 预算（$1 个 Token），已从上下文中排除。"],
    [new RegExp("^(.+?) \\(Experimental\\)$"), "$1（实验性）"],
    [new RegExp("^Auth code for (.+)$"), "$1 的授权码"],
    [new RegExp("^(\\d+) tools? enabled$"), "已启用 $1 个工具"],
    [new RegExp("^(\\d+) tools? disabled$"), "已禁用 $1 个工具"],
    [new RegExp("^Error submitting auth code: (.+)$"), "提交授权码时出错：$1"],
    [new RegExp("^Error disconnecting MCP server: (.+)$"), "断开 MCP 服务器连接时出错：$1"],
    [new RegExp("^Error installing MCP server: (.+)$"), "安装 MCP 服务器时出错：$1"],
    [new RegExp("^Added MCP server \"(.+?)\", but it failed to start: (.+)$"), "已添加 MCP 服务器“$1”，但启动失败：$2"],
    [new RegExp("^MCP server \"(.+?)\" does not have a remote configuration\\.$"), "MCP 服务器“$1”没有远程配置。"],
    [new RegExp("^MCP server \"(.+?)\" does not have a supported configuration\\.$"), "MCP 服务器“$1”没有受支持的配置。"],
    [new RegExp("^No installation command found for MCP server \"(.+?)\"\\.$"), "未找到 MCP 服务器“$1”的安装命令。"],
    [new RegExp("^MCP server \"(.+?)\" does not have any installation commands\\.$"), "MCP 服务器“$1”没有任何安装命令。"],
    [new RegExp("^MCP server \"(.+?)\" not found in the store\\.$"), "商店中未找到 MCP 服务器“$1”。"],
    [new RegExp("^Error toggling MCP server: (.+)$"), "切换 MCP 服务器状态时出错：$1"],
    [new RegExp("^Server \"(.+?)\" not found in config$"), "配置中未找到服务器“$1”"],
    [new RegExp("^Error deleting MCP server: (.+)$"), "删除 MCP 服务器时出错：$1"],
    [new RegExp("^Error restarting MCP server: (.+)$"), "重启 MCP 服务器时出错：$1"],
    [new RegExp("^Error toggling tool: (.+)$"), "切换工具状态时出错：$1"],
    [new RegExp("^Error refreshing MCP servers: (.+)$"), "刷新 MCP 服务器时出错：$1"],
    [new RegExp("^Are you sure you want to delete the hook \"(.+?)\"\\?$"), "确定要删除钩子“$1”吗？"],
    [new RegExp("^Please fill in all required fields: (.+)$"), "请填写所有必填字段：$1"],
    [new RegExp("^Sign-ins to (.+?) are kept in the cloud with your account\\.$"), "$1 的登录状态将随您的账户保存在云端。"],
    [new RegExp("^Secret for (.+)$"), "$1 的密钥"],
    [new RegExp("^New secret for (.+)$"), "$1 的新密钥"],
    [new RegExp("^Make (.+?) the default (.+?) account$"), "将 $1 设为默认 $2 账户"],
    [new RegExp("^Secret for a new (.+?) account$"), "新 $1 账户的密钥"],
    [new RegExp("^Label for (.+)$"), "$1 的标签"],
    [new RegExp("^Authorization code for (.+)$"), "$1 的授权码"],
    [new RegExp("^Couldn't load apps: (.+)$"), "无法加载应用：$1"],
    [new RegExp("^Couldn't disconnect (.+?): (.+)$"), "无法断开 $1 的连接：$2"],
    [new RegExp("^(.+?) \\(Remote\\)$"), "$1（远程）"],
    [new RegExp("^Sign in to (.+?) remotely$"), "远程登录到 $1"],
    [new RegExp("^More for (.+)$"), "更多关于 $1 的操作"],
    [new RegExp("^A project's private resources must all belong to one owner \\((.+?)\\)\\.$"), "项目的私有资源必须全部属于同一所有者（$1）。"],
    [new RegExp("^Add \\((\\d+)\\)$"), "添加 ($1)"],
    [new RegExp("^(\\d+) active conversations$"), "$1 个活跃对话"],
    [new RegExp("^(\\d+) archived conversations$"), "$1 个已归档对话"],
    [new RegExp("^Conversation ([A-Z0-9]+)$"), "对话 $1"],
    [new RegExp("^Started voice chat · (.*)$"), "已开始语音对话 · $1"],
    [new RegExp("^Stopped voice chat · (.*)$"), "已停止语音对话 · $1"],
    [new RegExp("^Open (.+?), (.+?)\\. Summarizing call$"), "打开 $1，$2。正在总结通话"],
    [new RegExp("^Recording exceeds 15MB limit \\(([\\d.]+)MB\\)$"), "录制内容超出 15MB 限制（$1MB）"],
    [new RegExp("^Connecting to (.+)…$"), "正在连接到 $1…"],
    [new RegExp("^Couldn't connect to (.+?)\\. (.+)$"), "无法连接到 $1。$2"],
    [new RegExp("^Couldn't connect to (.+)$"), "无法连接到 $1"],
    [new RegExp("^SSH config: (.+)$"), "SSH 配置：$1"],
    [new RegExp("^Remove (.+) from Recent$"), "从最近列表中移除 $1"],
    [new RegExp("^Removed (.+) from Recent$"), "已从最近列表中移除 $1"],
    [new RegExp("^Couldn't remove (.+) from Recent$"), "无法从最近列表中移除 $1"],
    [new RegExp("^Hide (.+) from this list$"), "从此列表中隐藏 $1"],
    [new RegExp("^Show (.+) in the list again$"), "重新在列表中显示 $1"],
    [new RegExp("^Showing (.+) again$"), "已重新显示 $1"],
    [new RegExp("^SSH Config \\((.+)\\)$"), "SSH 配置（$1）"],
    [new RegExp("^(\\d+) hidden hosts$"), "$1 个已隐藏的主机"],
    [new RegExp("^You're signing in on (.+)\\. Your sign-in stays on that machine\\.$"), "您正在 $1 上登录。您的登录状态将保留在该设备上。"],
    [new RegExp("^Connected to (.+)$"), "已连接到 $1"],
    [new RegExp("^This window's agents, files, and terminals are on (.+)\\.$"), "此窗口的智能体、文件和终端均位于 $1。"],
    [new RegExp("^(\\d+) lines added, (\\d+) lines removed$"), "新增 $1 行，删除 $2 行"],
    [new RegExp("^(Commit|Amend|Push|Pull|Fetch|Stage|Unstage|Discard|Merge|Rebase|Stash|Checkout|Sync|Revert) Failed$"), "$1 失败"],
    [new RegExp("^Amended commit on (.+)\\.$"), "已修改 $1 上的提交。"],
    [new RegExp("^You need at least (\\d+) AI Credits to send messages\\. To continue using (.+?) now, purchase more AI Credits\\. Your plan's baseline quota will refresh on (.+?)\\.$"), "您需要至少 $1 AI 积分才能发送消息。要立即继续使用 $2，请购买更多 AI 积分。您的套餐基础配额将于 $3 刷新。"],
    [new RegExp("^You need more AI Credits to send messages\\. To continue using (.+?) now, purchase more AI Credits\\. Your plan's baseline quota will refresh on (.+?)\\.$"), "您需要更多 AI 积分才能发送消息。要立即继续使用 $1，请购买更多 AI 积分。您的套餐基础配额将于 $2 刷新。"],
    [new RegExp("^You need at least (\\d+) AI Credits to send messages\\. To continue using (.+?) now, purchase more AI Credits\\.$"), "您需要至少 $1 AI 积分才能发送消息。要立即继续使用 $2，请购买更多 AI 积分。"],
    [new RegExp("^You need more AI Credits to send messages\\. To continue using (.+?) now, purchase more AI Credits\\.$"), "您需要更多 AI 积分才能发送消息。要立即继续使用 $1，请购买更多 AI 积分。"],
    [new RegExp("^Your plan's baseline quota will refresh on (.+?)\\. To continue using this model now, enable AI Credit overages\\.$"), "您的套餐基础配额将于 $1 刷新。若要立即继续使用此模型，请启用 AI 积分超额使用。"],
    [new RegExp("^Your plan's baseline quota will refresh on ((?:(?!\\.\\s+[A-Z]).)+)\\.$"), "您的套餐基础配额将于 $1 刷新。"],
    [new RegExp("^Couldn't (.+) conversation$"), "无法对对话执行 $1 操作"],
    [new RegExp("^Open (.+) link\\?$"), "打开 $1 链接？"],
    [new RegExp("^A file already exists at (.+)\\.$"), "$1 处已存在同名文件。"],
    [new RegExp("^Can’t create this path — “(.+)” is a file, not a folder\\.$"), "无法创建此路径——“$1”是文件，而不是文件夹。"],
    [new RegExp("^The folder “(.+)” does not exist\\. Would you like to create it\\?$"), "文件夹“$1”不存在。您要创建它吗？"],
    [new RegExp("^Go to slide (\\d+)$"), "转到第 $1 张幻灯片"],
    [new RegExp("^Open conversation (.+)$"), "打开对话 $1"],
    [new RegExp("^Open the (.+) plugin$"), "打开 $1 插件"],
    [new RegExp("^Opens external link: (.+)$"), "打开外部链接：$1"],
    [new RegExp("^Cancel Questionnaire and Stop the Agent \\((.+)\\)$"), "取消问卷并停止智能体（$1）"],
    [new RegExp("^Show (\\d+) earlier steps$"), "显示 $1 个较早的步骤"],
    [new RegExp("^Showing latest (\\d+) browser steps$"), "显示最近 $1 个浏览器步骤"],
    [new RegExp("^(\\d+) browser steps$"), "$1 个浏览器步骤"],
    [new RegExp("^Wants to run: (.+)$"), "请求运行：$1"],
    [new RegExp("^Message from (.+)$"), "来自 $1 的消息"],
    [new RegExp("^Minimum length is (\\d+)$"), "最小长度为 $1"],
    [new RegExp("^Maximum length is (\\d+)$"), "最大长度为 $1"],
    [new RegExp("^Input must match (.+)$"), "输入必须匹配 $1"],
    [new RegExp("^Minimum value is (-?[\\d.]+)$"), "最小值为 $1"],
    [new RegExp("^Maximum value is (-?[\\d.]+)$"), "最大值为 $1"],
    [new RegExp("^Select at least (\\d+) items$"), "请至少选择 $1 项"],
    [new RegExp("^Select at most (\\d+) items$"), "最多选择 $1 项"],
    [new RegExp("^Open Subagent: (.+?) \\((.+?)\\)$"), "打开子智能体：$1（$2）"],
    [new RegExp("^Open Subagent: (.+)$"), "打开子智能体：$1"],
    [new RegExp("^(\\d+) folders in this project could not be loaded because their locations are invalid\\.$"), "此项目中的 $1 个文件夹因位置无效而无法加载。"],
    [new RegExp("^Creating (.+)…$"), "正在创建 $1…"],
    [new RegExp("^App view for (.+)$"), "$1 的应用视图"],
    [new RegExp("^Open URL in system browser: (.+)$"), "在系统浏览器中打开 URL：$1"],
    [new RegExp("^Waiting for command completion \\(up to (\\d+) seconds\\)$"), "正在等待命令完成（最多 $1 秒）"],
    [new RegExp("^(\\d+) chunks$"), "$1 个分块"],
    [new RegExp("^Chunk (\\d+)$"), "分块 $1"],
    [new RegExp("^Typing '(.+)' in Browser$"), "正在浏览器中输入 '$1'"],
    [new RegExp("^Typed '(.+)' in Browser$"), "已在浏览器中输入 '$1'"],
    [new RegExp("^(-?\\d+)px horizontally, (-?\\d+)px vertically$"), "水平 $1px，垂直 $2px"],
    [new RegExp("^(-?\\d+)px horizontally$"), "水平 $1px"],
    [new RegExp("^(-?\\d+)px vertically$"), "垂直 $1px"],
    [new RegExp("^\\((\\d+) steps?\\)$"), "（$1 个步骤）"],
    [new RegExp("^Generating with (.+) 🍌$"), "正在使用 $1 生成 🍌"],
    [new RegExp("^Generated with (.+) 🍌$"), "已使用 $1 生成 🍌"],
    [new RegExp("^Generate with (.+) 🍌$"), "使用 $1 生成 🍌"],
    [new RegExp("^(\\d+) questions?$"), "$1 个问题"],
    [new RegExp("^Model unavailable, retrying in (\\d+)s \\(attempt (\\d+)/(\\d+)\\)$"), "模型不可用，$1 秒后重试（第 $2/$3 次尝试）"],
    [new RegExp("^Model unavailable, retrying in (\\d+)s$"), "模型不可用，$1 秒后重试"],
    [new RegExp("^Model unavailable, retrying \\(attempt (\\d+)/(\\d+)\\)$"), "模型不可用，正在重试（第 $1/$2 次尝试）"],
    [new RegExp("^Model unavailable, retrying$"), "模型不可用，正在重试"],
    [new RegExp("^Using browser · (.+) \\((\\d+)s\\)$"), "正在使用浏览器 · $1（$2 秒）"],
    [new RegExp("^Using browser \\((\\d+)s\\)$"), "正在使用浏览器（$1 秒）"],
    [new RegExp("^Using browser · (.+)$"), "正在使用浏览器 · $1"],
    [new RegExp("^Waiting for (\\d+) timers$"), "正在等待 $1 个计时器"],
    [new RegExp("^(\\d+) blocked$"), "$1 个已阻塞"],
    [new RegExp("^Searched for \"(.+)\"$"), "已搜索 \"$1\""],
    [new RegExp("^Searched for files: (.+)$"), "已搜索文件：$1"],
    [new RegExp("^Code search: \"(.+)\"$"), "代码搜索：\"$1\""],
    [new RegExp("^Internal search: \"(.+)\"$"), "内部搜索：\"$1\""],
    [new RegExp("^Listed directory (.+)$"), "已列出目录 $1"],
    [new RegExp("^Browser task: \"(.+)\"$"), "浏览器任务：\"$1\""],
    [new RegExp("^Opened browser: (.+)$"), "已打开浏览器：$1"],
    [new RegExp("^Read URL: (.+)$"), "已读取 URL：$1"],
    [new RegExp("^Searched web: \"(.+)\"$"), "已搜索网络：\"$1\""],
    [new RegExp("^Invoked subagent: (.+)$"), "已调用子智能体：$1"],
    [new RegExp("^Error (\\d+)$"), "错误 $1"],
    [new RegExp("^(.+) \\(Error ID: (.+)\\)$"), "$1（错误 ID：$2）"],
    [new RegExp("^Used MCP tool: (.+)$"), "已使用 MCP 工具：$1"],
    [new RegExp("^Generated image: \"(.+)\"$"), "已生成图像：\"$1\""],
    [new RegExp("^Used tool: (.+)$"), "已使用工具：$1"],
    [new RegExp("^Side question \\(conversation (.+?)\\): (.+)$"), "旁支提问（对话 $1）：$2"],
    [new RegExp("^Turn: ([^/]+)/(.+)$"), "本轮：$1/$2"],
    [new RegExp("^Tot: ([^/]+)/(.+)$"), "总计：$1/$2"],
    [new RegExp("^Cost summary: (.+)$"), "费用摘要：$1"],
    [new RegExp("^Review permissions for (.+)$"), "审阅 $1 的权限"],
    [new RegExp("^On top of those defaults, (.+) requests the access below\\.$"), "除上述默认设置外，$1 还请求以下访问权限。"],
    [new RegExp("^Enabled \"(.+)\"\\.$"), "已启用“$1”。"],
    [new RegExp("^Agents created by this (.+?) run in a dedicated (.+?) with its own permissions\\. You can change the permissions in the (.+?) settings page\\.$"), "由此 $1 创建的智能体将在专用的 $2 中运行并拥有独立权限。您可以在 $3 设置页面中更改权限。"],
    [new RegExp("^Started \"(.+)\"\\.$"), "已启动“$1”。"],
    [new RegExp("^(\\d{1,2}):00 PM$"), "下午 $1:00"],
    [new RegExp("^(\\d{1,2}):00 AM$"), "上午 $1:00"],
    [new RegExp("^Restarted \"(.+)\"\\.$"), "已重启“$1”。"],
    [new RegExp("^\\+(\\d+) more$"), "还有 $1 项"],
    [new RegExp("^Sort and filter conversations \\((\\d+) active\\)$"), "排序和筛选对话（已启用 $1 项）"],
    [new RegExp("^Marked (\\d+) conversations as read$"), "已将 $1 个对话标记为已读"],
    [new RegExp("^Help us improve (.+)\\.$"), "帮助我们改进 $1。"],
    [new RegExp("^Showing first (\\d+) references$"), "显示前 $1 个引用"],
    [new RegExp("^Unfold lines (\\d+)-(\\d+)$"), "展开第 $1-$2 行"],
    [new RegExp("^Fold lines (\\d+)-(\\d+)$"), "折叠第 $1-$2 行"],
    [new RegExp("^Edit comment: (.+)$"), "编辑评论：$1"],
    [new RegExp("^Artifact image (.+)$"), "产物图片 $1"],
    [new RegExp("^Proceed with implementation plan and (\\d+) comments?$"), "附带 $1 条评论继续执行实施计划"],
    [new RegExp("^Show (\\d+) more subagents?$"), "再显示 $1 个子智能体"],
    [new RegExp("^Plan, (\\d+) of (\\d+) steps done$"), "计划，已完成 $1/$2 步"],
    [new RegExp("^(\\d+)/(\\d+) steps$"), "$1/$2 步"],
    [new RegExp("^(\\d+) failed$"), "$1 项失败"],
    [new RegExp("^(\\d+) skipped$"), "$1 项已跳过"],
    [new RegExp("^@(.+?) is currently unavailable$"), "@$1 当前不可用"],
    [new RegExp("^Sign in to (.+)$"), "登录 $1"],
    [new RegExp("^Column (\\d+)$"), "第 $1 列"],
    [new RegExp("^(\\d+) rows$"), "$1 行"],
    [new RegExp("^Image: (.+)$"), "图像：$1"],
    [new RegExp("^Disable Word Wrap(.*)$"), "禁用自动换行$1"],
    [new RegExp("^Enable Word Wrap(.*)$"), "启用自动换行$1"],
    [new RegExp("^Toggle Word Wrap(.*)$"), "切换自动换行$1"],
    [new RegExp("^Preview unavailable — (.+)$"), "预览不可用 — $1"],
    [new RegExp("^Work locally on (.+)$"), "在本地 $1 上工作"],
    [new RegExp("^Worktree from (.+)$"), "来自 $1 的工作树"],
    [new RegExp("^(.+?), and reuse (.+)$"), "$1，并复用 $2"],
    [new RegExp("^(\\d+) models selected$"), "已选择 $1 个模型"],
    [new RegExp("^Environment: (.+)$"), "环境：$1"],
    [new RegExp("^System default \\((.+)\\)$"), "系统默认（$1）"],
    [new RegExp("^No audio from (.+)$"), "未检测到来自 $1 的音频"],
    [new RegExp("^(.+)\\. Switch microphone\\.$"), "$1。切换麦克风。"],
    [new RegExp("^(.+)\\. Switch mic$"), "$1。切换麦克风"],
    [new RegExp("^Send Message (.+)$"), "发送消息 $1"],
    [new RegExp("^\\+(\\d+) attachments$"), "+$1 个附件"],
    [new RegExp("^(\\d+) attachment\\(s\\)$"), "$1 个附件"],
    [new RegExp("^Edit: (.+)$"), "编辑：$1"],
    [new RegExp("^Delete: (.+)$"), "删除：$1"],
    [new RegExp("^Send now: (.+)$"), "立即发送：$1"],
    [new RegExp("^(\\d+) comments$"), "$1 条评论"],
    [new RegExp("^Attachment error: (.+)$"), "附件错误：$1"],
    [new RegExp("^Upload error: (.+)$"), "上传错误：$1"],
    [new RegExp("^MCP error: (.+)$"), "MCP 错误：$1"],
    [new RegExp("^Retrying transcription \\(attempt (\\d+)\\)…$"), "正在重试转录（第 $1 次尝试）…"],
    [new RegExp("^Welcome to (.+)!$"), "欢迎使用 $1！"],
    [new RegExp("^Sorry, this account is ineligible to use (.+)$"), "抱歉，此账号不符合使用 $1 的条件"],
    [new RegExp("^Further action is required to use (.+)$"), "需要进一步操作才能使用 $1"],
    [new RegExp("^Hey (.+)!$"), "您好，$1！"],
    [new RegExp("^Select (.+) Theme$"), "选择 $1 主题"],
    [new RegExp("^Added (.+?) and installed (.+)\\.$"), "已添加 $1 并安装 $2。"],
    [new RegExp("^(.+?)\\. Disabling or removing the bundle applies only to the ones it installed\\.$"), "$1。禁用或移除该插件包仅影响通过它安装的插件。"],
    [new RegExp("^Add bundle (.+)$"), "添加插件包 $1"],
    [new RegExp("^Adding plugins from (.+)$"), "正在添加来自 $1 的插件"],
    [new RegExp("^This plugin in (.+?) may have looser code review\\. Review its contents before adding the bundle\\.$"), "$1 中的此插件可能经过了较为宽松的代码审阅。请在添加插件包前审阅其内容。"],
    [new RegExp("^These plugins in (.+?) may have looser code review\\. Review their contents before adding the bundle\\.$"), "$1 中的这些插件可能经过了较为宽松的代码审阅。请在添加插件包前审阅其内容。"],
    [new RegExp("^More actions for (.+)$"), "$1 的更多操作"],
    [new RegExp("^Credentials expire in (.+?)\\. Refresh credentials to keep this automation running$"), "凭据将在 $1 后过期。请刷新凭据以保持此自动化运行"],
    [new RegExp("^Deleted \"(.+)\"\\.$"), "已删除“$1”。"],
    [new RegExp("^Run (.+?) now$"), "立即运行 $1"],
    [new RegExp("^No MCP servers found for \"(.+)\"$"), "未找到与“$1”匹配的 MCP 服务器"],
    [new RegExp("^See (\\d+) more (.+)$"), "再查看 $1 个 $2"],
    [new RegExp("^See more in (.+)$"), "在 $1 中查看更多"],
    [new RegExp("^See less in (.+)$"), "在 $1 中收起"],
    [new RegExp("^Filter skills and rules: (.+)$"), "筛选技能和规则：$1"],
    [new RegExp("^Error updating agent: (.+)$"), "更新智能体时出错：$1"],
    [new RegExp("^Search for \"(.+)\" in the Marketplace$"), "在插件市场中搜索“$1”"],
    [new RegExp("^No plugins found for \"(.+)\"\\.$"), "未找到与“$1”匹配的插件。"],
    [new RegExp("^(.+?) installed$"), "已安装 $1"],
    [new RegExp("^Blocked: (.+)$"), "已阻止：$1"],
    [new RegExp("^Details for (.+)$"), "$1 的详情"],
    [new RegExp("^Plugins in (.+)$"), "$1 中的插件"],
    [new RegExp("^No apps found for \"(.+)\"\\.$"), "未找到与“$1”相关的应用。"],
    [new RegExp("^Delete side question: (.+)$"), "删除旁支提问：$1"],
    [new RegExp("^You have (\\d+) conversations in progress\\. Updating will interrupt them, and they will automatically resume once the update completes\\.$"), "您有 $1 个对话正在进行中。更新将会中断这些对话，并在更新完成后自动恢复。"],
    [new RegExp("^You have (\\d+) conversations in progress\\. Updating will cancel them and you'll need to manually restart them\\.$"), "您有 $1 个对话正在进行中。更新将会取消这些对话，您需要手动重新启动它们。"],
    [new RegExp("^Switch environment \\((.+)\\)$"), "切换环境（$1）"],
    [new RegExp("^Load older messages, showing (\\d+) of (\\d+)$"), "加载更早的消息，已显示 $1 / $2 条"],
    [new RegExp("^No more older messages, showing (\\d+) of (\\d+)$"), "没有更多历史消息，已显示 $1 / $2 条"],
    [new RegExp("^Turn (\\d+)$"), "第 $1 轮"],
    [new RegExp("^Turns (\\d+)–(\\d+)$"), "第 $1–$2 轮"],
    [new RegExp("^(\\d+) turns?$"), "$1 轮"],
    [new RegExp("^Go to turn (\\d+) of (\\d+)$"), "跳转到第 $1 / $2 轮"],
    [new RegExp("^(\\d+) Files? With Changes$"), "$1 个已更改的文件"],
    [new RegExp("^Requesting permission to (.+)$"), "正在请求权限：$1"],
    [new RegExp("^Yes, allow downloads from (.+) for this run$"), "是的，在此次运行中允许从 $1 下载"],
    [new RegExp("^Conflicts with your configured Ask permission: (.+)$"), "与您配置的询问权限冲突：$1"],
    [new RegExp("^Requires manual confirmation: (.+)$"), "需要手动确认：$1"],
    [new RegExp("^Hey (.+?), what should we build today\\?$"), "你好，$1，今天我们来构建点什么？"],
    [new RegExp("^Welcome back, (.+?)\\. Where should we pick up\\?$"), "欢迎回来，$1。我们从哪里继续？"],
    [new RegExp("^Good to see you, (.+?)\\. What's next\\?$"), "很高兴见到您，$1。接下来做什么？"],
    [new RegExp("^Select model with (.+)$"), "使用 $1 选择模型"],
    [new RegExp("^Error: (.+)$"), "错误：$1"],
    [new RegExp("^Moved conversation (.+)$"), "已移动对话 $1"],
    [new RegExp("^Managed by the (.+) automation$"), "由 $1 自动化管理"],
    [new RegExp("^Managed by the (.+) plugin$"), "由 $1 插件管理"],
    [new RegExp("^(.+) \\(Archived\\)$"), "$1（已归档）"],
    [new RegExp("^(.+)\\. Show in (.+)$"), "$1。在 $2 中显示"],
    [new RegExp("^Side Question: (.+)$"), "旁支提问：$1"],
    [new RegExp("^Edit side question title: (.+)$"), "编辑旁支提问标题：$1"],
    [new RegExp("^(.+) header$"), "$1 标题栏"],
    [new RegExp("^Aux pane (.+)$"), "辅助窗格 $1"],
    [new RegExp("^Search Google for \"(.+)\"$"), "在 Google 中搜索“$1”"],
    [new RegExp("^(.+) tab$"), "$1 标签页"],
    [new RegExp("^Every (\\d+) minutes(.*)$"), "每 $1 分钟$2"],
    [new RegExp("^Every (\\d+) hours(.*)$"), "每 $1 小时$2"],
    [new RegExp("^Monthly on the (.+?) at (.+)$"), "每月 $1 $2"],
    [new RegExp("^Daily at (.+)$"), "每天 $1"],
    [new RegExp("^Keep: (.+)$"), "保留：$1"],
    [new RegExp("^(.+?) is no longer available\\. Runs use (.+?) instead\\.$"), "$1 已不再可用。运行将改用 $2。"],
    [new RegExp("^(.+?) is no longer available\\. Runs will fail until you pick another model\\.$"), "$1 已不再可用。在您选择其他模型之前，运行将会失败。"],
    [new RegExp("^(.+) \\(unavailable\\)$"), "$1（不可用）"],
    [new RegExp("^(.+) \\(latest\\)$"), "$1（最新）"],
    [new RegExp("^(.+) · This computer$"), "$1 · 此电脑"],
    [new RegExp("^Failed: (.+)$"), "失败：$1"],
    [new RegExp("^Agent: (.+)$"), "智能体：$1"],
    [new RegExp("^Hidden by policy \\((.+)\\)\\.$"), "已根据策略隐藏（$1）。"],
    [new RegExp("^Low contrast ratio \\(([\\d.]+):1\\)\\. Text may be hard to read\\.$"), "对比度过低（$1:1），文本可能难以辨认。"],
    [new RegExp("^Web app: (.+)$"), "Web 应用：$1"],
    [new RegExp("^Language server: (.+)$"), "语言服务器：$1"],
    [new RegExp("^Release channel: (.+)$"), "发布渠道：$1"],
    [new RegExp("^Committed to (.+)\\.$"), "已提交至 $1。"],
    [new RegExp("^Push (\\d+) commits? to (.+)$"), "推送 $1 个提交至 $2"],
    [new RegExp("^Publish (.+) to origin$"), "将 $1 发布到 origin"],
    [new RegExp("^Pushed (\\d+) commits? to (.+)\\.$"), "已推送 $1 个提交至 $2。"],
    [new RegExp("^Pushed to (.+)\\.$"), "已推送至 $1。"],
    [new RegExp("^Published (.+) to origin\\.$"), "已将 $1 发布到 origin。"],
    [new RegExp("^All changes since (.+)$"), "自 $1 以来的所有更改"],
  ];
  const v233UiControlRegexRules = [
    [new RegExp("^Opening (.+)$"), "正在打开 $1"],
    [new RegExp("^Pressing (.+)$"), "正在按下 $1"],
    [new RegExp("^Toggle (.+)$"), "切换 $1"],
    [new RegExp("^Configure (.+)$"), "配置 $1"],
    [new RegExp("^Connect (.+)$"), "连接 $1"],
    [new RegExp("^Hid (.+)$"), "已隐藏 $1"],
    [new RegExp("^Waiting for (.+)$"), "正在等待 $1"],
    [new RegExp("^Created (.+)$"), "已创建 $1"],
    [new RegExp("^Deleted (.+)$"), "已删除 $1"],
    [new RegExp("^Edited (.+)$"), "已编辑 $1"],
    [new RegExp("^Viewed (.+)$"), "已查看 $1"],
    [new RegExp("^Set up (.+)$"), "设置 $1"],
    [new RegExp("^Copy (?!of )(.+)$"), "复制 $1"],
    [new RegExp("^Creating (.+)$"), "正在创建 $1"],
    [new RegExp("^Running (.+)$"), "正在运行 $1"],
    [new RegExp("^Explored (.+)$"), "已探索 $1"],
    [new RegExp("^Reconnect (.+)$"), "重新连接 $1"],
    [new RegExp("^Remove (.+)$"), "移除 $1"],
    [new RegExp("^Using (.+)$"), "正在使用 $1"],
    [new RegExp("^View (.+)$"), "查看 $1"],
    [new RegExp("^Added (.+)\\.$"), "已添加 $1。"],
    [new RegExp("^Removed (.+)\\.$"), "已移除 $1。"],
    [new RegExp("^Enable (.+)$"), "启用 $1"],
    [new RegExp("^See more (.+)$"), "查看更多 $1"],
    [new RegExp("^Adding (.+)$"), "正在添加 $1"],
    [new RegExp("^Add (.+)$"), "添加 $1"],
    [new RegExp("^Disconnect (.+)$"), "断开与 $1 的连接"],
    [new RegExp("^Close (.+)$"), "关闭 $1"],
    [new RegExp("^Unpin (.+)$"), "取消置顶 $1"],
    [new RegExp("^Back to (.+)$"), "返回 $1"],
    [new RegExp("^Today (.+)$"), "今天 $1"],
    [new RegExp("^Tomorrow (.+)$"), "明天 $1"],
    [new RegExp("^Yesterday (.+)$"), "昨天 $1"],
    [new RegExp("^(.+?) \\((\\d+) image attachments?\\)$"), "$1（$2 张图片附件）"],
  ];

  function translateText(text, isUiControl) {
    if (!text || typeof text !== 'string') return text;
    let trimmed = text.trim();
    if (!trimmed) return text;

    if (dictionary[trimmed]) {
      return text.replace(trimmed, dictionary[trimmed]);
    }
    const normalized = trimmed.replace(/[\u200B-\u200D\uFEFF]/g, '').replace(/[\u00A0\s]+/g, ' ').trim();
    if (normalized !== trimmed && dictionary[normalized]) {
      return text.replace(trimmed, dictionary[normalized]);
    }
    
    // Dynamic Regex Translations
    let m;
    if (text.indexOf("of the customization budget is available") !== -1) {
      text = text.replace(/(\d+(?:\.\d+)?)% of the customization budget is available\.?/g, "自定义项预算可用额度为 $1%。");
      text = text.replace(/%\s*of the customization budget is available\.?/g, "% 的自定义项预算可用额度。");
      text = text.replace(/(^\s*)of the customization budget is available\.?/g, "$1的自定义项预算可用额度。");
    }
    if ((m = trimmed.match(/^Show (\d+) breakdowns?$/))) {
      return text.replace(trimmed, "显示 " + m[1] + " 项明细");
    }
    if ((m = trimmed.match(/^Explored (\d+) files? >$/))) {
      return text.replace(trimmed, "已浏览 " + m[1] + " 个文件 >");
    }
    if ((m = trimmed.match(/^Editing (.+) \+(\d+) -(\d+)$/))) {
      return text.replace(trimmed, "正在编辑 " + m[1] + " +" + m[2] + " -" + m[3]);
    }
    if (trimmed === "Waiting for user input") {
      return text.replace(trimmed, "等待用户输入");
    }
    if ((m = trimmed.match(/^Artifacts?\s*(\d+)$/i))) {
      return text.replace(trimmed, "产物 " + m[1]);
    }
    if ((m = trimmed.match(/^No artifacts generated\.?$/i))) {
      return text.replace(trimmed, "未生成任何产物");
    }
    if (/(?:No|否)\s*(?:projects?|项目)?\s*found/i.test(text) || text.indexOf("No projects found") !== -1 || text.indexOf("No project found") !== -1) {
      return text.replace(/(?:No|否)\s*(?:projects?|项目)?\s*found\.?|No projects found\.?|No project found\.?/gi, "暂无项目");
    }
    if ((m = trimmed.match(/^(?:No|否)\s*projects?\s*found\.?$/i))) {
      return text.replace(trimmed, "暂无项目");
    }
    if ((m = trimmed.match(/^No\s+Project$/i))) {
      return text.replace(trimmed, "无项目");
    }
    if (trimmed === "Type") return text.replace(trimmed, "输入");
    if (trimmed === "and select") return text.replace(trimmed, "并选择");
    if (trimmed === "to have the agent generate a plan." || trimmed === "to have the agent generate a plan") {
      return text.replace(trimmed, "即可让智能体生成计划。");
    }
    if (trimmed === "Visit") return text.replace(trimmed, "访问");
    if (trimmed === "Legal Help") return text.replace(trimmed, "法律帮助");
    if (trimmed === "to ask for content changes for legal reasons." || trimmed === "to ask for content changes for legal reasons") {
      return text.replace(trimmed, "以出于法律原因请求更改内容。");
    }
    if ((m = trimmed.match(/^Learn more about (.+)$/))) {
      return text.replace(trimmed, "了解更多关于 " + (dictionary[m[1]] || m[1]) + " 的信息");
    }
    if ((m = trimmed.match(/^You have used some of your weekly limit, it will fully refresh in (.*)\.$/))) {
      let timeStr = m[1].replace(/days?/g, "天").replace(/hours?/g, "小时").replace(/minutes?/g, "分钟").replace(/,/g, "");
      return text.replace(trimmed, "您已使用部分每周限额，它将在 " + timeStr + " 后完全重置。");
    }
    if ((m = trimmed.match(/^You have used some of your 5-hour limit, it will fully refresh in (.*)\.$/))) {
      let timeStr = m[1].replace(/days?/g, "天").replace(/hours?/g, "小时").replace(/minutes?/g, "分钟").replace(/,/g, "");
      return text.replace(trimmed, "您已使用部分五小时限额，它将在 " + timeStr + " 后完全重置。");
    }
    if ((m = trimmed.match(/^You have hit your (5-hour|weekly) limit, so the (?:5-hour|weekly) limit does not currently apply\. Your (?:5-hour|weekly) limit will refresh in (.*)\.$/))) {
      let limitName = m[1] === "5-hour" ? "五小时限额" : "每周限额";
      let otherName = m[1] === "5-hour" ? "每周限额" : "五小时限额";
      let timeStr = m[2].replace(/days?/g, "天").replace(/hours?/g, "小时").replace(/minutes?/g, "分钟").replace(/,/g, "");
      return text.replace(trimmed, "您已达到" + limitName + "上限，因此当前不适用" + otherName + "。您的" + limitName + "将在 " + timeStr + " 后重置。");
    }
    if ((m = trimmed.match(/^You have hit your (5-hour|weekly) limit, it will refresh in (.*?)\. If on a supported paid plan, you can use AI credits in the interim\.$/))) {
      let limitName = m[1] === "5-hour" ? "五小时限额" : "每周限额";
      let timeStr = m[2].replace(/days?/g, "天").replace(/hours?/g, "小时").replace(/minutes?/g, "分钟").replace(/,/g, "");
      return text.replace(trimmed, "您已达到" + limitName + "上限，它将在 " + timeStr + " 后重置。如果您使用的是受支持的付费套餐，在此期间可以使用 AI 积分。");
    }
    if ((m = trimmed.match(/^You have hit your (5-hour|weekly) limit, it will refresh in (.*)\.$/))) {
      let limitName = m[1] === "5-hour" ? "五小时限额" : "每周限额";
      let timeStr = m[2].replace(/days?/g, "天").replace(/hours?/g, "小时").replace(/minutes?/g, "分钟").replace(/,/g, "");
      return text.replace(trimmed, "您已达到" + limitName + "上限，它将在 " + timeStr + " 后重置。");
    }
    if ((m = trimmed.match(/^Resets? in\s+(.+)$/i))) {
      let timeStr = m[1]
        .replace(/(\d+)\s*d(?:ays?)?/gi, "$1天 ")
        .replace(/(\d+)\s*h(?:ours?)?/gi, "$1小时 ")
        .replace(/(\d+)\s*m(?:inutes?|ins?)?/gi, "$1分钟 ")
        .replace(/(\d+)\s*s(?:econds?|ecs?)?/gi, "$1秒 ")
        .replace(/,\s*/g, " ")
        .trim();
      return text.replace(trimmed, "将在 " + timeStr + " 后重置");
    }
    if (/^Exploring\b/i.test(trimmed) || /running command/i.test(trimmed)) {
      let translatedActions = trimmed
        .replace(/Exploring file/gi, "浏览文件")
        .replace(/running command/gi, "运行命令")
        .replace(/editing file/gi, "编辑文件")
        .replace(/,\s*/g, "、");
      return text.replace(trimmed, translatedActions);
    }
    if (/^(?:Explored|Ran|Edited)\b/i.test(trimmed) && (/(?:files?|artifacts?|commands?)/i.test(trimmed) || trimmed.indexOf(",") !== -1)) {
      let translatedSummary = trimmed
        .replace(/Explored files?/gi, "已浏览文件")
        .replace(/Explored artifacts?/gi, "已浏览产物")
        .replace(/Explored/gi, "已浏览")
        .replace(/Ran commands?/gi, "已运行命令")
        .replace(/Edited files?/gi, "已编辑文件")
        .replace(/Edited artifacts?/gi, "已编辑产物")
        .replace(/,\s*/g, "、");
      return text.replace(trimmed, translatedSummary);
    }
    if ((m = trimmed.match(/^Reading\s+(.+)$/))) {
      return text.replace(trimmed, "正在读取 " + m[1]);
    }
    if ((m = trimmed.match(/^Listing\s+(.+)$/))) {
      return text.replace(trimmed, "正在列出 " + m[1]);
    }
    if ((m = trimmed.match(/^Searching\s+(.+)$/))) {
      return text.replace(trimmed, "正在搜索 " + m[1]);
    }
    if ((m = trimmed.match(/^Editing\s+(.+)$/))) {
      return text.replace(trimmed, "正在编辑 " + m[1]);
    }
    if ((m = trimmed.match(/^(.*?)\s+-\s+Exited with code\s+(-?\d+)(.*)$/i))) {
      return text.replace(trimmed, m[1] + " - 退出代码 " + m[2] + m[3]);
    }
    if ((m = trimmed.match(/^Exited with code\s+(-?\d+)\.?$/i))) {
      return text.replace(trimmed, "退出代码 " + m[1]);
    }
    if ((m = trimmed.match(/^Use\s+([A-Z][a-z]+)$/))) {
      return text.replace(trimmed, "应用 " + m[1]);
    }
    if ((m = trimmed.match(/^Files? Changed\s*(\d+)$/i))) return text.replace(trimmed, "已修改文件 " + m[1]);
    if ((m = trimmed.match(/^Uploads?\s*(\d+)$/i))) return text.replace(trimmed, "已上传文件 " + m[1]);
    if ((m = trimmed.match(/^See all\s*\((.+?)\)$/i))) return text.replace(trimmed, "查看全部 (" + m[1] + ")");
    if ((m = trimmed.match(/^Background Tasks?\s*(\d+)$/i))) return text.replace(trimmed, "后台任务 " + m[1]);
    if ((m = trimmed.match(/^Terminals?\s*(\d+)$/i))) return text.replace(trimmed, "终端 " + m[1]);
    if ((m = trimmed.match(/^No subagents?(?:\s*running)?\.?$/i))) return text.replace(trimmed, "暂无子智能体");
    if ((m = trimmed.match(/^Available AI Credits: ([\d,]+)$/))) {
      return text.replace(trimmed, "可用 AI 积分: " + m[1]);
    }
    if ((m = trimmed.match(/^Send feedback as (.+)$/))) {
      return text.replace(trimmed, "以 " + m[1] + " 的身份发送反馈");
    }
    if ((m = trimmed.match(/^(\+?\d+) more lines$/))) {
      return text.replace(trimmed, "更多 " + m[1] + " 行");
    }
    if ((m = trimmed.match(/^(\d+) files? changed$/))) {
      return text.replace(trimmed, m[1] + " 个文件已修改");
    }
    if ((m = trimmed.match(/^See (\d+) more$/i))) return text.replace(trimmed, "查看更多 " + m[1] + " 项");
    if ((m = trimmed.match(/^Last (\d+) days?$/i))) return text.replace(trimmed, "最近 " + m[1] + " 天");
    if ((m = trimmed.match(/^Last (\d+) hours?$/i))) return text.replace(trimmed, "最近 " + m[1] + " 小时");
    if ((m = trimmed.match(/^Last (\d+) months?$/i))) return text.replace(trimmed, "最近 " + m[1] + " 个月");
    if ((m = trimmed.match(/^Version ([\d\.]+(-\w+)?)$/))) {
      return text.replace(trimmed, "版本 v" + m[1]);
    }
    if ((m = trimmed.match(/^Start using (.+?), our best (.+?) model\.?$/i))) {
      return text.replace(trimmed, "开始使用 " + m[1] + "，我们最强大的 " + m[2] + " 模型。");
    }
    if (text.indexOf("is now available on paid Pro and Ultra plans") !== -1 || text.indexOf("Third-party model access will no longer be available") !== -1) {
      return "Sonnet 5.5 现已在付费的 Pro 和 Ultra 方案中提供。从 2026 年 11 月 2 日起，您当前的方案将不再支持访问第三方模型。";
    }
    if ((m = trimmed.match(/^(.+?)\s+will be removed from\s+(.+?)\s+on\s+(.+?)\.?$/i))) {
      const monthMap = {
        january: "1", february: "2", march: "3", april: "4", may: "5", june: "6",
        july: "7", august: "8", september: "9", october: "10", november: "11", december: "12"
      };
      let dateStr = m[3];
      const dm = dateStr.match(/^([A-Za-z]+)\s+(\d{1,2}),?\s*(\d{4})$/);
      if (dm && monthMap[dm[1].toLowerCase()]) {
        dateStr = dm[3] + " 年 " + monthMap[dm[1].toLowerCase()] + " 月 " + dm[2] + " 日";
      }
      return text.replace(trimmed, m[1] + " 将于 " + dateStr + "从 " + m[2] + " 中移除。");
    }
    if ((m = trimmed.match(/^Hi\s+(.+?),\s*what can we get done today\?$/i))) {
      return text.replace(trimmed, "你好 " + m[1] + "，今天想完成什么工作？");
    }
    if ((m = trimmed.match(/^(.+?)\s+(Weekly|Daily|Monthly|Five Hour|5-Hour|5h|Hourly)\s+Limit(?:\s+(Remaining))?$/i))) {
      const periodMap = {
        "weekly": "每周限额",
        "daily": "每日限额",
        "monthly": "每月限额",
        "five hour": "五小时限额",
        "5-hour": "五小时限额",
        "5h": "五小时限额",
        "hourly": "每小时限额"
      };
      const periodStr = periodMap[m[2].toLowerCase()] || (m[2] + " 限额");
      const remStr = m[3] ? "剩余" : "";
      return text.replace(trimmed, m[1] + " " + periodStr + remStr);
    }
    if ((m = trimmed.match(/^(\d+)\s*([smhd])\s+limit$/i))) {
      const unitMap = { s: "秒", m: "分钟", h: "小时", d: "天" };
      const limitStr = (m[1] === "5" && m[2].toLowerCase() === "h")
        ? "五小时限额"
        : (m[1] + " " + (unitMap[m[2].toLowerCase()] || m[2]) + "限额");
      return text.replace(trimmed, limitStr);
    }
    if ((m = trimmed.match(/^(\d+(?:\.\d+)?)%\s*left$/i))) {
      return text.replace(trimmed, m[1] + "% 剩余");
    }
    if ((m = trimmed.match(/^(.+?)\s*\((Low|Medium|High|XHigh|Extra|Max)(?:\s+(Thinking))?\)$/i))) {
      const effortMap = { low: "低", medium: "中", high: "高", xhigh: "超高", extra: "超高", max: "最高" };
      const effortStr = effortMap[m[2].toLowerCase()] || m[2];
      return text.replace(trimmed, m[1] + " (" + effortStr + (m[3] ? "·思考" : "") + ")");
    }
    if ((m = trimmed.match(/^Your quota for (.+?) will reset on (.+?)\. Switch to another available model to continue\.$/i))) {
      return text.replace(trimmed, "您的 " + m[1] + " 配额将于 " + m[2] + " 重置。请切换至其他可用模型以继续。");
    }
    if ((m = trimmed.match(/^Your quota for (.+?) has been reached\. Switch to another available model to continue\.$/i))) {
      return text.replace(trimmed, "您的 " + m[1] + " 配额已用尽。请切换至其他可用模型以继续。");
    }
    // v2.29.0 Dynamic Permission Prompts & Rules
    if ((m = trimmed.match(/^Yes, save rule for '(.+)' in this conversation$/))) {
      return text.replace(trimmed, "是，在本次对话中保存 '" + m[1] + "' 的规则");
    }
    if ((m = trimmed.match(/^Yes, save rule for '(.+)' globally$/))) {
      return text.replace(trimmed, "是，全局保存 '" + m[1] + "' 的规则");
    }
    if ((m = trimmed.match(/^Yes, (?:and always )?allow '?(.+?)'? in this conversation$/))) {
      return text.replace(trimmed, "是，在本次对话中始终允许 '" + m[1] + "'");
    }
    if ((m = trimmed.match(/^Yes, (?:and )?always allow '?(.+?)'?$/))) {
      return text.replace(trimmed, "是，始终允许 '" + m[1] + "'");
    }
    if ((m = trimmed.match(/^Allow (.+)\?$/))) {
      return text.replace(trimmed, "允许 " + m[1] + " 吗？");
    }
    if ((m = trimmed.match(/^Save rule to always allow (.+)\?$/))) {
      return text.replace(trimmed, "保存规则以始终允许 " + m[1] + " 吗？");
    }
    // v2.29.0 Dynamic Settings, Context, Tools & Status Patterns
    if ((m = trimmed.match(/^(Enter|\u23ce|Alt\+Enter|\u2325\u23ce)\s+(Sends immediately|Queues after the turn|On empty prompt, sends next in queue)$/))) {
      const actionMap = {
        "Sends immediately": "立即发送",
        "Queues after the turn": "在当前轮次后排队",
        "On empty prompt, sends next in queue": "在输入为空时，发送队列中的下一条"
      };
      return text.replace(trimmed, m[1] + " 键：" + (actionMap[m[2]] || m[2]));
    }
    if ((m = trimmed.match(/^Context window (?:about )?(\d+)% full(.*)$/i))) {
      return text.replace(trimmed, "上下文窗口已使用约 " + m[1] + "%" + m[2]);
    }
    if ((m = trimmed.match(/^(\d+)% of the context window used$/i))) {
      return text.replace(trimmed, "已使用 " + m[1] + "% 的上下文窗口");
    }
    if ((m = trimmed.match(/^Thinking for (\d+)s$/i)) || (m = trimmed.match(/^Still thinking, (\d+) seconds$/i))) {
      return text.replace(trimmed, "已思考 " + m[1] + " 秒");
    }
    if ((m = trimmed.match(/^(\d+) tools? (enabled|disabled|excluded)$/i))) {
      const stateMap = { enabled: "已启用", disabled: "已禁用", excluded: "已排除" };
      return text.replace(trimmed, m[1] + " 个工具" + (stateMap[m[2].toLowerCase()] || m[2]));
    }
    if ((m = trimmed.match(/^(\d+) tools?$/i))) {
      return text.replace(trimmed, m[1] + " 个工具");
    }
    if ((m = trimmed.match(/^Build with (.+) Plugins$/i))) {
      return text.replace(trimmed, "使用 " + m[1] + " 插件构建");
    }
    if ((m = trimmed.match(/^(\d+) (subagents?|tasks?|subagents\/tasks) (running|blocked)$/i))) {
      const unitMap = { subagent: "个子智能体", subagents: "个子智能体", task: "个任务", tasks: "个任务", "subagents/tasks": "个子智能体/任务" };
      const statusMap = { running: "正在运行", blocked: "已阻塞" };
      return text.replace(trimmed, m[1] + " " + (unitMap[m[2].toLowerCase()] || m[2]) + (statusMap[m[3].toLowerCase()] || m[3]));
    }
    if ((m = trimmed.match(/^(\d+) Files? With Changes$/i))) {
      return text.replace(trimmed, m[1] + " 个文件有更改");
    }
    if ((m = trimmed.match(/^Turn (\d+) of (\d+)$/i))) {
      return text.replace(trimmed, "第 " + m[1] + " / " + m[2] + " 轮");
    }
    if ((m = trimmed.match(/^Question (\d+) of (\d+)$/i))) {
      return text.replace(trimmed, "第 " + m[1] + " / " + m[2] + " 个问题");
    }
    if ((m = trimmed.match(/^Step (\d+) of (\d+)$/i))) {
      return text.replace(trimmed, "第 " + m[1] + " / " + m[2] + " 步");
    }
    if ((m = trimmed.match(/^Updated (.+)$/))) {
      return text.replace(trimmed, "更新于 " + m[1]);
    }
    if ((m = trimmed.match(/^Forked from (.+)$/))) {
      return text.replace(trimmed, "分支自 " + m[1]);
    }
    if ((m = trimmed.match(/^Signed in as (.+)$/))) {
      return text.replace(trimmed, "已登录为 " + m[1]);
    }
    if ((m = trimmed.match(/^Inherits your Global Permissions when working in this (project|workspace)\.?$/i))) {
      return text.replace(trimmed, "在此" + (m[1].toLowerCase() === "workspace" ? "工作区" : "项目") + "中工作时继承您的全局权限。");
    }
    if ((m = trimmed.match(/^Manage (project|workspace) (resources|folders)(?:, agent settings, and permissions| and settings)\.?$/i))) {
      return text.replace(trimmed, "管理" + (m[1].toLowerCase() === "workspace" ? "工作区" : "项目") + "文件夹、智能体设置和权限。");
    }
    if ((m = trimmed.match(/^(\d+)\s*s(?:\s*ago)?$/i))) return text.replace(trimmed, m[1] + "秒前");
    if ((m = trimmed.match(/^(\d+)\s*m(?:\s*ago)?$/i))) return text.replace(trimmed, m[1] + "分钟前");
    if ((m = trimmed.match(/^(\d+)\s*h(?:\s*ago)?$/i))) return text.replace(trimmed, m[1] + "小时前");
    if ((m = trimmed.match(/^(\d+)\s*d(?:\s*ago)?$/i))) return text.replace(trimmed, m[1] + "天前");

    // Dynamic Time Formatter
    if (text.indexOf("Worked for") !== -1) {
      return text.replace(/Worked for ([\d\.a-z ]+)/gi, function(_, timeStr) {
        let t = timeStr.replace(/ms/g, "毫秒").replace(/s/g, "秒").replace(/m/g, "分").replace(/h/g, "小时");
        return "运行耗时 " + t;
      });
    }
    if (text.indexOf("Thought for") !== -1) {
      return text.replace(/Thought for ([\d\.a-z ]+)/gi, function(_, timeStr) {
        let t = timeStr.replace(/ms/g, "毫秒").replace(/s/g, "秒").replace(/m/g, "分").replace(/h/g, "小时");
        return "思考耗时 " + t;
      });
    }
    if (text.indexOf("Working") !== -1) {
      text = text.replace(/Working(\.*)/g, "运行中$1");
    }

    // Special Multi-segment Matches
    if (text.indexOf("Google Developer Knowledge") !== -1 || text.indexOf("official developer documentation and retrieve") !== -1) {
      return "Google Developer Knowledge MCP 服务器使 AI 驱动的开发工具能够搜索 Google 的官方开发者文档并检索相关内容...";
    }
    if (text.indexOf("Ask questions. Get answers") !== -1) {
      if (text.indexOf("PostHog") !== -1) {
        return "提出问题。获取答案。该 MCP 是您的编程智能体与之对话的服务器。用英语提问，它会针对您的 PostHog 数据运行查询并返回结果。";
      }
      return "提出问题。获取答案。该 MCP 是您的 ";
    }
    if (text.indexOf("talks to. Ask a question in English") !== -1 || text.indexOf("runs the query against your") !== -1) {
      return " 与之对话的服务器。用英语提问，它会针对您的 ";
    }
    if (text.indexOf("The answer lands") !== -1 || text.indexOf("data. The answer") !== -1) {
      return " 数据运行查询并返回结果。";
    }

    if (text.indexOf("Configure the browser subagent") !== -1) {
      text = text.replace(/Configure the browser subagent\.?/g, "配置浏览器子智能体。");
    }
    if (text.indexOf("It requires") !== -1 && text.indexOf("Configure") === -1) {
      text = text.replace(/It requires\s?/g, "需要安装 ");
    }
    if (text.indexOf("to be installed.") !== -1) {
      text = text.replace(/\s?to be installed\./g, "");
    }
    if (text.indexOf("The browser subagent can be invoked by typing") !== -1) {
      text = text.replace(/The browser subagent can be invoked by typing \/browser in the conversation input box\./g, "您可以在对话输入框中输入 /browser 来调用浏览器子智能体。");
    }

    if (text.indexOf("You currently don't have any MCP Servers installed.") !== -1) {
      text = text.replace(/You currently don't have any MCP Servers installed\./g, "您目前尚未安装任何 MCP 服务器。");
    }
    if (text.indexOf("Add an MCP server above") !== -1) {
      text = text.replace(/Add an MCP server above or add a custom one via the MCP Config\./g, "请在上方添加 MCP 服务器，或通过 MCP 配置添加自定义服务器。");
    }

    // v2.33.0 Dynamic Regex Matching
    for (let i = 0; i < v233RegexRules.length; i++) {
      const rule = v233RegexRules[i];
      if (rule[0].test(trimmed)) {
        return text.replace(trimmed, trimmed.replace(rule[0], rule[1]));
      }
    }
    if (isUiControl) {
      for (let i = 0; i < v233UiControlRegexRules.length; i++) {
        const rule = v233UiControlRegexRules[i];
        if (rule[0].test(trimmed)) {
          return text.replace(trimmed, trimmed.replace(rule[0], rule[1]));
        }
      }
    }

    // Prefix Rules Matching
    for (let i = 0; i < textPrefixRules.length; i++) {
      if (text.indexOf(textPrefixRules[i][0]) !== -1) {
        return textPrefixRules[i][1];
      }
    }

    // Short Word Exact Replacement
    if (trimmed === "New") {
      return text.replace(trimmed, isUiControl ? "新建" : "新");
    }
    if (trimmed === "No" && isUiControl) {
      return text.replace(trimmed, "否");
    }
    if (trimmed === "Use" && isUiControl) {
      return text.replace(trimmed, "应用");
    }
    if (trimmed === "Quote" && isUiControl) {
      return text.replace(trimmed, "引用");
    }
    let wordsCount = trimmed.split(/\s+/).length;
    if (wordsCount <= 3) {
      let lowerText = trimmed.toLowerCase();
      if (coreWords[lowerText]) {
        return text.replace(trimmed, coreWords[lowerText]);
      }
    }
    
    return text;
  }

  function checkEmptyContainer(el) {
    if (!el || el.tagName === 'BODY' || el.tagName === 'HTML') return false;
    if (el.closest && el.closest('[data-empty-handled="true"]')) return false;
    if (el.querySelector && el.querySelector('svg, button, input')) return false;
    let t = el.textContent ? el.textContent.trim() : '';
    if (!t) return false;
    let m = t.match(/^(?:No|否)\s*(.*?)\s*(?:found|yet)\.?$/i) || t.match(/^(.*?)\s+found\.?$/i) || t === "暂无项目" || t === "暂无对话";
    if (el.__empty_handled) return false;
    if (m) {
      let target = (m[1] || '').trim().toLowerCase();
      let label = "";
      let svg = "";
      if (target === 'automations' || target === 'automation' || target === '自动化' || target === '自动化任务') {
        label = "暂无自动化任务";
        svg = '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>';
      } else if (target === 'scheduled tasks' || target === 'scheduled task' || target === '计划任务') {
        label = "暂无计划任务";
        svg = '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>';
      } else if (target === 'projects' || target === 'project' || target === '项目' || target === '' || t === '暂无项目') {
        label = "暂无项目";
        svg = '<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-1.2-1.8A2 2 0 0 0 7.55 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z"></path>';
      } else if (target === 'conversations' || target === 'conversation' || target === '对话' || t === '暂无对话') {
        label = "暂无对话";
        svg = '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>';
      } else if (target === 'results' || target === 'result' || target === '结果') {
        label = "未找到结果";
        svg = '<circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>';
      } else if (target === 'artifacts' || target === 'artifact' || target === '产物') {
        label = "暂无产物";
        svg = '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>';
      } else if (target === 'files' || target === 'file' || target === '文件') {
        label = "暂无文件";
        svg = '<path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14 2 14 8 20 8"></polyline>';
      } else if (target === 'models' || target === 'model' || target === '模型') {
        label = "暂无模型";
        svg = '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>';
      } else if (target === 'subagents' || target === 'subagent' || target === '子智能体') {
        label = "暂无子智能体";
        svg = '<rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line>';
      }
      if (label) {
        el.setAttribute('data-empty-handled', 'true');
        el.innerHTML = '<span style="display: inline-flex; align-items: center; gap: 8px; opacity: 0.6; padding: 2px 0;"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + svg + '</svg><span>' + label + '</span></span>';
        el.__empty_handled = true;
        return true;
      }
    }
    return false;
  }

  function processNode(node) {
    if (node.nodeType === Node.TEXT_NODE) {
      // Avoid modifying code snippets or editor content, while allowing UI tooltips/buttons inside <pre> wrappers
      if (node.parentElement && node.parentElement.closest) {
        if (node.parentElement.closest('code, .code-block, .monaco-editor')) {
          return;
        }
        if (node.parentElement.closest('pre') && !node.parentElement.closest('[role="tooltip"], .react-tooltip, button, [data-testid="code-block-preview-toggle"]')) {
          return;
        }
      }
      if (node.parentElement) {
        if (checkEmptyContainer(node.parentElement) ||
            (node.parentElement.parentElement && checkEmptyContainer(node.parentElement.parentElement))) {
          return;
        }
      }
      if (node.textContent && node.textContent.trim() === "at" && node.parentElement &&
          (!node.parentElement.closest || !node.parentElement.closest('p, .prose, .markdown')) &&
          node.parentElement.querySelector && node.parentElement.querySelector('button, select, [role="combobox"]')) {
        node.textContent = node.textContent.replace("at", "于");
        return;
      }
      const isUiControl = !!(node.parentElement && node.parentElement.closest &&
        node.parentElement.closest('button, [role="button"], [role="menuitem"], [role="tab"], [role="tooltip"], .react-tooltip, label, summary, nav, header'));
      let uiFlag = isUiControl;
      if (node.textContent && node.textContent.trim() === "New") {
        const ctrl = node.parentElement && node.parentElement.closest &&
          node.parentElement.closest('button, [role="button"], [role="menuitem"], [role="tab"]');
        const ctrlText = ctrl && ctrl.textContent ? ctrl.textContent.replace(/\s+/g, ' ').trim() : '';
        uiFlag = !!(ctrl && (ctrlText === 'New' || ctrlText === '+ New'));
      }
      const translated = translateText(node.textContent, uiFlag);
      if (translated !== node.textContent) {
        node.textContent = translated;
      }
    } else if (node.nodeType === Node.ELEMENT_NODE) {
      if (node.tagName === 'SCRIPT' || node.tagName === 'STYLE' || node.tagName === 'CODE') return;
      if (checkEmptyContainer(node)) return;
      translateElementAttrs(node);
      if (node.tagName === 'SPAN' && node.children && node.children.length === 0 && node.childNodes && node.childNodes.length > 1) {
        if (!node.closest || (!node.closest('code, .code-block, .monaco-editor') && (!node.closest('pre') || node.closest('[role="tooltip"], .react-tooltip, button')))) {
          const isUiCtrl = !!(node.closest && node.closest('button, [role="button"], [role="menuitem"], [role="tab"], [role="tooltip"], .react-tooltip, label, summary, nav, header'));
          const spanTranslated = translateText(node.textContent, isUiCtrl);
          if (spanTranslated !== node.textContent) {
            node.textContent = spanTranslated;
            return;
          }
        }
      }
      // Recursively process child nodes
      Array.from(node.childNodes).forEach(processNode);
    }
  }

  function translateElementAttrs(node) {
    if (!node || node.nodeType !== Node.ELEMENT_NODE) return;
    if (node.placeholder) {
      const translated = translateText(node.placeholder, true);
      if (translated !== node.placeholder) {
        node.placeholder = translated;
      }
    }
    if (node.title) {
      const translated = translateText(node.title, true);
      if (translated !== node.title) {
        node.title = translated;
      }
    }
    if (node.getAttribute) {
      const attrs = ['aria-label', 'aria-placeholder', 'data-slot-out'];
      for (let i = 0; i < attrs.length; i++) {
        const val = node.getAttribute(attrs[i]);
        if (val) {
          const translated = translateText(val, true);
          if (translated !== val) {
            node.setAttribute(attrs[i], translated);
          }
        }
      }
    }
  }

  const observer = new MutationObserver((mutations) => {
    mutations.forEach(mutation => {
      if (mutation.type === 'childList') {
        mutation.addedNodes.forEach(node => {
          processNode(node);
          if (typeof requestAnimationFrame === 'function' && node.nodeType === Node.ELEMENT_NODE &&
              ((node.getAttribute && node.getAttribute('role') === 'menu') || (node.querySelector && node.querySelector('[role="menu"], [role="menuitem"]')))) {
            requestAnimationFrame(() => processNode(node));
          }
        });
      } else if (mutation.type === 'characterData') {
        processNode(mutation.target);
      } else if (mutation.type === 'attributes') {
        translateElementAttrs(mutation.target);
      }
    });
  });

  function startLocalization() {
    if (!document.body) return;
    processNode(document.body);
    observer.observe(document.body, {
      childList: true,
      subtree: true,
      characterData: true,
      attributes: true,
      attributeFilter: ['title', 'aria-label', 'placeholder', 'aria-placeholder', 'data-slot-out']
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startLocalization);
  } else {
    startLocalization();
  }
})();
"""

MENU_TRANSLATOR_INJECTION = r"""
// Antigravity Chinese Localization Engine - Menu
(function() {
  const menuTranslationMap = {
    'File': '文件', 'Edit': '编辑', 'View': '视图', 'Window': '窗口', 'Help': '帮助',
    'New Conversation': '新建对话', 'New Window': '新建窗口', 'Close Window': '关闭窗口',
    'Check for Updates': '检查更新', 'Checking for Updates...': '正在检查更新...',
    'Downloading Update...': '正在下载更新...', 'Restart to Update': '重启以应用更新',
    'Undo': '撤销', 'Redo': '重做', 'Cut': '剪切', 'Copy': '复制', 'Paste': '粘贴',
    'Select All': '全选', 'Minimize': '最小化', 'Close': '关闭', 'Quit Antigravity': '退出 Antigravity',
    'Quit': '退出', 'Open Antigravity': '打开 Antigravity', 'Show Antigravity': '显示 Antigravity',
    'No agents running': '暂无运行中的智能体', 'Docs': '文档',
    'Connect to WSL': '连接到 WSL', 'Reopen Locally': '在本地重新打开',
    'About Antigravity': '关于 Antigravity', 'Services': '服务', 'Hide Antigravity': '隐藏 Antigravity',
    'Hide Others': '隐藏其他', 'Show All': '显示全部', 'Force Reload': '强制重新加载',
    'Reload': '重新加载', 'Actual Size': '实际大小', 'Zoom In': '放大', 'Zoom Out': '缩小',
    'Toggle Full Screen': '切换全屏',
    'Split': '分屏', 'Split Right': '向右分屏', 'Split Down': '向下分屏', 'Replace With New': '替换为新建', 'Replace with New': '替换为新建',
    'Back': '后退', 'Forward': '前进', 'Settings': '设置', 'Open In': '打开方式',
    'Open in Side Panel': '在侧边面板中打开', 'Open in Built-in Browser': '在内置浏览器中打开',
    'Open in External Browser': '在外部浏览器中打开', 'Open in New Tab': '在新标签页中打开',
    'Side Panel': '侧边面板', 'Side Panel (Default)': '侧边面板 (默认)',
    'Built-in Browser': '内置浏览器', 'Built-in Browser (Default)': '内置浏览器 (默认)',
    'External Browser': '外部浏览器', 'External Browser (Default)': '外部浏览器 (默认)',
    'New Tab': '新标签页', 'New Tab (Default)': '新标签页 (默认)',
    'Open Link in New Tab': '在新标签页中打开链接', 'Open Link in External Browser': '在外部浏览器中打开链接',
    'Copy Link': '复制链接', 'Copy Link Address': '复制链接地址',
    'Open Image in New Tab': '在新标签页中打开图片', 'Copy Image': '复制图片', 'Copy Image Address': '复制图片地址',
    'Rename': '重命名', 'Rename This Conversation': '重命名此对话', 'Duplicate': '制作副本',
    'Pin': '置顶', 'Unpin': '取消置顶', 'Pin This Conversation': '置顶此对话', 'Unpin This Conversation': '取消置顶此对话',
    'Stop': '停止', 'View Debug': '查看调试', 'Telemetry': '遥测',
    'Archive': '归档', 'Archive This Conversation': '归档此对话', 'Archive / Restore': '归档 / 恢复', 'Restore': '恢复',
    'Delete': '删除', 'Delete Conversation': '删除对话', 'Delete Permanently': '永久删除',
    'Mark Unread': '标记为未读', 'Mark Read': '标记为已读',
    'Mark as Read': '标记为已读', 'Mark as Unread': '标记为未读', 'Mark All as Read': '全部标为已读',
    'Mark This Conversation as Read': '将此对话标为已读', 'Mark This Conversation as Unread': '将此对话标为未读',
    'Conversation Name': '对话名称', 'Conversation ID': '对话 ID', 'Project Name': '项目名称', 'Workspace Name': '工作区名称', 'Worktree Name': '工作树名称',
    'Copy Conversation ID': '复制对话 ID', 'Copy Conversation Markdown': '复制对话 Markdown',
    'Copy Trajectory ID': '复制轨迹 ID', 'Copy Message': '复制消息',
    'Fork': '分支对话', 'Share': '分享', 'Move to Group': '移动到分组', 'Move to New Group': '移动到新分组',
    'Remove from Group': '从分组中移除', 'New Group': '新建分组',
    'Close Tab': '关闭标签页', 'Close Other Tabs': '关闭其他标签页',
    'Close Tabs to the Left': '关闭左侧标签页', 'Close Tabs to the Right': '关闭右侧标签页',
    'Reopen Closed Tab': '重新打开关闭的标签页', 'Split Terminal': '拆分终端', 'Close Terminal Tab': '关闭终端标签页', 'New Terminal Tab': '新建终端标签页',
    'Paste and Match Style': '粘贴并匹配样式', 'Speech': '语音', 'Start Speaking': '开始朗读', 'Stop Speaking': '停止朗读',
    'Bring All to Front': '前置全部窗口', 'Enter Full Screen': '进入全屏', 'Exit Full Screen': '退出全屏',
    'Toggle Developer Tools': '切换开发者工具', 'Connection info…': '连接信息…'
  };
  function translateMenu(menuItem) {
    if (menuItem.label) {
      if (menuTranslationMap[menuItem.label]) {
        menuItem.label = menuTranslationMap[menuItem.label];
      } else {
        const m = menuItem.label.match(/^(\d+)\s+agents?\s+running$/i);
        if (m) {
          menuItem.label = m[1] + ' 个智能体正在运行';
        }
      }
    }
    if (menuItem.submenu && menuItem.submenu.items) {
      menuItem.submenu.items.forEach(translateMenu);
    }
    if (menuItem.submenu && Array.isArray(menuItem.submenu)) {
      menuItem.submenu.forEach(translateMenu);
    }
    if (menuItem.items && Array.isArray(menuItem.items)) {
      menuItem.items.forEach(translateMenu);
    }
  }

  try {
    const { Menu } = require('electron');
    if (Menu && Menu.buildFromTemplate && !Menu.__isTranslated) {
      const originalBuildFromTemplate = Menu.buildFromTemplate;
      Menu.buildFromTemplate = function(template) {
        if (template && Array.isArray(template)) {
          template.forEach(translateMenu);
        }
        return originalBuildFromTemplate.call(this, template);
      };
      if (Menu.setApplicationMenu) {
        const originalSetApplicationMenu = Menu.setApplicationMenu;
        Menu.setApplicationMenu = function(menu) {
          if (menu) {
            translateMenu(menu);
          }
          return originalSetApplicationMenu.call(this, menu);
        };
      }
      Menu.__isTranslated = true;
    }
  } catch(e) {
    console.error("Menu hooking failed:", e);
  }
})();
"""

def extract_asar(asar_path, dest_dir):
    """Pure-Python asar archive extractor."""
    with open(asar_path, 'rb') as f:
        data = f.read(16)
        magic, size, u1, header_size = struct.unpack('<4I', data)
        header_json = f.read(header_size).decode('utf-8')
        header = json.loads(header_json)
        base_offset = 8 + size
        
        def extract_node(node, current_path):
            if not os.path.exists(current_path):
                os.makedirs(current_path)
            for name, info in node.items():
                path = os.path.join(current_path, name)
                if 'files' in info:
                    extract_node(info['files'], path)
                elif 'offset' in info:
                    f.seek(base_offset + int(info['offset']))
                    file_data = f.read(int(info['size']))
                    with open(path, 'wb') as out_f:
                        out_f.write(file_data)
        
        extract_node(header.get('files', {}), dest_dir)

def append_once(file_path, content, marker, name):
    if not os.path.exists(file_path):
        print(f"[警告] 未找到文件 {os.path.basename(file_path)}，已跳过注入 {name}。")
        return
    
    with open(file_path, "r", encoding="utf-8") as f:
        existing = f.read()
    
    if marker in existing:
        print(f"[状态] 发现已存在的 {name}，正在热更新词典...")
        idx = existing.find("// " + marker)
        if idx == -1:
            idx = existing.find(marker)
        if idx != -1:
            clean_content = existing[:idx].rstrip()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(clean_content + "\n" + content + "\n")
            print(f"[成功] 词典热更新完成：{name} ({os.path.basename(file_path)})")
        return
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n" + content + "\n")
    print(f"[成功] 注入完成：{name} ({os.path.basename(file_path)})")

def replace_in_file(file_path, target, replacement):
    if not os.path.exists(file_path):
        return
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    if replacement in content:
        print(f"[跳过] 目标已替换 ({os.path.basename(file_path)})")
        return
    if target not in content:
        return
    content = content.replace(target, replacement)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[成功] 执行目标替换 ({os.path.basename(file_path)})")

def apply_patch():
    print("==================================================================")
    print("                                                                ")
    print("              Antigravity v2.33.0 桌面端 一键汉化补丁               ")
    print("Github 开源项目地址：https://github.com/MIMICTE/Antigravity-zh-CN")
    print("                                                                ")
    print("==================================================================")
    print("                                                                ")
    print("[执行] 正在为您关闭 Antigravity 程序...")
    if sys.platform == "win32":
        os.system("taskkill /F /IM Antigravity.exe >nul 2>&1")
    elif sys.platform == "darwin":
        os.system("pkill -f Antigravity >/dev/null 2>&1")

    # 1. 确保 unpacked app 文件夹存在
    is_fresh_install = os.path.exists(ASAR_PATH) and not os.path.exists(ASAR_PATH + ".disabled")
    if is_fresh_install and os.path.exists(UNPACKED_APP_DIR):
        print("[状态] 检测到软件可能已更新，正在清理旧的解包缓存...")
        shutil.rmtree(UNPACKED_APP_DIR, ignore_errors=True)

    if not os.path.exists(UNPACKED_APP_DIR):
        source_asar = ASAR_PATH
        if not os.path.exists(source_asar) and os.path.exists(ASAR_PATH + ".disabled"):
            source_asar = ASAR_PATH + ".disabled"
            
        if not os.path.exists(source_asar):
            print(f"[错误] 未找到 app.asar: {ASAR_PATH}")
            return False

        print("[执行] 正在提取 app.asar 核心文件 (使用原生 Python 解析器)...")
        try:
            extract_asar(source_asar, UNPACKED_APP_DIR)
            print("[完成] 文件提取完毕.")
        except Exception as e:
            print(f"[错误] 提取 app.asar 失败: {e}")
            return False
    else:
        print(f"[状态] 发现已解包的工作目录: {UNPACKED_APP_DIR}")

    # 2. 注入各个组件
    preload_path = os.path.join(UNPACKED_APP_DIR, "dist", "preload.js")
    menu_path = os.path.join(UNPACKED_APP_DIR, "dist", "menu.js")
    tray_path = os.path.join(UNPACKED_APP_DIR, "dist", "tray.js")
    main_path = os.path.join(UNPACKED_APP_DIR, "dist", "main.js")

    append_once(preload_path, DOM_TRANSLATOR_INJECTION, "Antigravity Chinese Localization Engine", "Web UI Injection")
    append_once(menu_path, MENU_TRANSLATOR_INJECTION, "Antigravity Chinese Localization Engine - Menu", "Menu Translator Injection")

    # 兼容 v2.21.1 与 v2.29.0 托盘及主菜单文本替换
    replace_in_file(tray_path, "'Show Antigravity'", "'显示 Antigravity'")
    replace_in_file(tray_path, "'Quit'", "'退出'")
    replace_in_file(
        tray_path,
        "(count > 0 ? `${count}` : 'No') +\n                    ' agent' +\n                    (count === 1 ? '' : 's') +\n                    ' running'",
        "(count > 0 ? `${count} 个智能体正在运行` : '暂无运行中的智能体')"
    )
    replace_in_file(
        tray_path,
        "(count > 0 ? `${count}` : 'No') +\r\n                    ' agent' +\r\n                    (count === 1 ? '' : 's') +\r\n                    ' running'",
        "(count > 0 ? `${count} 个智能体正在运行` : '暂无运行中的智能体')"
    )
    replace_in_file(main_path, "label: 'No agents running'", "label: '暂无运行中的智能体'")
    replace_in_file(main_path, "label: `Open ${electron_1.app.getName()}`", "label: `打开 ${electron_1.app.getName()}`")
    replace_in_file(main_path, "label: 'Quit'", "label: '退出'")
    replace_in_file(menu_path, "label: 'New Window'", "label: '新建窗口'")
    replace_in_file(menu_path, "label: 'Docs'", "label: '文档'")
    replace_in_file(menu_path, "label: 'Connect to WSL'", "label: '连接到 WSL'")
    replace_in_file(menu_path, "label: 'Reopen Locally'", "label: '在本地重新打开'")
    # 兼容 v2.33.0 异步插入 WSL 菜单时 File 已被汉化为“文件”的情况
    replace_in_file(
        menu_path,
        "const submenuItem = appMenu.items.find((item) => item.label === submenuLabel);",
        "const __zhMap = { File: '文件', Edit: '编辑', View: '视图', Window: '窗口', Help: '帮助' }; const submenuItem = appMenu.items.find((item) => item.label === submenuLabel || item.label === __zhMap[submenuLabel]);"
    )
    replace_in_file(
        menu_path,
        "const viewMenuItem = appMenu.items?.find((item) => item.label === 'View');",
        "const viewMenuItem = appMenu.items?.find((item) => item.label === 'View' || item.label === '视图');"
    )

    # v2.33.0 Electron 原生对话框与更新菜单汉化
    updater_path = os.path.join(UNPACKED_APP_DIR, "dist", "updater.js")
    ipc_path = os.path.join(UNPACKED_APP_DIR, "dist", "ipcHandlers.js")
    popup_sec_path = os.path.join(UNPACKED_APP_DIR, "dist", "webviewPopupSecurity.js")
    remote_mgr_path = os.path.join(UNPACKED_APP_DIR, "dist", "remote", "remoteManager.js")

    replace_in_file(main_path, "buttons: ['Cancel', 'Quit']", "buttons: ['取消', '退出']")
    replace_in_file(main_path, "title: 'Confirm Quit'", "title: '确认退出'")
    replace_in_file(main_path, "message: 'Are you sure you want to quit?'", "message: '您确定要退出吗？'")
    replace_in_file(main_path, "detail: 'There may be agents or background tasks running.'", "detail: '当前可能有智能体或后台任务正在运行。'")
    replace_in_file(main_path, "title: 'WSL distro not found'", "title: '未找到 WSL 分发版'")
    replace_in_file(main_path, "detail: 'Antigravity opened on Windows instead.'", "detail: 'Antigravity 已改为在 Windows 本地打开。'")

    replace_in_file(updater_path, 'MenuUpdateStep["CheckForUpdates"] = "Check for Updates";', 'MenuUpdateStep["CheckForUpdates"] = "检查更新";')
    replace_in_file(updater_path, 'MenuUpdateStep["CheckingForUpdates"] = "Checking for Updates...";', 'MenuUpdateStep["CheckingForUpdates"] = "正在检查更新...";')
    replace_in_file(updater_path, 'MenuUpdateStep["DownloadingUpdate"] = "Downloading Update...";', 'MenuUpdateStep["DownloadingUpdate"] = "正在下载更新...";')
    replace_in_file(updater_path, 'MenuUpdateStep["RestartToUpdate"] = "Restart to Update";', 'MenuUpdateStep["RestartToUpdate"] = "重启以应用更新";')
    replace_in_file(updater_path, "title: 'Check for Updates'", "title: '检查更新'")
    replace_in_file(updater_path, "message: 'No updates available'", "message: '当前已是最新版本'")
    replace_in_file(updater_path, "buttons: ['OK']", "buttons: ['确定']")

    replace_in_file(ipc_path, "title: 'Open workspace'", "title: '打开工作区'")
    replace_in_file(ipc_path, "title: 'Open workspaces'", "title: '打开工作区'")
    replace_in_file(ipc_path, "title: 'Select Download Folder'", "title: '选择下载文件夹'")
    replace_in_file(ipc_path, "message: 'Folder is on the Windows filesystem'", "message: '文件夹位于 Windows 文件系统中'")

    replace_in_file(popup_sec_path, "label: 'Connection info…'", "label: '连接信息…'")
    replace_in_file(popup_sec_path, "title: 'Connection info'", "title: '连接信息'")
    replace_in_file(popup_sec_path, "buttons: ['OK']", "buttons: ['确定']")

    replace_in_file(remote_mgr_path, "title: 'Choose an SSH config file'", "title: '选择 SSH 配置文件'")
    replace_in_file(remote_mgr_path, "title: 'Choose another SSH config file'", "title: '选择其他 SSH 配置文件'")
    replace_in_file(remote_mgr_path, "buttons: ['Choose Another File…', 'Cancel']", "buttons: ['选择其他文件…', '取消']")
    replace_in_file(remote_mgr_path, "title: 'SSH connection failed'", "title: 'SSH 连接失败'")

    # 3. 汉化 loadingOverlay (Splash Screen)
    loading_path = os.path.join(UNPACKED_APP_DIR, "dist", "loadingOverlay.js")
    if os.path.exists(loading_path):
        with open(loading_path, "r", encoding="utf-8") as f:
            loading_content = f.read()
        patched_loading = loading_content.replace(">Loading Antigravity<", ">正在加载 Antigravity<")
        if patched_loading != loading_content:
            with open(loading_path, "w", encoding="utf-8") as f:
                f.write(patched_loading)
            print(f"[成功] 已成功汉化启动加载界面 ({os.path.basename(loading_path)})")

    # 4. 禁用原生 app.asar
    if os.path.exists(ASAR_PATH):
        print("[执行] 正在禁用官方 app.asar，以强制读取汉化代码...")
        os.rename(ASAR_PATH, ASAR_PATH + ".disabled")
        print("[成功] app.asar -> app.asar.disabled")

    print("                                                                ")
    print("==================================================================")
    print("                                                                ")
    print("       汉化补丁注入成功！正在为您自动启动 Antigravity...              ")
    print("                                                                ")
    print("==================================================================")
    
    if sys.platform == "win32":
        exe_path = os.path.join(APP_DIR, "Antigravity.exe")
        if os.path.exists(exe_path):
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            subprocess.Popen(
                [exe_path],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                close_fds=True
            )
    elif sys.platform == "darwin":
        subprocess.Popen(["open", APP_DIR])
    return True

if __name__ == "__main__":
    try:
        apply_patch()
        input("\n执行完毕，按 Enter 键退出...")
    except KeyboardInterrupt:
        print("\n\n[提示] 用户取消操作。")
        input("\n按 Enter 键退出...")
    except Exception as e:
        print(f"\n[错误] 执行过程中出现异常: {e}")
        print("\n如果问题持续，请访问 GitHub 提交 Issue:")
        print("https://github.com/MIMICTE/Antigravity-zh-CN/issues")
        input("\n按 Enter 键退出...")
        raise
