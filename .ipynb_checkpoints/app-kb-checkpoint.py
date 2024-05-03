import streamlit as st
from streamlit_chat import message
import pandas as pd  # to create a dataframe for displaying all models from Bedrock
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.app_logo import add_logo
from BedrockResponse import BedrockProcessing
br=BedrockProcessing()

st.set_page_config(
    layout="wide"
)
model_name = "Claude3-sonnet"
col1, gap, col3 = st.columns([40, 1, 30])

    # Static component
with col1:

    # Build the icon + title
    c1, mid, c2 = st.columns([1, 1, 30])
    with c1:
        st.image("images.png", width = 50)
    with c2:
        st.title("Enterprise Metadata Evolution")

    # Application description
    # st.write("View a wide range of data details and explore the depths of Fannie Mae data with AI powered super search technology!")

    add_vertical_space(2)

    col1.header("Data Architecture")
    tab1, tab2 = st.tabs(["Parameters", "Columns"])

    tab1.subheader("Tune Parameters")
    max_gen_len = tab1.slider("Maximum Length Generation:", min_value=0, max_value=4096, value=(2048))
    temperature = tab1.slider("Temperature:", min_value=0.0, max_value=1.0, value=(0.3))
    top_p = tab1.slider("Top_p:", min_value=0.0, max_value=1.0, value=(0.5))
#     df = pd.read_csv("data/dataset_metadata.csv")
#     # df = df[['Dataset Name', 'Table Name', 'Dataset Reg ID', 'Dataset Description']]
#     df["show"] = False

#     table = tab1.data_editor(
#         df,
#         column_config = {
#             "show": st.column_config.CheckboxColumn(
#                 "Show Columns",
#                 help = "Select to show the columns in this table",
#                 default = False
#             )
#         },
#         disabled = ['Dataset Name', 'Table Name', 'Dataset Reg ID', 'Dataset Description'],
#         hide_index= True
#     )

#     selected_tables = table.loc[table['show'] == True]

#     tab2.subheader("Column Summary")
#     df2 = pd.read_csv("data/attribute_metadata.csv")
#     df2 = df2[['Physical Attribute Name', 'Logical Attribute Name', 'Description', 'Dataset Reg ID', 'DataType']]

#     col_df = selected_tables.merge(df2, on='Dataset Reg ID', how = 'left')
#     col_df = col_df[['Table Name', 'Physical Attribute Name', 'Logical Attribute Name', 'Description', 'DataType']]
#     col_df['show'] = False

#     table2 = tab2.data_editor(
#         col_df,
#         column_config = {
#             "show": st.column_config.CheckboxColumn(
#                 "Show Profile",
#                 help = "Select to show the profile for this column",
#                 default = False
#             )
#         },
#         disabled = ['Table Name', 'Physical Attribute Name', 'Logical Attribute Name', 'Description', 'DataType'],
#         hide_index= True
#     )

#     tab3.subheader("Profile Summary")
#     prof_tables = table2.loc[table2['show'] == True]

#     if prof_tables.shape[0] > 0:
#         selected = prof_tables.iloc[0]['Physical Attribute Name']
#         tab3.text(f"Showing profile information for column: {selected}")
#         tab3.text("")
#         tab3.text("Attribute Type: Continuous Number")
#         tab3.text("Minimum Value: 0")
#         tab3.text("Median Value: 500")
#         tab3.text("Maximum Value: 1000")    

# Chatbot Component
with col3:
    col3.header("AI Chatbot")
    col3.image("chatbot_image.jpeg", width = 70)
    overall_container = st.container(border=True)
    with overall_container:

        # Container for chat history
        response_container = st.container(height = 450)

        # container for user text
        container = st.container()
        
            
        with container:
            with st.form(key='my_form', clear_on_submit=True):
                prompt = st.text_input("Please enter your query:", max_chars=2000)
                with response_container:
                    if prompt:
                        st.text(f"Q: {prompt}")
                # user_input = st.text_input("Query:", placeholder="Ask questions here", key='input')
                submit_button = st.form_submit_button(label="Submit", type="primary")
                end_session_button = st.form_submit_button("End Session")
                

                # submit_button = st.button("Submit", type="primary")
        
    
            # if submit_button and user_input:
            #     output = conversational_chat(user_input)

