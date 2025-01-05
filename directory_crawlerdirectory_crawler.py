import requests
from urllib.parse import urljoin

class DirectoryCrawler:
    def __init__(self, base_url, directory_list_file):
        self.base_url = base_url
        self.directory_list_file = directory_list_file
        self.discovered_paths = []

    def load_directories(self):
        with open(self.directory_list_file, 'r') as file:
            directories = [line.strip() for line in file.readlines()]
        return directories

    def test_directories(self, directories):
        for directory in directories:
            url = urljoin(self.base_url, directory)
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    print(f"[+] Found: {url}")
                    self.discovered_paths.append(url)
                elif response.status_code == 302:
                   print(f"[+] Found 302: {url}")
                   self.discovered_paths.append(url) 
                else:
                    print(f"[-] Not Found: {url}")
            except requests.RequestException as e:
                print(f"Error accessing {url}: {e}")

    def save_results(self, output_file='discovered_paths.txt'):
        with open(output_file, 'w') as file:
            file.writelines(f"{path}\n" for path in self.discovered_paths)
        print(f"[+] Results saved to {output_file}")

    def crawl(self):
        print("[*] Starting directoryOWASP DirBuster Project enumeration...")
        directories = self.load_directories()
        self.test_directories(directories)
        self.save_results()

if __name__ == "__main__":
    base_url = input("Enter the target base URL (e.g., http://example.com/): ").strip()
    directory_list_file = "C:/Users/humza/Downloads/Final/directory-list-1.0.txt"
    crawler = DirectoryCrawler(base_url, directory_list_file)
    crawler.crawl()
