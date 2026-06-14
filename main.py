import sys
import io
from typing import List

# Fix for Windows UnicodeEncodeError with emojis/special characters
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent


# ==========================================
# 1. Tool Definitions
# ==========================================

@tool
def attendance_calculator(total_classes: int, attended_classes: int) -> str:
    """Calculates attendance percentage and checks eligibility for exams.
    
    Args:
        total_classes: The total number of classes.
        attended_classes: The number of classes the student attended.
    """
    attendance_percentage = (attended_classes / total_classes) * 100
    if attendance_percentage >= 75:
        status = "Eligible for Exam"
    else:
        status = "Not Eligible for Exam"
    return f"Attendance Percentage: {attendance_percentage:.2f}%\nEligibility Status: {status}"


@tool
def result_calculator(marks: List[float]) -> str:
    """Calculates the average marks, final grade, and pass/fail status.
    
    Args:
        marks: A list of exactly five subject marks.
    """
    average = sum(marks) / len(marks)
    
    # Grade Rules
    if average >= 90:
        grade = "Grade A"
    elif average >= 75:
        grade = "Grade B"
    elif average >= 60:
        grade = "Grade C"
    else:
        grade = "Grade D"
        
    # Pass Rule
    if average >= 50:
        status = "Pass"
    else:
        status = "Fail"
        
    return f"Average: {average:.2f}\nGrade: {grade}\nStatus: {status}"


@tool
def fee_balance_calculator(total_fee: float, paid_fee: float) -> str:
    """Calculates the pending fee amount for a student.
    
    Args:
        total_fee: The total course fee.
        paid_fee: The amount the student has already paid.
    """
    pending_fee = total_fee - paid_fee
    return f"Pending Fee Amount: {pending_fee}"


@tool
def library_fine_calculator(delayed_days: int) -> str:
    """Calculates the library fine amount based on delayed days.
    
    Args:
        delayed_days: The number of days the book return is delayed.
    """
    fine = delayed_days * 5
    return f"Fine Amount: {fine}"


@tool
def hostel_fee_calculator(monthly_fee: float, months_stayed: int) -> str:
    """Calculates the total hostel fee based on monthly rent and duration of stay.
    
    Args:
        monthly_fee: The fee per month for the hostel.
        months_stayed: The number of months the student stayed.
    """
    hostel_fee = monthly_fee * months_stayed
    return f"Total Hostel Fee: {hostel_fee}"


# Student Information Database
students = {
    "101": {
        "name": "Rahul",
        "branch": "CSE",
        "year": "3rd"
    },
    "102": {
        "name": "Priya",
        "branch": "ECE",
        "year": "2nd"
    },
    "103": {
        "name": "Aman",
        "branch": "IT",
        "year": "4th"
    }
}


@tool
def student_information_tool(student_id: str) -> str:
    """Retrieves student details by their student ID.
    
    Args:
        student_id: The ID of the student to look up (e.g., '101', '102').
    """
    student = students.get(student_id)
    if student:
        return f"Student Details:\nName: {student['name']}\nBranch: {student['branch']}\nYear: {student['year']}"
    else:
        return f"Error: Student details for ID '{student_id}' not found."


# ==========================================
# 2. Agent Construction
# ==========================================

def create_college_assistant() -> AgentExecutor:
    """Creates and returns the LangChain Tool Calling Agent."""
    
    # Define LLM connection
    llm = ChatOllama(
        model="qwen3:4b",
        temperature=0
    )
    
    # List all available tools
    tools = [
        attendance_calculator,
        result_calculator,
        fee_balance_calculator,
        library_fine_calculator,
        hostel_fee_calculator,
        student_information_tool
    ]
    
    # Prompt Design
    system_prompt = (
        "You are Smart College Assistant.\n"
        "Your responsibility is to help students by using available tools.\n"
        "Always call tools whenever numerical calculations or student information retrieval is required.\n"
        "If multiple calculations are requested, call all required tools and provide a consolidated response.\n"
        "Never perform calculations manually when a tool is available."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    # Create Tool Calling Agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create Agent Executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )
    
    return agent_executor


# ==========================================
# 3. Interactive Mode
# ==========================================

def interactive_loop():
    """Enters an interactive loop for the student to prompt the agent."""
    
    agent_executor = create_college_assistant()
    
    print("\n==================================================")
    print("   Smart College Assistant - Interactive Mode")
    print("==================================================")
    print("Type 'exit' or 'quit' to close the application.")
    
    while True:
        try:
            user_input = input("\nEnter your query: ")
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye!")
                break
            
            if not user_input.strip():
                continue
                
            agent_executor.invoke({"input": user_input})
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    interactive_loop()
