# Agentic AI: Foundations and Open-Source Practice

## Day 2 Assessment — Reasoning and Acting

### Scenario: College Library Book Purchase

This assessment compares three approaches for solving problems involving a college library:

1. Direct Prompting
2. Chain-of-Thought (CoT) Style Reasoning
3. ReAct (Reasoning and Acting)

A self-consistency experiment is also performed to study how temperature affects repeated reasoning results.

---

# 1. Scenario Description

The scenario is based on purchasing books from a college library.

The available books and their prices are:

| Book             |   Price |
| ---------------- | ------: |
| Python Basics    | Rs. 450 |
| Data Structures  | Rs. 600 |
| Machine Learning | Rs. 750 |

The assessment uses two types of questions.

### Question 1 — Tool-Based Question

> I have Rs. 1,200. Which two books can I buy together within my budget?

This question can benefit from external information or tools because the system needs to obtain and compare book prices.

The possible combinations are:

* Python Basics + Data Structures = Rs. 1,050
* Python Basics + Machine Learning = Rs. 1,200
* Data Structures + Machine Learning = Rs. 1,350

Therefore, the first two combinations are within the budget, while the third combination exceeds the budget.

### Question 2 — Reasoning Question

> I have Rs. 2,000. I buy a book for Rs. 750. After buying the book, I spend 20% of the remaining money on stationery. How much money is left?

The expected calculation is:

* Initial money = Rs. 2,000
* Money after buying the book = Rs. 2,000 − Rs. 750 = Rs. 1,250
* Stationery cost = 20% of Rs. 1,250 = Rs. 250
* Remaining money = Rs. 1,250 − Rs. 250 = Rs. 1,000

Expected answer: **Rs. 1,000**

---

# 2. Direct Prompting

## How it works

Direct prompting gives the complete question to the language model without explicitly asking it to perform a multi-step reasoning process or use tools.

In this project, the direct prompting program gives the model the book names, prices, and budget.

The model then generates an answer directly.

## Example

The prompt asks:

> I have Rs. 1,200. Which two books can I buy together within my budget?

The model compares the given prices and identifies the combinations that fit within the budget.

## Advantages

* Simple to implement.
* Fast to execute.
* Requires very little code.
* Suitable for straightforward questions.

## Limitations

* It does not automatically access external tools.
* The model depends on the information provided in the prompt.
* It may make calculation or reasoning mistakes.
* It is less suitable when information must be retrieved dynamically.

---

# 3. Chain-of-Thought Style Reasoning

## How it works

Chain-of-Thought style reasoning encourages the model to solve a problem step by step.

For this assessment, the reasoning question is:

> I have Rs. 2,000. I buy a book for Rs. 750. After buying the book, I spend 20% of the remaining money on stationery. How much money is left?

The model is instructed to provide a concise reasoning summary and final answer rather than exposing private internal chain-of-thought.

## Reasoning Process

The calculation is:

1. Start with Rs. 2,000.
2. Subtract the book price of Rs. 750.
3. Remaining money = Rs. 1,250.
4. Calculate 20% of Rs. 1,250.
5. Stationery cost = Rs. 250.
6. Subtract Rs. 250 from Rs. 1,250.
7. Final amount = Rs. 1,000.

## Advantages

* Useful for multi-step reasoning.
* Makes the solution structure easier to understand.
* Helps break a problem into smaller calculations.
* Useful for arithmetic and logical problems.

## Limitations

* Reasoning does not automatically provide current or external information.
* The model can still make mistakes.
* Longer reasoning can increase response time and token usage.
* The quality depends on the model's reasoning ability.

---

# 4. ReAct Agent

## How it works

ReAct stands for **Reasoning and Acting**.

A ReAct-style system combines reasoning with actions such as calling tools.

The general cycle is:

**Reason → Action → Observation → Reason → Final Answer**

For this project, the agent uses two tools:

### Tool 1 — `get_book_price`

This tool retrieves the price of a book from the predefined library catalog.

### Tool 2 — `calculator`

This tool performs arithmetic calculations safely.

The ReAct demonstration first obtains the prices of:

* Python Basics
* Data Structures
* Machine Learning

The observations are then given to the language model.

The model compares all possible pairs and determines which pairs are within the Rs. 1,200 budget.

## Tool Observations

| Book             | Observed Price |
| ---------------- | -------------: |
| Python Basics    |        Rs. 450 |
| Data Structures  |        Rs. 600 |
| Machine Learning |        Rs. 750 |

## Pair Comparison

| Combination                        |     Total | Result         |
| ---------------------------------- | --------: | -------------- |
| Python Basics + Data Structures    | Rs. 1,050 | Within budget  |
| Python Basics + Machine Learning   | Rs. 1,200 | Within budget  |
| Data Structures + Machine Learning | Rs. 1,350 | Exceeds budget |

## Final Result

The user can buy:

* **Python Basics + Data Structures**
* **Python Basics + Machine Learning**

The combination of Data Structures and Machine Learning exceeds the budget.

## Advantages

* Can use external tools.
* Reduces dependence on information stored only in the model.
* Useful for tasks involving calculations or data retrieval.
* Separates tool observations from the final response.
* More suitable for tasks requiring interaction with external systems.

