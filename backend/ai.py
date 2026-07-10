"""
backend.ai

Groq AI integration for PrepWise.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


class AIService:
    """
    Groq AI service.
    """

    def __init__(self) -> None:

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY not found in environment variables."
            )

        self.client = Groq(
            api_key=api_key
        )

        # Fast + excellent for analysis
        self.model = "llama-3.3-70b-versatile"

    # -------------------------------------------------------
    # Generic Prompt
    # -------------------------------------------------------

    def ask(
        self,
        prompt: str,
    ) -> str:

        try:

            response = self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are PrepWise AI, an expert data scientist "
                            "and machine learning assistant."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],

                temperature=0.3,
                max_tokens=1200,
            )

            return response.choices[0].message.content

        except Exception as exc:

            return f"AI Error:\n\n{str(exc)}"
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

1. Overall data quality
2. Missing values
3. Duplicate rows
4. Potential issues
5. Recommended preprocessing
6. Suitable machine learning models
7. Business insights

Respond professionally using Markdown.
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

• Missing value strategy
• Outlier handling
• Encoding
• Scaling
• Feature engineering
• ML readiness

Explain every recommendation clearly.
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
Dataset Columns

{columns}

Suggest useful feature engineering ideas.

Include:

• Encoding
• Scaling
• Feature combinations
• Date features
• Target leakage warnings

Respond in Markdown.
"""

        return self.ask(prompt)

    # -------------------------------------------------------
    # Executive Dashboard Summary
    # -------------------------------------------------------

    def dashboard_summary(
        self,
        report: dict,
    ) -> str:

        prompt = f"""
Generate an executive summary for this dataset.

Dataset

{report}

Requirements:

• Maximum 250 words
• Professional tone
• Mention data quality
• Mention possible ML use cases
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
Dataset Context

{context}

User Question

{message}

Answer clearly and professionally.
"""

        return self.ask(prompt)