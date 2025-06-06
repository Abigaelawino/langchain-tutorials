from dotenv import load_dotenv
import redis
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Redis as RedisVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain.memory.buffer import ConversationBufferMemory

load_dotenv()

# LLM
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=os.getenv("OPENAI_API_KEY"))

# Vector Store (your RAG index)
vectorstore = RedisVectorStore(
    redis_url=os.getenv("redislink"),
    index_name=os.getenv("index"),
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 50})

# Memory
def get_redis_history(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id,
        url="redis://localhost:6379/0")

memory = ConversationBufferMemory(
    memory_key="chat_history",
    chat_memory=get_redis_history("dfsdfsfs"),
    return_messages=True,
    output_key="answer"  # <-- This tells LangChain which output to save
)


# Conversational Chain with Retrieval
chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
    verbose=False,
)

# Interaction Loop
while True:
    user_question = input(">>>> ")
    result = chain.invoke({"question": user_question})
    print("\n🧠 Answer:", result["answer"])

# Adapted from 
# Extended to support Redis vector store, LangChain memory, and custom session logic.

