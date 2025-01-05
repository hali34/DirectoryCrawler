import requests
from urllib.parse import urljoin

class DirectoryCrawler:
    def __init__(self, base_url, directory_list_url):
        self.base_url = base_url
        self.directory_list_url = directory_list_url
        self.discovered_paths = []

    def load_directories(self):
        try:
            print(f"[*] Downloading directory list from: {self.directory_list_url}")
            response = requests.get(self.directory_list_url, timeout=10)
            response.raise_for_status()  # Raise an exception for HTTP errors
            directories = response.text.splitlines()
            print("[+] Directory list downloaded successfully.")
            return [line.strip() for line in directories if line.strip()]
        except requests.RequestException as e:
            print(f"Error downloading directory list: {e}")
            return []

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
        print("[*] Starting directory enumeration...")
        directories = self.load_directories()
        if directories:
            self.test_directories(directories)
            self.save_results()
        else:
            print("[!] No directories to test.")

if __name__ == "__main__":
    base_url = input("Enter the target base URL (e.g., http://example.com/): ").strip()
    directory_list_url = "https://raw.githubusercontent.com/hali34/DirectoryCrawler/main/directory-list-1.0.txt"  # Updated URL
    crawler = DirectoryCrawler(base_url, directory_list_url)
    crawler.crawl()
