from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from crew import research_crew
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins, or specify origins if you want stricter control
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or set to ["https://your-html-host.com"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchInput(BaseModel):
    topic: str

@app.post("/research")
def start_research(input: ResearchInput):
    try:
        # Trigger the research process
        result = research_crew.kickoff({"topic": input.topic})
        # Optionally, save result to a file or DB if persistence is needed
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report/{report_type}")
def get_report(report_type: str):
    """report_type can be 'research_findings', 'analysis_report', 'final_report'"""
    filename_map = {
        "research_findings": "research_findings.md",
        "analysis_report": "analysis_report.md",
        "final_report": "final_report.md",
    }
    filename = filename_map.get(report_type)
    if not filename:
        raise HTTPException(status_code=400, detail="Invalid report type.")
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return {"file": filename, "content": content}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")


