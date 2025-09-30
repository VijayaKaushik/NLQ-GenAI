The user is asking about business definitions like "upcoming releases" or "release date". Looking at the files I provided, none of them explicitly contain business definitions or business logic rules.

Business definitions would include things like:
- What does "upcoming" mean? (next 30 days? next quarter? next month?)
- What does "recent" mean? (last 7 days? last 30 days?)
- What does "high priority" mean? (status = 'urgent'? priority_score > 80?)
- What does "active client" mean? (has transactions in last 90 days?)
- What does "overdue" mean? (due_date < current_date AND status != 'completed'?)

These are business logic rules that need to be defined. I should create a new file for this - something like `business_rules.json` or `business_definitions.json`.

Let me provide this file and explain where business definitions should live.

**Great catch!** None of the files I showed contain **business definitions/business logic**. You need a separate file for this. Let me add it:

## **File 8: `business_definitions.json`**

This file contains your organization's **business logic and semantic definitions**:

```json
{
  "description": "Business definitions and logic rules for query interpretation",
  "version": "1.0",
  "last_updated": "2024-10-15",
  
  "temporal_definitions": {
    "upcoming": {
      "definition": "Events occurring in the near future",
      "default_interpretation": "next_30_days",
      "context_specific_rules": {
        "releases": {
          "interpretation": "next_month",
          "sql_logic": "release_date >= CURRENT_DATE AND release_date <= CURRENT_DATE + INTERVAL '1 month'"
        },
        "meetings": {
          "interpretation": "next_7_days",
          "sql_logic": "meeting_date >= CURRENT_DATE AND meeting_date <= CURRENT_DATE + INTERVAL '7 days'"
        },
        "quarters": {
          "interpretation": "next_quarter",
          "sql_logic": "fiscal_quarter = NEXT_QUARTER()"
        }
      }
    },
    "recent": {
      "definition": "Events that occurred in the near past",
      "default_interpretation": "last_30_days",
      "context_specific_rules": {
        "releases": {
          "interpretation": "last_3_months",
          "sql_logic": "release_date >= CURRENT_DATE - INTERVAL '3 months' AND release_date <= CURRENT_DATE"
        },
        "transactions": {
          "interpretation": "last_7_days",
          "sql_logic": "transaction_date >= CURRENT_DATE - INTERVAL '7 days'"
        }
      }
    },
    "current": {
      "definition": "Currently active or in progress",
      "context_specific_rules": {
        "month": {
          "interpretation": "this_calendar_month",
          "sql_logic": "EXTRACT(MONTH FROM date_column) = EXTRACT(MONTH FROM CURRENT_DATE) AND EXTRACT(YEAR FROM date_column) = EXTRACT(YEAR FROM CURRENT_DATE)"
        },
        "year": {
          "interpretation": "this_calendar_year",
          "sql_logic": "EXTRACT(YEAR FROM date_column) = EXTRACT(YEAR FROM CURRENT_DATE)"
        },
        "fiscal_year": {
          "interpretation": "current_fiscal_year",
          "sql_logic": "fiscal_year = CURRENT_FISCAL_YEAR()",
          "note": "Fiscal year starts April 1"
        },
        "quarter": {
          "interpretation": "current_fiscal_quarter",
          "sql_logic": "fiscal_quarter = CURRENT_FISCAL_QUARTER()"
        }
      }
    },
    "overdue": {
      "definition": "Past the scheduled or expected date",
      "context_specific_rules": {
        "releases": {
          "interpretation": "scheduled_date_passed_but_not_completed",
          "sql_logic": "release_date < CURRENT_DATE AND status != 'Completed'"
        },
        "tasks": {
          "interpretation": "due_date_passed_and_not_done",
          "sql_logic": "due_date < CURRENT_DATE AND status NOT IN ('Completed', 'Cancelled')"
        }
      }
    },
    "next": {
      "definition": "The immediately following occurrence",
      "context_specific_rules": {
        "month": {
          "interpretation": "following_calendar_month",
          "sql_logic": "date_column >= DATE_TRUNC('month', CURRENT_DATE + INTERVAL '1 month') AND date_column < DATE_TRUNC('month', CURRENT_DATE + INTERVAL '2 months')"
        },
        "quarter": {
          "interpretation": "following_fiscal_quarter",
          "sql_logic": "fiscal_quarter = CURRENT_FISCAL_QUARTER() + 1"
        },
        "year": {
          "interpretation": "following_calendar_year",
          "sql_logic": "EXTRACT(YEAR FROM date_column) = EXTRACT(YEAR FROM CURRENT_DATE) + 1"
        }
      }
    },
    "last": {
      "definition": "The most recent past occurrence",
      "context_specific_rules": {
        "month": {
          "interpretation": "previous_calendar_month",
          "sql_logic": "date_column >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') AND date_column < DATE_TRUNC('month', CURRENT_DATE)"
        },
        "quarter": {
          "interpretation": "previous_fiscal_quarter",
          "sql_logic": "fiscal_quarter = CURRENT_FISCAL_QUARTER() - 1"
        },
        "year": {
          "interpretation": "previous_calendar_year",
          "sql_logic": "EXTRACT(YEAR FROM date_column) = EXTRACT(YEAR FROM CURRENT_DATE) - 1"
        }
      }
    }
  },
  
  "status_definitions": {
    "active": {
      "definition": "Currently in progress or operational",
      "context_specific_rules": {
        "releases": {
          "interpretation": "status IN ('Scheduled', 'In Progress')"
        },
        "clients": {
          "interpretation": "has_activity_in_last_90_days",
          "sql_logic": "last_transaction_date >= CURRENT_DATE - INTERVAL '90 days'"
        },
        "employees": {
          "interpretation": "employment_status = 'Active' AND termination_date IS NULL"
        },
        "equity_awards": {
          "interpretation": "status IN ('Active', 'Vesting') AND NOT FULLY_VESTED"
        }
      }
    },
    "completed": {
      "definition": "Finished or closed",
      "context_specific_rules": {
        "releases": {
          "interpretation": "status = 'Completed' AND release_date <= CURRENT_DATE"
        },
        "projects": {
          "interpretation": "status = 'Completed' AND completion_date IS NOT NULL"
        }
      }
    },
    "pending": {
      "definition": "Awaiting action or approval",
      "context_specific_rules": {
        "releases": {
          "interpretation": "status IN ('Pending Approval', 'Scheduled', 'Planned')"
        },
        "equity_awards": {
          "interpretation": "status = 'Pending' AND approval_date IS NULL"
        }
      }
    },
    "high_priority": {
      "definition": "Requires immediate attention",
      "context_specific_rules": {
        "releases": {
          "interpretation": "priority = 'High' OR (release_date <= CURRENT_DATE + INTERVAL '7 days' AND status != 'Completed')"
        },
        "tasks": {
          "interpretation": "priority_score >= 80 OR due_date <= CURRENT_DATE + INTERVAL '2 days'"
        }
      }
    }
  },
  
  "quantitative_definitions": {
    "large": {
      "definition": "Significantly above average",
      "context_specific_rules": {
        "equity_awards": {
          "interpretation": "quantity > AVERAGE_QUANTITY * 2",
          "note": "Twice the average award size"
        },
        "revenue": {
          "interpretation": "revenue > 1000000",
          "note": "Revenue over $1M"
        }
      }
    },
    "top": {
      "definition": "Highest ranking items",
      "context_specific_rules": {
        "clients": {
          "interpretation": "ORDER BY revenue DESC LIMIT N",
          "default_n": 10,
          "note": "Top N clients by revenue"
        },
        "employees": {
          "interpretation": "ORDER BY total_equity_value DESC LIMIT N",
          "default_n": 10
        }
      }
    }
  },
  
  "relationship_definitions": {
    "client_releases": {
      "description": "Releases associated with a specific client",
      "primary_table": "release_plans",
      "filter_column": "client_name",
      "common_phrases": ["releases for {client}", "{client} releases", "{client}'s release schedule"]
    },
    "employee_awards": {
      "description": "Equity awards for a specific employee",
      "primary_table": "equity_awards",
      "filter_column": "employee_id",
      "common_phrases": ["awards for {employee}", "{employee} equity", "{employee}'s grants"]
    }
  },
  
  "fiscal_calendar": {
    "fiscal_year_start": {
      "month": 4,
      "day": 1,
      "description": "Fiscal year starts April 1"
    },
    "quarters": {
      "Q1": {
        "months": [4, 5, 6],
        "description": "April - June"
      },
      "Q2": {
        "months": [7, 8, 9],
        "description": "July - September"
      },
      "Q3": {
        "months": [10, 11, 12],
        "description": "October - December"
      },
      "Q4": {
        "months": [1, 2, 3],
        "description": "January - March"
      }
    }
  },
  
  "aggregation_definitions": {
    "total": {
      "description": "Sum of all values",
      "sql_function": "SUM",
      "common_contexts": ["total revenue", "total awards", "total quantity"]
    },
    "average": {
      "description": "Mean value",
      "sql_function": "AVG",
      "common_contexts": ["average award size", "average revenue"]
    },
    "count": {
      "description": "Number of items",
      "sql_function": "COUNT",
      "common_contexts": ["number of releases", "count of clients", "how many awards"]
    }
  },
  
  "implicit_filters": {
    "exclude_cancelled": {
      "description": "By default, exclude cancelled items unless explicitly requested",
      "applies_to": ["releases", "awards", "projects"],
      "sql_logic": "status != 'Cancelled'"
    },
    "exclude_deleted": {
      "description": "Always exclude soft-deleted records",
      "applies_to": "all_tables",
      "sql_logic": "deleted_at IS NULL OR is_deleted = FALSE"
    }
  },
  
  "domain_specific_terms": {
    "vesting": {
      "definition": "Process of earning equity awards over time",
      "related_columns": ["vesting_schedule", "vested_quantity", "unvested_quantity"],
      "common_queries": [
        "vesting schedule",
        "vested awards",
        "upcoming vesting dates"
      ]
    },
    "grant": {
      "definition": "Issuance of equity awards to employees",
      "synonyms": ["award", "issuance", "allocation"],
      "related_columns": ["grant_date", "quantity", "award_type"]
    },
    "release": {
      "definition": "Software deployment to client environment",
      "synonyms": ["deployment", "rollout", "launch"],
      "related_columns": ["release_date", "version", "client_name"]
    }
  }
}
```