## Limitations

* Requires additional implementation.
* Tool failures can affect the result.
* More steps can increase execution time.
* The agent needs proper tool definitions and input handling.

---

# 5. Self-Consistency Experiment

## Purpose

Self-consistency tests whether repeated reasoning attempts produce the same answer.

The reasoning question used is:

> I have Rs. 2,000. I buy a book for Rs. 750. After buying the book, I spend 20% of the remaining money on stationery. How much money is left?

The expected correct answer is:

**Rs. 1,000**

The program runs the question five times using a non-zero temperature of **0.8**.

It also runs the question once with **temperature 0**.

## Expected Observation

At temperature 0.8, the model may produce slightly different wording or reasoning across runs. The final numerical answer may remain the same.

The results should be recorded from the actual program output.

Example table:

| Run           | Temperature | Answer    | Correct? |
| ------------- | ----------: | --------- | -------- |
| 1             |         0.8 | Rs. 1,000 | Yes      |
| 2             |         0.8 | Rs. 1,000 | Yes      |
| 3             |         0.8 | Rs. 1,000 | Yes      |
| 4             |         0.8 | Rs. 1,000 | Yes      |
| 5             |         0.8 | Rs. 1,000 | Yes      |
| Temperature 0 |           0 | Rs. 1,000 | Yes      |

If the actual outputs differ, the table should be updated using the observed results.

## Majority Answer

The majority answer is determined by counting the answers produced by the five non-zero-temperature runs.

For this problem, the expected correct result is:

**Rs. 1,000**

## Temperature 0

At temperature 0, the model is expected to produce a more deterministic response.

Repeated execution with the same input and configuration will generally be more consistent than a higher-temperature configuration.

---

# 6. Comparison of the Three Approaches

| Feature              | Direct Prompting  | CoT Style            | ReAct                            |
| -------------------- | ----------------- | -------------------- | -------------------------------- |
| Reasoning depth      | Low to medium     | Medium to high       | Medium to high                   |
| Tool usage           | No                | No                   | Yes                              |
| External information | Depends on prompt | Depends on prompt    | Can retrieve using tools         |
| Calculation support  | Model-based       | Model-based          | Can use calculator tool          |
| Implementation       | Very simple       | Simple               | More complex                     |
| Speed                | Fast              | Usually slower       | Usually slower                   |
| Cost                 | Lower             | Can be higher        | Can be higher                    |
| Transparency         | Direct answer     | Reasoning summary    | Actions and observations visible |
| Suitable for         | Simple questions  | Multi-step reasoning | Tool-based tasks                 |

---

# 7. Reliability

### Direct Prompting

Direct prompting is reliable when all required information is already included in the prompt and the task is simple.

For example, the book prices are explicitly provided to the model.

### Chain-of-Thought Style

CoT-style reasoning can help with multi-step calculations by organizing the solution into smaller steps.

However, reasoning alone does not guarantee correctness.

### ReAct

ReAct can improve reliability when the task requires external information or calculations because the agent can obtain observations from tools instead of relying entirely on its internal knowledge.

However, the tools themselves must be correctly implemented.

---

# 8. Speed and Cost

Direct prompting generally requires the fewest steps and is therefore the simplest and fastest approach.

CoT-style reasoning may require more generated tokens because the model performs a structured reasoning process.

ReAct can require additional tool calls and model interactions. Therefore, it can take more time and computational resources.

The choice depends on whether the additional reasoning or tool usage is necessary for the task.

---

# 9. Transparency

Direct prompting mainly provides the final answer.

CoT-style reasoning provides a concise reasoning summary in this project, which makes the calculation easier to understand.

ReAct provides visible actions and observations, such as retrieving each book price. This makes the interaction between the model and tools easier to inspect.

Private chain-of-thought is not exposed; only concise reasoning summaries or tool observations are shown.

---

# 10. Suitability Analysis

### Direct Prompting

Suitable for:

* Simple questions
* Questions where all information is already provided
* Fast responses
* Basic information processing

### CoT Style Reasoning

Suitable for:

* Multi-step calculations
* Logical reasoning
* Problems requiring several intermediate steps
* Situations where the solution structure matters

### ReAct

Suitable for:

* Tool-based tasks
* Information retrieval
* Calculations requiring external tools
* Tasks involving multiple actions and observations
* Agentic workflows

---

# 11. General Conclusion

The experiment demonstrates that different prompting approaches are suitable for different types of problems.

Direct prompting is the simplest approach when the required information is already available.

CoT-style reasoning is useful for problems that require multiple reasoning steps, such as calculating the remaining money after buying a book and spending part of the remaining amount.

ReAct extends the process by allowing an AI system to interact with tools. In the library scenario, the agent retrieves book prices, observes the results, and then uses those observations to determine which book combinations fit within the budget.

Self-consistency demonstrates that non-zero temperature can produce variation between repeated responses, while temperature 0 generally produces more deterministic behavior.

Overall, the experiment shows the progression from:

**Prompt → Reason → Act with Tools**

This progression is an important foundation for understanding agentic AI systems.
