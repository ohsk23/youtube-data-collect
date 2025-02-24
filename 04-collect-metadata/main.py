from collect_metadata import update_csv_with_youtube_data

# 실행 예시 (파일 경로를 직접 입력받음)
if __name__ == "__main__":
    input_csv = input("입력 CSV 파일 경로: ")
    update_csv_with_youtube_data(input_csv)
