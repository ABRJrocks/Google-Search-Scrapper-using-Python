
import csv
import time
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from googlesearch import search

def get_google_urls(query, num_results=10, language='en', country='US'):
    try:
        # Perform Google search with specified parameters
        urls = search(query, num_results=num_results, lang=language, tld=country)
        return list(urls)
    except Exception as e:
        print(f"Error during Google search: {e}")
        return []

def filter_urls(urls):
    # Filter out duplicate URLs
    return list(set(urls))

def store_urls(urls, filename):
    # Store extracted URLs in a CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['URL'])
        for url in urls:
            writer.writerow([url])

def search_and_store():
    query = query_entry.get().strip()
    num_results = num_results_entry.get().strip()
    language = language_var.get()
    filename = filename_entry.get().strip()

    if not query:
        result_label.config(text="Query cannot be empty. Please provide a valid query.")
        return

    if not filename:
        result_label.config(text="Filename cannot be empty. Please provide a valid filename.")
        return

    try:
        num_results = int(num_results) if num_results else 10
    except ValueError:
        result_label.config(text="Invalid input for number of results. Defaulting to 10.")
        num_results = 10

    max_retries = 3
    retry_count = 0
    while retry_count < max_retries:
        urls = get_google_urls(query, num_results, language)
        if urls:
            break
        retry_count += 1
        time.sleep(2)

    if not urls:
        result_label.config(text="Failed to retrieve search results after multiple attempts. Please try again later.")
        return

    filtered_urls = filter_urls(urls)
    if filtered_urls:
        store_urls(filtered_urls, filename + '.csv')
        result_label.config(text=f"Successfully extracted {len(filtered_urls)} unique URLs and stored in {filename}.csv")
    else:
        result_label.config(text="No relevant URLs found.")

def browse_file():
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filename:
        filename_entry.delete(0, tk.END)
        filename_entry.insert(0, filename[:-4])  # Remove the '.csv' extension

# Create GUI
root = tk.Tk()
root.title("Google Search Tool")

main_frame = ttk.Frame(root, padding="20")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

query_label = ttk.Label(main_frame, text="Enter your query:")
query_label.grid(row=0, column=0, sticky=tk.W)

query_entry = ttk.Entry(main_frame, width=50)
query_entry.grid(row=0, column=1)

num_results_label = ttk.Label(main_frame, text="Enter the number of results to scrape (default is 10):")
num_results_label.grid(row=1, column=0, sticky=tk.W)

num_results_entry = ttk.Entry(main_frame, width=10)
num_results_entry.grid(row=1, column=1)

language_label = ttk.Label(main_frame, text="Select language:")
language_label.grid(row=2, column=0, sticky=tk.W)

language_var = tk.StringVar(value="en")
language_combobox = ttk.Combobox(main_frame, textvariable=language_var, values=["en", "es"])
language_combobox.grid(row=2, column=1)

filename_label = ttk.Label(main_frame, text="Enter filename for export:")
filename_label.grid(row=3, column=0, sticky=tk.W)

filename_entry = ttk.Entry(main_frame, width=50)
filename_entry.grid(row=3, column=1)

browse_button = ttk.Button(main_frame, text="Browse", command=browse_file)
browse_button.grid(row=3, column=2)

search_button = ttk.Button(main_frame, text="Search and Store URLs", command=search_and_store)
search_button.grid(row=4, column=0, columnspan=3)

result_label = ttk.Label(main_frame, text="")
result_label.grid(row=5, column=0, columnspan=3)

root.mainloop()
