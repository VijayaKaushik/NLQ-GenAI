Ah! That makes much more sense! The user is asking about:
- RSU (Restricted Stock Units)
- PSU (Performance Stock Units)
- NQO (Non-Qualified Options)

These are equity compensation award types, not "Raus Pause NQAPs"! This is a perfect example of domain-specific terminology that a text-to-SQL system needs to handle.

Let me trace through how this query would actually be processed with the correct terminology:

"Show me all the RSUs PSUs NQOs issued in 2023 fiscal year"

This is asking for three different award types:
- RSU
- PSU  
- NQO

I should show how the entity recognition and normalization would work for this real equity compensation scenario.

Ah! That makes WAY more sense! So you're dealing with **equity compensation awards**:
- **RSU** = Restricted Stock Units
- **PSU** = Performance Stock Units  
- **NQO** = Non-Qualified Options

Let me trace through how this query would actually be processed:

## **Query Analysis**
```
User Query: "Show me all the RSUs PSUs NQOs issued in 2023 fiscal year"

Entities to extract:
- "RSUs" - Award type (plural, needs normalization to RSU)
- "PSUs" - Award type (plural, needs normalization to PSU)
- "NQOs" - Award type (plural, needs normalization to NQO)
- "issued" - Action/event type
- "2023 fiscal year" - Time period
```

This is a **multi-entity query** - user wants THREE different award types in one query!

## **Step-by-Step Execution**

### **Step 1: Build Prompt with Equity Award Context**

```python
def build_equity_awards_prompt(user_input):
    # Get available award types from database
    available_award_types = get_available_award_types()
    # Returns: ['RSU', 'PSU', 'NQO', 'ISO', 'SAR']
    
    prompt = f"""
You are a text-to-SQL converter for an equity compensation system.

DATABASE SCHEMA:
Table: equity_awards
Columns: award_id, award_type, grant_date, fiscal_year, employee_id, quantity, vesting_schedule, status

AVAILABLE AWARD TYPES:
{', '.join(available_award_types)}

Common abbreviations:
- RSU = Restricted Stock Unit
- PSU = Performance Stock Unit
- NQO = Non-Qualified Option
- ISO = Incentive Stock Option
- SAR = Stock Appreciation Right

ENTITY NORMALIZATION RULES:
1. Users may use plural forms: RSUs → RSU, PSUs → PSU, NQOs → NQO
2. Users may list multiple award types: "RSUs PSUs NQOs" means award_type IN ('RSU', 'PSU', 'NQO')
3. "issued" or "granted" maps to grant_date or fiscal_year columns
4. Fiscal year: "2023 fiscal year" → fiscal_year = 2023

RESPONSE FORMATS:
- SQL: [your query]
- CLARIFICATION_NEEDED: [message]
- CONFIRM: [confirmation]

USER INPUT: "{user_input}"

Process:
1. Extract award types: RSUs, PSUs, NQOs
2. Normalize: Remove plural 's' → RSU, PSU, NQO
3. Check if these exist in available award types
4. Build SQL with IN clause for multiple types

Respond now:
"""
    
    return prompt
```

### **Step 2: GPT Processes the Multi-Entity Query**

```python
# GPT's reasoning:
"""
User input: "Show me all the RSUs PSUs NQOs issued in 2023 fiscal year"

Step 1 - Extract entities:
- Award types mentioned: "RSUs", "PSUs", "NQOs"
- Time period: "2023 fiscal year"
- Action: "issued" (maps to grant_date/fiscal_year)

Step 2 - Normalize award types:
- "RSUs" (plural) → "RSU" (singular)
- "PSUs" (plural) → "PSU" (singular)
- "NQOs" (plural) → "NQO" (singular)

Step 3 - Validate against available types:
Available: ['RSU', 'PSU', 'NQO', 'ISO', 'SAR']
Requested: ['RSU', 'PSU', 'NQO']
✓ All found!

Step 4 - Build SQL:
Multiple award types → Use IN clause
award_type IN ('RSU', 'PSU', 'NQO')
AND fiscal_year = 2023

Can generate SQL!
"""
```

### **Step 3: GPT Responds**

**Scenario A: All award types found (Success)**
```python
gpt_response = """
SQL: SELECT * FROM equity_awards WHERE award_type IN ('RSU', 'PSU', 'NQO') AND fiscal_year = 2023
"""
```

**Scenario B: One or more award types not found**
```python
gpt_response = """
CLARIFICATION_NEEDED: Found award types 'RSU' and 'PSU', but could not find 'NQO'. Available award types: RSU, PSU, ISO, SAR. Did you mean 'ISO' instead of 'NQO'?
"""
```

**Scenario C: Typo in award type**
```python
# User typed: "Show me all the RSAs PSUs NQOs..." (RSA instead of RSU)
gpt_response = """
CONFIRM: Did you mean 'RSAs' as 'RSU' (Restricted Stock Unit)? Found matches for PSU and NQO.
"""
```

### **Step 4: Execute the Query**

