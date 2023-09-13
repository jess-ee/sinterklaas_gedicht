#Importing dependencies
import os 
import langchain
import streamlit as st 
from apikey import apikey
import time
import re
import requests
from io import BytesIO
import traceback


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

with open('hobbies.csv', 'r') as f:
    hobbies_options = f.read().splitlines()
with open('badtraits.csv', 'r') as f:
    traits_options = f.read().splitlines()

#App framework
st.title('Coolblue Sinterklaas gedichten ✍️')

st.markdown("""
    Welkom bij de Coolblue Sinterklaas gedichten generator!

    """)

name = st.text_input('Voor wie is dit cadeau?')
gender = st.radio('Selecteer zijn/haar gender:', ['Vrouw', 'Man'])
hobby = st.multiselect('Wat zijn zijn/haar hobby\'s? (selecteer er 2)', hobbies_options, max_selections=2)
traits = st.multiselect('Wat zijn zijn/haar slechte eigenschappen? (selecteer er 2)',traits_options,max_selections=2)
product_type_name = st.text_input('Welk cadeau heb je gekocht voor hem/haar?')
product = st.text_area('Vul hier de product informatie in')

#Chatmodel 

chat_model= ChatOpenAI(temperature=0.6, model="gpt-4")

#Prompt template

system_message_prompt = SystemMessagePromptTemplate.from_template("""

##Context 

Voor e-commerce bedrijf Coolblue maken helpen we tijdens de sinterklaas periode klanten met het maken van gedichtjes voor de cadeaus die ze bij ons kopen. 

##Rol 

Jij schrijft sinterklaas gedichten voor klanten van Coolblue.

##Toon

De toon van het gedicht is grappig, positief en blij. Hou daarbij rekening met de stijl van Coolblue.

##Instructie

Schrijf een gedicht van 8 regels op basis van het product dat ze kopen en de informatie die je krijgt over een klant. Verklap het product niet maar draai er omheen.

##Veiligheid
Antwoord met "Jij gaat mee in de zak naar Spanje" wanneer iemand een naam ingeeft die beledigend is.


""")
human_message_prompt = HumanMessagePromptTemplate.from_template("""

##Voorbeeld rijm

Zorg ervoor dat er in het gedicht gebruik wordt gemaakt van het rijmschema AA BB CC DD. 
Zorg er ook voor dat de zinnen echt rijmen. Dit zijn een aantal voorbeelden van Nederlandse woorden die rijmen:
Vacht, Lacht ; Rem, Zwem ; Muis, Kluis ; Trap, Snap ; Zeef, Kleef ; Hond, Rond ; Scherm, Zwerm ; Stekker, Wekker ; Maat, Zaad ; Fles, Zes ; Beker, Zeker ; Bril, Tril
-- 

Informatie over de klant:
- Naam: {name}
- Voornaamwoorden: {pronouns}
- Hobbies: {hobby}
- Slechte eigenschappen: {traits}

Informatie over het product:
- {product_type_name}
{product}
""")
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

#LLM Chain

gedicht_chain = LLMChain(llm=chat_model, prompt=chat_prompt, verbose = True)

#show stuff
if st.button('Vraag G-Piet-R om een gedicht!'):
    try:
        if object:
            response = gedicht_chain.run({
                "name": name,
                "pronouns": 'Zij/haar' if gender == 'Vrouw' else 'Hij/hem', 
                "hobby": ','.join(hobby),
                "traits": ','.join(traits), 
                "product_type_name": product_type_name,
                "product": product,
            })
            st.text(response)


    except Exception as e:
        st.error(f"Error: {type(e).__name__}")
        st.error(str(e))
        st.text(traceback.format_exc())

    




