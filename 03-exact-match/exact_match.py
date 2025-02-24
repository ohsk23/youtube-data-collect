def exact_match_title(df, keywords_list, output_file):
  #    - (?i): 대소문자 무시(케이스 인식 끔)
  #    - \b: 단어 경계
  #    - (?: ... ): 그룹핑 (캡처는 안 하는) => or 조건
  #    - 만약 복수형 처리를 하려면 "gans?" 식으로 s? 추가도 가능
  #    - 단, 여기선 간단히 작성
  pattern = r"(?i)\b(?:{})\b".format("|".join(keywords_list))
  # NaN 값을 빈 문자열로 대체
  df['title'] = df['title'].fillna('')
  searched = df[df['title'].str.contains(pattern, regex=True)]
  searched.to_csv(output_file, index=False)
  print('검색된 항목 개수: ', len(searched))


def exact_match_title_and_description(df, keywords_list, output_file):
  #    - (?i): 대소문자 무시(케이스 인식 끔)
  #    - \b: 단어 경계
  #    - (?: ... ): 그룹핑 (캡처는 안 하는) => or 조건
  #    - 만약 복수형 처리를 하려면 "gans?" 식으로 s? 추가도 가능
  #    - 단, 여기선 간단히 작성
  pattern = r"(?i)\b(?:{})\b".format("|".join(keywords_list))
  # NaN 값을 빈 문자열로 대체
  df['title'] = df['title'].fillna('')
  searched = df[df['title'].str.contains(pattern, regex=True) | df['description'].str.contains(pattern, regex=True)]
  searched.to_csv(output_file, index=False)
  print('검색된 항목 개수: ', len(searched))

