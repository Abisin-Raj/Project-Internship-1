import tkinter as tk
from tkinter import messagebox, filedialog
from analyzer import analyze_strength
from generator import generate_wordlist, save_wordlist

# This is the GUI part. If this doesn't run, check if you installed tkinter!
# Common mistake: forgetting that tkinter is a separate install on Linux.
class PasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Power Tool - Beginner Version")
        self.root.geometry("400x520")
        
        # --- Analyzer Section ---
        tk.Label(root, text="Password Strength Analyzer", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(root, text="Enter Password:").pack()
        self.pass_entry = tk.Entry(root, show="*", width=30)
        self.pass_entry.pack(pady=5)
        
        tk.Button(root, text="Analyze", command=self.run_analysis).pack()
        
        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)
        
        tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=10, pady=10)
        
        # --- Generator Section ---
        tk.Label(root, text="Wordlist Generator", font=("Arial", 14, "bold")).pack(pady=10)
        
        tk.Label(root, text="Name:").pack()
        self.name_entry = tk.Entry(root, width=30)
        self.name_entry.pack()
        
        tk.Label(root, text="Pet Name:").pack()
        self.pet_entry = tk.Entry(root, width=30)
        self.pet_entry.pack()
        
        tk.Label(root, text="Birthdate:").pack()
        self.date_entry = tk.Entry(root, width=30)
        self.date_entry.pack()
        
        tk.Button(root, text="Generate Wordlist", command=self.run_generation).pack(pady=10)

    def run_analysis(self):
        pwd = self.pass_entry.get()
        if not pwd:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return
            
        res = analyze_strength(pwd)
        output = f"Rating: {res['rating']}\nEntropy: {res['entropy']} bits"
        self.result_label.config(text=output, fg="green" if res['score'] > 4 else "orange" if res['score'] > 2 else "red")
        
        # This joins the feedback list into one big string
        feedback_text = "\n".join(res['feedback'])
        messagebox.showinfo("Detailed Feedback", feedback_text)

    def run_generation(self):
        details = {
            "name": self.name_entry.get(),
            "pet": self.pet_entry.get(),
            "birthdate": self.date_entry.get()
        }
        
        if not any(details.values()):
            messagebox.showwarning("Input Error", "Please fill in at least one field.")
            return
            
        wl = generate_wordlist(details)
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile="wordlist.txt")
        
        if file_path:
            if save_wordlist(wl, file_path):
                messagebox.showinfo("Success", f"Wordlist with {len(wl)} words saved to:\n{file_path}")
            else:
                messagebox.showerror("Error", "Failed to save file.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordApp(root)
    root.mainloop()
