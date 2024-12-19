from sqlalchemy import create_engine
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import (
    SQLChatMessageHistory,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory


model = ChatOpenAI(model="gpt-4o-mini")

human_template = f"{{question}}"
prompt_template = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="history"),
        ("human", human_template),
    ]
)
chain = prompt_template | model

engine = create_engine("sqlite:///db.sqlite")
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: SQLChatMessageHistory(session_id=session_id, connection=engine),
    input_messages_key="question",
    history_messages_key="history",
)

while True:
    user_question = input(">>>>")
    result = chain_with_history.invoke(
        {"question": user_question},
        config={"configurable": {"session_id": "21312423456896456"}},
    )
    print(result.content)
