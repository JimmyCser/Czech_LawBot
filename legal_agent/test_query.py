from legal_agent.agent import app

def test():
    question = "Which agency is responsible for trade licensing in Czech law?"
    print("\n📌 Câu hỏi:")
    print(question)

    state = {"input": question}  

    try:
        result = app.invoke(state)
        print("\n🧠 Trả lời từ AI:")
        print(result.get("answer", result))
    except Exception as e:
        print("❌ Lỗi khi gọi agent:", e)

if __name__ == "__main__":
    test()
