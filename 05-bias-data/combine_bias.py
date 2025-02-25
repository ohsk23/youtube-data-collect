import pandas as pd

def combine_bias(input_csv, bias_csv):
    # input_csv에 채널 bias 정보인 새 행을 추가
    df = pd.read_csv(input_csv)
    bias_df = pd.read_csv(bias_csv)

    df = pd.merge(df, bias_df, on='channel_id', how='left')
    # input filename에서 with_bias.csv 파일 생성
    output_path = input_csv.replace('.csv', '_with_bias.csv')
    df.to_csv(output_path, index=False)
