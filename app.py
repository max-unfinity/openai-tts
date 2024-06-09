import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os


voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


@st.cache_resource
def get_client():
    if not os.path.exists("output"):
        os.makedirs("output")
    load_dotenv(".env")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    return client

input_text = st.text_area("Input text")
st.caption(f"Characters: {len(input_text)}")
st.caption(f"Estimated cost: $ {len(input_text) / 1e6 * 30:.4f}")
voice = st.selectbox("Voice", voices)
use_hd = st.checkbox("Use HD voice")

if st.button("Generate"):
    output_file = f"output/output.mp3"
    client = get_client()

    if use_hd:
        model = "tts-1-hd"
    else:
        model = "tts-1"

    with st.spinner("Generating..."):
        response = client.audio.speech.create(
            model=model,
            voice=voice,
            input=input_text,
            response_format="mp3",
        )

        response.write_to_file(output_file)

    st.audio(output_file, format="audio/mpeg", loop=False)