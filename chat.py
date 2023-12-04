import openai
import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
import numpy as np

openai.api_key = st.secrets.OPENAI_API_KEY

option = st.sidebar.selectbox("Which Dashboard?", ('Home','Youtube Video Summarizer','Chat Helper Bot Ai','Book Summarizer'),3)
if option == 'Home':
    st.title("Streamlit App Homepage")
    st.header("Welcome to the Streamlit App")

    # Add a section for the video summarizer
    st.header("Video Summarizer")
    st.write("Our video summarizer helps you easily condense long videos into shorter, more manageable clips. You can specify the length of the summary, and our AI algorithms will automatically select the most important parts of the video to include. Whether you're looking to save time or simply want to get a quick overview of a video, our video summarizer is the perfect tool for the job.")
    st.image("https://wtax-am.sagacom.com/files/2020/12/bored-work-12-2-20-shutterstock_1229760310.jpg")

    # Add a section for the book summarizer
    st.header("Book Summarizer")
    st.write("Reading a book can be time-consuming, but with our book summarizer, you can quickly get the main ideas and key takeaways. Our AI algorithms analyze the text of the book and extract the most important information, so you can get a good understanding of the book's content without having to read every word. Whether you're short on time or simply prefer to get the gist of things, our book summarizer is here to help.")
    st.image("https://i.pinimg.com/736x/d8/0e/25/d80e252b34c01df04574003a319ec283.jpg")

    # Add a section for the chatbot helper AI
    st.header("Chatbot Helper AI")
    st.write("Need help with something? Our AI chatbot is here to assist you 24/7. Whether you have a question about how to use our app or just need some advice, our chatbot can help. With its natural language processing capabilities, you can have a conversation with our chatbot just as you would with a human, and it will do its best to provide you with the information you need. Don't hesitate to reach out and get the help you need.")
    st.image("https://media.zenfs.com/en/euronews_uk_articles_973/9ee59a030ffefd7950ae1f11628604e7")

    
if option == 'Youtube Video Summarizer':
    st.header(option)
    #remove fed_meeting.mp4 and fed_meeting.mp3 if they exist
    if os.path.exists('fed_meeting.mp4'):
        os.remove('fed_meeting.mp4')
    if os.path.exists('fed_meeting.mp3'):
        os.remove('fed_meeting.mp3')
    st.write('To use this find a youtube video you would like a summary for then enter the url. Then enter a start time and end time in seconds and please be patient as I have not purchased a lot of cloud computing credits so it will take a little while to process your request. If you look at the top right hand corner you will see a running logo to indiciate the app is working correctly.')
    start_time = st.number_input('Enter the start time in seconds')
    end_time = st.number_input('Enter the end time in seconds')
    yt_video_url = st.text_input('Enter the video URL')
    calculate = st.button("convert")
    if calculate:
        
        youtube_video = YouTube(yt_video_url)
        streams = youtube_video.streams.filter(only_audio=True)
        stream = streams.first()
        stream.download(filename='fed_meeting.mp4')
        ffmpeg.input('fed_meeting.mp4').output('fed_meeting.mp3',ss=start_time, to=end_time).run()
        #ffmpeg.input('fed_meeting.mp4').output('fed_meeting.mp3',ss=start_time, to=end_time).run()
        #os.system('ffmpeg -ss 3 -i fed_meeting.mp4 -t 30 fed_meeting_trimmed.mp4')
        model = whisper.load_model("base")
        response = openai.Audio.transcribe("whisper-1", open("fed_meeting.mp3", "rb"))
        st.write(response)
        transcript = response['text']
        words = transcript.split(" ")
        chunks = np.array_split(words, 3)
        sentences = ' '.join(list(chunks[0]))
        
        summary_responses = []

        for chunk in chunks:
            
            sentences = ' '.join(list(chunk))

            prompt = f"{sentences}\n\ntl;dr:"

            response = openai.Completion.create(
                engine="text-davinci-003", 
                prompt=prompt,
                temperature=0.3, # The temperature controls the randomness of the response, represented as a range from 0 to 1. A lower value of temperature means the API will respond with the first thing that the model sees; a higher value means the model evaluates possible responses that could fit into the context before spitting out the result.
                max_tokens=150,
                top_p=1, # Top P controls how many random results the model should consider for completion, as suggested by the temperature dial, thus determining the scope of randomness. Top P’s range is from 0 to 1. A lower value limits creativity, while a higher value expands its horizons.
                frequency_penalty=0,
                presence_penalty=1
            )

            response_text = response["choices"][0]["text"]
            summary_responses.append(response_text)

        full_summary = "".join(summary_responses)

        st.header("full summary")
        st.write(full_summary)

if option == 'Book Summarizer':
    st.header(option)
    input = st.text_input('Enter words from the book that you want summarized')
    summarize = st.button('Summarize') 
    if summarize:
        transcript = input
        st.write (transcript)
        words = transcript.split(" ")
        chunks = np.array_split(words, 3)
        sentences = ' '.join(list(chunks[0]))
        summary_responses = []
        for chunk in chunks:
            
            sentences = ' '.join(list(chunk))

            prompt = f"{sentences}\n\ntl;dr:"

            response = openai.Completion.create(
                engine="text-davinci-003", 
                prompt=prompt,
                temperature=0.3, # The temperature controls the randomness of the response, represented as a range from 0 to 1. A lower value of temperature means the API will respond with the first thing that the model sees; a higher value means the model evaluates possible responses that could fit into the context before spitting out the result.
                max_tokens=150,
                top_p=1, # Top P controls how many random results the model should consider for completion, as suggested by the temperature dial, thus determining the scope of randomness. Top P’s range is from 0 to 1. A lower value limits creativity, while a higher value expands its horizons.
                frequency_penalty=0,
                presence_penalty=1
            )

            response_text = response["choices"][0]["text"]
            summary_responses.append(response_text)

        full_summary = "".join(summary_responses)

        st.header("full summary")
        st.write(full_summary)


if option == 'Chat Helper Bot Ai':
    st.header(option)
    def open_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()


    def gpt3_completion(prompt, engine='text-davinci-003', temp=.9, top_p=1.0, tokens=400, freq_pen=0.0, pres_pen=0.0, stop=['AI:', 'USER:']):
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


        
            
    
