from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

# Define the directory to persist the vector store
persist_directory = './vectorstore'

# Load the SentenceTransformer model and embeddings
embeddings = SentenceTransformerEmbeddings(model_name='all-MiniLM-L6-v2')

loader = PyMuPDFLoader("https://www.dbs-sar.com/LPB/Introduction.pdf")
docs = loader.load()

# Split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Create and save the vector store
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=persist_directory)
