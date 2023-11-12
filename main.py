
import os #توفر ادوات للتعامل مع الملفات
import openai

from PyPDF2 import  PdfReader
from dotenv  import load_dotenv
import streamlit as st


load_dotenv()
api_key = st.secrets["OPENAI_API_KEY"]

#api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise Exception("API key is missing. Set the OPENAI_API_KEY environment variable.")
openai.api_key = api_key


def get_response(text):
    prompt = f"""
            You are an expert in summaerizing text, you will be given a text delimited by four backquotes,
            make sure to capture the main points,key agrguments , and any supporting evidence presented in the article .
            Your summery should be informative and well-structured, ideally consisting of 3-5 sentences.
                   
            text: ''''{text}''''
            """
    response = openai.Completion.create(model="text-davinci-002", prompt=prompt,
    max_tokens=100)
    print("Full Response:", response)
    return response["choices"][0]["text"]


def load_files():#take whats inside data
    text ="" #varنعبي فيه التكست اللي بنسوي ليه summerize
    data_dir = os.path.join(os.getcwd(),"data")# نعرف وين موجود getcwd:get current working directory
    for filename in os.listdir(data_dir):
        with open(os.path.join(data_dir,filename),"r") as f:
            text+=f.read()
    return text


def extract_text_from_pdf(pdf_file):
    #load pdf file and split into pages
    reader = PdfReader(pdf_file)
    raw_text=""
    for page in reader.pages:
        content=page.extract_text()
        if content:
            raw_text+= content
    return raw_text

#raise Exception("The 'openai.api_key' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(api_key=os.getenv(\"OPENAI_API_KEY\"))'")

def main():
    st.set_page_config( 
        page_title="Summarizer",
        page_icon="📚🐥"
    )
    #Header
    st.title("Summarization app")
    st.write("This app uses OpenAI's GPT-3 to summerize a given text or a pdf file .")
    st.divider()

    #check if input wants to select text or upload a file
    option = st.radio("Select Input Type",("Text","PDF"))
    #craete a text area for the user to input text
    if option == "Text":
        user_input=st.text_area("Enter Text", "")
        #create submit button 
        if st.button("Submit") and user_input !="":
            #call the get_response function and display the response
            response=get_response(user_input)
            #display the summery
            st.subheader("Summery")
            st.markdown(f">{response}")
        else:
            st.error("Please enter text.")
    
    else:
        #create a file uploader for the user to upload a pdf
        uploaded_file = st.file_uploader("Choos a pdf file",type="pdf")
        #create a submit button
        if st.button("Submit") and uploaded_file is not None:
            text = extract_text_from_pdf(uploaded_file)
            #call the get response function and display the response
            response = get_response(text=text)
            st.subheader("Summary")
            st.markdown(f">{response}")
        else:
            st.error("Please upload a PDF file.")
if __name__ == "__main__":
    main()
