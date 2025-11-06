from tokenizer import stop_words
from scraper import stats

def generate_report(full=False):
    visited_urls, total_freq, subdomains, longest_page = stats()
    num_unique_pages = len(visited_urls)
    longest_page_url, longest_page_word_count = longest_page

    with open("report2.txt", "a") as f:
        f.write("\n=== Report Snapshot ===\n") if not full else f.write("\n=== Final Snapshot ===\n")
            
        f.write(f"Number of unique pages: {num_unique_pages}\n")
        f.write(f"Longest page: {longest_page_url}\n")
        f.write(f"Word count: {longest_page_word_count}\n\n")

        if full:
            filtered_freq = {
                word: freq
                for word, freq in total_freq.items()
                if word.lower() not in stop_words and word.isalpha()
            }
            top_50 = sorted(filtered_freq.items(), key=lambda x: x[1], reverse=True)[:50]

            f.write("50 most common words:\n")
            for word, freq in top_50:
                f.write(f"{word}: {freq}\n")

            f.write("\nSubdomains:\n")
            for domain, count in sorted(subdomains.items()):
                f.write(f"{domain}, {count}\n")

if __name__ == "__main__":
    generate_report()
