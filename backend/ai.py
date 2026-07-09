"""
backend.ai

Gemini AI integration for PrepWise.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from google import genai


load_dotenv()


class AIService:
    """
    Gemini AI service.
    """

    def __init__(self) -> None:

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        self.client = genai.Client(api_key=api_key)

        self.model = "gemini-2.5-flash"

    # -------------------------------------------------------
    # Generic Prompt
    # -------------------------------------------------------

    def ask(
        self,
        prompt: str,
    ) -> str:

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text

    # -------------------------------------------------------
    # Dataset Analysis
    # -------------------------------------------------------

    def analyze_dataset(
        self,
        report: dict,
    ) -> str:

        prompt = f"""
You are PrepWise AI.

You are a professional data scientist.

Analyze the following dataset summary.

Dataset Summary

{report}

Explain:

1. Overall quality

2. Missing values

3. Duplicate rows

4. Potential issues

5. Recommended preprocessing

6. Suggested ML models

7. Business insights

Respond in professional markdown.
"""

        return self.ask(prompt)

    # -------------------------------------------------------
    # Cleaning Suggestions
    # -------------------------------------------------------

    def cleaning_recommendations(
        self,
        report: dict,
    ) -> str:

        prompt = f"""
You are an expert data engineer.

Dataset Information

{report}

Suggest:

- Missing value strategy
- Outlier handling
- Encoding
- Scaling
- Feature engineering
- ML readiness

Explain every recommendation.
"""

        return self.ask(prompt)

    # -------------------------------------------------------
    # Feature Engineering
    # -------------------------------------------------------

    def feature_engineering(
        self,
        columns: list[str],
    ) -> str:

        prompt = f"""
Columns

{columns}

Suggest useful feature engineering ideas.

Include:

- Encoding
- Scaling
- Feature combinations
- Date features
- Target leakage warnings
"""

        return self.ask(prompt)

    # -------------------------------------------------------
    # Dashboard Insights
    # -------------------------------------------------------

    def dashboard_summary(
        self,
        report: dict,
    ) -> str:

        prompt = f"""
Generate an executive summary.

Dataset

{report}

Keep it concise.

Maximum 250 words.
"""

        return self.ask(prompt)

    # -------------------------------------------------------
    # Custom Chat
    # -------------------------------------------------------

    def chat(
        self,
        message: str,
        context: Optional[dict] = None,
    ) -> str:

        prompt = f"""
Context

{context}

Question

{message}
"""

        return self.ask(prompt)