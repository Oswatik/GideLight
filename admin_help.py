import streamlit as st
from langchain_community.llms import Ollama
from langchain.chains import ConversationChain
from langchain.schema import HumanMessage, SystemMessage

# Initialize Llama3 with Ollama
llm = Ollama(model="llama3")

# Define the conversation chain
conversation = ConversationChain(llm=llm)

system_prompt = f"""
You are an HR bot that is now going to talk to the real HR!
Be straight-forward and blunt to the HR in your answers.
For example, if the HR asks, on what criteria the candidates have been shortlisted then, just answer that they have been shortlisted on the basis of similarity of their skills mentioned in their resumes and the job description, which would make them the best fit for the job
If the HR asks you some question which is beyond your capabilities then answer - This is your job not mine.
IMPORTANT do not reply with "As an AI model..." under any circumstances.
"""

def assisting_chatbot(user_query):
    # Add a SystemMessage to provide context to the chatbot
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_query)
    ]

    # Generate a response from the LLM
    response = conversation.run(messages)
    
    return response