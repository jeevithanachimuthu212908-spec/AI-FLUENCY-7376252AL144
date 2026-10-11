\# Agentic AI Day 1 - Course Advisor



\## Scenario



This project compares three approaches for answering course-related questions using a private course database:



1\. Plain Chatbot

2\. Rule-Based Workflow

3\. AI Agent



\## Private Data



The private course information is stored in:



`data/courses.json`



It contains course names, fees, duration, level, and prerequisites.



\## Test Question



> Which two courses can I take together within a budget of ₹30,000?



\## Approaches



\### 1. Plain Chatbot



Uses an LLM without access to the private course database.



\### 2. Rule-Based Workflow



Uses predefined Python rules to read the private course data and find valid course combinations.



\### 3. AI Agent



Uses:



\*\*LLM + Tools + Loop\*\*



The LLM decides when to use the course-search tool, the tool accesses the private data, and the LLM uses the tool result to produce the final response.



\## Project Structure



```text

day1\_task/

├── data/

│   └── courses.json

├── Output/

│   ├── chatbot.png

│   ├── workflow.png

│   └── agent.png

├── chatbot.py

├── workflow.py

├── tools.py

├── agent.py

├── analysis.md

├── README.md

├── requirements.txt

└── .gitignore