# st.header("Bedrock Knowledgebase Semantic Search")

# def display_local_image(image_path, max_width=None, caption=None):
#     """Displays a local image on the Streamlit UI with customization options.

#     Args:
#         image_path (str): The path to the local image file.
#         max_width (int, optional): The maximum width for the image. Defaults to None.
#         caption (str, optional): A caption for the image. Defaults to None.
#     """

#     try:
#         with open(image_path, 'rb') as f:
#             image_data = f.read()
#             st.image(image_data, caption=caption, width=max_width)
#     except FileNotFoundError:
#         st.error(f"Image not found: {image_path}")
#     except Exception as e:
#         st.error(f"An error occurred displaying the image: {e}")

# # Choose the image path based on your environment
# image_path = 'bedrock-example.jpg'  # Replace with the actual path

# # Optional: Apply customization options
# max_width = 300  # Set a maximum width
# caption = "AWS Bedrock Architecture Pattern"  # Add a caption

#display_local_image(image_path, max_width, caption) 




#with st.chat_message("user"):
#    st.write("Hello 👋")
    
#prompt = st.chat_input("Say something")
#if prompt:
#    st.write(f"User has sent the following prompt: {prompt}")

    
# Display a text box for input
#col1, col2 = st.columns(2)

# Input elements placed in separate columns
#prompt = col1.text_input("Enter your query:", key="query")
#model_name = col2.selectbox("Select Model:", ["","Llama2_13B", "Claude21"], key="Model")
# prompt = st.text_input("Please enter your query", max_chars=2000)
# model_name = st.selectbox("Select Model:", ["","Llama2_13B", "Claude21","Claude3-sonnet"], key="Model")
# print(f"Model name selected = {model_name}")
prompt = prompt.strip()

#print(prompt)




# Session State Management
if 'history' not in st.session_state:
    st.session_state['history'] = []



# Handling user input and responses
if submit_button and prompt:
    event = {
        "sessionId": "MYSESSION",
        "question": prompt
    }

    print(event)
    #llama_response, location = br.get_response_from_becrock_model_llama2(prompt)

    bedrock_response =br.get_bedrock_model_response(prompt, model_name)
    print(f"bedrock_response type ={type(bedrock_response)}")
    print(f"response keys = {bedrock_response.keys()}")
    #print(bedrock_response)
    response = bedrock_response['response']
    #claude21_response = bedrock_response['claude21_response']
    location=bedrock_response['location']
    # Use trace_data and formatted_response as needed
    #st.sidebar.text_area("Trace Data", value=all_data, height=300)
    st.session_state['history'].append({"question": prompt, "answer": response, "model":model_name, "refrences":','.join(location)})
    st.session_state['trace_data'] = response


if end_session_button:
    st.session_state['history'].append({"question": "Session Ended", "answer": "Thank you for using Enterprise Architect Agent!"})
    event = {
        "sessionId": "MYSESSION",
        "question": "placeholder to end session",
        "endSession": True
    }
    #agenthelper.lambda_handler(event, None)
    st.session_state['history'].clear()

with response_container:
    for chat in reversed(st.session_state['history']):

        # Creating columns for Question
        print (f"chat keys = {chat.keys()}")
        # st.text(f"Q: {chat['question']}")
        st.text_area(f"{chat['model']}:", value=chat["answer"], height=100, key=str(chat)+"a")
# Display conversation history
st.write("## References")

for chat in reversed(st.session_state['history']):

    st.text_area("References:", value=chat["refrences"], height=20,key=str(chat)+"r", disabled=True)





# st.write("## Test Knowledge Base Prompts")
# st.markdown("""
# - "What is LTV in MISMO? "

# - "what is possible MISMO datapoint with definition as " the date the LTV was calculated"

# - "Identify the entities described by term BaseLTVRatioPercent in MISMO"

# - "Provide description for datapoint Orignial LTV indicator, what are proper mapping this data point to FIBO?"

# - "What concept or classes can BaseLTVRatioPercent be presented in FIBO"
# - "You are knowledge graph accesible via SPARQL. Your dataset is built using schema.org as the underlying structure, and using mf URIs in order to identify resources. Translate each prompt into SPARQL query and then prouce sample out from this query as Turtle. Continue until the words' end queries' are typed as a prompt"

# """)
