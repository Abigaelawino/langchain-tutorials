from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage


model = ChatOpenAI(model="gpt-3.5-turbo")

# ! No memory example...
# while True:
#     user_question = input(">>>>")
#     result = model.invoke([user_question])
#     # The model on its own does not have any concept of state.
#     print(result.content)

# ! Brute Force memory example...
past_messages = []
while True:
    user_question = input(">>>>")
    past_messages.append(HumanMessage(user_question))
    result = model.invoke(past_messages)
    past_messages.append(AIMessage(result.content))
    print(result.content)
