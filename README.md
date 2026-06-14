# Smart College Assistant using LangChain Tool Calling Agent

This project implements a production-quality LangChain Tool Calling Agent designed to assist students with various college-related calculations. It relies exclusively on the LangChain `create_tool_calling_agent` API and Ollama for local LLM inference.

## Architecture & Logic

This application defines 6 distinct tools using the LangChain `@tool` decorator, integrating them into an agent execution loop:

1. **Attendance Calculator** (`attendance_calculator`): Evaluates attendance percentage and verifies eligibility (`>= 75%`).
2. **Result Calculator** (`result_calculator`): Computes average marks across 5 subjects, determines passing status (`>= 50%`), and assigns a grade based on custom criteria.
3. **Fee Balance Calculator** (`fee_balance_calculator`): Subtracts paid fees from total course fees to calculate the pending balance.
4. **Library Fine Calculator** (`library_fine_calculator`): Calculates library fines (`$5 / day`) based on delayed days.
5. **Hostel Fee Calculator** (`hostel_fee_calculator`): Multiplies monthly fee by months stayed to compute total hostel rent.
6. **Student Information Tool** (`student_information_tool`): Retrieves hardcoded database entries for student details based on a student ID.

The `qwen3:4b` model (hosted locally via Ollama) processes user queries. The agent understands which tools to trigger based on user intent, and even coordinates multiple tools in parallel/sequence for multi-part requests.

---

## 🛠️ Requirements & Dependencies

*   **Python:** 3.12 or newer
*   **Package Manager:** [uv](https://github.com/astral-sh/uv) (blazing fast Python packaging)
*   **LLM Engine:** [Ollama](https://ollama.com/) (running `qwen3:4b`)

### Required Python Packages
*   `langchain`
*   `langchain-core`
*   `langchain-community`
*   `langchain-ollama`

---

## ⚙️ Installation Instructions

### 1. Install Ollama and Pull the Model
First, ensure you have Ollama installed on your system. 
1. Download Ollama from the [official website](https://ollama.com/download) and install it.
2. Open your terminal or command prompt and run the following command to download the highly capable `qwen3:4b` model:

```bash
ollama pull qwen3:4b
```
*(Ensure the Ollama application is running in the background).*

### 2. Set Up the Project Environment
We use `uv` for dependency management. If you don't have `uv` installed, you can install it using pip (`pip install uv`).

Navigate to the project directory and install the required dependencies:

```bash
uv add langchain langchain-core langchain-community langchain-ollama
```

---

## 🚀 Running the Project

To execute the smart college assistant and run all predefined assignment test cases, run:

```bash
uv run main.py
```

---

## 📸 Screenshot Instructions for Assignment Submission

When submitting this project for grading:
1. Ensure the `qwen3:4b` model is downloaded and Ollama is running.
2. Run `uv run main.py` in your terminal.
3. **Capture Screenshots:**
   * Take a screenshot showing the dependency installation success (optional but recommended).
   * Take a screenshot of the `Multi Tool Challenge` output to prove the agent can successfully invoke multiple tools correctly (Attendance + Result + Fees) in a single request.
   * Make sure the `verbose=True` output (highlighting the "Invoking: `tool_name` with..." logs) is visible in your screenshots to demonstrate that `create_tool_calling_agent` is being properly utilized.
4. Package the `main.py`, `pyproject.toml`, `README.md`, and the screenshots into a zip file for your submission.

---

## 📊 Sample Output

Below is a snippet of what you can expect when running the application (especially for the multi-tool challenge):

```text
==================================================
Running Query 6 / Multi Tool Challenge if last
==================================================
Query: I attended 80 classes out of 100.
My marks are 90, 85, 88, 92 and 95.
My course fee is 60000 and I paid 45000.

Provide:
1. Attendance Status
2. Grade
3. Pending Fee


> Entering new AgentExecutor chain...

Invoking: `attendance_calculator` with `{'attended_classes': 80, 'total_classes': 100}`
...
Invoking: `result_calculator` with `{'marks': [90, 85, 88, 92, 95]}`
...
Invoking: `fee_balance_calculator` with `{'paid_fee': 45000, 'total_fee': 60000}`
...

Final Response:

1. Attendance Status: Eligible for Exam (Attendance Percentage: 80.00%)
2. Grade: Grade A (Average: 90.00)
3. Pending Fee: 15000.00

> Finished chain.
```
