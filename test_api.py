import argparse
import json
from pathlib import Path

import requests


def print_response(name: str, response: requests.Response) -> None:
    print(f"\n=== {name} ===")
    print(f"Status: {response.status_code}")
    try:
        print(json.dumps(response.json(), ensure_ascii=False, indent=2))
    except Exception:
        print(response.text)


def test_health(base_url: str) -> None:
    response = requests.get(f"{base_url}/health", timeout=30)
    print_response("GET /health", response)


def test_predict_with_text(base_url: str, text: str) -> None:
    response = requests.post(
        f"{base_url}/predict",
        data={"text": text},
        timeout=120,
    )
    print_response("POST /predict (text)", response)


def test_predict_with_file(base_url: str, file_path: Path) -> None:
    mime = "text/plain"
    if file_path.suffix.lower() == ".pdf":
        mime = "application/pdf"
    elif file_path.suffix.lower() == ".docx":
        mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    with file_path.open("rb") as f:
        response = requests.post(
            f"{base_url}/predict",
            files={"file": (file_path.name, f, mime)},
            timeout=180,
        )
    print_response(f"POST /predict (file={file_path.name})", response)


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple API test script using requests.")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000", help="FastAPI base URL")
    parser.add_argument("--file", default="", help="Optional path to .txt/.docx/.pdf to test upload")
    args = parser.parse_args()

    sample_text = (
        "The global COVID-19 pandemic (also known as the coronavirus pandemic), caused by" 
        "severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2), began with an outbreak" 
        "in Wuhan, China, in December 2019. It spread to other parts of Asia and then" 
        "worldwide in early 2020. The World Health Organization (WHO) declared the outbreak" 
        "a public health emergency of international concern (PHEIC) on 30 January 2020, and" 
        "assessed it as having become a pandemic on 11 March.[3] The WHO declared that the" 
        "public health emergency caused by COVID-19 had ended in May 2023."
    )

    print(f"Testing API at: {args.base_url}")
    test_health(args.base_url)
    test_predict_with_text(args.base_url, sample_text)

    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"\n[WARN] File not found: {file_path}")
            return
        test_predict_with_file(args.base_url, file_path)


if __name__ == "__main__":
    main()
