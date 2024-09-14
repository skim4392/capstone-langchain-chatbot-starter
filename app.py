from flask import Flask, render_template
from flask import request, jsonify, abort

from langchain.llms import Cohere
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

import os
from dotenv import load_dotenv
load_dotenv('./.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

def createChatbot():
    template = """You are a helpful assistant. Answer all questions to the best of your ability.
        If you do not know the answer to a question, say so.

        {chat_history}
        Human: {human_input}
        Chatbot:
    """

    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], template=template
    )

    llm = Cohere(cohere_api_key=os.environ.get("COHERE_API_KEY"))
    memory = ConversationBufferMemory(memory_key="chat_history")
    chatbot = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory
    )

    return chatbot

def answer_from_knowledgebase(message):
    # TODO: Write your code here
    return ""

def search_knowledgebase(message):
    # TODO: Write your code here
    sources = ""
    return sources

def answer_as_chatbot(message):
    res = chatbot.run(message)
    return res


chatbot = createChatbot()

@app.route('/kbanswer', methods=['POST'])
def kbanswer():
    # TODO: Write your code here
    
    # call answer_from_knowledebase(message)
        
    # Return the response as JSON
    return 

@app.route('/search', methods=['POST'])
def search():    
    # Search the knowledgebase and generate a response
    # (call search_knowledgebase())
    
    # Return the response as JSON
    return

@app.route('/answer', methods=['POST'])
def answer():
    message = request.json['message']
    
    # Generate a response
    response_message = answer_as_chatbot(message)
    
    # Return the response as JSON
    return jsonify({'message': response_message}), 200

@app.route("/")
def index():
    return render_template("index.html", title="")

if __name__ == "__main__":
    app.run()