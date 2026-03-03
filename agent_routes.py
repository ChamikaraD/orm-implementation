from fastapi import APIRouter, HTTPException
from starlette import status

from db_agent import query_db_with_natural_language
from resp_models import AgentQueryRequest, AgentQueryResponse

router  = APIRouter(prefix="/agent", tags=["Database Agent Routes"])



#study about - MCP Servers (Model Context protocol)
@router.post("/query", response_model=AgentQueryResponse)
def query_database(request: AgentQueryRequest) -> AgentQueryResponse:

    try:
        thread_id = request.thread_id
        result = query_db_with_natural_language(user_input=request.query, thread_id=thread_id)
        return AgentQueryResponse(query=request.query, result=result, thread_id=thread_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=True
        )