import streamlit as st
from PIL import Image

def home_page():
    image = Image.open('Images/HR-Management-Systems-scaled.jpeg')
    st.image(image)
    st.header("About Us")
    st.write("""
             Welcome to AI-HR!\n 
             Our simple, straight-forward approach makes it easy for you to use AI in your hiring process, in a low-risk environment, without changing your existing workflows. Our platform helps both the candidate and the employer to go through the process smoothly and find their best fit.
             Use our services to hire the best candidate there is and automate your hiring process! Our team will present you with pre-screened, vetted candidates for your unique search. \n
             AI-driven hiring is the future and we are determined to making it a reality. Our AI platform for all talent brings to light everything you need to hire and develop people to their highest potential \n
             Everything talent,\n 
             powered by AI
             """)
    st.subheader("Creator")
    st.write("""
             A. Swatik Samam, 121FP1121 \n
             Final-year Student \n
             Food Process Engineering \n
             NIT Rourkela
             """)