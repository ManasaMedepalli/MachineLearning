import time
import os
from langchain_community.utilities import SQLDatabase
from langchain_ollama import OllamaLLM
# from langchain_community.chains.sql_database.base import SQLDatabaseChain
from langchain_experimental.sql import SQLDatabaseChain
# from langchain_community.chains import SQLDatabaseChain
#from langchain.chains import SQLDatabaseChain
from termcolor import colored
from dotenv import load_dotenv

load_dotenv()
# --- Config ---
db_uri = (
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
)
QUERY = "What is the average closing price of AAPL in 2023?"

MODELS = [
    "llama3",
    "mistral",
    "gemma",
    "phi3",
    "neural-chat",
    "codellama"
]

# --- Setup DB connection ---
db = SQLDatabase.from_uri(db_uri)

# --- Benchmarking function ---
def benchmark_model(model_name, db, query):
    try:
        llm = OllamaLLM(model=model_name)
        chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=False)
        start = time.time()
        response = chain.run(query)
        end = time.time()
        latency = round(end - start, 2)
        return {"model": model_name, "latency": latency, "response": response}
    except Exception as e:
        return {"model": model_name, "latency": -1, "response": f"Error: {str(e)}"}

# --- Run Benchmarks ---
print(colored("🔎 Starting Benchmarking...\n", "cyan", attrs=["bold"]))

for model in MODELS:
    print(colored(f"🚀 Testing Model: {model}", "yellow"))
    result = benchmark_model(model, db, QUERY)

    if result["latency"] >= 0:
        print(colored(f"✅ Model: {model}", "green"))
        print(colored(f"⏱️  Latency: {result['latency']}s", "magenta"))
        print(colored(f"📤 Response: {result['response']}", "cyan"))
    else:
        print(colored(f"❌ Model: {model} failed to run.", "red"))
        print(colored(f"🛑 Error: {result['response']}", "red"))

    print(colored("-" * 60, "white"))
    
print(colored("\n✅ Benchmarking complete.", "green", attrs=["bold"]))
