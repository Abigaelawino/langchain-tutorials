from cassandra.cluster import Cluster
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import (
    CassandraChatMessageHistory,
)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import (
    BaseChatMessageHistory,
)

model = ChatOpenAI(model="gpt-4o-mini")

human_template = f"{{question}}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
    ]
)
chain = prompt_template | model


def connect_to_cassandra():
    cluster = Cluster(["127.0.0.1"], port=9042)
    session = cluster.connect()
    return session


def get_cassandra_history(session_id: str) -> BaseChatMessageHistory:
    session = connect_to_cassandra()
    return CassandraChatMessageHistory(
        session_id=session_id,
        session=session,
        keyspace="my_keyspace",
    )


chain_with_history = RunnableWithMessageHistory(
    chain,
    get_cassandra_history,
    input_messages_key="question",
    history_messages_key="history",
)

while True:
    user_question = input(">>>>")
    result = chain_with_history.invoke(
        {"size": "concise", "question": user_question},
        config={"configurable": {"session_id": "alice_123"}},
    )
    print(result.content)
