# request.py 修改后完整代码
import os
import json
import requests

CONVERSATION_FILE = "output/conversation_id.txt"

def save_conversation_id(conversation_id):
    """保存会话ID到文件"""
    os.makedirs(os.path.dirname(CONVERSATION_FILE), exist_ok=True)
    with open(CONVERSATION_FILE, 'w') as f:
        f.write(conversation_id)

def load_conversation_id():
    """从文件加载会话ID"""
    try:
        if os.path.exists(CONVERSATION_FILE):
            with open(CONVERSATION_FILE, 'r') as f:
                return f.read().strip()
    except:
        pass
    return ""

def query_dify(input_path, output_path, api_key):
    with open(input_path, 'r') as f:
        query_text = f.read()

    url = "https://api.dify.ai/v1/chat-messages"
    
    # 构建请求payload
    payload = {
        "inputs": {},
        "query": query_text,
        "response_mode": "streaming",
        "conversation_id": load_conversation_id(),  # 加载已有会话ID
        "user": "abc-123"
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    def process_stream(response):
        accumulated_answer = ""
        current_conversation_id = ""
        
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith('data: '):
                    try:
                        data = json.loads(decoded_line[len('data: '):])
                        
                        # 处理消息内容
                        if data.get('event') == 'agent_message':
                            accumulated_answer += data.get('answer', '')
                            
                        # 捕获会话结束事件
                        if data.get('event') == 'message_end':
                            current_conversation_id = data.get('conversation_id', '')
                            if current_conversation_id:
                                save_conversation_id(current_conversation_id)
                                
                    except json.JSONDecodeError:
                        continue
        return accumulated_answer

    answer = process_stream(response)
    with open(output_path, 'w') as f:
        f.write(answer)
    return answer