import openai
import whisper
from api_key import API_KEY
from pytube import YouTube

import ffmpeg
import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
import numpy as np

openai.api_key = st.secrets["API_KEY"]

option = st.sidebar.selectbox("Which Dashboard?", ('Home','Video to Text','Chat Helper Bot Ai','AI Translator'),0)
if option == 'Home':
    st.header(option)
    st.write('The current home for all things AI since other website has decided to shit the bed.')
    st.write('This is a work in progress and will be updated as I learn more about AI and Streamlit. The AI translator is a work in progress and will be updated as I learn more about AI and Streamlit.')
    st.subheader('Earning call currently working')
    
if option == 'Video to Text':
    st.header(option)
        #remove fed_meeting.mp4 and fed_meeting.mp3 if they exist
    if os.path.exists('fed_meeting.mp4'):
        os.remove('fed_meeting.mp4')
    if os.path.exists('fed_meeting.mp3'):
        os.remove('fed_meeting.mp3')
    st.write('This is a work in progress and will be updated as I learn more about AI and Streamlit.')
    yt_video_url = st.text_input('Enter the video URL')
    start_time = st.number_input('Enter the start time in seconds')
    end_time = st.number_input('Enter the end time in seconds')
    st.button('Convert')
    if yt_video_url:
        youtube_video = YouTube(yt_video_url)
        streams = youtube_video.streams.filter(only_audio=True)
        stream = streams.first()
        stream.download(filename='fed_meeting.mp4')
        ffmpeg.input('fed_meeting.mp4').output('fed_meeting.mp3',ss=start_time, to=end_time).run()
        #ffmpeg.input('fed_meeting.mp4').output('fed_meeting.mp3',ss=start_time, to=end_time).run()
        #os.system('ffmpeg -ss 3 -i fed_meeting.mp4 -t 30 fed_meeting_trimmed.mp4')
        model = whisper.load_model("base")
        response = model.transcribe('fed_meeting.mp3')
        transcript = response['text']
        words = transcript.split(" ")
        prompt = f"{transcript}\n\ntl;dr:"
        #we need to chunk our data or we will get an error becasue open ai has a limit of 2048 characters
        chunks = np.array_split(words, 10)
        sentences = ' '.join(list(chunks[0]))
        
        prompt = f"{sentences}\n\ntl;dr:"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
        )
        response_text = response['choices'][0]['text']
        summary_responses = []
        for chunk in chunks: 
            sentences = ' '.join(list(chunk))
            prompt = f"{sentences}\n\ntl;dr:"
            response = openai.Completion.create(
                engine="davinci",
                prompt=prompt,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
            )
            response_text = response['choices'][0]['text']
            summary_responses.append(response_text)
        full_summary = ' '.join(summary_responses)
        st.header('Summary')
        st.write(full_summary)
    
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
        

        
        

if option == 'AI Translator': 

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    # Custom REACT-based component for recording client audio in browser
    build_dir = os.path.join(parent_dir, "st_audiorec/frontend/build")
    # specify directory and initialize st_audiorec object functionality
    st_audiorec = components.declare_component("st_audiorec", path=build_dir)

    # TITLE and Creator information
    st.title('streamlit audio recorder')
    st.write('\n\n')


    # STREAMLIT AUDIO RECORDER Instance
    val = st_audiorec()
    # web component returns arraybuffer from WAV-blob
    st.write('Audio data received in the Python backend will appear below this message ...')

    if isinstance(val, dict):  # retrieve audio data
        with st.spinner('retrieving audio-recording...'):
            ind, val = zip(*val['arr'].items())
            ind = np.array(ind, dtype=int)  # convert to np array
            val = np.array(val)             # convert to np array
            sorted_ints = val[ind]
            stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
            wav_bytes = stream.read()
            


        # wav_bytes contains audio data in format to be further processed
        # display audio data as received on the Python side
        st.audio(wav_bytes, format='audio/wav')
    # if record == True:
    #     model = whisper.load_model("base")
    #     out = model.transcribe('myvoice.mp3', language='en')
    #     st.write(out['text'])


        
            
    
