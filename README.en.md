## Video Data Collection and Keyword Search Pipeline

### 0. Pipeline Overview

1. Collect channel video data using the yt-dlp library
2. Convert all data to CSV and merge them
3. Filter keywords using exact match
4. (Optional) Collect additional video information (engagement data, etc.)

### 1. Collecting Channel Video Data Using yt-dlp

1. Install the yt-dlp library (one-time setup)

- Reference: https://github.com/yt-dlp/yt-dlp
- Installation options:

  ```bash
  # For macOS (using Homebrew)
  $ brew install yt-dlp

  # For Windows (using pip)
  $ pip install yt-dlp

  # For Linux
  $ sudo curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp
  $ sudo chmod a+rx /usr/local/bin/yt-dlp
  ```

2. Enter channel URLs and names in the `01-yt-dlp/channels.txt` file

- Refer to the example file `channels.sample.txt`
- You can use channel URLs or channel ID URLs as shown below:

```python
# channels.txt
https://www.youtube.com/@cnn CNN
https://www.youtube.com/channel/UCCjG8NtOig0USdrT5D1FpxQ NewsNation
```

3. Run the following code from the project root

- This may take over 3 hours depending on the number of videos in the channel
- Even if warning messages appear, data collection will proceed normally, so please wait patiently
- If the resulting file is empty, retry the process

```bash
$ source ./01-yt-dlp/yt-dlp.sh
```

4. Channel video data will be saved in the `data/YYYYMMDD/json` folder

- Check for empty files and repeat steps 1-3 for those channels if necessary

### 2. Converting Data to CSV

1. Run the following code from the project root. Enter the date folder as an argument (`/YYYYMMDD` folder, not `/json`)

```bash
$ python 02-preprocessing/main.py ./data/20240315
```

2. Converted CSV files for each channel will be saved in `data/YYYYMMDD/csv`, and the merged file will be saved as `data/YYYYMMDD/all.csv` (takes about 3 minutes)

### 3. Keyword Filtering Using Exact Match

0. If needed, install the libraries from `03-exact-match/requirements.txt`

```bash
$ cd 03-exact-match
$ pip install -r requirements.txt
$ cd ../
```

1. Write your desired keywords in the `03-exact-match/keywords.txt` file

- Refer to the example file `keywords.sample.txt`
- Write one keyword per line (case insensitive)

```python
# keywords.txt
ai
artificial intelligence
machine learning
deep learning
neural network
```

2. Run the code from the project root with your desired search options (takes about 3 minutes)

```bash
$ python 03-exact-match/main.py title ./data/20240315/all.csv
$ python 03-exact-match/main.py title_desc ./data/20240315/all.csv
```

3. Search results will be saved as `data/YYYYMMDD/result_title.csv` or `data/YYYYMMDD/result_title_desc.csv`

### 4. (Optional) Collecting Additional Video Information

- Uses Youtube data api v3's videos api to collect additional information
- For large datasets, concurrent.futures.ThreadPoolExecutor (multithreading) can be used to collect data faster

0. If needed, install the libraries from `04-collect-metadata/requirements.txt`

```bash
$ cd 04-collect-metadata
$ pip install -r requirements.txt
$ cd ../
```

1. Enter your valid API key in the `04-collect-metadata/.env` file

- Get an API key by referring to https://developers.google.com/youtube/v3/getting-started
- Important: Keep your API key secure and never commit it to version control
- Create a new .env file and add your API key:

```bash
$ echo "YOUTUBE_API_KEY=YOUR_API_KEY_HERE" > 04-collect-metadata/.env
```

2. Run `04-collect-metadata/main.py`. Enter the target file for metadata collection as an argument (takes about 10 minutes)

```bash
$ python 04-collect-metadata/main.py ./data/20240315/result_title.csv
```

3. The file with collected metadata will be saved as {target_file_path}\_metadata.csv

### 5. (Optional) Combining with Channel Bias Data

1. Write channel bias data in the `05-bias-data/channel_bias.csv` file

- Refer to the example file `channel_bias.sample.csv`

2. Run the following code from the project root

```bash
$ python 05-bias-data/main.py
# Enter the path to ./data/YYYYMMDD/result_title_metadata.csv file
```

3. The file with combined bias data will be saved as `{target_file_path}\_with_bias.csv`
