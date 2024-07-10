from crewai import Task
class SARTasks:

    def drug_analysis(self, agent, inputs):
        return Task(
            agent=agent,
            description=f"Look through the list of medicines the missing person takes: {inputs}. Based on the results, find out the effects of overdosing and underdosing each drug through a google search.",
            expected_output=f"A list of the effects of overdosing and underdosing each drug the missing person takes. sources of information and links to the original articles. Prioritize these sources: WebMD, Drugs.com, Mayo Clinic, and PubMed.")

    def document_analysis(self, agent, inputs):
        return Task(
            agent=agent,
            description=f"Query {inputs} in the vector store and returing the information without any changes.",
            expected_output="To pass the information you get from vector store without any changes."
        )