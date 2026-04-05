"""平行人生模拟器 MVP — Flask 后端"""

import os
import json
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from openai import OpenAI
from prompts import INTERVIEWER, EXTRACT_PERSONA, GENERATE_VARIABLES, SIMULATE, BRANCH

app = Flask(__name__)
app.secret_key = os.urandom(24)

client = OpenAI(
    base_url="https://coding.dashscope.aliyuncs.com/v1",
    api_key=os.environ.get("DASHSCOPE_API_KEY", "your-api-key-here"),
)

MODEL = "qwen3.5-plus"


def chat_completion(messages, system=None, stream=False):
    """统一的 API 调用"""
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.extend(messages)
    return client.chat.completions.create(
        model=MODEL,
        messages=msgs,
        stream=stream,
        max_tokens=8000,
    )


# ---------- 页面 ----------

@app.route("/")
def index():
    return render_template("index.html")


# ---------- 对话采集 ----------

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """对话式采集用户信息"""
    data = request.json
    history = data.get("history", [])

    # 如果是第一条消息，加入系统引导
    if not history:
        history = [{"role": "user", "content": data.get("message", "")}]
    else:
        history.append({"role": "user", "content": data.get("message", "")})

    resp = chat_completion(history, system=INTERVIEWER)
    reply = resp.choices[0].message.content

    persona_ready = "[PERSONA_READY]" in reply
    clean_reply = reply.replace("[PERSONA_READY]", "").strip()

    history.append({"role": "assistant", "content": clean_reply})

    return jsonify({
        "reply": clean_reply,
        "history": history,
        "persona_ready": persona_ready,
    })


# ---------- 人格档案 ----------

@app.route("/api/extract-persona", methods=["POST"])
def api_extract_persona():
    """从对话历史中提取人格档案"""
    data = request.json
    history = data.get("history", [])

    chat_text = "\n".join(
        f"{'用户' if m['role'] == 'user' else 'AI'}: {m['content']}"
        for m in history
    )

    resp = chat_completion(
        [{"role": "user", "content": f"对话记录：\n{chat_text}"}],
        system=EXTRACT_PERSONA,
    )
    persona = resp.choices[0].message.content
    return jsonify({"persona": persona})


# ---------- 保存人格档案 ----------

@app.route("/api/save-persona", methods=["POST"])
def api_save_persona():
    """保存用户编辑后的人格档案"""
    data = request.json
    persona = data.get("persona", "")
    # 保存到文件
    import pathlib
    save_dir = pathlib.Path(__file__).parent / "data"
    save_dir.mkdir(exist_ok=True)
    (save_dir / "persona.md").write_text(persona, encoding="utf-8")
    return jsonify({"ok": True})


# ---------- 变量生成 ----------

@app.route("/api/generate-variables", methods=["POST"])
def api_generate_variables():
    """根据人格档案生成变量面板"""
    data = request.json
    persona = data.get("persona", "")

    resp = chat_completion(
        [{"role": "user", "content": f"人格档案：\n{persona}"}],
        system=GENERATE_VARIABLES,
    )
    raw = resp.choices[0].message.content

    # 提取 JSON
    try:
        # 尝试从 markdown code block 中提取
        if "```" in raw:
            json_str = raw.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]
            variables = json.loads(json_str.strip())
        else:
            variables = json.loads(raw.strip())
    except (json.JSONDecodeError, IndexError):
        variables = {"personal": [], "interpersonal": [], "social": [], "raw": raw}

    return jsonify({"variables": variables})


# ---------- 模拟 ----------

@app.route("/api/simulate", methods=["POST"])
def api_simulate():
    """运行人生模拟（SSE 流式输出）"""
    data = request.json
    persona = data.get("persona", "")
    variables = data.get("variables", {})
    custom_instructions = data.get("custom_instructions", "")

    var_text = ""
    for category in ["personal", "interpersonal", "social"]:
        items = variables.get(category, [])
        if items:
            var_text += f"\n### {category} 变量\n"
            for v in items:
                name = v.get("name", "")
                val = v.get("current", "")
                var_text += f"- {name}: {val}\n"

    user_msg = f"""人格档案：
{persona}

变量配置：
{var_text}
"""
    if custom_instructions:
        user_msg += f"\n用户附加指令：{custom_instructions}\n"

    def generate():
        stream = chat_completion(
            [{"role": "user", "content": user_msg}],
            system=SIMULATE,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield f"data: {json.dumps({'text': delta.content}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


# ---------- 分支 ----------

@app.route("/api/branch", methods=["POST"])
def api_branch():
    """从某个节点分支（SSE 流式输出）"""
    data = request.json
    persona = data.get("persona", "")
    timeline_before = data.get("timeline_before", "")
    branch_age = data.get("branch_age", "")
    modification = data.get("modification", "")

    prompt = BRANCH.format(
        timeline_before=timeline_before,
        branch_age=branch_age,
        modification=modification,
    )

    user_msg = f"人格档案：\n{persona}\n\n{prompt}"

    def generate():
        stream = chat_completion(
            [{"role": "user", "content": user_msg}],
            system=SIMULATE,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta and delta.content:
                yield f"data: {json.dumps({'text': delta.content}, ensure_ascii=False)}\n\n"
        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5678))
    print(f"\n  平行人生模拟器 MVP")
    print(f"  http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
