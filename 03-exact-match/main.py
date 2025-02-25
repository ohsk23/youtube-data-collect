import sys
import pandas as pd
from exact_match import exact_match_title, exact_match_title_and_description
import os

def show_help():
    print("""
Usage: python main.py [--help] <function_type> <input_csv>

Arguments:
    function_type    'title' or 'title_desc'
                    - title: 제목에서만 키워드 검색
                    - title_desc: 제목과 설명 모두에서 키워드 검색
    input_csv       입력 CSV 파일 경로

Options:
    --help          도움말 표시

Example:
    python main.py title input.csv
    python main.py title_desc input.csv
    """)
    sys.exit(0)

def read_keywords(keyword_file):
    with open(keyword_file, 'r', encoding='utf-8') as f:
        # 각 줄을 읽어서 공백을 제거하고 빈 줄은 제외
        keywords = [line.strip() for line in f if line.strip()]
    return keywords

def main():
    if len(sys.argv) == 2 and sys.argv[1] == '--help':
        show_help()
    
    if len(sys.argv) != 3:
        print("Usage: python main.py <function_type> <input_csv>")
        print("Try 'python main.py --help' for more information")
        sys.exit(1)

    function_type = sys.argv[1]
    input_csv = sys.argv[2]
    keyword_file = "03-exact-match/keywords.txt"
    
    # CSV 파일 읽기
    df = pd.read_csv(input_csv, low_memory=False)
    
    # 키워드 목록 읽기
    keywords_list = read_keywords(keyword_file)
    
    input_dir = os.path.dirname(input_csv)
    # 출력 파일명 설정
    output_file = f"{input_dir}/result_{function_type}.csv"
    
    # 함수 선택 및 실행
    if function_type == 'title':
        exact_match_title(df, keywords_list, output_file)
    elif function_type == 'title_desc':
        exact_match_title_and_description(df, keywords_list, output_file)
    else:
        print("Invalid function type. Use 'title' or 'title_desc'")
        sys.exit(1)

if __name__ == "__main__":
    main()
