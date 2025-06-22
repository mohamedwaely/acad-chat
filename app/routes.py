from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
# from fastapi.responses import StreamingResponse

from app import models, schemas
from app.db import get_db
from chat.generate_response import llm_response
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

router = APIRouter()

from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

@router.post("/v1/add-project")
async def add_project(data: schemas.ProjectBase, db: Session = Depends(get_db)):
    # Create document string for embedding - now including team_members
    tools_str = " ".join(data.tools)
    team_members_str = " ".join(data.team_members)
    doc = f"{data.title} {data.supervisor} {data.description} {tools_str} {team_members_str} {data.year}"
    doc_embedding = embeddings.embed_query(doc)

    proj = models.Project(
        title=data.title,
        description=data.description,
        tools=data.tools,
        team_members=data.team_members,
        supervisor=data.supervisor,
        year=data.year,
        embedding=doc_embedding
    )
    
    if db.query(models.Project).filter(models.Project.title == data.title).first():
        raise HTTPException(status_code=500, detail=f"Project title already exists")
    
    try:
        db.add(proj)
        db.commit()
        db.refresh(proj)
        return {"res": "Project added successfully"}
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Failed to add project: {str(e)}")



# @router.post("/v1/chat", response_class=StreamingResponse)
@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(query: schemas.ChatRequest, db: Session = Depends(get_db)):
    if not query.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    query_embedding = embeddings.embed_query(query.query)
    
    similar_projects = db.query(models.Project).order_by(
        models.Project.embedding.cosine_distance(query_embedding)
    ).limit(3).all()
    if not similar_projects:
        raise HTTPException(status_code=400, detail="No projects found")
    
    # async def stream_res():
    #     try:
    #         async for chunk in llm_response(query.query, similar_projects):
    #             yield f"data: {chunk}\n\n"
    #     except Exception as e:
    #         yield f"data: {str(e)}\n\n"
    #         yield f"data: [DONE]\n\n"

    # return StreamingResponse(stream_res(), media_type="text/event-stream")

    response = await llm_response(query.query, similar_projects)

    return {"response": response}