from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import time
import uvicorn
from io import BytesIO
from docx import Document
from SummarizeText import SummarizeText

app = FastAPI()
summarizer = SummarizeText("summarize_config.yaml")
model_id = summarizer.model_path
started_at = time.time()

@app.get("/")
def root():
    return {
        "system": "FastAPI + Hugging Face Text Summarization API",
        "description": "Tóm tắt văn bản bằng mô hình AI trên Hugging Face.",
        "main_features": [
            "Nhận file văn bản từ người dùng",
            "Tóm tắt nội dung bằng facebook/bart-large-cnn",
            "Trả kết quả dưới dạng JSON"
        ],
        "version": "1.0"
    }

@app.post("/predict")
async def predict(file: Optional[UploadFile] = File(None), text: Optional[str] = Form(None)):
    # Allow either text file upload or raw text input.
    if file is None and (text is None or not text.strip()):
        raise HTTPException(status_code=400, detail="Provide either 'file' (.txt/.docx/.doc/.pdf) or non-empty 'text'.")

    input_text = None
    source = "text"
    filename = None

    if file is not None:
        filename = (file.filename or "").strip()
        _, ext = os.path.splitext(filename.lower())
        allowed_exts = {".txt", ".docx", ".doc", ".pdf"}
        if ext and ext not in allowed_exts:
            raise HTTPException(status_code=400, detail="Only .txt, .docx, .doc, .pdf file is supported.")

        raw = await file.read()
        if not raw:
            raise HTTPException(status_code=400, detail="Empty file.")

        try:
            if ext == ".txt" or ext == "":
                input_text = raw.decode("utf-8").strip()
            elif ext == ".docx":
                doc = Document(BytesIO(raw))
                input_text = "\n".join(p.text for p in doc.paragraphs).strip()
            elif ext == ".doc":
                raise HTTPException(
                    status_code=400,
                    detail="Legacy .doc is not supported in this environment. Please convert to .docx or .txt.",
                )
            elif ext == ".pdf":
                from pypdf import PdfReader
                reader = PdfReader(BytesIO(raw))
                pages = [page.extract_text() or "" for page in reader.pages]
                input_text = "\n".join(pages).strip()
        except HTTPException:
            raise
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text.")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Could not parse input file: {e}")

        source = "file"
    else:
        input_text = text.strip()

    if not input_text:
        raise HTTPException(status_code=400, detail="Input text is empty.")

    # Bound input length to keep inference stable with long documents.
    max_chars = 4000
    was_truncated = len(input_text) > max_chars
    model_input = input_text[:max_chars]

    try:
        summary_text = summarizer(model_input)

        return {
            "status": "ok",
            "input": {
                "source": source,
                "filename": filename,
                "original_chars": len(input_text),
                "used_chars": len(model_input),
                "truncated": was_truncated,
            },
            "prediction": {
                "summary": summary_text
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {e}")

@app.get("/health")
def health():
    try:
        _ = summarizer is not None and summarizer.model is not None and summarizer.tokenizer is not None
        return {
            "status": "ok",
            "uptime_s": round(time.time() - started_at, 3),
            "model_id": model_id,
            "model_loaded": True,
        }
    except Exception as e:
        return {
            "status": "error",
            "uptime_s": round(time.time() - started_at, 3),
            "model_id": model_id,
            "model_loaded": False,
            "detail": str(e),
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)