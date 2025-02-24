import pandas as pd
import googleapiclient.discovery
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# YouTube Data API 키 설정
API_KEY = os.getenv("YOUTUBE_API_KEY")  # .env에서 API 키 가져오기
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

def get_youtube_client(api_key):
    """YouTube API 클라이언트 생성"""
    return googleapiclient.discovery.build(API_SERVICE_NAME, API_VERSION, developerKey=api_key)

def get_video_details(youtube, video_id):
    """비디오 ID를 받아서 조회수, 좋아요, 댓글 수, 업로드 날짜를 가져옴"""
    request = youtube.videos().list(
        part="statistics,snippet",
        id=video_id
    )
    response = request.execute()

    if "items" not in response or len(response["items"]) == 0:
        return None

    item = response["items"][0]
    stats = item["statistics"]
    snippet = item["snippet"]

    return {
        "viewCount": int(stats.get("viewCount", 0)),
        "likeCount": int(stats.get("likeCount", 0)),
        "commentCount": int(stats.get("commentCount", 0)),
        "publishedAt": snippet.get("publishedAt", "")
    }

def update_csv_with_youtube_data(input_csv):
    """CSV 파일을 불러와 YouTube API에서 추가 데이터를 가져와 업데이트"""
    youtube = get_youtube_client(API_KEY)
    
    # CSV 데이터 불러오기
    df = pd.read_csv(input_csv)

    # 새로운 컬럼 추가 (없으면 생성)
    df["likes"] = None
    df["comments"] = None
    df["published_at"] = None

    # 비디오 정보 업데이트
    for idx, row in df.iterrows():
        video_id = row["id"]
        video_data = get_video_details(youtube, video_id)

        if video_data:
            df.at[idx, "view_count"] = video_data["viewCount"]
            df.at[idx, "likes"] = video_data["likeCount"]
            df.at[idx, "comments"] = video_data["commentCount"]
            df.at[idx, "published_at"] = video_data["publishedAt"]

    output_csv = input_csv.replace(".csv", "_metadata.csv")
    # 업데이트된 데이터 저장
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"업데이트된 데이터가 {output_csv} 파일에 저장되었습니다.")

