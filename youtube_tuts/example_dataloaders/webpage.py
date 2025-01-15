import os
from dotenv import load_dotenv

load_dotenv()

from dotenv import load_dotenv
import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_unstructured import UnstructuredLoader
from get_relevant_documents import get_answer_from_llm

from typing import List


page_url = "https://frequentmiler.com/ihg-giving-opportunity-to-buy-status-it-could-be-a-good-deal/"

# ! Simple Extraction (one Document)
loader = WebBaseLoader(web_paths=[page_url])
documents: List[Document] = []

for doc in loader.lazy_load():
    documents.append(doc)

answer = get_answer_from_llm(
    documents=documents,
    question="How much would buying diamond status cost me?",
)
print(answer)


# ! Advanced Extraction (multiple Documents)
# loader = UnstructuredLoader(web_url=page_url)
# documents: List[Document] = []

# for doc in loader.lazy_load():
#     documents.append(doc)
