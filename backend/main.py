"""
backend.main

FastAPI backend for PrepWise.
"""

from __future__ import annotations

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.ai import AIService
from backend.analyzer import DatasetAnalyzer
from backend.cleaner import DataCleaner
from backend.loader import (
    DatasetLoaderError,
    get_dataset_info,
    load_dataset,
)
from backend.utils import dataset_report


app = FastAPI(
    title="PrepWise API",
    version="1.0.0",
    description="AI-Powered Data Preparation Platform",
)


# --------------------------------------------------------
# CORS
# --------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------------
# Health
# --------------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to PrepWise API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------------
# Upload
# --------------------------------------------------------

@app.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...),
):

    try:

        dataframe = load_dataset(
            file.file,
            file.filename,
        )

        analyzer = DatasetAnalyzer(dataframe)

        return {
            "dataset": get_dataset_info(dataframe),
            "analysis": analyzer.analyze(),
        }

    except DatasetLoaderError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# --------------------------------------------------------
# Clean
# --------------------------------------------------------

@app.post("/clean")
async def clean_dataset(
    file: UploadFile = File(...),
):

    try:

        dataframe = load_dataset(
            file.file,
            file.filename,
        )

        cleaner = DataCleaner(dataframe)

        cleaned = cleaner.clean()

        analyzer = DatasetAnalyzer(cleaned)

        return {
            "dataset": get_dataset_info(cleaned),
            "analysis": analyzer.analyze(),
        }

    except DatasetLoaderError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# --------------------------------------------------------
# AI Insights
# --------------------------------------------------------

@app.post("/ai-insights")
async def ai_insights(
    file: UploadFile = File(...),
):

    try:

        dataframe = load_dataset(
            file.file,
            file.filename,
        )

        analyzer = DatasetAnalyzer(dataframe)

        score = analyzer.quality_score()

        report = dataset_report(
            dataframe,
            score,
        )

        ai = AIService()

        insights = ai.analyze_dataset(
            report,
        )

        return {
            "quality_score": score,
            "report": report,
            "ai_insights": insights,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# --------------------------------------------------------
# AI Cleaning Suggestions
# --------------------------------------------------------

@app.post("/cleaning-recommendations")
async def cleaning_recommendations(
    file: UploadFile = File(...),
):

    try:

        dataframe = load_dataset(
            file.file,
            file.filename,
        )

        analyzer = DatasetAnalyzer(dataframe)

        report = dataset_report(
            dataframe,
            analyzer.quality_score(),
        )

        ai = AIService()

        suggestions = ai.cleaning_recommendations(
            report,
        )

        return {
            "recommendations": suggestions
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


# --------------------------------------------------------
# Dashboard Summary
# --------------------------------------------------------

@app.post("/dashboard-summary")
async def dashboard_summary(
    file: UploadFile = File(...),
):

    try:

        dataframe = load_dataset(
            file.file,
            file.filename,
        )

        analyzer = DatasetAnalyzer(dataframe)

        report = dataset_report(
            dataframe,
            analyzer.quality_score(),
        )

        ai = AIService()

        summary = ai.dashboard_summary(
            report,
        )

        return {
            "summary": summary
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )