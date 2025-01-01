import os
from flask import Flask, render_template, request, jsonify
from langchain.prompts import ChatPromptTemplate
from langchain.llms import Cohere
from langchain.chains import LLMChain, RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Chroma

app = Flask(__name__)

def load_db():

    try:
        embeddings = CohereEmbeddings(cohere_api_key=os.environ["COHERE_API_KEY"])
        vectordb = Chroma(persist_directory='db', embedding_function=embeddings)
        qa = RetrievalQA.from_chain_type(
            llm=Cohere(),
            chain_type="refine",
            retriever=vectordb.as_retriever(),
            return_source_documents=True
        )
        return qa
    except Exception as e:
        print("Error:", e)

qa = load_db()

def answer_from_knowledgebase(message):
   
    if qa is None:
        return "Sorry, the knowledge base is not available at the moment. Please try again later."
    try:
        res = qa({"query": message})
        return res['result']
    except Exception as e:
        print(f"Error in answer_from_knowledgebase: {e}")
        return "An error occurred while processing your request. Please try again."

def search_knowledgebase(message):
    if qa is None:
        return "Sorry, the knowledge base is not available at the moment. Please try again later."
    try:
        res = qa({"query": message})
        sources = ""
        for count, source in enumerate(res['source_documents'], 1):
            sources += f"Source {count}\n"
            sources += f"{source.page_content}\n"
        return sources.strip()
    except Exception as e:
        print(f"Error in search_knowledgebase: {e}")
        return "An error occurred while searching the knowledge base. Please try again."

def answer_as_chatbot(message):
    try:
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable not set")
    
        llm = Cohere(cohere_api_key=cohere_api_key, temperature=0.7)

        template = """You are a helpful AI assistant. Your goal is to provide informative and engaging responses to user queries.

        Current conversation:
        {chat_history}

        Human: {human_input}
        AI Assistant:"""

        prompt = ChatPromptTemplate.from_template(template)
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversation_chain = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=memory
        )

        response = conversation_chain.predict(human_input=message)
        return response
    except Exception as e:
        print(f"Error in answer_as_chatbot: {e}")
        return "An error occurred while processing your request. Please try again."

@app.route('/kbanswer', methods=['POST'])
def kbanswer():
    message = request.json['message']
    response_message = answer_from_knowledgebase(message)
    return jsonify({'message': response_message}), 200

@app.route('/search', methods=['POST'])
def search():
    message = request.json['message']
    search_results = search_knowledgebase(message)
    return jsonify({'message': search_results}), 200

@app.route('/answer', methods=['POST'])
def answer():
    message = request.json['message']
    response_message = answer_as_chatbot(message)
    return jsonify({'message': response_message}), 200

@app.route("/")
def index():
    return render_template("index.html", title="")

if __name__ == "__main__":
    app.run()
