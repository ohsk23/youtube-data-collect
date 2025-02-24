import argparse
from json_to_csv import convert_and_combine_all

def main():
    parser = argparse.ArgumentParser(description='Convert JSON files to CSV and combine them')
    parser.add_argument('data_path', type=str, help='Path to the data directory containing json and csv subdirectories')
    
    args = parser.parse_args()
    convert_and_combine_all(args.data_path)

if __name__ == '__main__':
    main()
