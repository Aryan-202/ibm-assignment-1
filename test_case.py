import pytest   # type: ignore
from main import create_college_assistant

# Define the queries as requested by the assignment
queries = [
    {
        "id": "1_attendance",
        "prompt": "I attended 72 classes out of 90. Am I eligible for exams?",
        "expected_keywords": ["80", "Eligible"]
    },
    {
        "id": "2_results",
        "prompt": "My marks are 95, 90, 88, 91 and 87. What is my grade?",
        "expected_keywords": ["90", "Grade A"]
    },
    {
        "id": "3_fee",
        "prompt": "My course fee is 50000 and I have paid 35000. How much fee is pending?",
        "expected_keywords": ["15000"]
    },
    {
        "id": "4_library",
        "prompt": "I returned a library book 8 days late. What is the fine amount?",
        "expected_keywords": ["40"]
    },
    {
        "id": "5_hostel",
        "prompt": "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",
        "expected_keywords": ["30000"]
    },
    {
        "id": "6_multi_tool",
        "prompt": (
            "I attended 80 classes out of 100.\n"
            "My marks are 90, 85, 88, 92 and 95.\n"
            "My course fee is 60000 and I paid 45000.\n\n"
            "Provide:\n"
            "1. Attendance Status\n"
            "2. Grade\n"
            "3. Pending Fee"
        ),
        "expected_keywords": ["80", "Grade A", "15000", "Eligible"]
    }
]

@pytest.fixture(scope="module")
def agent():
    """Fixture to initialize the agent once for all tests."""
    return create_college_assistant()

@pytest.mark.parametrize("query_data", queries, ids=lambda q: q["id"])
def test_agent_responses(agent, query_data):
    """
    Test each assignment query against the LangChain Tool Calling Agent.
    Validates that the output is not empty and loosely contains expected calculations.
    """
    prompt = query_data["prompt"]
    expected_keywords = query_data.get("expected_keywords", [])
    
    # Invoke the agent
    response = agent.invoke({"input": prompt})
    
    # Ensure there is an output
    assert "output" in response
    output_text = response["output"]
    assert len(output_text.strip()) > 0, "Agent returned an empty response"
    
    # Clean the output to ignore commas in formatted numbers
    clean_output = output_text.lower().replace(",", "")
    
    # Check that expected calculation results/keywords appear in the final response
    for keyword in expected_keywords:
        assert keyword.lower() in clean_output, f"Expected to find '{keyword}' in response: {output_text}"

if __name__ == "__main__":
    import sys
    # -v for verbose output, -s to disable stdout capturing so the conversation prints in the terminal
    sys.exit(pytest.main(["-v", "-s", __file__]))
