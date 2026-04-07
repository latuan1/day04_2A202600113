from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
import os

# Tải các biến môi trường
load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Kiểm tra xem tin nhắn đầu tiên có phải là SystemMessage không
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"\n[Gọi tool: {tc['name']}]({tc['args']})")
    else:
        print("\n[TravelBuddy trả lời trực tiếp]")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)

# Thêm các nodes
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# Thiết lập các Edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

# Compile graph
graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy — Trợ lý Du lịch Thông minh (LangGraph)")
    print("Gõ 'quit', 'exit' hoặc 'q' để kết thúc cuộc hội thoại.")
    print("=" * 60)

    while True:
        try:
            user_input = input("\nBạn: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                print("Cảm ơn bạn đã sử dụng TravelBuddy. Hẹn gặp lại!")
                break

            if not user_input:
                continue

            print("\n[TravelBuddy đang suy nghĩ...]")
            
            # Khởi tạo trạng thái ban đầu cho mỗi câu hỏi nếu cần
            # Hoặc duy trì hội thoại bằng cách truyền state cũ vào (ở đây đơn giản hóa là hội thoại mới mỗi lần gọi, nhưng LangGraph có thể duy trì state)
            # Để demo đúng ReAct Agent, ta thường truyền cả lịch sử messages.
            
            result = graph.invoke({"messages": [("human", user_input)]})
            
            # Lấy tin nhắn cuối cùng từ Agent (không phải lỗi từ tool)
            final_response = result["messages"][-1]
            print(f"\nTravelBuddy: {final_response.content}")
            
        except Exception as e:
            print(f"\n[Lỗi hệ thống]: {e}")
            break