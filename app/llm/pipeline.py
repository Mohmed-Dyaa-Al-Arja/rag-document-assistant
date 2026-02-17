from typing import List, Dict, AsyncIterator
from langchain_core.documents import Document
from langchain_community.chat_models import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.retrieval.retriever import SemanticRetriever
from app.memory.conversation import ConversationManager
from app.config import settings
class RAGPipeline:

    def __init__(self, retriever: SemanticRetriever):
        self.retriever = retriever
        self.memory = ConversationManager()

        # Initialize LLM once with fallback
        self.llm = self._initialize_llm()

        # Prompt
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful assistant that answers questions based only on the provided context.

If the answer is not in the context, say:
"I cannot find enough information in the document to answer this question."

Context:
{context}

Conversation history:
{history}
"""),
            ("user", "{question}")
        ])

        self.chain = self.prompt | self.llm | StrOutputParser()

    #  LLM Initialization (Auto Fallback)

    def _initialize_llm(self):

        # AUTO MODE
        if settings.LLM_PROVIDER == "auto":
            if settings.GEMINI_API_KEY:
                print("Using Gemini model")
                return ChatGoogleGenerativeAI(
                    model=settings.GEMINI_MODEL,
                    google_api_key=settings.GEMINI_API_KEY,
                    temperature=0.1
                )
            else:
                print("Using Ollama (fallback)")
                return ChatOllama(
                    model=settings.OLLAMA_MODEL,
                    base_url=settings.OLLAMA_BASE_URL,
                    temperature=0.1
                )

        # FORCE GEMINI
        if settings.LLM_PROVIDER == "gemini":
            return ChatGoogleGenerativeAI(
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=0.1
            )

        # FORCE OLLAMA
        return ChatOllama(
            model=settings.OLLAMA_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
            temperature=0.1
        )

    # Formatting Helpers

    def _format_documents(self, docs: List[Document]) -> str:
        if not docs:
            return "No relevant information found."

        context_parts = []
        for i, doc in enumerate(docs, 1):
            page = str(doc.metadata.get("page", "Unknown"))
            content = doc.page_content.strip()
            context_parts.append(f"[Source {i} - Page {page}]\n{content}")

        return "\n\n".join(context_parts)

    def _format_history(self) -> str:
        history = self.memory.get_history()
        if not history:
            return "No previous conversation."

        formatted = []
        for msg in history[-6:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted.append(f"{role}: {msg['content']}")

        return "\n".join(formatted)

    def _extract_sources(self, docs: List[Document]) -> List[Dict]:
        return [
            {
                "page": str(doc.metadata.get("page", "Unknown")),
                "snippet": doc.page_content[:200]
            }
            for doc in docs
        ]

    # Ask

    async def ask_async(self, question: str) -> Dict:

        docs = self.retriever.retrieve(question)

        print(f"Retrieved {len(docs)} documents")

        context = self._format_documents(docs)
        history = self._format_history()

        answer = await self.chain.ainvoke({
            "context": context,
            "history": history,
            "question": question
        })

        self.memory.add_user_message(question)
        self.memory.add_ai_message(answer)

        return {
            "answer": answer,
            "sources": self._extract_sources(docs),
            "confidence": "high" if len(docs) >= 2 else "low"
        }

    async def ask_stream(self, question: str) -> AsyncIterator[str]:

        docs = self.retriever.retrieve(question)

        context = self._format_documents(docs)
        history = self._format_history()

        full_answer = ""

        async for chunk in self.chain.astream({
            "context": context,
            "history": history,
            "question": question
        }):
            full_answer += chunk
            yield chunk

        self.memory.add_user_message(question)
        self.memory.add_ai_message(full_answer)

# app/llm/pipeline.py
