import json
from urllib.parse import urlparse

def extract_domains_from_har(har_file_path):
    domains = set()
    with open(har_file_path, 'r', encoding='utf-8') as f:
        har_data = json.load(f)

    for entry in har_data['log']['entries']:
      url = entry['request']['url']
      parsed_url = urlparse(url)
      if parsed_url.netloc:
        domains.add(parsed_url.netloc)

    return sorted(list(domains))

if __name__ == '__main__':
    har_file_path = 'D:\\Загрузки\\x.ai_Archive [24-12-21 15-42-27].har'  # замените на путь к вашему HAR файлу
    extracted_domains = extract_domains_from_har(har_file_path)
    for domain in extracted_domains:
      print(domain)
    with open("domains.txt", "w", encoding="utf-8") as f:
        for domain in extracted_domains:
            f.write(domain + "\n")

    print("\nСписок доменов сохранен в domains.txt")