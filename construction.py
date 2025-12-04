import openai

# Set your OpenAI API key (recommended: use environment variable for security)
openai.api_key = "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"  # Or better: os.getenv("OPENAI_API_KEY")

def reply(user_query, conversation_history=[]):
    system_prompt = """
    You are an expert AI assistant specialized in construction-related topics 
    (building, civil engineering, architecture, materials, safety, machinery, etc.).
    Answer any question about construction accurately and professionally.

    If the question is not related to construction, politely respond with:
    "I'm sorry, I'm specialized only in construction topics. Please ask me anything about building, engineering, or construction!"

    Always greet the user naturally when appropriate.
    """

    messages = [{"role": "system", "content": system_prompt}]

    # Add last 5 exchanges
    for pair in conversation_history[-5:]:
        messages.append({"role": "user", "content": pair["user"]})
        messages.append({"role": "assistant", "content": pair["assistant"]})

    messages.append({"role": "user", "content": user_query})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8
    )

    assistant_reply = response.choices[0].message.content.strip()

    # Update history in-place
    conversation_history.append({
        "user": user_query,
        "assistant": assistant_reply
    })

    # Keep only last 5 exchanges
    conversation_history[:] = conversation_history[-5:]

    return assistant_reply

# Example usage:
if __name__ == "__main__":
    history = []                     # you still create it once
    print(reply("How deep should footings be?", history))

    print("\n---\n")

    print(reply("Who won the 2025 World Cup?", history))