
import requests
import gradio as gr
import uuid

print("GRADIO FILE LOADED")

API_BASE = "http://127.0.0.1:8000"

HEADERS = {
    "X-API-KEY": "dev-secret-key"
}

SESSION_ID = str(uuid.uuid4())


# Upload

def upload_document(file):

    if file is None:
        return "Please upload a document."

    files = {"file": open(file.name, "rb")}

    response = requests.post(
        f"{API_BASE}/upload",
        files=files,
        headers=HEADERS
    )

    if response.status_code != 200:
        return f"Error: {response.text}"

    data = response.json()

    return f"{data['message']}\nTotal Chunks: {data['total_chunks']}"


# Ask

def ask_question(question, chat_history):

    if not question.strip():
        return "", chat_history

    payload = {
        "question": question,
        "session_id": SESSION_ID
    }

    response = requests.post(
        f"{API_BASE}/ask",
        json=payload,
        headers=HEADERS
    )

    if response.status_code != 200:
        chat_history.append(
            {"role": "assistant", "content": f"Error: {response.text}"}
        )
        return "", chat_history

    data = response.json()

    answer = data["answer"]
    sources = data.get("sources", [])

    formatted_sources = "\n\n".join(
        [
            f"Page {s['page']}: {s['snippet'][:150]}..."
            for s in sources
        ]
    )

    final_answer = f"{answer}\n\n---\n{formatted_sources}"

    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": final_answer})

    return "", chat_history


# -------------------------
# Clear
# -------------------------

def clear_chat():

    payload = {
        "question": "",
        "session_id": SESSION_ID
    }

    requests.post(
        f"{API_BASE}/clear-memory",
        json=payload,
        headers=HEADERS
    )

    return []


# -------------------------
# UI
# -------------------------

with gr.Blocks(title="Smart Contract Assistant") as demo:

    gr.Markdown("# Smart Contract Summary & Q&A Assistant")

    with gr.Tab("Upload Document"):
        file_input = gr.File(label="Upload PDF or DOCX")
        upload_output = gr.Textbox(label="Upload Status", lines=4)
        upload_btn = gr.Button("Process Document")

        upload_btn.click(
            upload_document,
            inputs=file_input,
            outputs=upload_output
        )

    with gr.Tab("Chat"):
        chatbot = gr.Chatbot(height=400)
        msg = gr.Textbox(label="Ask a question")
        send_btn = gr.Button("Send")
        clear_btn = gr.Button("Clear Chat")

        def send_message(question, history):
            return ask_question(question, history)

        send_btn.click(
            fn=send_message,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )

        clear_btn.click(
            fn=clear_chat,
            outputs=chatbot
        )




# -------------------------
# Launch
# -------------------------

if __name__ == "__main__":
    demo.launch(server_port=7860)