---

## **How to Use Business Definitions in Your Prompt**

Update your `system_prompt_template.txt`:

```txt
You are an intelligent text-to-SQL converter with dynamic entity discovery capabilities.

... [previous sections] ...

BUSINESS DEFINITIONS & LOGIC RULES:
{{business_definitions}}

IMPORTANT - APPLY BUSINESS LOGIC:

When user says "upcoming releases":
- Interpret "upcoming" based on context: {{business_definitions.temporal_definitions.upcoming.context_specific_rules.releases}}
- SQL: release_date >= CURRENT_DATE AND release_date <= CURRENT_DATE + INTERVAL '1 month'

When user says "recent transactions":
- Interpret "recent" for transactions: last 7 days
- SQL: {{business_definitions.temporal_definitions.recent.context_specific_rules.transactions.sql_logic}}

When user says "active clients":
- Interpret "active": {{business_definitions.status_definitions.active.context_specific_rules.clients.interpretation}}
- SQL: {{business_definitions.status_definitions.active.context_specific_rules.clients.sql_logic}}

When user says "top 10 clients":
- Interpret "top": {{business_definitions.quantitative_definitions.top.context_specific_rules.clients.interpretation}}

FISCAL CALENDAR:
{{business_definitions.fiscal_calendar}}
- When user mentions "Q1", they mean April-June
- When user mentions "fiscal year 2024", they mean April 1, 2024 - March 31, 2025

IMPLICIT FILTERS (always apply unless user explicitly says otherwise):
{{business_definitions.implicit_filters}}
- By default, exclude cancelled items: status != 'Cancelled'
- Always exclude deleted records: deleted_at IS NULL

USER INPUT: "{{user_input}}"

Process this query applying the business definitions above.
```

