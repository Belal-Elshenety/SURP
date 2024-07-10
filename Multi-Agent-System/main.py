from crewai import Crew, Process 
from agents import SARAgents
from tasks import SARTasks

class SARCrew:
    def __init__(self, inputs):
        self.inputs = inputs
        self.agents = SARAgents()
        self.tasks = SARTasks()

    def run_drug(self):
        # Initialize agents
        drug_analyst = self.agents.drug_analyst()

        # Initialize tasks with respective agents
        drug_analysis_task = self.tasks.drug_analysis(drug_analyst, self.inputs[0])

        # Form the crew with defined agents and tasks
        crew = Crew(
            agents=[drug_analyst],
            tasks=[drug_analysis_task],
            max_rpm=30,
            process= Process.sequential,
        )
        # Execute the crew to carry out the research project
        return crew.kickoff()
    def run_question(self):
        document_analyst = self.agents.document_analyst()
        document_analysis_task = self.tasks.document_analysis(document_analyst, self.inputs[0])

        crew = Crew(
            agents=[document_analyst],
            tasks=[document_analysis_task],
            max_rpm=30,
            process= Process.sequential,
        )
        return crew.kickoff()



if __name__ == "__main__":
    print("Welcome to the SAR Crew Setup")
    print("---------------------------------------")
    drugs = input("Please enter the drugs the missing person is taking:")
    questions = input("Please enter any additional question that you have:")

    inputs = [drugs, questions]
    sar_crew = SARCrew(inputs)
    result = sar_crew.run()

    print("\n\n##############################")
    print("## Here are the results of your intelligent search:")
    print("##############################\n")
    print(result)
