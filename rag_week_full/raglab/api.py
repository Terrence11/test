import logging
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .core import answer_question

logging.basicConfig(level=logging.INFO)
logger=logging.getLogger('raglab')
app=FastAPI(title='RAG Week 3 API')
xx = uu

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=5,ge=1,le=20)
    rerank: str = Field(default='none',pattern='^(none|keyword|cross)$')

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/ask')
def ask(payload: AskRequest):
    started=time.perf_counter()
    try:
        return answer_question(payload.question,payload.top_k,payload.rerank)
    except ValueError as exc:
        raise HTTPException(status_code=400,detail=str(exc)) from exc
    except RuntimeError as exc:
        logger.exception('RAG not ready')
        raise HTTPException(status_code=503,detail='RAG index or model response unavailable') from exc
    except Exception as exc:
        logger.exception('RAG request failed')
        raise HTTPException(status_code=502,detail='Upstream processing failed') from exc
    finally:
        logger.info('ask latency_seconds=%.2f',time.perf_counter()-started)
