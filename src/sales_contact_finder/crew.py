import os

from composio_crewai import Action, App, ComposioToolSet
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv

load_dotenv()

print("Loading environment variables...")
composio_api_key = os.getenv("COMPOSIO_API_KEY")
if not composio_api_key:
    raise ValueError("COMPOSIO_API_KEY not found in environment variables")

print(f"Initializing ComposioToolSet with API key: {composio_api_key[:8]}...")
composio_toolset = ComposioToolSet(api_key=composio_api_key)
tools = composio_toolset.get_tools(
    actions=[
        "FILETOOL_CREATE_FILE",
        "FILETOOL_WRITE",
        "EXA_SEARCH",
        "GOOGLEDRIVE_CREATE_FOLDER",
        "GOOGLEDRIVE_FIND_FOLDER",
        "GOOGLEDRIVE_UPLOAD_FILE",
        "SLACK_SENDS_A_MESSAGE_TO_A_SLACK_CHANNEL",
    ]
)
print("Got tools:", [t.name for t in tools])


@CrewBase
class SalesContactFinderCrew:
    """SalesContactFinder crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def company_researcher(self) -> Agent:
        print("Creating company_researcher agent...")
        return Agent(
            config=self.agents_config["company_researcher"],
            tools=tools,
            llm="o3-mini",
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def org_structure_analyst(self) -> Agent:
        print("Creating org_structure_analyst agent...")
        return Agent(
            config=self.agents_config["org_structure_analyst"],
            tools=tools,
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def contact_finder(self) -> Agent:
        print("Creating contact_finder agent...")
        return Agent(
            config=self.agents_config["contact_finder"],
            tools=tools,
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def sales_strategist(self) -> Agent:
        print("Creating sales_strategist agent...")
        return Agent(
            config=self.agents_config["sales_strategist"],
            tools=tools,
            allow_delegation=False,
            verbose=True,
        )

    @task
    def research_company_task(self) -> Task:
        print("Creating research_company_task...")
        return Task(
            config=self.tasks_config["research_company_task"],
            agent=self.company_researcher(),
        )

    @agent
    def brand_alignment_agent(self) -> Agent:
        print("Creating brand_alignment_agent agent...")
        return Agent(
            config=self.agents_config["brand_alignment_agent"],
            tools=tools,
            llm="o3-mini",
            allow_delegation=False,
            verbose=True,
        )

    @task
    def analyze_org_structure_task(self) -> Task:
        print("Creating analyze_org_structure_task...")
        return Task(
            config=self.tasks_config["analyze_org_structure_task"],
            agent=self.org_structure_analyst(),
        )

    @task
    def find_key_contacts_task(self) -> Task:
        print("Creating find_key_contacts_task...")
        return Task(
            config=self.tasks_config["find_key_contacts_task"],
            agent=self.contact_finder(),
        )

    @task
    def develop_approach_strategy_task(self) -> Task:
        print("Creating develop_approach_strategy_task...")
        return Task(
            config=self.tasks_config["develop_approach_strategy_task"],
            agent=self.sales_strategist(),
            output_file="buyer_contact.md",
        )

    @task
    def create_branded_report_website_task(self) -> Task:
        print("Creating create_branded_report_website_task...")
        return Task(
            config=self.tasks_config["create_branded_report_website_task"],
            agent=self.sales_strategist(),
            output_file="final_report.html",
        )

    @task
    def generate_prospecting_report_task(self) -> Task:
        print("Creating generate_prospecting_report_task...")
        return Task(
            config=self.tasks_config["generate_prospecting_report_task"],
            agent=self.sales_strategist(),
            output_file="mattress_king_prospecting_report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SalesContactFinder crew"""
        print("Creating crew with agents and tasks...")
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
