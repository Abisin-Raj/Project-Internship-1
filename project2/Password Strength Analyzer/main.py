import argparse
import sys
from analyzer import analyze_strength
from generator import generate_wordlist, save_wordlist

# This is the main file. It uses argparse, which is a bit complex.
# ProTip: Don't use sys.argv manually unless you want a headache.
def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer & Wordlist Generator")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Analyze Command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a password's strength")
    analyze_parser.add_argument("password", help="The password to analyze")
    
    # Generate Command
    generate_parser = subparsers.add_parser("generate", help="Generate a custom wordlist")
    generate_parser.add_argument("--name", help="User's name")
    generate_parser.add_argument("--pet", help="Pet's name")
    generate_parser.add_argument("--birthdate", help="Birth date or year")
    generate_parser.add_argument("--output", default="wordlist.txt", help="Output filename")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        result = analyze_strength(args.password)
        print("\n--- Password Analysis ---")
        print(f"Password: {args.password}")
        print(f"Strength: {result['rating']}")
        print(f"Entropy: {result['entropy']} bits")
        print("\nFeedback:")
        for note in result['feedback']:
            print(f"- {note}")
        print("-------------------------\n")
        
    elif args.command == "generate":
        details = {
            "name": args.name,
            "pet": args.pet,
            "birthdate": args.birthdate
        }
        print("\n--- Generating Wordlist ---")
        wordlist = generate_wordlist(details)
        if save_wordlist(wordlist, args.output):
            print(f"Success! {len(wordlist)} words saved to {args.output}")
        else:
            print("Failed to save wordlist.")
            
    else:
        # Default behavior if no command is given
        print("Starting interactive mode...")
        print("1. Analyze Password")
        print("2. Generate Wordlist")
        choice = input("Select an option (1-2): ")
        
        if choice == "1":
            pwd = input("Enter password to analyze: ")
            result = analyze_strength(pwd)
            print(f"Rating: {result['rating']}")
            for note in result['feedback']: print(f"- {note}")
        elif choice == "2":
            name = input("Enter Name: ")
            pet = input("Enter Pet Name: ")
            date = input("Enter Birthdate: ")
            wl = generate_wordlist({"name": name, "pet": pet, "birthdate": date})
            save_wordlist(wl, "wordlist.txt")
            print(f"Wordlist saved to wordlist.txt")
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
