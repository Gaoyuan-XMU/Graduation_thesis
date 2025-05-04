# 基于RAG技术建立基于通用开源大模型和专业知识库的问答系统

## 项目概述

本项目旨在设计并实现一个基于检索增强生成（Retrieval-Augmented Generation, RAG）的语音交互式问答系统。系统整合了大型语言模型（LLM）、专业领域知识库、自动语音识别（ASR）、文本到语音（TTS）以及图像驱动数字人动画等多项技术，构建了一个从语音输入到数字人视频输出的完整交互闭环。旨在克服传统LLM在处理未知或未明确记忆信息时易产生的“幻觉”问题，提供更准确、更可靠、更生动的问答体验。

## 主要特性

  * **语音输入**：通过高鲁棒性的ASR技术（基于Whisper）准确识别用户自然语音查询，并进行简繁转换]。
  * **RAG增强问答**：利用Dify平台搭建RAG管道，结合开源LLM（如DeepSeek）和专业知识库，生成基于事实的准确答案，减少LLM幻觉。
  * **专业知识库**：支持导入特定领域的专业文档，构建可检索的知识库，确保问答内容的专业性和时效性.
  * **语音合成输出**：将生成的文本答案通过高质量TTS技术（基于EdgeTTS）合成为流畅自然的语音.
  * **数字人视频输出**：应用图像驱动动画技术（基于SadTalker），根据用户上传的静态人物肖像和合成语音生成具有同步口型的数字人说话视频，增强交互的视觉吸引力.
  * **模块化设计**：系统采用模块化架构，各功能单元职责清晰，易于维护和技术替换.

## 技术栈

  * **核心框架**: Python
  * **前端界面**: Gradio
  * **语音识别**: Whisper (openai-whisper)
  * **RAG/LLM平台**: Dify.ai (集成DeepSeek LLM)
  * **语音合成**: EdgeTTS (edge-tts)
  * **数字人生成**: SadTalker
  * **简繁转换**: opencc-python-reimplemented
  * **HTTP请求**: requests
  * **其他**: os, subprocess, glob, json, asyncio

## 系统架构

系统采用前后端分离的模块化设计。前端基于Gradio构建用户交互界面，负责语音录制、图像上传和结果展示。后端是核心处理引擎，按序调用语音识别模块（trans.py）、语义问答模块（request.py与Dify交互）、语音合成模块（speak.py）和视频生成模块（app.py调用SadTalker）。各模块通过文件传递和函数调用进行协作

## 安装与运行

1.  **克隆项目仓库**：
    ```bash
    git clone https://github.com/Gaoyuan-XMU/Graduation_thesis.git
    cd project
    ```
2.  **安装Python依赖**：
    ```bash
    pip install -r requirements.txt
    ```
    （注意：`requirements.txt` 文件需要您根据项目使用的具体库和版本手动创建，或者从您的项目中提取）。主要的依赖包括：`gradio`, `openai-whisper`, `requests`, `edge-tts`, `opencc-python-reimplemented`, `torch`, `torchaudio`, `torchvision`。
3.  **安装和配置SadTalker**：
    请参照SadTalker官方文档进行安装和配置. **注意**：`app.py` 中的 `SADTALKER_PATH` 需要修改为您本地SadTalker项目的实际路径.
4.  **配置Dify平台**：
      * 注册Dify.ai账户并创建工作区。
      * 创建“聊天机器人”应用，选择RAG类型，并导入您的专业领域知识文档构建知识库
      * 在应用设置中获取API Key，并将其配置在 `app.py` 的 `CONFIG` 字典中.
5.  **下载Whisper模型**：
    首次运行`trans.py` 时，如果本地没有Whisper 'base' 模型，会自动下载.
6.  **运行应用**：
    ```bash
    python app.py
    ```
    应用将在本地启动一个Web服务，通常在 `http://127.0.0.1:7860/` 地址访问.

## 文件结构

```
.
├── app.py          # 主程序，Gradio界面和流程控制 
├── trans.py        # 语音识别模块 (基于Whisper) 
├── request.py      # 语义问答模块 (与Dify API交互) 
├── speak.py        # 语音合成模块 (基于EdgeTTS) 
├── output/         # 输出目录，存放生成的中间文件和结果文件 (如transcript.txt, answer.txt, answer.mp3, conversation_id.txt, 视频文件) 
├── 基于RAG技术建立基于通用开源大模型和专业知识库的问答系统（第四版）.docx # 论文文档 
└── requirements.txt  # 项目依赖列表 (需要手动创建或生成)
```

## 未来改进方向

  * 优化系统实时性，减少响应时延.
  * 实现知识库的自动化更新和管理.
  * 增强对话管理能力，支持更复杂的交互.
  * 提升数字人视频生成效果，例如增加表情和姿态的丰富度.
  * 探索离线部署方案，减少对外部服务的依赖.
