\# Day 1 Analysis: Plain Chatbot vs Rule-Based Workflow vs AI Agent



\## 1. Scenario



The scenario used in this project is a \*\*Personal Course Advisor\*\*.



A private course database is stored in `data/courses.json`. It contains:



\* Course name

\* Fee

\* Duration

\* Level

\* Prerequisite



The same user request is tested using three different approaches:



> \*\*Which two courses can I take together within a budget of ₹30,000?\*\*



The three approaches are:



1\. Plain Chatbot

2\. Rule-Based Workflow

3\. AI Agent



\---



\## 2. Plain Chatbot



\### How it works



The plain chatbot uses an LLM to understand the user's question and generate a response.



In this implementation, the chatbot does \*\*not\*\* have access to the private `courses.json` database.



The user sends a question to the LLM, and the LLM generates a response based on the information available in its context.



\### Data and Private Data Access



The chatbot does not directly access the private course database.



Therefore, it cannot reliably know the actual course fees, durations, or prerequisites stored in `courses.json`.



\### Tools and Rules



No external tools are provided to the chatbot.



There are also no predefined programming rules for calculating course combinations.



\### Request Handling



The process is:



1\. User enters a question.

2\. The question is sent to the LLM.

3\. The LLM generates a response.

4\. The response is displayed to the user.



\### Limitations



\* Cannot directly access private course data.

\* May ask for additional information instead of answering the exact database question.

\* May generate information that is not present in the private database.

\* Cannot perform reliable database-based calculations without additional tools or data.



\---



\## 3. Rule-Based Workflow



\### How it works



The rule-based workflow uses predefined Python logic to access the private course database and calculate valid course combinations.



The workflow does not use an LLM.



\### Data and Private Data Access



The Python program directly reads:



`data/courses.json`



It retrieves the course information and checks combinations of two courses.



\### Tools and Rules



The workflow uses fixed programming rules.



For example:



\* Select two courses.

\* Add their fees.

\* Check whether the total is less than or equal to ₹30,000.

\* Display the valid combinations.



\### Request Handling



The process is:



1\. Load the private course data.

2\. Set the budget to ₹30,000.

3\. Generate pairs of courses.

4\. Calculate the combined fee for each pair.

5\. Check the predefined budget condition.

6\. Display valid pairs.



\### Limitations



\* The logic is fixed in advance.

\* It does not naturally understand varied user language.

\* New types of questions require additional programming rules.

\* It cannot dynamically decide which tool or action is required.



\---



\## 4. AI Agent



\### How it works



The AI agent combines:



\*\*LLM + Tools + Loop\*\*



The LLM understands the user's request and decides whether a tool is required.



In this project, the agent has access to a course-search tool called:



`find\_course\_pairs`



The tool accesses the private course data and returns valid course combinations.



\### Data and Private Data Access



The agent does not directly place all private data into the LLM prompt.



Instead, the LLM can use a tool that accesses the private course database.



The tool reads `data/courses.json` and returns the required information.



\### Tools and Decision-Making



The LLM decides whether to use the available tool.



For the test question about course combinations and budget, the LLM selects the `find\_course\_pairs` tool.



The tool calculates the valid combinations and returns the result.



\### Request Handling



The process is:



1\. User sends a natural-language request.

2\. The LLM interprets the request.

3\. The LLM decides whether a tool is needed.

4\. The course-search tool is selected.

5\. The tool accesses the private course data.

6\. The tool calculates the valid course combinations.

7\. The tool result is returned to the LLM.

8\. The LLM processes the result.

9\. The final answer is provided to the user.



\### Loop



The agent follows an LLM-tool-observation loop.



The loop allows the agent to continue working when additional tool calls are required.



For this simple scenario, only one tool call is required before producing the final answer.



\### Limitations



\* Depends on the LLM correctly understanding the request.

\* Tool-selection errors are possible.

\* LLM responses may still be incorrect if the tool result is misunderstood.

\* API failures or unavailable tools can affect the result.

\* More complex agent systems require additional safeguards and validation.



\---



\## 5. Comparison



| Basis                    | Plain Chatbot                     | Rule-Based Workflow                    | AI Agent                                   |

| ------------------------ | --------------------------------- | -------------------------------------- | ------------------------------------------ |

| Flexibility              | High for conversation             | Low because logic is predefined        | High because the LLM can adapt to requests |

| Decision-making          | Generates responses from context  | Uses fixed conditions                  | LLM can decide which tool/action is needed |

| Tool usage               | No tool                           | Fixed Python logic                     | LLM-selected tool                          |

| Private-data access      | No access in this implementation  | Direct access to JSON                  | Access through a tool                      |

| Multi-step task handling | Limited                           | Possible only through predefined steps | Can perform iterative tool-based tasks     |

| Automation               | Mainly response generation        | High for predefined tasks              | High for dynamic tasks                     |

| Reliability              | Can produce unsupported responses | Predictable for programmed cases       | Flexible but depends on LLM and tools      |



\---



\## 6. Suitability Analysis



\### Plain Chatbot



A plain chatbot is suitable when:



\* The user needs general explanations.

\* No private or external data is required.

\* The task mainly involves conversation, brainstorming, or summarization.

\* Tool-based actions are not necessary.



\### Rule-Based Workflow



A rule-based workflow is suitable when:



\* The process is predictable.

\* The rules are clearly defined.

\* Deterministic results are important.

\* The same steps are repeated regularly.

\* Auditability and control are important.



\### AI Agent



An AI agent is suitable when:



\* Users may express requests in different ways.

\* The task requires private or external data.

\* Tools need to be selected dynamically.

\* Multiple steps may be required.

\* The system needs to adapt its actions based on intermediate results.



\---



\## 7. Which Approach Fits This Scenario?



The three approaches demonstrate different capabilities.



The plain chatbot can understand the question conversationally, but it does not have access to the private course database in this implementation.



The rule-based workflow can access the private data and produce deterministic results, but its behaviour is predefined and less flexible.



The AI agent combines natural-language understanding with tool access. It can interpret the request, select the appropriate course-search tool, receive the private-data result, and generate a final response.



Therefore, the project demonstrates the key difference between:



\* \*\*LLM-only interaction\*\*

\* \*\*Predefined program logic\*\*

\* \*\*LLM + Tools + Loop\*\*



\---



\## 8. Conclusion



A plain chatbot is useful for general conversational tasks where private data and external actions are not required.



A rule-based workflow is useful for fixed, predictable tasks where predefined rules provide reliable and controllable behaviour.



An AI agent is useful for dynamic tasks where an LLM needs to understand a request, select tools, access information, observe results, and continue until the task is completed.



This project demonstrates that an AI agent is not simply a chatbot. The important difference is the combination of an \*\*LLM, tools, and an execution loop\*\* that allows the system to take actions based on the user's request.
