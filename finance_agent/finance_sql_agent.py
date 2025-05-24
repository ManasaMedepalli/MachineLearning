from langchain_community.llms import Ollama
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit, SQLDatabase
from langchain.agents import initialize_agent, AgentType
import os
from dotenv import load_dotenv

load_dotenv()

db_uri = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
db = SQLDatabase.from_uri(db_uri)

llm = Ollama(model="llama3")  # You can try mistral/gemma here too

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# question = "What is the average closing price of AAPL in 2023?"
#add more context to the question
question = (
    "The table is called mag7 and it contains columns: ticker, date, open, high, low, close, volume, change_percent. "
    "Query the average closing price for AAPL in 2023 using this table."
)

response = agent.run(question)
print(f"🔍 Answer: {response}")
