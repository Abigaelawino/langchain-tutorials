# LangChain with Redis Example

This project demonstrates how to build a conversational retrieval-augmented generation (RAG) system using LangChain and Redis. The application allows users to interact with a chatbot that can retrieve relevant information from a Redis vector store and maintain conversation history.

## Key Features

- **OpenAI Integration**: Uses the GPT-4o-mini model for generating responses
- **Redis Vector Store**: Stores and retrieves vector embeddings for semantic search
- **Conversation Memory**: Maintains chat history between user interactions using Redis
- **Retrieval-Augmented Generation**: Enhances LLM responses with relevant context from the vector database

## How It Works

1. The application loads environment variables containing API keys and Redis configuration
2. It initializes an OpenAI language model and embeddings
3. A Redis vector store is set up as a retrieval system for relevant documents
4. Chat history is maintained in Redis, allowing for persistent conversations
5. The ConversationalRetrievalChain combines the LLM, retriever, and memory components
6. Users can interact with the system through a simple command-line interface


## Requirements

See the requirements.txt file for all dependencies. Key components include:
- langchain
- langchain-openai
- langchain-community
- redis
- python-dotenv