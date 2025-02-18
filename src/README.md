 ## Installation
    python packages 
        python 3.11
        langchain
        streamlit
        streamlit_chat
        langchain-community
    
    just use conda env backup if you use macbook.
    ```bash
        Conda env create -f env.yaml
    ```



## Ollama Instalation:
    Ollama is an simple and efficient way to deploy a LLM in CPU/GPU machines. It comes with default REST-API's to communicate with LLM. It is not a production ready pipeline. 
    
    Follow thee instllation instruction given in the attached link : https://github.com/ollama/ollama?tab=readme-ov-file
    I used the docker-cpu version.

## Ollama Model Selection
    Select the best model according to the requirement and the hardware availability from the link: https://ollama.com/library

    I have used llama3.2-1b model. Its a 4bit quantized model. Its a relatively good model considering the benchmark scores and it comes it resonable context length. I also have problems with GPU machine, thats why I went with 1billion-CPU-q4 model. 


## To run the project
    Configure the "base_url" and "model" parameters in "__init__" function 
    Open the terminal and run "streamlit run app.py"



#TODO 

    1. In the above project i'm ot considering the chat length.
    2. Input Validation, cleaning and sanitization.
    3. Context management and guard rails for keep the model to alighn with the query.
    4. Async operation and rate limiting for scalability.
    5. Caching for repeated query.
    6. HW data pipeline. For this requirement, we havt to use either MM-LLM or propriatory OCR api.
    
