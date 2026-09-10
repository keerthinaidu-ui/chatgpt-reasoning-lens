from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class HighlightIssue:
    id: str
    text: str
    issue_type: str
    badge_color: str
    underline_color: str
    issue: str
    why_it_matters: str
    confidence: str
    what_to_check: str
    what_could_change: str

SCENARIOS: Dict[str, Dict] = {
    "📊 Data Analysis": {
        "id": "data_analysis",
        "title": "📊 Data Analysis",
        "prompt": "Analyze this data. Are our advertising campaigns becoming more effective, and what should we do next?",
        "user_data": """Month\tSales\tAdvertising Spend
January\t1,000\t$5,000
February\t1,100\t$5,500
March\t1,250\t$8,000
April\t1,300\t$10,000""",
        "response": "Sales increased by 30% from January to April, which shows that the advertising campaigns are becoming more effective. Because sales continued to increase as advertising spending increased, the company should increase its advertising budget further.",
        "highlights": [
            {
                "id": "da_hl_1",
                "text": "Sales increased by 30%",
                "issue_type": "Supported calculation",
                "badge_color": "#10B981", # Green/Teal
                "underline_color": "#10B981",
                "issue": "The calculation is consistent with the numbers provided: sales increased from 1,000 in January to 1,300 in April, which is a 30% increase.",
                "why_it_matters": "This conclusion is directly supported by the available data.",
                "confidence": "High",
                "what_to_check": "Verify that both periods use the same definition of sales and cover comparable time periods.",
                "what_could_change": "If the periods or sales definitions are different, the percentage increase may not be directly comparable."
            },
            {
                "id": "da_hl_2",
                "text": "advertising campaigns are becoming more effective",
                "issue_type": "Unsupported causal claim",
                "badge_color": "#F59E0B", # Orange
                "underline_color": "#F59E0B",
                "issue": "The data shows that sales increased, but it does not prove that advertising caused the increase.",
                "why_it_matters": "Other factors could have contributed to higher sales, such as pricing changes, seasonal demand, new products, or changes in the market.",
                "confidence": "High",
                "what_to_check": "Compare advertising spending with conversion rates, customer acquisition, pricing, and other major changes between the periods.",
                "what_could_change": "If additional evidence shows that advertising directly contributed to the additional sales, the causal explanation would become more convincing."
            },
            {
                "id": "da_hl_3",
                "text": "Because sales continued to increase as advertising spending increased",
                "issue_type": "Correlation vs. causation",
                "badge_color": "#A855F7", # Purple
                "underline_color": "#A855F7",
                "issue": "The response treats two variables increasing together as evidence that one caused the other.",
                "why_it_matters": "Sales and advertising spending can increase at the same time without advertising being the reason for the sales increase.",
                "confidence": "High",
                "what_to_check": "Look for controlled experiments, campaign-level performance data, conversion rates, and return on advertising spend.",
                "what_could_change": "If controlled or additional evidence shows that increased advertising caused incremental sales, the conclusion would be stronger."
            },
            {
                "id": "da_hl_4",
                "text": "the company should increase its advertising budget further",
                "issue_type": "Overconfident recommendation",
                "badge_color": "#EF4444", # Red
                "underline_color": "#EF4444",
                "issue": "The recommendation assumes that increasing advertising spending will continue producing enough additional sales to justify the cost.",
                "why_it_matters": "The company spent 100% more on advertising from January to April, while sales increased by only 30%. The additional profitability has not been established.",
                "confidence": "High",
                "what_to_check": "Calculate incremental revenue, profit margin, customer acquisition cost, and return on advertising spend.",
                "what_could_change": "If the additional advertising is producing sufficient incremental profit, increasing the budget could be reasonable."
            }
        ]
    },
    "🔎 Market Research": {
        "id": "market_research",
        "title": "🔎 Market Research",
        "prompt": "We are considering launching a premium coffee subscription in India. We surveyed 1,000 people. 620 said they drink coffee regularly, 280 said they would consider paying for a premium subscription, 160 said they would pay ₹1,000–₹1,500 per month, 540 respondents were between 18–30 years old, 300 respondents were from Bangalore, and 250 respondents were from Mumbai. Based on this research, should we launch the product?",
        "user_data": None,
        "response": "The research indicates that there is strong demand for a premium coffee subscription in India. 28% of respondents said they would consider paying for the service, which demonstrates significant market interest. The strongest opportunity is likely among younger consumers in Bangalore and Mumbai. Therefore, the company should launch the subscription in these markets.",
        "highlights": [
            {
                "id": "mr_hl_1",
                "text": "there is strong demand for a premium coffee subscription in India",
                "issue_type": "Unsupported generalization",
                "badge_color": "#F59E0B", # Orange
                "underline_color": "#F59E0B",
                "issue": "The survey provides responses from 1,000 people, but it does not establish that the sample represents the entire Indian market.",
                "why_it_matters": "A small or unrepresentative sample can produce results that do not reflect the broader population.",
                "confidence": "High",
                "what_to_check": "Review the survey sampling method, geographic distribution, demographics, sample size, and potential selection bias.",
                "what_could_change": "If the survey sample is representative of the target Indian customer population, the evidence for broader market demand becomes stronger."
            },
            {
                "id": "mr_hl_2",
                "text": "28% of respondents said they would consider paying for the service",
                "issue_type": "Supported calculation",
                "badge_color": "#10B981", # Green/Teal
                "underline_color": "#10B981",
                "issue": "280 out of 1,000 respondents equals 28%.",
                "why_it_matters": "This percentage is directly supported by the survey data provided.",
                "confidence": "High",
                "what_to_check": "Confirm how the question was worded and whether 'would consider paying' reflects actual purchase intent.",
                "what_could_change": "If the survey question measures weak interest rather than actual willingness to purchase, the business implication may be different."
            },
            {
                "id": "mr_hl_3",
                "text": "The strongest opportunity is likely among younger consumers in Bangalore and Mumbai",
                "issue_type": "Incomplete reasoning",
                "badge_color": "#A855F7", # Purple
                "underline_color": "#A855F7",
                "issue": "The data shows the number of younger respondents and respondents from Bangalore and Mumbai, but does not show that these groups have the highest willingness to pay.",
                "why_it_matters": "Having more respondents from a particular group does not mean that the group represents the strongest customer opportunity.",
                "confidence": "High",
                "what_to_check": "Compare willingness to pay, purchase intent, income, customer needs, and expected acquisition costs across age groups and cities.",
                "what_could_change": "If younger consumers in Bangalore and Mumbai demonstrate substantially higher purchase intent and willingness to pay, the conclusion would become more convincing."
            },
            {
                "id": "mr_hl_4",
                "text": "Therefore, the company should launch the subscription in these markets",
                "issue_type": "Overconfident conclusion",
                "badge_color": "#EF4444", # Red
                "underline_color": "#EF4444",
                "issue": "The survey results alone do not establish that launching the product will be commercially successful.",
                "why_it_matters": "Market size, competition, customer acquisition costs, retention, pricing, margins, and operational costs have not been evaluated.",
                "confidence": "High",
                "what_to_check": "Estimate the addressable market, unit economics, competitive landscape, acquisition costs, and expected retention.",
                "what_could_change": "If additional market and financial analysis supports profitable demand, launching could become a stronger recommendation."
            }
        ]
    },
    "💻 Code Generation": {
        "id": "code_gen",
        "title": "💻 Code Generation",
        "prompt": "Write a Python function that calculates the average age of users. Ignore users whose age is missing.",
        "user_data": """users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob"},
    {"name": "Charlie", "age": 35}
]""",
        "response": """def average_age(users):
    total = sum(user["age"] for user in users if user["age"])
    count = len([user for user in users if user["age"]])
    return total / count

This function ignores users without an age and calculates the average age of the remaining users.""",
        "highlights": [
            {
                "id": "code_hl_1",
                "text": 'if user["age"]',
                "issue_type": "Potential logic issue",
                "badge_color": "#F59E0B", # Orange
                "underline_color": "#F59E0B",
                "issue": "This condition treats the value 0 as missing because 0 is considered false in Python.",
                "why_it_matters": "If 0 is a valid value in another dataset or the function is reused for another numeric field, valid values could be incorrectly excluded.",
                "confidence": "High",
                "what_to_check": "Decide whether missing age should specifically mean that the key is absent or the value is None.",
                "what_could_change": "If the application guarantees that valid ages are always positive integers, this behavior may not matter."
            },
            {
                "id": "code_hl_2",
                "text": 'user["age"]',
                "issue_type": "Hidden assumption",
                "badge_color": "#A855F7", # Purple
                "underline_color": "#A855F7",
                "issue": "The code assumes every user dictionary contains an 'age' key.",
                "why_it_matters": "The requirement says to ignore users whose age is missing, but accessing a missing key can raise a KeyError.",
                "confidence": "High",
                "what_to_check": "Test the function with users where the age field is completely absent, as in the provided Bob example.",
                "what_could_change": "If all input records are guaranteed to contain an age key, this issue would not occur."
            },
            {
                "id": "code_hl_3",
                "text": "This function ignores users without an age",
                "issue_type": "Incorrect claim",
                "badge_color": "#EF4444", # Red
                "underline_color": "#EF4444",
                "issue": "The implementation does not safely ignore a missing age key. For the provided Bob example, user[\"age\"] raises a KeyError before the condition can filter the user.",
                "why_it_matters": "The code fails on exactly the type of missing-age input described in the requirement.",
                "confidence": "High",
                "what_to_check": "Run the function against the provided sample data and test records where age is missing or None.",
                "what_could_change": "If the implementation uses a safe lookup such as user.get(\"age\"), the function could properly handle missing keys."
            }
        ]
    }
}


