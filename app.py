from flask import Flask, render_template
from flask import request, jsonify, abort

from langchain.llms import Cohere
from langchain import PromptTemplate, LLMChain
from langchain.memory import ConversationBufferMemory

from langchain.chains import RetrievalQA
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma

import os
from dotenv import load_dotenv
load_dotenv('./.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

def load_chatbot():
    try:
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
    except Exception as e:
        print("Error loading chatbot:", e)

def load_db():
    try:
        embeddings = CohereEmbeddings(cohere_api_key=os.environ.get("COHERE_API_KEY"))
        vectordb = Chroma(persist_directory='db', embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(
            llm=Cohere(),
            chain_type="refine",
            retriever=vectordb.as_retriever(),
            return_source_documents=True
        )
        return qa
    except Exception as e:
        print("Error loading vector db:", e)

chatbot = load_chatbot()
qa = load_db()

def answer_from_knowledgebase(message):
    res = qa({"query": message})
    return res['result']

def search_knowledgebase(message):
    res = qa({"query": message})
    sources = ""
    for count, source in enumerate(res['source_documents'],1):
        sources += "<p><em><u>Source " + str(count) + "</u></em>\n"
        sources += source.page_content + "</p>"
    return sources

def answer_as_chatbot(message):
    res = chatbot.run(message)
    return res

@app.route('/kbanswer', methods=['POST'])
def kbanswer():
    return handle_request(request, answer_from_knowledgebase)

@app.route('/search', methods=['POST'])
def search():    
    return handle_request(request, search_knowledgebase)

@app.route('/answer', methods=['POST'])
def answer():
    return handle_request(request, answer_as_chatbot)

def handle_request(request, cb):
    message = request.json['message']
    if message == "":
        return jsonify({'error': 'We were unable to process your request. Please check the format of your query and try again.'}), 400

    try:
        response_message = cb(message)
        return jsonify({'message': response_message}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'We are currently experiencing an issue with our system. We apologize for the inconvenience; please try again later.'}), 500

@app.route("/")
def index():
    return render_template("index.html", title="")

if __name__ == "__main__":
    app.run()