```python
def main_text_to_sql(user_input):
    prompt = build_equity_awards_prompt(user_input)
    gpt_response = call_gpt(user_input, prompt)
    
    if gpt_response.startswith("SQL:"):
        sql = gpt_response.split("SQL:", 1)[1].strip()
        # sql = "SELECT * FROM equity_awards WHERE award_type IN ('RSU', 'PSU', 'NQO') AND fiscal_year = 2023"
        
        results = execute_query(sql)
        return {
            "type": "success",
            "sql": sql,
            "results": results,
            "count": len(results),
            "message": f"Found {len(results)} awards (RSU, PSU, NQO) issued in fiscal year 2023"
        }
    
    elif gpt_response.startswith("CLARIFICATION_NEEDED:"):
        message = gpt_response.split("CLARIFICATION_NEEDED:", 1)[1].strip()
        return {
            "type": "clarification",
            "message": message
        }
    
    elif gpt_response.startswith("CONFIRM:"):
        message = gpt_response.split("CONFIRM:", 1)[1].strip()
        return {
            "type": "confirmation",
            "message": message
        }
```

## **Complete Real Implementation**

```python
from openai import OpenAI
import sqlite3
from datetime import date

client = OpenAI(api_key="your-key")

def setup_equity_database():
    """Setup sample equity awards database"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE equity_awards (
            award_id INTEGER PRIMARY KEY,
            award_type TEXT,
            grant_date DATE,
            fiscal_year INTEGER,
            employee_id TEXT,
            quantity INTEGER,
            vesting_schedule TEXT,
            status TEXT
        )
    ''')
    
    # Sample data
    sample_awards = [
        (1, 'RSU', '2023-02-15', 2023, 'EMP001', 1000, '4-year vest', 'Active'),
        (2, 'RSU', '2023-03-20', 2023, 'EMP002', 500, '4-year vest', 'Active'),
        (3, 'PSU', '2023-04-10', 2023, 'EMP003', 750, '3-year performance', 'Active'),
        (4, 'PSU', '2023-06-15', 2023, 'EMP004', 1200, '3-year performance', 'Active'),
        (5, 'NQO', '2023-07-01', 2023, 'EMP005', 2000, '4-year vest', 'Active'),
        (6, 'NQO', '2023-09-12', 2023, 'EMP006', 1500, '4-year vest', 'Active'),
        (7, 'ISO', '2023-11-20', 2023, 'EMP007', 800, '4-year vest', 'Active'),
        (8, 'RSU', '2024-01-15', 2024, 'EMP008', 600, '4-year vest', 'Active'),
        (9, 'PSU', '2022-12-10', 2022, 'EMP009', 900, '3-year performance', 'Vested'),
    ]
    
    cursor.executemany('''
        INSERT INTO equity_awards VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', sample_awards)
    
    conn.commit()
    return conn

def get_available_award_types(conn):
    """Get all unique award types from database"""
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT award_type FROM equity_awards ORDER BY award_type")
    return [row[0] for row in cursor.fetchall()]

def process_equity_query(user_input):
    """Process the RSU PSU NQO query"""
    
    # Setup database
    conn = setup_equity_database()
    available_types = get_available_award_types(conn)
    
    print(f"Available award types in database: {available_types}\n")
    
    # Build prompt
    prompt = f"""
You are a text-to-SQL converter for equity compensation management.

DATABASE SCHEMA:
Table: equity_awards
Columns: award_id, award_type, grant_date, fiscal_year, employee_id, quantity, vesting_schedule, status

AVAILABLE AWARD TYPES IN DATABASE:
{', '.join(available_types)}

AWARD TYPE ABBREVIATIONS:
- RSU = Restricted Stock Unit
- PSU = Performance Stock Unit
- NQO = Non-Qualified Stock Option
- ISO = Incentive Stock Option
- SAR = Stock Appreciation Right

NORMALIZATION RULES:
1. Plural to singular: RSUs → RSU, PSUs → PSU, NQOs → NQO
2. Multiple award types: "RSUs PSUs NQOs" → award_type IN ('RSU', 'PSU', 'NQO')
3. "issued" or "granted" → Use fiscal_year column
4. Fiscal year format: "2023 fiscal year" → fiscal_year = 2023

RESPONSE FORMAT (MUST USE):
- SQL: [query]
- CLARIFICATION_NEEDED: [message]
- CONFIRM: [message]

USER INPUT: "{user_input}"

Think step-by-step:
1. Extract award types: What types did user mention?
2. Normalize: Remove plurals, check against available types
3. Extract time period: What fiscal year?
4. Build SQL: Use IN clause for multiple types

Respond:
"""
    
    # Call GPT
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1
    )
    
    gpt_response = response.choices[0].message.content
    print(f"GPT Response:\n{gpt_response}\n")
    
    # Parse response
    if gpt_response.startswith("SQL:"):
        sql = gpt_response.split("SQL:", 1)[1].strip()
        print(f"Executing SQL:\n{sql}\n")
        
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        
        print(f"Results: {len(results)} awards found\n")
        print("Award Details:")
        print("-" * 100)
        for row in results:
            print(f"ID: {row[0]}, Type: {row[1]}, Grant Date: {row[2]}, FY: {row[3]}, Employee: {row[4]}, Qty: {row[5]}")
        
        # Group by award type for summary
        cursor.execute(f"""
            SELECT award_type, COUNT(*), SUM(quantity) 
            FROM equity_awards 
            WHERE award_type IN ('RSU', 'PSU', 'NQO') AND fiscal_year = 2023
            GROUP BY award_type
        """)
        summary = cursor.fetchall()
        
        print("\nSummary by Award Type:")
        print("-" * 50)
        for award_type, count, total_qty in summary:
            print(f"{award_type}: {count} grants, {total_qty:,} units")
        
        conn.close()
        return {
            "type": "success",
            "sql": sql,
            "results": results,
            "summary": summary
        }
    
    elif gpt_response.startswith("CLARIFICATION_NEEDED:"):
        message = gpt_response.split("CLARIFICATION_NEEDED:", 1)[1].strip()
        print(f"❌ Clarification needed:\n{message}")
        conn.close()
        return {"type": "clarification", "message": message}
    
    elif gpt_response.startswith("CONFIRM:"):
        message = gpt_response.split("CONFIRM:", 1)[1].strip()
        print(f"⚠️  Confirmation needed:\n{message}")
        conn.close()
        return {"type": "confirmation", "message": message}

# Execute the query
print("=" * 100)
print("PROCESSING EQUITY AWARDS QUERY")
print("=" * 100)
print("\nUser Query: 'Show me all the RSUs PSUs NQOs issued in 2023 fiscal year'\n")
print("-" * 100)

result = process_equity_query("Show me all the RSUs PSUs NQOs issued in 2023 fiscal year")
```

