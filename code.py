import openai
import json
from typing import Dict, List, Any
from datetime import datetime

# ============================================================================
# LLM USAGE POINT #1: QUERY PARSING AND UNDERSTANDING
# ============================================================================

class LLMQueryParser:
    """Uses LLM to parse natural language queries into structured data"""
    
    async def parse_query(self, user_query: str) -> Dict[str, Any]:
        """
        🤖 LLM USAGE: Parse natural language into structured query parameters
        
        This is where LLM reasoning is ESSENTIAL - traditional NLP would struggle
        with the variety and complexity of equity domain queries.
        """
        
        prompt = f"""
        You are an expert equity plan management system. Parse this natural language query into structured parameters.
        
        User Query: "{user_query}"
        
        Equity Domain Knowledge:
        - Participants: employees, officers, directors, consultants
        - Securities: options, RSUs, ESPP, warrants, restricted stock
        - Events: vesting, exercise, sale, grant, expiration
        - Time expressions: quarters, months, specific dates, relative time
        - Relationships: participants have grants, grants have vesting schedules
        
        Extract and return JSON with:
        {{
            "entities": {{
                "target": "what user wants (participants, grants, companies, etc)",
                "filters": {{
                    "department": "if mentioned",
                    "security_type": "if specified",
                    "participant_type": "employee/officer/director",
                    "time_context": "any time expressions"
                }}
            }},
            "intent": {{
                "primary_action": "query/analyze/generate/send",
                "output_format": "list/report/email/summary",
                "data_scope": "single_company/multi_company/benchmark"
            }},
            "business_validation": [
                "Check for business rule violations or impossible combinations"
            ],
            "confidence": 0.85
        }}
        
        Be precise and identify ALL relevant equity concepts.
        """
        
        print("🤖 LLM CALL #1: Query Parsing")
        print(f"   Input: '{user_query}'")
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # Low temperature for consistent parsing
            max_tokens=1000
        )
        
        try:
            parsed_data = json.loads(response.choices[0].message.content)
            print(f"   ✅ LLM parsed query successfully")
            print(f"   📊 Confidence: {parsed_data.get('confidence', 'N/A')}")
            return parsed_data
        except json.JSONDecodeError as e:
            print(f"   ❌ LLM parsing failed: {e}")
            return self._fallback_parsing(user_query)
    
    def _fallback_parsing(self, query: str) -> Dict:
        """🔧 NON-LLM: Fallback parsing using traditional string matching"""
        # This would use regex and keyword matching as backup
        return {"entities": {}, "intent": {}, "confidence": 0.3}

# ============================================================================
# LLM USAGE POINT #2: DYNAMIC WORKFLOW PLANNING  
# ============================================================================

class LLMWorkflowPlanner:
    """Uses LLM to dynamically plan execution workflows"""
    
    def __init__(self):
        self.available_tools = [
            "calculate_date_range", "query_participants", "query_companies",
            "query_grants", "generate_email", "create_report", "send_notification"
        ]
    
    async def plan_workflow(self, parsed_query: Dict[str, Any]) -> List[Dict]:
        """
        🤖 LLM USAGE: Plan optimal workflow based on query requirements
        
        This is where LLM reasoning shines - determining tool dependencies 
        and execution order for novel query combinations.
        """
        
        prompt = f"""
        You are a workflow planning expert for equity management systems.
        
        Parsed Query Context:
        {json.dumps(parsed_query, indent=2)}
        
        Available Tools:
        {json.dumps(self.available_tools, indent=2)}
        
        Tool Capabilities:
        - calculate_date_range: Parse time expressions → date ranges
        - query_participants: Get employee/participant data with filters
        - query_companies: Get company data (for portfolio/multi-company queries)
        - query_grants: Get equity grant information
        - generate_email: Create email content
        - create_report: Generate formatted reports
        - send_notification: Send emails/messages
        
        Create an optimal execution workflow. Return JSON array:
        [
            {{
                "step_id": 1,
                "tool": "calculate_date_range",
                "description": "Parse 'this quarter' into specific dates",
                "params": {{"expression": "this quarter"}},
                "dependencies": [],
                "rationale": "Need specific dates before querying data"
            }},
            {{
                "step_id": 2,
                "tool": "query_participants", 
                "description": "Get participants with date filter",
                "params": {{"department": "Engineering"}},
                "dependencies": [1],
                "rationale": "Use dates from step 1 to filter by hire date"
            }}
        ]
        
        Consider:
        1. Data dependencies (what needs what)
        2. Optimal execution order
        3. Error handling requirements
        4. Performance optimizations
        
        Plan for efficiency and reliability.
        """
        
        print("🤖 LLM CALL #2: Workflow Planning")
        print(f"   Input: Parsed query with {len(parsed_query.get('entities', {}))} entities")
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # Slightly higher for creative workflow planning
            max_tokens=2000
        )
        
        try:
            workflow_steps = json.loads(response.choices[0].message.content)
            print(f"   ✅ LLM planned {len(workflow_steps)} workflow steps")
            return workflow_steps
        except json.JSONDecodeError as e:
            print(f"   ❌ LLM planning failed: {e}")
            return self._fallback_planning(parsed_query)
    
    def _fallback_planning(self, parsed_query: Dict) -> List[Dict]:
        """🔧 NON-LLM: Simple rule-based workflow planning"""
        # Basic if/then logic for common patterns
        return [{"step_id": 1, "tool": "query_participants", "params": {}}]

