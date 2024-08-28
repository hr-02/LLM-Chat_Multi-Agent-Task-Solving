
# AI Crew for Matching CVs to Job Proposals
## Introduction
This project demonstrates the use of the CrewAI framework to automate the process of matching CVs to job proposals. CrewAI orchestrates autonomous AI agents, enabling them to collaborate and execute complex tasks efficiently.

- [CrewAI Framework](#crewai-framework)
- [Running the script](#running-the-script)
- [Details & Explanation](#details--explanation)


## CrewAI Framework
CrewAI is designed to facilitate the collaboration of role-playing AI agents. In this example, these agents work together to extract relevant information from CVs and match them to job opportunities, ensuring the best fit between candidates and job roles.

## Running the Script


- **Configure Environment**: 
- **Install Dependencies**: Run `poetry lock && poetry install`.
- **Execute the Script**: Run `poetry run match_to_proposal` and input your project details.

## Details & Explanation
- **Running the Script**: Execute `poetry run match_to_proposal`. The script will leverage the CrewAI framework to match CVs to job proposals and generate a detailed report.
- **Key Components**:
  - `src/match_to_proposal/main.py`: Main script file.
  - `src/match_to_proposal/crew.py`: Main crew file where agents and tasks come together, and the main logic is executed.
  - `src/match_to_proposal/config/agents.yaml`: Configuration file for defining agents.
  - `src/match_to_proposal/config/tasks.yaml`: Configuration file for defining tasks.
  - `src/match_to_proposal/tools`: Contains tool classes used by the agents.


