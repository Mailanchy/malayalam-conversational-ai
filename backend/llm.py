import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")
conversation_history = []
# Initialize conversation history
def reset_history():
    conversation_history = [
        {
        "role": "system",
        "content": "You are part of a group conversation as an AI member. Each participant is identified by a speaker number. Your responses should be distinct for each speaker, addressing them directly and personally, while maintaining the flow of conversation. This text will later be converted to speech and translated into Malayalam, so please don't use labels in your response. Respond back as if you are speaking. Make sure to clearly separate each response for individual speakers. Explicit mention of each speaker would be great. The members talk mixed up but you can identify who is the speaker by looking into their speaker id. You respond as a single person.max 5-6 sentence"
        }
    ]
def get_response(prompt):
    # Add the user message to history
    conversation_history.append({"role": "user", "content": prompt})   
    # Call the OpenAI API
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_history
    )

    # Get response text
    response_text = response.choices[0].message.content
    # Add assistant's response to history
    conversation_history.append({"role": "assistant", "content": response_text})
    return response_text