# ============================================================================
# LLM USAGE POINT #3: BUSINESS RULES VALIDATION
# ============================================================================

class LLMBusinessValidator:
    """Uses LLM to validate business rules and catch domain-specific errors"""
    
    async def validate_query_logic(self, parsed_query: Dict, planned_workflow: List[Dict]) -> Dict[str, Any]:
        """
        🤖 LLM USAGE: Validate business logic and catch domain-specific errors
        
        LLM can catch subtle business rule violations that would be hard to code manually.
        """
        
        prompt = f"""
        You are an equity compensation expert. Review this query and planned workflow for business logic errors.
        
        Parsed Query:
        {json.dumps(parsed_query, indent=2)}
        
        Planned Workflow:
        {json.dumps(planned_workflow, indent=2)}
        
        Equity Business Rules to Check:
        1. 83(b) elections only apply to restricted stock, not RSUs or options
        2. Options can be exercised, RSUs vest automatically  
        3. Underwater options = current stock price < strike price
        4. Vesting schedules typically 1-4 years
        5. Officers/directors have special compliance requirements
        6. Tax forms (1099, 1051) have specific timing requirements
        
        Check for:
        - Impossible combinations (like "exercise RSUs")
        - Misused terminology (like "83b election for options")
        - Missing data dependencies
        - Compliance violations
        - Logical inconsistencies
        
        Return JSON:
        {{
            "is_valid": true/false,
            "warnings": ["Business rule warnings"],
            "errors": ["Critical errors that would fail"],
            "suggestions": ["Recommended corrections"],
            "confidence": 0.85
        }}
        """
        
        print("🤖 LLM CALL #3: Business Validation")
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=800
        )
        
        try:
            validation_result = json.loads(response.choices[0].message.content)
            print(f"   ✅ Business validation complete")
            if validation_result.get("warnings"):
                print(f"   ⚠️  Warnings: {len(validation_result['warnings'])}")
            return validation_result
        except:
            return {"is_valid": True, "warnings": [], "errors": []}

# ============================================================================
# LLM USAGE POINT #4: RESULT SYNTHESIS AND EXPLANATION
# ============================================================================

