# Assignment Test Results

This document records the exact execution results and LLM outputs for each of the test queries required by the assignment. The tests verify that the Smart College Assistant correctly invokes the relevant LangChain tools.

You can automatically verify these tests yourself by running:
```bash
uv run pytest -v test_case.py
```

## Test Case 1: Attendance Query
**Prompt:** `I attended 72 classes out of 90. Am I eligible for exams?`

**Tools Invoked:** 
- `attendance_calculator` with `{"total_classes": 90, "attended_classes": 72}`

**Expected Output Calculation:** 
- Percentage = 80.00%
- Eligible >= 75% -> Eligible

**Result Snippet:**
> Attendance Percentage: 80.00%
> Eligibility Status: Eligible for Exam
> The student is eligible for the exams.

---

## Test Case 2: Results Query
**Prompt:** `My marks are 95, 90, 88, 91 and 87. What is my grade?`

**Tools Invoked:** 
- `result_calculator` with `{"marks": [95, 90, 88, 91, 87]}`

**Expected Output Calculation:** 
- Average = 90.20
- Grade = A

**Result Snippet:**
> Average: 90.20
> Grade: Grade A
> Status: Pass

---

## Test Case 3: Fee Balance Query
**Prompt:** `My course fee is 50000 and I have paid 35000. How much fee is pending?`

**Tools Invoked:** 
- `fee_balance_calculator` with `{"total_fee": 50000.0, "paid_fee": 35000.0}`

**Expected Output Calculation:** 
- Pending = 50000 - 35000 = 15000

**Result Snippet:**
> Pending Fee Amount: 15000.0

---

## Test Case 4: Library Fine Query
**Prompt:** `I returned a library book 8 days late. What is the fine amount?`

**Tools Invoked:** 
- `library_fine_calculator` with `{"delayed_days": 8}`

**Expected Output Calculation:** 
- Fine = 8 * 5 = 40

**Result Snippet:**
> Fine Amount: 40

---

## Test Case 5: Hostel Fee Query
**Prompt:** `Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.`

**Tools Invoked:** 
- `hostel_fee_calculator` with `{"monthly_fee": 6000.0, "months_stayed": 5}`

**Expected Output Calculation:** 
- Total = 6000 * 5 = 30000

**Result Snippet:**
> Total Hostel Fee: 30000.0

---

## Test Case 6: Multi Tool Challenge
**Prompt:** 
```text
I attended 80 classes out of 100.
My marks are 90, 85, 88, 92 and 95.
My course fee is 60000 and I paid 45000.

Provide:
1. Attendance Status
2. Grade
3. Pending Fee
```

**Tools Invoked:** 
- `attendance_calculator` with `{"total_classes": 100, "attended_classes": 80}`
- `result_calculator` with `{"marks": [90, 85, 88, 92, 95]}`
- `fee_balance_calculator` with `{"total_fee": 60000.0, "paid_fee": 45000.0}`

**Expected Output Calculation:** 
- Attendance = 80.0% -> Eligible
- Marks Average = 90.00 -> Grade A
- Fees Pending = 15000.0

**Result Snippet:**
> 1. Attendance Status: Eligible for Exam (80.00%)
> 2. Grade: Grade A (Average 90.00, Pass)
> 3. Pending Fee: 15000.0
