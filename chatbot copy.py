import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import urllib.parse
import speech_recognition as sr

# Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='NASA_Hackathon_Challenges',
            user='root',
            password='3172004@mysql'
        )
        return connection
    except Error as e:
        st.error(f"Database Error: {e}")
        return None

# Function to initialize the database connection
def init_database(user: str, password: str, host: str, port: str, database: str) -> SQLDatabase:
    encoded_password = urllib.parse.quote_plus(password)
    db_uri = f"mysql+mysqlconnector://{user}:{encoded_password}@{host}:{port}/{database}"
    return SQLDatabase.from_uri(db_uri)


#Based on the table schema below, generate the necessary query that would answer the user's question. Consider the conversation history.

# Function to get the SQL chain for handling queries
def get_sql_chain(db):
    template = """
        You are a chatbot at NASA's Space Apps Hackathon. You are interacting with a participants who is asking you questions about the challenges database and the nasa space apps hackathon.
        
        Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.
        
        <SCHEMA>{schema}</SCHEMA>
        
        Conversation History: {chat_history}
        
        Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.
        
        For example:
        Question: What are the potential considerations for a challenge?
        SQL Query: SELECT PotentialConsiderations FROM Consideration WHERE ChallengeID = 'Challenge ID';
        
        Your turn:
        
        Question: {question}
        SQL Query:
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.7)
    
    def get_schema(_):
        return db.get_table_info()
    
    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

# Dummy classifier to determine if a question is related to the database
def classify_question(question: str) -> bool:
    return True

# Function to handle user queries and generate responses
def get_response(user_query: str, db: SQLDatabase, chat_history: list):
    sql_chain = get_sql_chain(db)
    
    template = """
        You are a chatbot at NASA's Space Apps Hackathon. You are interacting with a the competitors who is asking you questions about the challenges database.
        
        Based on the table schema below, question, SQL query, and SQL response, write a natural language response.
        
        <SCHEMA>{schema}</SCHEMA>
        Conversation History: {chat_history}
        SQL Query: <SQL>{query}</SQL>
        User question: {question}
        SQL Response: {response}
    """
    
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.5)
    
    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: db.get_table_info(),
            response=lambda vars: db.run(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })

# Function to recognize speech input
def recognize_speech():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        st.info("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        st.info("Recognizing...")
        query = recognizer.recognize_google(audio)
        st.success(f"Recognized: {query}")
        return query
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        st.error("Could not request results from Google Speech Recognition service.")
        return None

# Main function to run the chatbot interface
def chatbot_page():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm a Chatbot at NASA's Space Apps Hackathon. Ask me anything about our challenges."),
        ]

    if "db" not in st.session_state:
        st.session_state.db = None

    load_dotenv()

    st.title("NASA Space Apps Hackathon Challenge Chatbot")

    with st.sidebar:
        st.subheader("Settings")
        st.write("This is a chat application using MySQL to interact with the NASA Space Apps Hackathon Challenges database.")
        
        host = st.text_input("Host", value="localhost", key="Host")
        port = st.text_input("Port", value="3306", key="Port")
        user = st.text_input("User", value="root", key="User")
        password = st.text_input("Password", value="3172004@mysql", key="Password")
        database = st.text_input("Database", value="NASA_Hackathon_Challenges", key="Database")
        
        if st.button("Connect"):
            with st.spinner("Connecting to database..."):
                db = init_database(
                    st.session_state["User"],
                    st.session_state["Password"],
                    st.session_state["Host"],
                    st.session_state["Port"],
                    st.session_state["Database"]
                )
                st.session_state.db = db
                st.success("Connected to database!")
        
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)

    user_query = st.chat_input("Type a message...")
    if user_query is not None and user_query.strip() != "":
        if st.session_state.db:
            st.session_state.chat_history.append(HumanMessage(content=user_query))
            
            with st.chat_message("Human"):
                st.markdown(user_query)
                
            with st.chat_message("AI"):
                response = get_response(user_query, st.session_state.db, st.session_state.chat_history)
                st.markdown(response)
                
            st.session_state.chat_history.append(AIMessage(content=response))
        else:
            st.error("Please connect to the database first.")

    if st.button("Speak a message"):
        spoken_query = recognize_speech()
        if spoken_query:
            if st.session_state.db:
                st.session_state.chat_history.append(HumanMessage(content=spoken_query))
                
                with st.chat_message("Human"):
                    st.markdown(spoken_query)
                    
                with st.chat_message("AI"):
                    response = get_response(spoken_query, st.session_state.db, st.session_state.chat_history)
                    st.markdown(response)
                    
                st.session_state.chat_history.append(AIMessage(content=response))
            else:
                st.error("Please connect to the database first.")

if __name__ == "__main__":
    chatbot_page()
