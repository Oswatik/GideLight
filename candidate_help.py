import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage, SystemMessage

# Initialize Llama3 with Ollama
llm = Ollama(model="llama3")

# Define the conversation chain
conversation = ConversationChain(llm=llm)

system_prompt = f"""
You are an HR bot that answers queries related to job applications. 
You are friendly, concise, and professional. 
Answer crisply.
Also provide information on additional information that should be present in a Job description like company values, benefits, and any other relevant information if asked.
If some more complex question is asked answer that - The candidate will be contacted by the HR soon.
IMPORTANT do not reply with "As an AI model..." under any circumstances.
"""

def chatbot_response(user_query):
    # Add a SystemMessage to provide context to the chatbot
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query)
    ]

    # Generate a response from the LLM
    response = conversation.run(messages)
    
    return response
