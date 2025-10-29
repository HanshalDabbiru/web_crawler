import sys

# this runs in O(n) time where n is the number of characters in the file
def read_content(resp):
    content = resp.raw_response.content.decode("utf-8", errors="ignore")
    for line in content.splitlines():
        token = []
        for c in line:
            if c.isalnum() and c.isascii():
                token.append(c.lower())
            elif len(token) > 0:
                yield ''.join(token)
                token = []
        if len(token) > 0:
            yield ''.join(token)


# this runs in O(n) time where n is the number of characters in the file
def tokenize(file_path):
    tokens = []
    for token in read_content(file_path):
        tokens.append(token)
    return tokens

# this runs in O(n) time where n is the number of elements in tokens
def computeWordFrequencies(tokens):
    freq = {}
    for token in tokens:
        if token in freq:
            freq[token] += 1
        else:
            freq[token] = 1
    return freq

# this runs in O(n log(n)) time where n is the size of freq
def print_freqs(freq):
    for token in sorted(freq, key=freq.get, reverse=True):
        print(token, freq[token])

def main():
    file = sys.argv[1]
    print_freqs(computeWordFrequencies(tokenize(file)))


if __name__ == "__main__":
    main()