import itertools

# This makes the word look cooler (leetspeak).
# I call it "hacking mode" haha.
def generate_variations(word):
    """Generates variations of a word (leetspeak, title case, etc.)."""
    variations = set([word, word.lower(), word.upper(), word.capitalize()])
    
    # Leetspeak mappings - swapping letters for numbers
    leet_map = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7'}
    
    # Simple leetspeak version
    leet_word = word.lower()
    for char, replacement in leet_map.items():
        leet_word = leet_word.replace(char, replacement)
    variations.add(leet_word)
    
    return variations

def generate_wordlist(user_details, use_variations=True):
    """Generates a custom wordlist based on user inputs."""
    base_words = []
    for key, value in user_details.items():
        if value:
            if isinstance(value, list):
                base_words.extend(value)
            else:
                base_words.append(str(value))
                
    results = set()
    
    # Core generation logic
    for word in base_words:
        if use_variations:
            results.update(generate_variations(word))
        else:
            results.add(word)
            
    # Simple combinations (Suffixes)
    # Most people put a "!" or "123" at the end of their password.
    # So we do that too.
    suffixes = ['', '123', '!', '2024', '2025', '@']
    final_list = set()
    for word in results:
        for suffix in suffixes:
            final_list.add(word + suffix)
            
    # Combinations of two base words (like "JohnBuddy")
    if len(base_words) >= 2:
        # NOTE: If we used more than 2, the file would be HUGE. 
        # I nearly crashed my computer with a 3-word combination test.
        for r in range(2, 3): 
            for combo in itertools.permutations(base_words, r):
                combined = "".join(combo)
                if use_variations:
                    final_list.update(generate_variations(combined))
                else:
                    final_list.add(combined)

    return sorted(list(final_list))

def save_wordlist(wordlist, filename="wordlist.txt"):
    """Saves the wordlist to a .txt file."""
    try:
        with open(filename, 'w') as f:
            for word in wordlist:
                f.write(word + '\n')
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

if __name__ == "__main__":
    # Quick test
    details = {
        "name": "Abisin",
        "pet": "Buddy",
        "birth_year": "2000"
    }
    wl = generate_wordlist(details)
    print(f"Generated {len(wl)} words.")
    print(f"Sample: {wl[:10]}")
