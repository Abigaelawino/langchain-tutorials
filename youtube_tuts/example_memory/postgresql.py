import uuid
import psycopg
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
)
from langchain_postgres import PostgresChatMessageHistory

model = ChatOpenAI(model="gpt-4o-mini")

human_template = f"{{question}}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
    ]
)
chain = prompt_template | model


table_name = "chat_history"


def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
    sync_connection = psycopg.connect(
        dbname="dev_projects",
        user="docker",
        password="docker",
        host="localhost",
        port="5432",
    )

    return PostgresChatMessageHistory(
        table_name, session_id, sync_connection=sync_connection
    )


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_by_session_id,
    input_messages_key="question",
    history_messages_key="history",
)

fixed_session_id = str(uuid.uuid4())
while True:
    user_question = input(">>>>")
    result = chain_with_history.invoke(
        {"question": user_question},
        config={"configurable": {"session_id": "d4fa44bd-06e1-4ee1-8e05-57bfcd192090"}},
    )
    print(result.content)
