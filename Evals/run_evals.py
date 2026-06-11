import json
import requests

API_BASE_URL = "http://localhost:8000"


def load_eval_questions():
    with open("evals/eval_questions.json", "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate_answer(answer, expected_keywords):
    answer_lower = answer.lower()

    missing_keywords = [
        keyword for keyword in expected_keywords
        if keyword.lower() not in answer_lower
    ]

    return len(missing_keywords) == 0, missing_keywords


def run_evals():
    eval_questions = load_eval_questions()

    passed = 0
    total = len(eval_questions)

    for item in eval_questions:
        response = requests.post(
            f"{API_BASE_URL}/ask",
            json={
                "question": item["question"],
                "sources": [item["source"]],
                "session_id": "eval-session"
            }
        )

        data = response.json()
        answer = data["answer"]

        success, missing_keywords = evaluate_answer(
            answer,
            item["expected_keywords"]
        )

        if success:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"

        print("=" * 80)
        print(f"Question: {item['question']}")
        print(f"Answer: {answer}")
        print(f"Status: {status}")

        if missing_keywords:
            print(f"Missing Keywords: {missing_keywords}")

    print("=" * 80)
    print(f"Evaluation Results: {passed}/{total} passed")


if __name__ == "__main__":
    run_evals()