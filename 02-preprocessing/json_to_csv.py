import json
import csv
import os
import pandas as pd

def json_to_csv(data_path, csv_path):
    try:
        with open(data_path, 'r') as f:
            content = f.read().strip()
            if not content:  # 파일이 비어있는 경우
                print(f"Warning: {os.path.basename(data_path)}에 대해 데이터가 수집되지 않았습니다.")
                return False
            
            data = json.loads(content)
            
        videos = data['entries'][0]['entries']
        channel = data['channel']
        channel_id = data['channel_id']
        
        with open(csv_path, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'description', 'view_count', 'channel', 'channel_id'])
            for video in videos:
                writer.writerow([video['id'], video['title'], video['description'], video['view_count'], channel, channel_id])
        return True
        
    except json.JSONDecodeError:
        print(f"Warning: {os.path.basename(data_path)}에 대해 데이터가 수집되지 않았습니다.")
        return False

def convert_and_combine_all(data_path):
    json_path = f'{data_path}/json'
    csv_path = f'{data_path}/csv'
    
    # Create CSV directory if it doesn't exist
    os.makedirs(csv_path, exist_ok=True)
    
    successful_files = []
    for file in os.listdir(json_path):
        if json_to_csv(f'{json_path}/{file}', f'{csv_path}/{file.replace(".json", ".csv")}'):
            successful_files.append(file.replace(".json", ".csv"))

    if not successful_files:
        print("처리된 파일이 없습니다.")
        return None

    files = [f for f in successful_files if f.endswith('.csv')]
    df = pd.concat(
        [pd.read_csv(f'{csv_path}/{file}') for file in files],
        ignore_index=True
    )

    df.to_csv(f'{data_path}/all.csv', index=False)
    print(f'전체 수집된 행 개수: {len(df)}')
    return df

