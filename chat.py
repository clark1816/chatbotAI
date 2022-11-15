import openai
from api_key import API_KEY
import streamlit as st
import sounddevice as sd
import wavio
import whisper

openai.api_key = st.secrets["API_KEY"]

option = st.sidebar.selectbox("Which Dashboard?", ('Home','Chat Helper Bot Ai','AI Translator'),0)
if option == 'Home':
    st.header(option)
    st.write('The current home for all things AI since other website has decided to shit the bed.')

if option == 'Chat Helper Bot Ai':
    st.header(option)
    def open_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()


    def gpt3_completion(prompt, engine='text-davinci-002', temp=.9, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['AI:', 'USER:']):
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temp,
            max_tokens=tokens,
            top_p=top_p,
            frequency_penalty=freq_pen,
            presence_penalty=pres_pen,
            stop=stop)
        text = response['choices'][0]['text'].strip()
        return text


    if __name__ == '__main__':
        conversation = list()
        user_input = st.text_input(label='input') #input('USER: ')
        conversation.append('USER: %s' % user_input)
        #this line is basically a list comprehesion
        text_block = '\n'.join(conversation)
        prompt = open_file('prompt_chat.txt').replace('<<BLOCK>>', text_block)
        prompt = prompt + '\nAI:'
        response = gpt3_completion(prompt)
        st.write('AI:',response)
        conversation.append('AI: %s' % response)
        
def recrod_function():
    with st.empty():
        if record == True:
            st.write("Recording...")
            duration = 5  # seconds
            fs = 48000
            sd.default.samplerate = fs
            sd.default.channels = 1
            myrecording = sd.rec(int(duration * fs))
            sd.wait(duration)
            print("Saving sample as myvoice.mp3")
            path_myrecording = "myvoice.mp3"
            wavio.write(path_myrecording, myrecording, fs, sampwidth=2)
            sd.play(myrecording, fs) #st
            st.write("Done! Saved sample as myvoice.mp3")

            




        
            
    