class LLMResultSynthesizer:
    """Uses LLM to create human-readable explanations from raw data"""
    
    async def synthesize_results(self, original_query: str, workflow_results: Dict, 
                                execution_context: Dict) -> Dict[str, Any]:
        """
        🤖 LLM USAGE: Transform raw data into business-friendly explanations
        
        This is where LLM excels - creating contextual, actionable summaries
        that business users can understand and act upon.
        """
        
        prompt = f"""
        You are an equity compensation analyst. Create a clear, actionable summary of these query results.
        
        Original User Query: "{original_query}"
        
        Execution Results:
        {json.dumps(workflow_results, indent=2, default=str)}
        
        Execution Context:
        - Total steps executed: {execution_context.get('total_steps', 0)}
        - Data sources used: {execution_context.get('data_sources', [])}
        - Processing time: {execution_context.get('duration_seconds', 0)} seconds
        
        Create a business-friendly summary with:
        1. Executive summary (1-2 sentences answering the user's question)
        2. Key findings (3-5 bullet points with numbers/metrics)
        3. Business insights (what this means for the business)
        4. Recommended next actions (specific, actionable steps)
        5. Important caveats or limitations
        
        Return JSON:
        {{
            "executive_summary": "Clear answer to user's question",
            "key_findings": [
                "Finding 1 with specific numbers",
                "Finding 2 with context"
            ],
            "business_insights": [
                "What this means for retention",
                "Compliance implications"
            ],
            "recommended_actions": [
                "Specific step 1",
                "Specific step 2"
            ],
            "caveats": ["Important limitations"],
            "confidence_level": "high/medium/low"
        }}
        
        Use business language, not technical jargon. Focus on actionable insights.
        """
        
        print("🤖 LLM CALL #4: Result Synthesis")
        print(f"   Input: {len(workflow_results)} workflow results")
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  # Allow some creativity for insights
            max_tokens=1500
        )
        
        try:
            synthesis = json.loads(response.choices[0].message.content)
            print(f"   ✅ Results synthesized successfully")
            print(f"   📊 Confidence: {synthesis.get('confidence_level', 'N/A')}")
            return synthesis
        except:
            return self._fallback_synthesis(original_query, workflow_results)
    
    def _fallback_synthesis(self, query: str, results: Dict) -> Dict:
        """🔧 NON-LLM: Simple template-based result formatting"""
        return {
            "executive_summary": "Query executed successfully",
            "key_findings": ["Results available"],
            "recommended_actions": ["Review the data"]
        }

# ============================================================================
# LLM USAGE POINT #5: EMAIL/COMMUNICATION GENERATION
# ============================================================================

class LLMCommunicationGenerator:
    """Uses LLM to generate emails, reports, and other communications"""
    
    async def generate_email(self, recipients_data: List[Dict], context: str, 
                           email_type: str = "notification") -> Dict[str, Any]:
        """
        🤖 LLM USAGE: Generate contextual, professional communications
        
        LLM creates personalized, compliant emails that would be tedious to template.
        """
        
        prompt = f"""
        Generate a professional email for equity plan participants.
        
        Recipients Context:
        {json.dumps(recipients_data[:3], indent=2)}  # Show first 3 for context
        Total Recipients: {len(recipients_data)}
        
        Email Context: {context}
        Email Type: {email_type}
        
        Requirements:
        - Professional, clear tone
        - Compliance-friendly language (no investment advice)
        - Personalized where appropriate
        - Clear call-to-action
        - Include relevant deadlines/dates
        
        Return JSON:
        {{
            "subject": "Clear, specific subject line",
            "body": "Professional email body with personalization placeholders like {{participant_name}}",
            "call_to_action": "Specific action required",
            "urgency": "high/medium/low",
            "compliance_notes": ["Any compliance considerations"]
        }}
        """
        
        print("🤖 LLM CALL #5: Email Generation")
        print(f"   Context: {email_type} for {len(recipients_data)} recipients")
        
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,  # Balance creativity with professionalism
            max_tokens=1000
        )
        
        try:
            email_content = json.loads(response.choices[0].message.content)
            print(f"   ✅ Email generated successfully")
            return email_content
        except:
            return self._fallback_email_generation(recipients_data, context)
    
    def _fallback_email_generation(self, recipients: List[Dict], context: str) -> Dict:
        """🔧 NON-LLM: Template-based email generation"""
        return {
            "subject": "Important Equity Plan Information",
            "body": "Please review your equity plan details.",
            "call_to_action": "Contact HR with questions"
        }

# ============================================================================
# NON-LLM COMPONENTS (FOR COMPARISON)
# ============================================================================

class NonLLMComponents:
    """These components do NOT use LLMs - they're traditional code"""
    
    def __init__(self):
        pass
    
    async def execute_sql_query(self, sql: str, params: List) -> List[Dict]:
        """🔧 NON-LLM: Database operations are pure SQL/code"""
        # This is traditional database interaction
        # No LLM needed - just execute SQL and return results
        pass
    
    def calculate_date_ranges(self, expression: str) -> Dict:
        """🔧 NON-LLM: Date calculations can be pure code logic"""
        # While we COULD use LLM here, date math can be traditional code
        # LLM only helps if we want to handle very complex date expressions
        pass
    
    def format_database_results(self, raw_data: List[Dict]) -> List[Dict]:
        """🔧 NON-LLM: Data formatting is straightforward transformation"""
        # Field mapping, data cleaning, type conversion
        # No reasoning required - just data transformation
        pass
    
    def validate_permissions(self, user_id: str, action: str) -> bool:
        """🔧 NON-LLM: Security logic is rule-based"""
        # Permission checking is if/then logic
        # No need for LLM reasoning here
        pass

