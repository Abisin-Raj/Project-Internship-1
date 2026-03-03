import re
import math

# This part is for entropy... which is just a fancy word for "how random is it?"
# I had to look up the Shannon Entropy formula like 3 times lol.
def calculate_entropy(password):
    """Calculates the Shannon entropy of a password."""
    if not password:
        return 0
    
    # We count how many times each character shows up
    char_count = {}
    for char in password:
        char_count[char] = char_count.get(char, 0) + 1
    
    entropy = 0
    for count in char_count.values():
        p = count / len(password)
        entropy -= p * math.log2(p)
    
    return entropy * len(password)

# This looks for common stuff people use when they are lazy.
# Note: I originally forgot to use .lower() and it didn't catch "QWERTY". 
# Common mistake: forgetting that passwords can be CAPSLOCK too!
def check_patterns(password):
    """Detects weak patterns like '123', 'qwerty', etc."""
    weak_patterns = [
        r'123', r'abc', r'qwerty', r'asdf', r'password',
        r'admin', r'welcome', r'111', r'000'
    ]
    detected = []
    for pattern in weak_patterns:
        if re.search(pattern, password.lower()):
            detected.append(pattern)
    return detected

def analyze_strength(password):
    """Analyzes password strength based on various criteria."""
    score = 0
    feedback = []
    
    # 1. Length Check
    length = len(password)
    if length < 8:
        feedback.append("Password is too short (min 8 characters).")
    elif length >= 12:
        score += 2
        feedback.append("Excellent length.")
    else:
        score += 1
        feedback.append("Good length.")
        
    # 2. Character Variety
    types = {
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "numbers": bool(re.search(r'[0-9]', password)),
        "symbols": bool(re.search(r'[^a-zA-Z0-9]', password))
    }
    
    variety_count = sum(types.values())
    score += variety_count
    
    if variety_count < 3:
        feedback.append("Try adding more variety (uppercase, numbers, symbols).")
    else:
        feedback.append("Great character variety.")
        
    # 3. Pattern Detection
    patterns = check_patterns(password)
    if patterns:
        score -= len(patterns)
        feedback.append(f"Weak patterns detected: {', '.join(patterns)}")
        
    # 4. Entropy (Bonus)
    entropy = calculate_entropy(password)
    if entropy > 50:
        score += 1
        
    # Final Scoring - this part is just a basic if/else tree.
    # If the score is low, it's Weak. If high, it's Strong.
    # Simple, right?
    if score < 3:
        rating = "Weak"
    elif score < 5:
        rating = "Medium"
    else:
        rating = "Strong"
        
    return {
        "rating": rating,
        "score": score,
        "feedback": feedback,
        "entropy": round(entropy, 2)
    }

if __name__ == "__main__":
    # Just a quick test to see if it actually works.
    test_pwd = "P@ssw0rd123!"
    result = analyze_strength(test_pwd)
    print(f"Test Password: {test_pwd}")
    print(f"Rating: {result['rating']}")
    print(f"Feedback: {result['feedback']}")
