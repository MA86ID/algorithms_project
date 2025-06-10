import json
import difflib
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re

def normalize_text(text):
    return re.sub(r'[\s\.\,\؛\:\!\؟\?\-\(\)\[\]\{\}\"\'،؛]', '', text.lower())

def similarity(a, b):
    if not a or not b:
        return 0.0
    norm_a = normalize_text(a)
    norm_b = normalize_text(b)
    return difflib.SequenceMatcher(None, norm_a, norm_b).ratio()

def get_similarity_data(data):
    results = []
    num_questions = max(max(item['qnumber'] for item in answers) for answers in data.values())
    for ref_name, ref_answers in data.items():
        reference_answers = {item["qnumber"]: item["description"] for item in ref_answers}
        for q in range(1, num_questions + 1):
            ref_desc = reference_answers.get(q)
            if not isinstance(ref_desc, str) or not ref_desc:
                continue
            for name, answers in data.items():
                if name == ref_name:
                    continue
                user_answers = {item["qnumber"]: item["description"] for item in answers}
                desc = user_answers.get(q)
                sim = similarity(desc, ref_desc)
                if sim > 0.77:
                    if sim >= 0.97:
                        status = "⛔ Copy"
                    elif sim >= 0.92:
                        status = "📛 Taghalob"
                    elif sim >= 0.88:
                        status = "❗ Shebahat Ziad"
                    else:
                        status = "❓ Shabih"
                    results.append({
                        "Sual": q,
                        "Fard A": name,
                        "Fard B": ref_name,
                        "Shebahat": f"{sim*100:.2f}%",
                        "Vaziat": status,
                        "Javab A": desc,
                        "Javab B": ref_desc
                    })
    return results

def load_file():
    filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if not filepath:
        return
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        results = get_similarity_data(data)
        display_results(results)
    except Exception as e:
        messagebox.showerror("خطا", f"مشکل در خواندن فایل:\n{e}")

def display_results(results):
    for row in tree.get_children():
        tree.delete(row)
    for idx, item in enumerate(results):
        tree.insert("", "end", iid=str(idx), values=(
            item["Sual"],
            item["Fard A"],
            item["Fard B"],
            item["Shebahat"],
            item["Vaziat"],
            item["Javab A"][:40] + ("..." if len(item["Javab A"]) > 40 else ""),
            item["Javab B"][:40] + ("..." if len(item["Javab B"]) > 40 else "")
        ))
    tree.bind("<Double-1>", lambda e: open_highlight_popup(results))

def open_highlight_popup(results):
    selected = tree.selection()
    if not selected:
        return
    idx = int(selected[0])
    item = results[idx]
    popup = tk.Toplevel(root)
    popup.title(f"مقایسه پاسخ‌ها - سؤال {item['Sual']}")
    popup.geometry("1000x500")

    frame = tk.Frame(popup)
    frame.pack(expand=True, fill="both")

    text_a = tk.Text(frame, wrap="word", bg="#AEDBDE")
    text_b = tk.Text(frame, wrap="word", bg="#ddc2c2")

    text_a.pack(side="left", expand=True, fill="both", padx=5, pady=5)
    text_b.pack(side="right", expand=True, fill="both", padx=5, pady=5)

    text_a.insert("1.0", item["Javab A"])
    text_b.insert("1.0", item["Javab B"])

    # هایلایت قسمت‌های مشابه با استفاده از difflib
    matcher = difflib.SequenceMatcher(None, item["Javab A"], item["Javab B"])
    for tag in matcher.get_matching_blocks():
        i1, i2, size = tag
        if size > 0:
            text_a.tag_add("highlight", f"1.0+{i1}c", f"1.0+{i1+size}c")
            text_b.tag_add("highlight", f"1.0+{i2}c", f"1.0+{i2+size}c")

    text_a.tag_config("highlight", background="yellow", foreground="black")
    text_b.tag_config("highlight", background="yellow", foreground="black")

    text_a.config(state="disabled")
    text_b.config(state="disabled")

# رابط گرافیکی اصلی
root = tk.Tk()
root.title("بررسی تشابه پاسخ‌ها")
root.geometry("1300x600")

btn_load = tk.Button(root, text="📂 بارگذاری فایل پاسخ‌ها", font=("B Nazanin", 12), command=load_file)
btn_load.pack(pady=10)

columns = ("Sual", "Fard A", "Fard B", "Shebahat", "Vaziat", "Javab A", "Javab B")
tree = ttk.Treeview(root, columns=columns, show="headings", height=20)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150 if "Javab" in col else 100, anchor="w")

scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tree.pack(expand=True, fill="both")

root.mainloop()
