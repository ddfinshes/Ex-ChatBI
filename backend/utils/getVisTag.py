from .get_llm_deepseek import LLM
from decimal import Decimal

def convert_decimals(obj):
    if isinstance(obj, Decimal):
        return float(obj)  # Or str(obj) if you prefer string representation
    elif isinstance(obj, list):
        return [convert_decimals(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}
    return obj

def get_vis_tag(user_query, excute_sql_output):
    prompt_system = """
        You are a seasoned business data analyst and need to process visualization recommendation requests according to the following rules:
        # Task Description
            1. The user will provide a question description and corresponding structured data results (including table name and data content).
            2. You need to determine the most suitable visualization form based on the analysis objectives:
                - Bar chart: Suitable for category comparison (≤6 categories) or discrete comparison of time series.
                - Line chart: Suitable for continuous time trend analysis (≥3 time points) or change trend display.
                - Pie chart: Suitable for showing the proportion of each part in the whole (3-5 categories).
        # Input Data Example
            {
            "question": "Quarterly sales comparison by region",
            "data": {
                "table_name": "sales_q3",
                "records": [
                {"region": "North", "amount": 450},
                {"region": "South", "amount": 320}
                    ]
                }
            }
        # Processing Requirements
            1. Strictly limit the output to only one of the following three options: bar-chart / line-chart / pie-chart.
            2. Must verify whether the data characteristics meet the applicable conditions of the selected chart type.
            3. If the data does not meet the conditions for any chart type, return a bar chart by default.
            4. The output must be in pure JSON format, with no additional explanations allowed.
        # Output Example
        ```json
            {"vis_tag":"bar-chart"}
        ```
    """
    prompt_user = {
        "question":user_query,
        "data":excute_sql_output
    }
    prompt_system = convert_decimals(prompt_system)
    prompt_user = convert_decimals(prompt_user)
    prompt = f"System: {prompt_system}\nUser: {prompt_user}"
    response = LLM(prompt)
    print("===============================LLM GET VIS TAG ==============================",response)
    return response


