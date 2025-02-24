## 영상 데이터 수집 및 키워드 검색 파이프라인

### 0. 전체 파이프라인 개요

1. yt-dl 라이브러리를 이용하여 채널 전체 영상 데이터 수집
2. 전체 데이터를 CSV로 변환하고 하나로 합침
3. exact match를 이용한 키워드 필터링
4. (Optional) 수집한 데이터에 대한 추가 영상 정보를 수집하기 (engagement data 등)

### 1. yt-dl 라이브러리를 이용하여 채널 전체 영상 데이터 수집

1. yt-dlp 라이브러리를 설치한다. (한번만)

```bash
$ brew install yt-dlp
```

2. 채널 url과 이름을 01-yt-dlp/channels.txt 파일에 입력한다.

- 해당 파일 예시인 channels.sample.txt 파일을 참고하여 작성한다.
- 아래와 같이 채널 URL이나 채널 ID를 이용한 URL을 사용할 수 있다.

```python
# channels.txt
https://www.youtube.com/@cnn CNN
https://www.youtube.com/channel/UCCjG8NtOig0USdrT5D1FpxQ NewsNation
```

3. 프로젝트 루트에서 아래 코드를 실행한다.

- 채널 내 영상 개수가 많은 경우 30분 ~ 1시간 이상 소요될 수 있다.
- 실행 후 빈 파일인 경우 재시도해야 함.

```bash
$ source ./01-yt-dlp/yt-dlp.sh
```

4. 채널 전체 영상 데이터가 data/YYYYMMDD/json 폴더에 저장된다.

- 빈 파일이 있는지 확인하고 있다면 해당 채널에 대해서 1 - 3 단계를 반복한다.

### 2. yt-dl을 이용하여 수집한 데이터 전처리

1. 프로젝트 루트에서 아래 코드를 실행한다. 변환을 원하는 날짜의 폴더를 args로 입력한다. (/json 이 아니라 /YYYYMMDD 폴더를 입력)

```bash
$ python 02-preprocessing/main.py ./data/20250224
```

2. 채널 별로 변환된 CSV 파일이 data/YYYYMMDD/csv 폴더에 저장되며, 전체를 합친 파일은 data/YYYYMMDD/all.csv 파일에 저장된다.

### 3. exact match를 이용한 키워드 필터링

0. 필요한 경우 03-exact-match/requirements.txt 의 라이브러리를 설치한다.

```bash
$ cd 03-exact-match
$ pip install -r requirements.txt
$ cd ../
```

1. 원하는 키워드 목록을 03-exact-match/keywords.txt 파일에 작성한다.

- 해당 파일 예시인 keywords.sample.txt 파일을 참고하여 작성한다.
- 키워드는 한 줄에 하나씩 작성한다. (대소문자 구분 없음)

```python
# keywords.txt
ai
artificial intelligence
machine learning
deep learning
neural network
```

2. 프로젝트 루트에서 원하는 검색 옵션에 따라 코드를 실행한다.

- title에서만 검색을 원하는 경우 title 옵션을, title과 description에서 검색을 원하는 경우 title_desc 옵션을 입력한다.

```bash
$ python 03-exact-match/main.py title ./data/20250224/all.csv
$ python 03-exact-match/main.py title_desc ./data/20250224/all.csv
```

3. 검색 결과는 data/YYYYMMDD/result_title.csv 또는 data/YYYYMMDD/result_title_desc.csv 파일에 저장된다.

### 4. (Optional) 추가 영상 정보 수집

0. 필요한 경우 04-collect-metadata/requirements.txt 의 라이브러리를 설치한다.

```bash
$ cd 04-collect-metadata
$ pip install -r requirements.txt
$ cd ../
```

1. 04-collect-metadata/.env 파일에 올바른 API 키를 입력한다.

- https://developers.google.com/youtube/v3/getting-started 를 참고하여 API 키를 발급받는다.

```bash
$ echo "YOUTUBE_API_KEY=AIzaS...." > 04-collect-metadata/.env
```

2. 04-collect-metadata/main.py 파일을 실행한다. 메타데이터를 수집할 타겟 파일을 args로 입력한다.

```bash
$ python 04-collect-metadata/main.py ./data/20250224/result_title.csv
```

3. 메타데이터가 수집된 파일은 {타겟 파일 경로}\_metadata.csv 파일에 저장된다.

## 기타 데이터 수집 방법

98. search API를 이용하여 영상 데이터 수집하는 방법
99. 댓글 데이터 수집 - 멀티스레딩

- colab에서 부하가 많이 걸리므로 가능한 로컬에서 실행

  > $ source ./01-yt-dlp/yt-dlp-url.sh