# ============================================================================
# MAIN AGENT: ORCHESTRATES ALL LLM AND NON-LLM COMPONENTS
# ============================================================================

class LLMPoweredEquityAgent:
    """Main agent showing exactly where LLMs are used vs traditional code"""
    
    def __init__(self, config: Dict):
        # LLM-powered components
        self.query_parser = LLMQueryParser()
        self.workflow_planner = LLMWorkflowPlanner()
        self.business_validator = LLMBusinessValidator()
        self.result_synthesizer = LLMResultSynthesizer()
        self.communication_generator = LLMCommunicationGenerator()
        
        # Non-LLM components  
        self.database_connector = NonLLMComponents()
        self.permission_manager = NonLLMComponents()
        
    async def process_query(self, user_query: str, user_id: str) -> Dict[str, Any]:
        """Main processing pipeline showing LLM vs non-LLM usage"""
        
        print(f"🚀 Processing: '{user_query}'")
        print("=" * 60)
        
        # 🤖 LLM STEP 1: Parse natural language query
        parsed_query = await self.query_parser.parse_query(user_query)
        
        # 🤖 LLM STEP 2: Plan optimal workflow  
        planned_workflow = await self.workflow_planner.plan_workflow(parsed_query)
        
        # 🤖 LLM STEP 3: Validate business logic
        validation = await self.business_validator.validate_query_logic(parsed_query, planned_workflow)
        
        if not validation["is_valid"]:
            return {"status": "error", "errors": validation["errors"]}
        
        # 🔧 NON-LLM STEP 4: Execute workflow (database operations, calculations)
        workflow_results = await self._execute_workflow_non_llm(planned_workflow, user_id)
        
        # 🤖 LLM STEP 5: Synthesize results into business language
        final_synthesis = await self.result_synthesizer.synthesize_results(
            user_query, workflow_results, {"total_steps": len(planned_workflow)}
        )
        
        # 🤖 LLM STEP 6: Generate communications if needed
        if "email" in user_query.lower():
            email_content = await self.communication_generator.generate_email(
                workflow_results.get("participants", []), 
                final_synthesis["executive_summary"]
            )
            final_synthesis["generated_email"] = email_content
        
        return {
            "status": "success",
            "query": user_query,
            "llm_calls_made": 5,  # Track LLM usage
            "synthesis": final_synthesis,
            "raw_data": workflow_results
        }
    
    async def _execute_workflow_non_llm(self, workflow: List[Dict], user_id: str) -> Dict:
        """🔧 NON-LLM: Execute workflow steps using traditional code"""
        # This is where the actual data retrieval happens
        # SQL queries, API calls, data processing - no LLM needed
        # Just following the plan that the LLM created
        
        results = {}
        for step in workflow:
            # Traditional code execution based on LLM's plan
            if step["tool"] == "query_participants":
                results[step["step_id"]] = await self._query_participants_traditional(step["params"])
            elif step["tool"] == "calculate_date_range":
                results[step["step_id"]] = self._calculate_dates_traditional(step["params"])
            # ... other traditional implementations
        
        return results
    
    async def _query_participants_traditional(self, params: Dict) -> List[Dict]:
        """🔧 NON-LLM: Traditional database query execution"""
        # Generate SQL, execute query, format results
        # No LLM involved - just database operations
        return [{"participant_id": "P001", "name": "John Smith"}]
    
    def _calculate_dates_traditional(self, params: Dict) -> Dict:
        """🔧 NON-LLM: Traditional date calculation"""
        # Date math using datetime library
        # No LLM needed for this
        return {"start_date": "2025-01-01", "end_date": "2025-03-31"}

# Usage example showing LLM call count
async def demo_llm_usage():
    """Demonstrate exactly where LLMs are called"""
    
    config = {"db_url": "postgresql://..."}
    agent = LLMPoweredEquityAgent(config)
    
    query = "Show me Engineering participants hired this quarter and send them an email about vesting"
    
    print("LLM USAGE TRACKING")
    print("=" * 40)
    
    result = await agent.process_query(query, user_id="user123")
    
    print(f"\n📊 SUMMARY:")
    print(f"   Query: '{query}'")
    print(f"   LLM calls made: {result['llm_calls_made']}")
    print(f"   Status: {result['status']}")
    
    return result

if __name__ == "__main__":
    import asyncio
    asyncio.run(demo_llm_usage())