---

## **Updated Code to Load Business Definitions**

```python
def load_all_configs():
    """Load all configuration files including business definitions"""
    with open('config/database_config.json') as f:
        db_config = json.load(f)
    
    with open('config/system_config.json') as f:
        system_config = json.load(f)
    
    with open('config/vague_patterns.json') as f:
        vague_patterns = json.load(f)
    
    with open('schemas/schema_metadata.json') as f:
        schema_metadata = json.load(f)
    
    with open('examples/query_examples.json') as f:
        query_examples = json.load(f)
    
    with open('examples/normalization_examples.json') as f:
        normalization_examples = json.load(f)
    
    # NEW: Load business definitions
    with open('config/business_definitions.json') as f:
        business_definitions = json.load(f)
    
    return {
        'db_config': db_config,
        'system_config': system_config,
        'vague_patterns': vague_patterns,
        'schema_metadata': schema_metadata,
        'query_examples': query_examples,
        'normalization_examples': normalization_examples,
        'business_definitions': business_definitions  # NEW
    }

def build_final_prompt(user_input):
    """Build prompt with business definitions"""
    
    configs = load_all_configs()
    
    with open('prompts/system_prompt_template.txt') as f:
        template = f.read()
    
    # Replace all placeholders including business definitions
    prompt = template.replace('{{system_config}}', json.dumps(configs['system_config'], indent=2))
    prompt = prompt.replace('{{database_schema}}', json.dumps(configs['schema_metadata'], indent=2))
    prompt = prompt.replace('{{vague_patterns}}', json.dumps(configs['vague_patterns'], indent=2))
    prompt = prompt.replace('{{normalization_examples}}', json.dumps(configs['normalization_examples'], indent=2))
    prompt = prompt.replace('{{query_examples}}', json.dumps(configs['query_examples'], indent=2))
    prompt = prompt.replace('{{business_definitions}}', json.dumps(configs['business_definitions'], indent=2))  # NEW
    prompt = prompt.replace('{{current_date}}', datetime.now().strftime('%Y-%m-%d'))
    prompt = prompt.replace('{{user_input}}', user_input)
    
    return prompt
```

