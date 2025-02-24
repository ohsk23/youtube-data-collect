
import concurrent.futures

def collect_all_comments(video_ids):
  api_call_count = 0

  with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
      futures = {executor.submit(get_video_comments, video_id, API_KEY): video_id for video_id in video_ids}
      
      for future in concurrent.futures.as_completed(futures):
          video_id = futures[future]
          try:
              result = future.result()
              api_call_count += result
          except Exception as e:
              print(f"❌ {video_id} 처리 중 에러 발생: {e}")

  print(f"\n🚀 총 API 호출 횟수: {api_call_count}")
