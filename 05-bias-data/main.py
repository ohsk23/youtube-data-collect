from combine_bias import combine_bias

# 실행 예시 (파일 경로를 직접 입력받음)
if __name__ == "__main__":
    input_csv = input("입력 CSV 파일 경로: ")
    combine_bias(input_csv=input_csv, bias_csv='05-bias-data/channel_bias.csv')
