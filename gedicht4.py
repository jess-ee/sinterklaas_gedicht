#Importing dependencies
import os 
import langchain
import streamlit as st 
from apikey import apikey
import time
import re
import pandas as pd

from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessage
)

from langchain.chains import LLMChain

os.environ['OPENAI_API_KEY'] = apikey

#App framework
st.title('Coolblue Sinterklaas gedichten🖊️')

st.markdown("""
    Welkom bij de Coolblue Sinterklaas gedichten generator!

    """)


name = st.text_input('Vul hier je naam in')
gender = st.radio('Selecteer je gender:', ['Vrouw', 'Man'])
hobby = st.text_input('Vul hier je hobby in')
product_id = st.number_input(min_value=0, max_value=100000000, step=1, label='Vul hier het product_id in')



#Chatmodel 

chat_model= ChatOpenAI(temperature=0.6, model="gpt-4")

#Prompt template

system_message_prompt = SystemMessagePromptTemplate.from_template("""Je schrijft Sinterklaasgedichten voor de klanten van Coolblue.

Schrijf de gedichten op basis van informatie over de klant en het product dat ze hebben gekocht.

Het gedicht moet grappig, positief en blij. Verklap het product niet maar draai er omheen.

Gebruik maximaal 8 regels.
""")
human_message_prompt = HumanMessagePromptTemplate.from_template("""Informatie over de klant:
- Naam: {name}
- Voornaamwoorden: {pronouns}
- Hobbies: {hobby}

Informatie over het product:
- {product_type_name}
- {pro_1}
- {pro_2}
- {pro_3}
""")
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

#LLM Chain

gedicht_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

#show stuff
if st.button('Begin te schrijven!'):
    try:
        if object:
            product_information_df = pd.read_csv("./product_information_small.csv")
            product_df = product_information_df.query(f"""product_id == {product_id}""")
            pro_1 = product_df.iloc[0,1]
            pro_2 = product_df.iloc[0,2]
            pro_3 = product_df.iloc[0,3]
            product_type_name = product_df.iloc[0,4]

            response = gedicht_chain.run({
                "name": name,
                "pronouns": 'Zij/haar' if gender == 'Vrouw' else 'Hij/hem', 
                "hobby":hobby, 
                "pro_1": pro_1,
                "pro_2": pro_2,
                "pro_3": pro_3,
                "product_type_name": product_type_name
            })
            st.text(response)
    except Exception as e:
        st.error(f"an error occurred:{e}")



