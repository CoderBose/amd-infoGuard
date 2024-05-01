import os
import openai
from chat import Chat
import pandas as pd
openai.api_key = ""

chat_model = Chat("gpt-3.5-turbo", 0.1)

data = pd.read_csv("politifact_articles.csv")

def generate_data(question, newsContext):
    initial_instruction = f"""You are a fact news checker, On the basis of the information given below fact check the user's question.
    information: {newsContext}
    You have to fact check the question with the contextual information and provide response accordingly also mention the source. """
    systemMessage = {'role': 'system', 'content': initial_instruction}
    userMessage = {'role': 'user', 'content': question}
    response = chat_model.chat([systemMessage,userMessage])
    return response
syntheticData = pd.DataFrame({"news":[], "question":[], "response":[] })

for index, row in data.iterrows():
    news = row['Text']
    question = "is this news real: " +  row['Title'] + '?'
    response = generate_data(question, news)
    new_row = {"news":news, "question":question, "response":response }
    syntheticData = syntheticData._append(new_row, ignore_index=True)
    

syntheticData.to_csv("syntheticData.csv")