## **Expected Output**

```
====================================================================================================
PROCESSING EQUITY AWARDS QUERY
====================================================================================================

User Query: 'Show me all the RSUs PSUs NQOs issued in 2023 fiscal year'

----------------------------------------------------------------------------------------------------
Available award types in database: ['ISO', 'NQO', 'PSU', 'RSU']

GPT Response:
SQL: SELECT * FROM equity_awards WHERE award_type IN ('RSU', 'PSU', 'NQO') AND fiscal_year = 2023

Executing SQL:
SELECT * FROM equity_awards WHERE award_type IN ('RSU', 'PSU', 'NQO') AND fiscal_year = 2023

Results: 6 awards found

Award Details:
----------------------------------------------------------------------------------------------------
ID: 1, Type: RSU, Grant Date: 2023-02-15, FY: 2023, Employee: EMP001, Qty: 1000
ID: 2, Type: RSU, Grant Date: 2023-03-20, FY: 2023, Employee: EMP002, Qty: 500
ID: 3, Type: PSU, Grant Date: 2023-04-10, FY: 2023, Employee: EMP003, Qty: 750
ID: 4, Type: PSU, Grant Date: 2023-06-15, FY: 2023, Employee: EMP004, Qty: 1200
ID: 5, Type: NQO, Grant Date: 2023-07-01, FY: 2023, Employee: EMP005, Qty: 2000
ID: 6, Type: NQO, Grant Date: 2023-09-12, FY: 2023, Employee: EMP006, Qty: 1500

Summary by Award Type:
--------------------------------------------------
RSU: 2 grants, 1,500 units
PSU: 2 grants, 1,950 units
NQO: 2 grants, 3,500 units
```

## **Key Handling Points for This Query**

### **1. Multi-Entity Recognition**
```python
# User mentions THREE award types at once
"RSUs PSUs NQOs" 

# GPT must recognize this as:
award_types = ['RSU', 'PSU', 'NQO']

# And generate:
WHERE award_type IN ('RSU', 'PSU', 'NQO')
```

### **2. Plural Normalization**
```python
# User uses plurals, database has singulars
User says: "RSUs PSUs NQOs"
Database has: "RSU", "PSU", "NQO"

# Normalization:
"RSUs" → "RSU"
"PSUs" → "PSU"
"NQOs" → "NQO"
```

### **3. Domain-Specific Terminology**
```python
# These are equity compensation terms
# Must be in your entity mapping:

equity_abbreviations = {
    'RSU': 'Restricted Stock Unit',
    'PSU': 'Performance Stock Unit',
    'NQO': 'Non-Qualified Stock Option',
    'ISO': 'Incentive Stock Option',
    'SAR': 'Stock Appreciation Right'
}
```

### **4. Temporal Normalization**
```python
# User: "issued in 2023 fiscal year"
# Maps to: fiscal_year = 2023
# Could also mean: YEAR(grant_date) = 2023
```

## **Common Variations to Handle**

Your prompt should handle these variations:

```python
variations = [
    "Show me all RSUs PSUs NQOs issued in 2023 fiscal year",
    "Get RSU PSU NQO grants for FY2023",
    "List all restricted stock units, performance stock units, and non-qualified options from 2023",
    "2023 equity awards for RSUs, PSUs, and NQOs",
    "How many RSUs PSUs NQOs were granted in fiscal 2023"
]

# All should normalize to:
# WHERE award_type IN ('RSU', 'PSU', 'NQO') AND fiscal_year = 2023
```

Does this clarify how your actual equity awards query would be processed?
