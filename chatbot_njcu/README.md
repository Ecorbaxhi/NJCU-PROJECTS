# NJCU Incoming Student Chatbot

This project is a Retrieval-Augmented Generation (RAG) chatbot designed to assist incoming students at NJCU by answering their questions based on a curated knowledge base. The system leverages FastAPI for the backend, a modern JavaScript framework for the frontend, and a vector database for storing embedded questions and answers. The RAG logic is implemented using LangChain and LangGraph.

## Features

- **Conversational AI**: Answers student queries about campus, admissions, courses, and more.
- **Retrieval-Augmented Generation**: Combines knowledge base retrieval with generative AI for accurate responses.
- **Vector Database**: Stores and retrieves embedded questions and answers efficiently.
- **Modern Frontend**: Responsive web interface for easy interaction.
- **Modular Backend**: FastAPI-based, organized for scalability and maintainability.
- **Dependency Management**: Poetry for Python, npm/yarn for JavaScript.

## Project Structure

```
chatbot_njcu/
│
├── backend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   ├── db/
│   │   │   ├── rag/
│   │   │   ├── models/
│   │   │   ├── utils/
│   │   │   └── main.py
│   │   └── __init__.py
│   ├── tests/
│   ├── pyproject.toml
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.js
│   ├── package.json
│   └── README.md
│
├── .gitignore
└── README.md
```

## Technologies Used

- **Backend**: FastAPI, LangChain, LangGraph, Poetry
- **Frontend**: JavaScript (React or similar), npm/yarn
- **Database**: Vector database (e.g., Pinecone, FAISS, or similar)

## Getting Started

### Backend

1. Navigate to the backend directory:
   ```
   cd src/chatbot_njcu/backend
   ```
2. Install dependencies:
   ```
   poetry install
   ```
3. Run the FastAPI server:
   ```
   poetry run uvicorn app.main:app --reload
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd src/chatbot_njcu/frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm start
   ```

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

This project is licensed under the MIT License.