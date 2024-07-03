from gradio_client import Client
import streamlit as st 
import pyttsx3
from pydub import AudioSegment

# client = Client('AyushS9020/Bimbola_Project_Iter4')
client = Client('Julius133/Jaybot')

def answer(query) : 

    result = client.predict(
        query = query , 
        api_name = '/predict'
    )

    return result



def text_to_mp3(text) : 

    engine = pyttsx3.init()
    engine.save_to_file(text , 'output.wav')
    engine.runAndWait()
    
    # Convert WAV to MP3
    sound = AudioSegment.from_wav('output.wav')
    sound.export('response.mp3' , format = 'mp3')

def check_prompt(prompt) : 

    '''
    Function to check the prompt

    Args:
    prompt : str : The prompt to be checked

    Returns:
    bool : The boolean value indicating whether the prompt is valid or not
    '''

    try : 
        prompt.replace('' , '')
        return True 
    except : return False

def check_mesaage() : 
    '''
    Function to check the messages
    '''

    if 'messages' not in st.session_state : st.session_state.messages = []

check_mesaage()

for message in st.session_state.messages : 

    with st.chat_message(message['role']) : st.markdown(message['content'])

prompt = st.chat_input('Ask me anything')

if check_prompt(prompt) :

    with st.chat_message('user'): st.markdown(prompt)

    st.session_state.messages.append({
        'role' : 'user' , 
        'content' : prompt
    })

    if prompt != None or prompt != '' : 

        response = answer(prompt)

        with st.chat_message('assistant') : st.markdown(response)

        text_to_mp3(response)

        st.sidebar.audio('output.wav')

        st.session_state.messages.append({
            'role' : 'assistant' , 
            'content' : response
        })
