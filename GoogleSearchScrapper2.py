import csv
from googlesearch import search

def get_search_urls(query, num_results=10, search_engine='google', time_range=None, file_type=None, exclude_domains=None, language=None):
    """
    Fetch URLs from search engine results based on the given query and parameters.

    Args:
        query (str): The search query.
        num_results (int): Number of search results to fetch.
        search_engine (str): Name of the search engine (default is 'google').
        time_range (str): Time range for search results (e.g., 'hour', 'day', 'week', 'month', 'year').
        file_type (str): File type to filter search results (e.g., 'pdf', 'docx').
        exclude_domains (list): List of domains to exclude from search results.
        language (str): Language preference for search results (e.g., 'en', 'fr').

    Returns:
        list: List of URLs.
    """
    try:
        urls = search(query, num_results=num_results, stop=num_results, pause=2, lang=language, tbs=time_range, filetype=file_type, domains=exclude_domains, tpe='web')
        return list(urls)
    except Exception as e:
        print(f"Error during search: {e}")
        return []

def filter_urls(urls):
    """
    Filter out duplicate URLs from the list.

    Args:
        urls (list): List of URLs.

    Returns:
        list: Filtered list of URLs.
    """
    filtered_urls = []
    for url in urls:
        if url not in filtered_urls:
            filtered_urls.append(url)
    return filtered_urls

def store_urls(urls, filename):
    """
    Store URLs in a CSV file.

    Args:
        urls (list): List of URLs.
        filename (str): Name of the CSV file.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['No.', 'URL'])
        for i, url in enumerate(urls, start=1):
            writer.writerow([i, url])

def main():
    """
    Main function to execute the script.
    """
    print("Welcome to the Custom Search Results Scraper!")
    print("")

    # Prompt user for search query
    query = input("Enter your query: ").strip()
    if not query:
        print("Query cannot be empty. Please provide a valid query.")
        return

    # Prompt user for number of results
    num_results = input("Enter the number of results to scrape (default is 10): ").strip()
    try:
        num_results = int(num_results) if num_results else 10
    except ValueError:
        print("Invalid input. Using default number of results (10).")
        num_results = 10

    # Prompt user for additional search options
    search_engine = input("Enter the search engine (google, bing, duckduckgo, etc.): ").strip().lower()
    time_range = input("Enter the time range (hour, day, week, month, year, etc.): ").strip().lower()
    file_type = input("Enter the file type (pdf, docx, etc.): ").strip().lower()
    exclude_domains = input("Enter domains to exclude (separated by comma, leave empty if none): ").strip().split(',')
    language = input("Enter the language preference (e.g., en, fr, etc.): ").strip().lower()

    # Fetch URLs from search engine
    print("Fetching search results...")
    urls = get_search_urls(query, num_results=num_results, search_engine=search_engine, time_range=time_range, file_type=file_type, exclude_domains=exclude_domains, language=language)
    if urls:
        print(f"Successfully retrieved {len(urls)} URLs.")

        # Filter duplicate URLs
        print("Filtering duplicate URLs...")
        filtered_urls = filter_urls(urls)
        print(f"Filtered down to {len(filtered_urls)} unique URLs.")

        # Store URLs in CSV file
        filename = 'extracted_urls.csv'
        print(f"Storing URLs in {filename}...")
        store_urls(filtered_urls, filename)
        print(f"URLs successfully stored in {filename}.")
    else:
        print("Failed to retrieve search results.")

if __name__ == "__main__":
    main()
