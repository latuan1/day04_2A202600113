from agent import graph
from langchain_core.messages import HumanMessage
import sys

def run_test_case(test_name, user_input):
    print(f"\n{'='*20} {test_name} {'='*20}")
    print(f"User: {user_input}")
    
    # Reset state for each test case to ensure independence
    result = graph.invoke({"messages": [HumanMessage(content=user_input)]})
    
    # Trace the full conversation including tool calls
    full_conversation = []
    for msg in result["messages"]:
        role = "AI" if msg.type == "ai" else "Tool" if msg.type == "tool" else "Human"
        content = msg.content
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                full_conversation.append(f"[{role} gọi tool: {tc['name']}]({tc['args']})")
        
        if content:
            full_conversation.append(f"{role}: {content}")
            
    # Print the full conversation flow
    for line in full_conversation:
        print(line)
    
    return full_conversation

if __name__ == "__main__":
    test_cases = [
        ("Test 1: Direct Answer", "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."),
        ("Test 2: Single Tool Call", "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"),
        ("Test 3: Multi-step Tool Chaining", "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp."),
        ("Test 4: Missing Info / Clarification", "Tôi muốn đặt khách sạn"),
        ("Test 5: Guardrail / Refusal", "Giải giúp tôi bài tập lập trình Python về linked list")
    ]

    all_logs = []
    for name, input_text in test_cases:
        log = run_test_case(name, input_text)
        all_logs.append((name, input_text, log))

    # Ghi kết quả ra file test_results.md
    with open("test_results.md", "w", encoding="utf-8") as f:
        f.write("# KẾT QUẢ KIỂM THỬ AGENT TRAVELBUDDY\n\n")
        for name, input_text, log in all_logs:
            f.write(f"## {name}\n")
            f.write(f"**User:** `{input_text}`\n\n")
            f.write("**Log hệ thống:**\n")
            f.write("```\n")
            for line in log:
                f.write(f"{line}\n")
            f.write("```\n\n---\n\n")
            
    print(f"\n[DONE] Đã lưu kết quả vào file test_results.md")