from parser import parse_channels
from exporter import export_to_google_sheets

def main():
    parsed_data = parse_channels()
    export_to_google_sheets(parsed_data)

if __name__ == '__main__':
    main()