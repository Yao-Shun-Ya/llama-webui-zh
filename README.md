# llama.cpp WebUI 一键汉化补丁（b11344）

llama.cpp 官方 WebUI 的完整中文本地化补丁。一条命令，把英文界面变成带注释的中文界面。

## 特性

- **一键运行**：自动下载官方 UI 资源 → 精准翻译 496 处界面文本 → 生成可直接使用的 `webui-zh/` 目录
- **翻译精准**：按代码语法上下文逐条替换（非全局查找替换），不改动任何功能代码，不影响任何功能
- **术语注释**：普通人难以理解的参数都附带大白话解释，例如：

  | 英文原文 | 汉化后 |
  | --- | --- |
  | Temperature | 温度（越高越随机，越低越确定） |
  | Top K | Top K（只保留概率最高的 K 个词元） |
  | Top P | Top P（核采样：保留累积概率达到 P 的词元） |
  | Context Size | 上下文长度（模型能"记住"多少词元） |

- **自动修复 Service Worker 缓存问题**：避免浏览器旧缓存导致"改了不生效"
- **技术缩写保留英文**：模型名、Top K、MCP、JSON、KV 等业内通用写法不动

## 适用版本

- llama.cpp **b11344**（对应 `bundle.DvlqYeJf.js`）
- 其他版本：bundle 的哈希名会变，需要更新脚本内的 `LLAMA_TAG` 与 `BUNDLE` 两个常量；若界面文案没变，翻译表仍然有效

## 使用方法

1. 安装 [Python 3](https://www.python.org/downloads/)（需要 curl / tar，Windows 10+ 系统自带）
2. 运行脚本（会在脚本所在目录生成 `webui-zh/`，约 10 MB）：

   ```bash
   python 汉化补丁.py
   ```

3. 启动 llama-server 时用 `--path` 指向它：

   ```bash
   llama-server.exe --models-preset models.ini --path "D:\TOOLS\llama.cpp\webui-zh" --no-models-autoload --port 8080
   ```

   Windows 用户可以直接用本仓库附带的 `启动WebUI.cmd`：把它放到 llama.cpp 根目录（与 llama-server.exe、models.ini 同级），双击即可启动服务器并自动打开浏览器。

4. 浏览器打开 http://127.0.0.1:8080 ，看到中文界面即成功。

## 文件说明

| 文件 | 说明 |
| --- | --- |
| 汉化补丁.py | 一键汉化脚本（自包含，自动下载官方 UI，无需预先安装 llama.cpp） |
| 启动WebUI.cmd | Windows 一键启动示例（llama-server + 预设 + 自动打开浏览器） |
| LICENSE | MIT |

## 许可

MIT。llama.cpp 官方代码采用 MIT 许可；本仓库中的全部中文翻译均为原创文本。
