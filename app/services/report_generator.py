# from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv
from fastapi import HTTPException
from app.services.data_loader import load_data
from app.services.data_quality import run_data_quality_checks

from app.utils.config import REPORT_DIR
from app.utils.logger import get_logger
load_dotenv()
# llm=HuggingFaceEndpoint(
#         repo_id="Qwen/Qwen2.5-72B-Instruct",
#         task="text-generation"
#     )

from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.1-8b-instant",   # or mixtral-8x7b-32768
    
    temperature=0.3,
)


# llm = HuggingFaceEndpoint(
#     endpoint_url="https://api-inference.huggingface.co/models/Qwen/Qwen2.5-72B-Instruct",
#     task="text-generation"
# )
# model = ChatHuggingFace(llm=llm)
model=llm


logger=get_logger(__name__)

def generate_report_with_llm( file_id:str):

    import json

    report_path = REPORT_DIR / f"{file_id}_report.json"


    if report_path.exists():
        logger.info(f"Report already exists for {file_id}, loading from disk")
        with open(report_path, "r", encoding="utf-8") as f:
            report = json.load(f)
        return {
            "file_id": file_id,
            "report": report,
            "report_path": str(report_path)
        }
    data=load_data(file_id)
    metrics=run_data_quality_checks(data)
    metrics = json.dumps(metrics, indent=2)
    schema=[
        ResponseSchema(name='summary', description=(
                    "Provide a concise overview of the dataset quality based on the metrics. "
                        "Mention dataset size, presence of missing values, duplicates, and outliers. "
                        "Highlight whether the dataset is generally clean or requires attention.")),
        ResponseSchema(name="risk_level",description=(
                    "Assess the overall data quality risk level as one of: Low, Medium, or High. "
                    "Base this on missing values, duplicate records, and outliers. "
                    "Low means clean data, Medium means moderate issues, High means significant data quality problems.")),
        ResponseSchema(name="recommendations", description=(
                    "Provide actionable suggestions to improve data quality. "
                        "Include steps like handling missing values, removing duplicates, "
                        "treating outliers, or validating data types. Keep recommendations practical and concise."))
    ]

    parser=StructuredOutputParser.from_response_schemas(schema)
    template= PromptTemplate(
        template=
            """
            You are a professional data analyst.

            Your task is to analyze dataset quality metrics and generate a structured report.

            Dataset Quality Metrics:
            {metrics}

            Instructions:
            - Analyze the dataset based on missing values, duplicates, outliers, and metadata.
            - Be concise and factual.
            - Do not make assumptions beyond the provided data.
            - Keep the response professional and clear.

            {format_instructions}
            """,
        input_variables=['metrics'],
        partial_variables={'format_instructions':parser.get_format_instructions()}
    )

    # chain = template | model 

    try:
        prompt = template.format(metrics=metrics)
        raw_output = model.invoke(prompt).content

        if not isinstance(raw_output, str):
            raw_output = str(raw_output)

        try:
            response = parser.parse(raw_output)
        except Exception:
            logger.warning("Parser failed, returning raw output")
            response = {
                "summary": raw_output,
                "risk_level": "unknown",
                "recommendations": "Parsing failed. Check raw output."
            }
        logger.info(f"Report generated successfully for {file_id}")
    except Exception as e:
        logger.error(f"LLM report generation failed for {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Report generation failed")

    try:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(response, f,indent=4)
        logger.info(f"Report saved at {report_path}")
    except Exception as e:
        logger.error(f"Failed to save report for {file_id}: {str(e)}")

    return {
        "file_id": file_id,
        "report": response,
        "report_path": str(report_path)
    }