from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import get_web_search_tool, scrape_url 

#1st agent 
def build_search_agent(google_api_key: str, tavily_api_key: str, model_name: str = "gemini-flash-latest"):
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=google_api_key)
    web_search = get_web_search_tool(tavily_api_key)
    return create_agent(
        model = llm,
        tools= [web_search]
    )

#2nd agent 

def build_reader_agent(google_api_key: str, model_name: str = "gemini-flash-latest"):
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=google_api_key)
    return create_agent(
        model = llm,
        tools = [scrape_url]
    )


#writer chain 

def get_writer_chain(google_api_key: str, model_name: str = "gemini-flash-latest"):
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=google_api_key)
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
        ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
    ])

    return writer_prompt | llm | StrOutputParser()

#critic_chain 

def get_critic_chain(google_api_key: str, model_name: str = "gemini-flash-latest"):
    llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=google_api_key)
    critic_prompt = ChatPromptTemplate.from_messages([
         ("system", "You are a sharp and constructive research critic. Be honest and specific."),
        ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
    ])

    return critic_prompt | llm | StrOutputParser()
