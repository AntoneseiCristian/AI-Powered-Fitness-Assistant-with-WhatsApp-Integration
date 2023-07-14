from langchain import PromptTemplate, LLMChain
from langchain.llms import GPT4All
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool

PATH = '/Users/antoneseicristian/Library/Application Support/nomic.ai/GPT4All/ggml-model-gpt4all-falcon-q4_0.bin'
llm = GPT4All(model=PATH, verbose=True)

agent_executor = create_python_agent(
    llm=llm,
    tool=PythonREPLTool(),
    verbose=True
)

def get_response(prompt):
    return agent_executor.run(prompt)


