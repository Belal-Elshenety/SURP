from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_groq import ChatGroq
from crewai_tools import tool


llm = ChatGroq(model="llama3-70b-8192",groq_api_key="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",temperature=0.7)

persist_directory = './vectorstore'
embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')

@tool
def query_vector_store(query: str):
    """
    Tool to handle queries using the vector store.
    """
    # Load the vector store
    vectorstore = Chroma(embedding_function=embeddings, persist_directory=persist_directory)

    # Retrieve and generate using the relevant snippets of the blog
    retriever = vectorstore.as_retriever()
    prompt = hub.pull("rlm/rag-prompt")

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # Set up the RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain.invoke(query)
