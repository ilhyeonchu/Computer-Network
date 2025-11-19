# main.py
import os, time, httpx
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "tinyllama")   # 미리 pull 해두세요

class PromptRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=2000)
    model: str = "llama3.1"          # 미리 pull
    timeout_ms: int | None = None
    fallback: bool | None = False

@app.post("/ask")
async def ask_ollama(req: PromptRequest):
    t0 = time.perf_counter()
    payload = {"model": req.model, "prompt": req.prompt, "stream": False}
    timeout_s = (req.timeout_ms or 60000) / 1000.0

    async with httpx.AsyncClient(base_url=OLLAMA_BASE_URL, timeout=timeout_s) as client:
        try:
            m0 = time.perf_counter()
            r = await client.post("/api/generate", json=payload)
            r.raise_for_status()
            data = r.json()
            m1 = time.perf_counter()
            t1 = time.perf_counter()
            return {
                "ok": True,
                "data": {"response": data.get("response",""), "used_model": payload["model"]},
                "metrics": {"model_time_ms": int((m1-m0)*1000), "total_ms": int((t1-t0)*1000)}
            }
        except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.TimeoutException):
            if req.fallback and payload["model"] != FALLBACK_MODEL:
                try:
                    payload["model"] = FALLBACK_MODEL
                    m0 = time.perf_counter()
                    r = await client.post("/api/generate", json=payload)
                    r.raise_for_status()
                    data = r.json()
                    m1 = time.perf_counter(); t1 = time.perf_counter()
                    return {
                        "ok": True,
                        "data": {"response": data.get("response",""), "used_model": payload["model"], "strategy":"fallback"},
                        "metrics": {"model_time_ms": int((m1-m0)*1000), "total_ms": int((t1-t0)*1000)}
                    }
                except Exception:
                    pass
            return {"ok": False, "error": {"code":"TIMEOUT","message":"upstream timed out","phase":"ollama_call"}}
        except httpx.HTTPError as e:
            return {"ok": False, "error": {"code":"UPSTREAM_ERROR","message":str(e)}}
