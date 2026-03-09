from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from database_config import get_db
from db_agent import query_db_with_natural_language, propose_dml_statement_for_human_approval
from resp_models import AgentQueryRequest, AgentQueryResponse, DMLProposalResponse, DMLProposalRequest

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
            detail=str(e)
        )

@router.post("/dml/propose", response_model =DMLProposalResponse)
async def propose_dml_statement(
        request: DMLProposalRequest,
        session: AsyncSession = Depends(get_db)
):
    try:
        proposed_dml = await propose_dml_statement_for_human_approval(request.query, session=session)
        return DMLProposalResponse(
            approval_id=proposed_dml["approval_id"],
            sql=proposed_dml["sql"],
            status="pending"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

