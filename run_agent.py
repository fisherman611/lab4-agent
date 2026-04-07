import json
import argparse
import sys
import time
from datetime import datetime
from pathlib import Path

from langchain_core.messages import HumanMessage

# Cấu hình stdout/stderr UTF-8
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

# Import graph
try:
    from src.agent import graph
except ImportError:
    print("Lỗi: Không thể import 'graph' từ 'src.agent'. Đảm bảo bạn đang chạy từ thư mục gốc của dự án.")
    sys.exit(1)


def load_test_cases(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Hỗ trợ cả 2 dạng:
    # 1) [{"id": ...}, ...]
    # 2) {"tests": [{"id": ...}, ...]}
    if isinstance(data, dict) and "tests" in data:
        return data["tests"]
    return data


def make_logger(file_handle=None):
    def log(msg=""):
        # In ra console
        print(msg)

        # Ghi vào file nếu có
        if file_handle is not None:
            print(msg, file=file_handle)
            file_handle.flush()

    return log


def run_test_case(case, verbose=False, file_handle=None):
    log = make_logger(file_handle)
    start_time = time.time()

    header = f" TEST CASE {case['id']}: {case['name']} "

    log()
    log("=" * 80)
    log(header.center(80, "="))
    log("=" * 80)
    log(f"Bat dau luc: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"Mo ta: {case.get('description', 'Khong co mo ta')}")
    log(f"Input: {case['input']}")

    if verbose:
        log()
        log("Expected Behavior:")
        log(f"  {case['expected']['behavior']}")
        expected_tool_calls = case["expected"].get("tool_calls", [])
        if expected_tool_calls:
            log("  Expected Tool Calls:")
            log(json.dumps(expected_tool_calls, indent=2, ensure_ascii=False))

    log()
    log("*" * 10 + " AGENT EXECUTION " + "*" * 10)

    try:
        result = graph.invoke({
            "messages": [HumanMessage(content=case["input"])]
        })

        final_message = result["messages"][-1]

        log()
        log("TravelBuddy:")
        log("--- CONTENT BEGIN ---")
        log(final_message.content)
        log("--- CONTENT END ---")

        # Thu các tool calls từ toàn bộ history
        tool_calls = []
        for m in result["messages"]:
            if hasattr(m, "tool_calls") and m.tool_calls:
                tool_calls.extend(m.tool_calls)

        log()
        if tool_calls:
            log("Tools da goi:")
            for tc in tool_calls:
                log(f"  - {tc['name']}({tc['args']})")
        else:
            log("Agent khong goi tool nao.")

    except Exception as e:
        log()
        log(f"LOI KHI CHAY AGENT: {str(e)}")
        import traceback
        tb = traceback.format_exc()
        log(tb)

    duration = time.time() - start_time
    log()
    log(f"Thoi gian thuc hien: {duration:.2f} giay")
    log("=" * 80)
    log()

    return True


def list_test_cases(test_cases):
    print()
    print("=" * 50)
    print("DANH SACH TEST CASES".center(50))
    print("=" * 50)
    print(f"{'ID':<5} {'Ten Test Case':<30}")
    print("-" * 50)
    for case in test_cases:
        print(f"{case['id']:<5} {case['name']:<30}")
    print("=" * 50)
    print()


def main():
    parser = argparse.ArgumentParser(description="TravelBuddy Agent Testing Tool")
    parser.add_argument("--id", type=int, help="ID cua test case cu the")
    parser.add_argument("--all", action="store_true", help="Chay tat ca cac test cases")
    parser.add_argument("--list", action="store_true", help="Liet ke danh sach cac test cases")
    parser.add_argument("--verbose", action="store_true", help="Hien thi chi tiet expected behavior")
    parser.add_argument("--output", type=str, help="Luu log vao file UTF-8")
    args = parser.parse_args()

    test_cases_file = "tests/test_cases.json"

    try:
        test_cases = load_test_cases(test_cases_file)
    except FileNotFoundError:
        print(f"Khong tim thay file test cases tai: {test_cases_file}")
        return

    if args.list:
        list_test_cases(test_cases)
        return

    out_f = None
    if args.output:
        # utf-8-sig để Notepad/Windows đọc dễ hơn
        out_f = open(args.output, "w", encoding="utf-8-sig", newline="\n")
        print(f"Dang ghi log vao file: {args.output}")

    try:
        if args.all:
            print(f"Dang chay TAT CA {len(test_cases)} test cases...")
            for case in test_cases:
                run_test_case(case, args.verbose, file_handle=out_f)
            print("Hoan thanh chay tat ca test cases.")

        elif args.id is not None:
            case = next((c for c in test_cases if c["id"] == args.id), None)
            if case:
                run_test_case(case, args.verbose, file_handle=out_f)
            else:
                print(f"Khong tim thay test case voi ID: {args.id}")

        else:
            parser.print_help()

    finally:
        if out_f:
            out_f.close()


if __name__ == "__main__":
    main()