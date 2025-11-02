import json
from tokenizer import stop_words
from scraper import stats

def generate_report():
    visited_urls, total_freq, subdomains, longest_page = stats()

    num_unique_pages = len(visited_urls)

    longest_page_url, longest_page_word_count = longest_page
    
    filtered_freq = {
        word: freq
        for word, freq in total_freq.items()
        if word.lower() not in stop_words and word.isalpha()
    }
    top_50 = sorted(filtered_freq.items(), key=lambda x: x[1], reverse=True)[:50]

    sorted_subdomains = sorted(subdomains.items())

    with open("report.txt", "w") as f:
        f.write(f"Number of unique pages: {num_unique_pages}\n\n")

        f.write(f"Longest page: {longest_page_url}\n")
        f.write(f"Word count: {longest_page_word_count}\n\n")

        f.write("50 most common words:\n")
        for word, freq in top_50:
            f.write(f"{word}: {freq}\n")
        f.write("\n")

        f.write("Subdomains:\n")
        for domain, count in sorted_subdomains:
            f.write(f"{domain}, {count}\n")

    print("Report generated successfully as 'report.txt'")

if __name__ == "__main__":
    generate_report()