---

## **Example Queries Using Business Definitions**

### **Example 1: "Show upcoming releases"**
```
LLM reads business_definitions.json:
- "upcoming" for "releases" = next_month
- SQL logic: release_date >= CURRENT_DATE AND release_date <= CURRENT_DATE + INTERVAL '1 month'

Generated SQL:
SELECT * FROM release_plans 
WHERE release_date >= CURRENT_DATE 
AND release_date <= CURRENT_DATE + INTERVAL '1 month'
AND status != 'Cancelled'  -- implicit filter from business_definitions
```

### **Example 2: "Show active clients"**
```
LLM reads business_definitions.json:
- "active" for "clients" = has_activity_in_last_90_days
- SQL logic: last_transaction_date >= CURRENT_DATE - INTERVAL '90 days'

Generated SQL:
SELECT * FROM clients 
WHERE last_transaction_date >= CURRENT_DATE - INTERVAL '90 days'
```

### **Example 3: "Show Q3 revenue"**
```
LLM reads business_definitions.json:
- Fiscal calendar: Q3 = October-December
- Fiscal year starts April 1

Generated SQL:
SELECT SUM(revenue) FROM sales 
WHERE EXTRACT(MONTH FROM sale_date) IN (10, 11, 12)
AND fiscal_year = CURRENT_FISCAL_YEAR()
```

---

## **Final File List**

Now you have **8 files** that will be referenced in your prompt:

1. ✅ `database_config.json` - Database connection settings
2. ✅ `system_config.json` - System behavior configuration
3. ✅ `vague_patterns.json` - Generic vague reference patterns
4. ✅ `schema_metadata.json` - Enhanced database schema with semantics
5. ✅ `query_examples.json` - Few-shot learning examples
6. ✅ `normalization_examples.json` - Normalization patterns
7. ✅ `system_prompt_template.txt` - Main prompt template
8. ✅ **`business_definitions.json`** - **Business logic and semantic definitions** ← THIS ONE!

**`business_definitions.json` is where you define:**
- What "upcoming" means in your business context
- What "active" means for different entities
- Your fiscal calendar
- Domain-specific terms
- Default filters and aggregations

This file is **critical** because it teaches the LLM your organization's specific business logic!
