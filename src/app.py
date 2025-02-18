import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage, SystemMessage
import logging
import traceback

from utilities import SupportFun
logging.basicConfig(filename='chatbot.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


class Chatbot(SupportFun):
    """     Initize LLM chatboat with hyper parameters """

    def __init__(self, model = 'llama-3.2:1b',base_url='http://localhost:11434', temperature=0):
        SupportFun.__init__(self)
        self.llm = ChatOllama(model=model, base_url=base_url, temperature=temperature)
        self.initialize_session_state()

    def initialize_session_state(self):
        """Initializes the Streamlit session state for messages if it doesn't exist.
           This fun also adds the initial system message to the message memory"""
        
        if "messages" not in st.session_state:
            st.session_state.messages = [
                SystemMessage("""You are an assistant for question-answering tasks. Use the following pieces of retrieved context 
            to answer the question. If you don't know the answer, just say that you don't know. Use three sentences
             maximum and keep the answer concise.""")
            ]

        if "ocr_data" not in st.session_state:
            st.session_state.ocr_data = []  

        # if "doc_uploaded" not in st.session_state:
        #     st.session_state.doc_uploaded = []

    def display_messages(self):
        """Displays the chat messages from the message memory in the streamlit ui"""
        
        for message in st.session_state.messages:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):
                    st.markdown(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.markdown(message.content)

    def process_prompt(self, prompt):
        """Processes the user's prompt by adding it to the message history, 
           sending it to the LLM, displaying the response, and updating the message history.
        """
        if prompt:
            try :

                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append(HumanMessage(prompt))

                # ocr_context = f"OCR Data: {st.session_state.ocr_data}" if st.session_state.ocr_data else ""

                ocr_context = "OCR Data:\n" + "\n".join(st.session_state.ocr_data) if st.session_state.ocr_data else ""
                full_prompt = f"{ocr_context}\n\nUser Question: {prompt}"

                result = self.llm.invoke(st.session_state.messages + [HumanMessage(full_prompt)]).content

                with st.chat_message("assistant"):
                    st.markdown(result)
                st.session_state.messages.append(AIMessage(result))

            except Exception as e:
                error_message = f"Error processing prompt: {e}"
                logging.error(error_message)  
                st.error("An error occurred. Please try again later.") 
                return 

    def clear_message(self, **kwargs):
        """ Clear message, document queue, and OCR data """
        st.session_state.messages = [AIMessage(content="Welcome, How can I help you? ")]
        st.session_state.ocr_data = list()
        # st.session_state.doc_uploaded = list()  
        st.rerun()

    def upload_doc(self, **kwargs):
        """ upload document fun. """
        if st.session_state.doc_uploaded is not None:
            st.toast("Processing the uploaded documents. This may take a while....")
            progress_text = "operation in progress... "
            my_prog_bar = st.progress(0, text=progress_text)

            for file in st.session_state.doc_uploaded:
                try:

                    print(file.name)
                    bytes_data = file.read()
                    success = self.save_file(file_data= bytes_data, file_name=file.name, st=st)
                    
                    img_dict, raw_ocr_data, clean_ocr_data = self.create_image(file.name)

                    if clean_ocr_data and isinstance(clean_ocr_data, list):
                        st.session_state.ocr_data.extend(clean_ocr_data) 

                    st.write(f"Images: {len(img_dict)}")
                    
                except Exception as e:
                    print("error : ", e)
                    print(traceback.format_exc())
                    continue

            my_prog_bar.empty()
            
    def run(self):
        """Runs the Streamlit chatbot application.  Sets the title, displays messages, and processes user input."""

        st.title("Chatbot")

        with st.sidebar:
            st.session_state.model_name = st.selectbox("Select LLM", ('llama-3.2:1b', 'moondream'))
            st.file_uploader("Upload documents", type=["pdf","png", "jpg"], key="doc_uploaded", on_change=self.upload_doc, accept_multiple_files=True)
            st.button("Clear", on_click=self.clear_message)

        self.display_messages()
        prompt = st.chat_input("How are you?")
        self.process_prompt(prompt)


if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.run()

