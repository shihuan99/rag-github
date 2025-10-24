import loaders
from llm_retrival import build_query_engine
import gradio as gr


documents = loaders.documents
if not documents:
    print("No documents found in the repository path, program exit now.")
    exit(1)

query_engine = build_query_engine(documents)

def chat_query(message, history):
    response = query_engine.query(message)
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": str(response)})
    return history, ""


def chat_function(message, history):
    response = query_engine.query(message)
    return str(response)

gr.ChatInterface(
    fn=chat_function,
    type="messages",
    title="Kafka智能运维助手",
    description="向您的Github知识库提问",
    examples=["Kafka消息堆积的可能原因", "Kafka生产发送超时", "消费组出现位点重置"]
).launch()
