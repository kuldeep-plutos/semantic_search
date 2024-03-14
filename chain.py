from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain

llm = Ollama(model="llama2-uncensored")
output_parser = StrOutputParser()
embeddings = OllamaEmbeddings(model="llama2-uncensored")

loader = TextLoader("./data/essay.txt")

documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)

print(f"{'*'*50}\nChroma vectorization started\n{'*'*50}")

vector = Chroma.from_documents(docs, embeddings)

print(f"{'*'*50}\nvector\n{'*'*50}\n{vector}\n{'*'*50}\n")

prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:
<context>
{context}
</context>
Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever, document_chain)

response = retrieval_chain.invoke({"input": "What is plutos ONE? answer in one line"})
print(response["answer"])