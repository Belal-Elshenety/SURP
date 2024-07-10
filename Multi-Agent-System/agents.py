from crewai import Agent
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os
from crewai_tools import SerperDevTool, WebsiteSearchTool, ScrapeWebsiteTool
from tools import query_vector_store

class SARAgents:

    def __init__(self):
        # Initialize tools if needed
        self.serper = SerperDevTool()
        self.web = WebsiteSearchTool()
        self.web_scrape = ScrapeWebsiteTool()

       # OpenAI Models
        self.gpt3 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.gpt4 = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.7)
        self.gpt3_5_turbo_0125 = ChatOpenAI(
            model_name="gpt-3.5-turbo-0125", temperature=0.7)
        self.gpt3_5_turbo_1106 = ChatOpenAI(
            model_name="gpt-3.5-turbo-1106", temperature=0.7)
        self.gpt3_5_turbo_instruct = ChatOpenAI(
            model_name="gpt-3.5-turbo-instruct", temperature=0.7)

        # Groq Models
        self.llama3_8b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get(
            "GROQ_API_KEY"), model_name="llama3-8b-8192")
        self.llama3_70b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get(
            "GROQ_API_KEY"), model_name="llama3-70b-8192")
        self.mixtral_8x7b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get(
            "GROQ_API_KEY"), model_name="mixtral-8x7b-32768")
        self.gemma_7b = ChatGroq(temperature=0.7, groq_api_key=os.environ.get(
            "GROQ_API_KEY"), model_name="gemma-7b-it")

        # CHANGE YOUR MODEL HERE
        self.selected_llm = self.llama3_70b

    def drug_analyst(self):
        # Detailed agent setup for the Research Expert
        return Agent(
            role='Drug Analyst',
            goal='To search quickely the web and find the effects of underdosing and overdosing every single drug the missing person is taking. Do not search too long just a quick search and summarize the findings. Output has to be bullet points and at bottom the sources of your information then : then links to original articles',
            backstory="You are a search and rescue agent specialized in searching for information on drugs and their effects as a part of the missing person health assesment crew",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=3,
            tools=[self.serper, self.web, self.web_scrape],
        )
    
    def document_analyst(self):
        return Agent(
            role='Document Analyst',
            goal='Combine both inputs into one big output.',
            backstory="Combine both inputs into one big output.",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=3,
            tools=[query_vector_store],
        )
    
    def writer_agent(self):
        return Agent(
            role='Writer',
            goal='To combine and format the outputs of the drug analyst and document analyst into a cohesive report.',
            backstory="You are an agent specializing in combining and formatting information from both agent. take it from them and output it as is",
            verbose=True,
            allow_delegation=False,
            llm=self.selected_llm,
            max_iter=3,
        )
