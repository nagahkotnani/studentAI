'''AIzaSyBxF9vxhUNSsJamc1loHvLqhUJZ3lDOEXs'''
import streamlit as st
from PIL import Image
from googletrans import Translator
import google.generativeai as genai

# Initialize Translator and Google Generative AI
translator = Translator()
genai.configure(api_key="AIzaSyBxF9vxhUNSsJamc1loHvLqhUJZ3lDOEXs")  # Replace with your actual API key

# Streamlit UI
st.set_page_config(page_title="AI Tutor", layout="wide")
st.title("📚 AI-Powered Tutor for Mathematics, Physics & Chemistry")

# Sidebar for Language Selection (Now includes Telugu)
input_lang = st.sidebar.selectbox("Input Language", ["English"])
output_lang = st.sidebar.selectbox("Output Language", ["English", "Spanish", "French", "German", "Hindi", "Telugu"])

# Subject Selection
subject = st.sidebar.selectbox("Select Subject", ["Mathematics", "Physics", "Chemistry"])

# Text Input or Image Upload
input_mode = st.radio("Select Input Mode", ["Text", "Image"])

if input_mode == "Text":
    user_input = st.text_area(f"Ask your {subject} question:")

    if st.button("Get Answer") and user_input:
        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            response = model.generate_content(f"{subject} question: {user_input}")
            answer = response.text

            # Translate output if needed
            translated_answer = translator.translate(answer, dest=output_lang).text if output_lang != "English" else answer

            st.write("### ✨ AI Explanation:")
            st.write(translated_answer)

            # Provide language conversion option
            st.write("🔄 Need a different language? Select from the sidebar.")
        except Exception as e:
            st.error(f"⚠️ Error generating answer: {e}")

elif input_mode == "Image":
    uploaded_file = st.file_uploader(
        f"Upload an image related to {subject} (handwritten equations, textbook pages, etc.)",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Get Explanation"):
            try:
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content([
                    image,
                    f"This image contains a {subject} problem. Extract the text and provide an explanation."
                ])
                answer = response.text

                # Translate output if needed
                translated_answer = translator.translate(answer, dest=output_lang).text if output_lang != "English" else answer

                st.write("### ✨ AI Explanation:")
                st.write(translated_answer)

                # Provide language conversion option
                st.write("🔄 Need a different language? Select from the sidebar.")
            except Exception as e:
                st.error(f"⚠️ Error generating explanation: {e}")

# Interactive Features
if st.sidebar.checkbox("Enable Voice Input (Coming Soon)"):
    st.sidebar.write("🎙 Voice input will be integrated in future updates!")

if st.sidebar.checkbox("Gamification Mode"):
    st.sidebar.write("🏆 Earn badges and rewards for learning achievements!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🔗 Developed by AI Learning Hub")
