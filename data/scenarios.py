from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class HighlightIssue:
    id: str
    text: str
    issue_type: str
    badge_color: str
    underline_color: str
    confidence: str
    why_flagged: str
    what_assumes: str
    evidence_supports: str
    evidence_missing: str
    why_uncertain: str
    what_could_change: str
    sources: Optional[List[Dict[str, str]]] = None

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
                "confidence": "High",
                "why_flagged": "The percentage calculation is verified mathematically (from 1,000 in January to 1,300 in April is a 30% increase).",
                "what_assumes": "Assumes January and April sales data are directly comparable and measure the same metric.",
                "evidence_supports": "Internal prompt data: January sales = 1,000; April sales = 1,300.",
                "evidence_missing": "Month-over-month baseline metrics or external industry benchmark data for seasonal sales trends.",
                "why_uncertain": "Internal math is correct, but whether 30% growth reflects true underlying performance depends on unmeasured external factors.",
                "what_could_change": "If sales are adjusted for seasonal variance or non-ad channels, the growth rate attributable to advertising may change.",
                "sources": []
            },
            {
                "id": "da_hl_2",
                "text": "advertising campaigns are becoming more effective",
                "issue_type": "Unsupported causal claim",
                "badge_color": "#F59E0B", # Orange
                "underline_color": "#F59E0B",
                "confidence": "High",
                "why_flagged": "Asserts that advertising spending caused the sales increase without establishing direct attribution.",
                "what_assumes": "Assumes increased advertising spend was the primary or sole driver of sales growth.",
                "evidence_supports": "Co-occurrence of ad spend increase ($5,000 to $10,000) and sales increase (1,000 to 1,300) in the user's data.",
                "evidence_missing": "Attribution data, customer acquisition cost (CAC), return on ad spend (ROAS), or a control group isolating ad impact from organic demand.",
                "why_uncertain": "Correlation does not equal causation; unmeasured external factors like pricing or seasonal demand could explain the increase.",
                "what_could_change": "Controlled A/B testing or incremental lift analysis proving advertising spend directly generated the additional sales.",
                "sources": [
                    {
                        "title": "Think with Google: Marketing Attribution & Causation",
                        "url": "https://www.thinkwithgoogle.com/marketing-strategies/data-and-measurement/",
                        "domain": "thinkwithgoogle.com"
                    }
                ]
            },
            {
                "id": "da_hl_3",
                "text": "Because sales continued to increase as advertising spending increased",
                "issue_type": "Correlation vs. causation",
                "badge_color": "#A855F7", # Purple
                "underline_color": "#A855F7",
                "confidence": "High",
                "why_flagged": "Treats two variables moving together as proof of causation, ignoring diminishing marginal efficiency.",
                "what_assumes": "Assumes a linear positive relationship where additional ad dollars yield proportional sales increases.",
                "evidence_supports": "Ad spend and sales increased simultaneously across all 4 recorded months.",
                "evidence_missing": "Marginal returns analysis; ad spend doubled (+100% from $5k to $10k) while sales only grew 30%, indicating diminishing marginal returns.",
                "why_uncertain": "Simultaneous growth does not account for declining return per dollar spent.",
                "what_could_change": "If marginal revenue per dollar spent exceeds marginal ad cost, the correlation would reflect profitable expansion.",
                "sources": [
                    {
                        "title": "Law of Diminishing Marginal Returns",
                        "url": "https://www.investopedia.com/terms/l/lawofdiminishingmarginalreturn.asp",
                        "domain": "investopedia.com"
                    }
                ]
            },
            {
                "id": "da_hl_4",
                "text": "the company should increase its advertising budget further",
                "issue_type": "Overconfident recommendation",
                "badge_color": "#EF4444", # Red
                "underline_color": "#EF4444",
                "confidence": "High",
                "why_flagged": "Recommends budget expansion without evaluating profitability or return on investment.",
                "what_assumes": "Assumes continuing to increase ad spend will generate enough additional revenue to cover the added costs.",
                "evidence_supports": "Short-term trend of concurrent sales and ad spend growth.",
                "evidence_missing": "Profit margins, customer lifetime value (LTV), cost per acquisition (CPA), and maximum profitable ad spend ceiling.",
                "why_uncertain": "Expanding budgets based solely on top-line revenue without unit economic evaluation risks negative ROI.",
                "what_could_change": "A financial analysis demonstrating that incremental sales margin exceeds incremental ad spend.",
                "sources": [
                    {
                        "title": "Return on Investment (ROI): Calculation & Meaning",
                        "url": "https://www.investopedia.com/terms/r/returnoninvestment.asp",
                        "domain": "investopedia.com"
                    }
                ]
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
                "confidence": "High",
                "why_flagged": "Generalizes survey results from 1,000 respondents to the entire Indian consumer market (~1.4B people).",
                "what_assumes": "Assumes the 1,000 survey respondents form a statistically representative sample of all potential Indian coffee consumers.",
                "evidence_supports": "620/1,000 respondents drink coffee regularly; 280/1,000 expressed initial interest in a subscription.",
                "evidence_missing": "Survey sampling methodology, geographic diversity beyond 2 cities, and demographic weighting across age and income brackets.",
                "why_uncertain": "Unweighted or convenience survey samples frequently overrepresent niche enthusiasm compared to national demand.",
                "what_could_change": "Nationally representative sampling data with confidence intervals confirming broader consumer demand.",
                "sources": [
                    {
                        "title": "Pew Research Center: Sampling Methods & Bias",
                        "url": "https://www.pewresearch.org/our-methods/",
                        "domain": "pewresearch.org"
                    }
                ]
            },
            {
                "id": "mr_hl_2",
                "text": "28% of respondents said they would consider paying for the service",
                "issue_type": "Supported calculation",
                "badge_color": "#10B981", # Green/Teal
                "underline_color": "#10B981",
                "confidence": "High",
                "why_flagged": "Calculation is mathematically correct (280 / 1,000 = 28%), but intent does not equal actual purchase behavior.",
                "what_assumes": "Assumes survey intent ('would consider paying') translates directly into active paying subscribers.",
                "evidence_supports": "Survey dataset provided in prompt: 280 out of 1,000 respondents.",
                "evidence_missing": "Historical conversion rates between stated survey interest and actual purchase conversion (the Say-Do gap).",
                "why_uncertain": "Self-reported intent in consumer surveys consistently overstates real willingness to pay.",
                "what_could_change": "Pre-launch deposit, pre-order, or pilot sign-up conversion rate data.",
                "sources": [
                    {
                        "title": "Qualtrics: Market Research Methodology",
                        "url": "https://www.qualtrics.com/experience-management/research/",
                        "domain": "qualtrics.com"
                    }
                ]
            },
            {
                "id": "mr_hl_3",
                "text": "The strongest opportunity is likely among younger consumers in Bangalore and Mumbai",
                "issue_type": "Incomplete reasoning",
                "badge_color": "#A855F7", # Purple
                "underline_color": "#A855F7",
                "confidence": "High",
                "why_flagged": "Conflates large subgroup sample counts with actual purchasing power and highest product affinity.",
                "what_assumes": "Assumes respondents aged 18–30 in Bangalore and Mumbai have the highest willingness to pay ₹1,000–₹1,500/month.",
                "evidence_supports": "High sample volume in these segments (540 aged 18–30; 550 total from Bangalore/Mumbai).",
                "evidence_missing": "Cross-tabulated survey data showing how many of the 160 high willingness-to-pay respondents are in those specific segments.",
                "why_uncertain": "Having more survey takers in a category does not mean that category has the highest conversion rate or willingness to pay.",
                "what_could_change": "Cross-tabulation metrics confirming that Bangalore/Mumbai youth have higher willingness to pay than other segments.",
                "sources": [
                    {
                        "title": "Qualtrics: Cross Tabulation Analysis Guide",
                        "url": "https://www.qualtrics.com/experience-management/research/cross-tabulation/",
                        "domain": "qualtrics.com"
                    }
                ]
            },
            {
                "id": "mr_hl_4",
                "text": "Therefore, the company should launch the subscription in these markets",
                "issue_type": "Overconfident conclusion",
                "badge_color": "#EF4444", # Red
                "underline_color": "#EF4444",
                "confidence": "High",
                "why_flagged": "Recommends full product launch based solely on survey interest without evaluating business viability.",
                "what_assumes": "Assumes positive unit economics, favorable competitive landscape, and manageable customer acquisition costs (CAC).",
                "evidence_supports": "Positive consumer interest survey responses in key metropolitan areas.",
                "evidence_missing": "Competitor pricing, distribution logistics, subscriber churn rates, customer acquisition cost, and gross margins.",
                "why_uncertain": "A viable launch decision requires unit economic validation (LTV > 3x CAC), not survey numbers alone.",
                "what_could_change": "A financial model demonstrating profitable customer acquisition and retention in target markets.",
                "sources": [
                    {
                        "title": "Business Model: Definition, Types & Evaluation",
                        "url": "https://www.investopedia.com/terms/b/businessmodel.asp",
                        "domain": "investopedia.com"
                    }
                ]
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
                "confidence": "High",
                "why_flagged": "In Python, if 0 evaluates to False. An age of 0 (e.g. for infants) will be mistakenly treated as missing.",
                "what_assumes": "Assumes all valid age values are non-zero truthy integers.",
                "evidence_supports": "Python's truth value testing rules specify that integer 0, None, and empty collections evaluate to False.",
                "evidence_missing": "Specification clarifying whether 0 is a valid input age in the target system.",
                "why_uncertain": "if user['age'] filters out valid numeric zeros alongside None or missing values.",
                "what_could_change": "Replacing if user['age'] with explicit null/existence checking (if user.get('age') is not None).",
                "sources": [
                    {
                        "title": "Python Documentation: Truth Value Testing",
                        "url": "https://docs.python.org/3/library/stdtypes.html#truth-value-testing",
                        "domain": "docs.python.org"
                    }
                ]
            },
            {
                "id": "code_hl_2",
                "text": 'user["age"]',
                "issue_type": "Hidden assumption",
                "badge_color": "#A855F7", # Purple
                "underline_color": "#A855F7",
                "confidence": "High",
                "why_flagged": "Direct dictionary access user['age'] raises an unhandled KeyError when the 'age' key is completely absent.",
                "what_assumes": "Assumes every dictionary object in the input list contains the 'age' key.",
                "evidence_supports": "Python language specifications state that accessing an absent key via square brackets raises KeyError.",
                "evidence_missing": "Dictionary key validation or safe key lookup using .get('age') or 'age' in user.",
                "why_uncertain": "The user's prompt explicitly included {'name': 'Bob'} (missing 'age' key), which will crash the function at runtime.",
                "what_could_change": "Using user.get('age') or checking 'age' in user to safely handle missing keys.",
                "sources": [
                    {
                        "title": "Python Documentation: Dictionaries & KeyError",
                        "url": "https://docs.python.org/3/tutorial/datastructures.html#dictionaries",
                        "domain": "docs.python.org"
                    }
                ]
            },
            {
                "id": "code_hl_3",
                "text": "This function ignores users without an age",
                "issue_type": "Incorrect claim",
                "badge_color": "#EF4444", # Red
                "underline_color": "#EF4444",
                "confidence": "High",
                "why_flagged": "The narrative claims the function ignores users without an age, but the code actually crashes with a KeyError on such inputs.",
                "what_assumes": "Assumes the python code executes without throwing an exception on missing key inputs.",
                "evidence_supports": "Running average_age([{'name': 'Bob'}]) raises an unhandled KeyError exception before filtering can occur.",
                "evidence_missing": "Testing or verification of the function implementation against missing-key user dictionary records.",
                "why_uncertain": "The explanatory text contradicts the actual runtime behavior of the code.",
                "what_could_change": "Updating the code logic to handle missing keys so that the narrative claim becomes true.",
                "sources": [
                    {
                        "title": "Python Documentation: dict.get() Method",
                        "url": "https://docs.python.org/3/library/stdtypes.html#dict.get",
                        "domain": "docs.python.org"
                    }
                ]
            }
        ]
    }
}


