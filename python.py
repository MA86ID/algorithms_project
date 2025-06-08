import json
import difflib

with open('C:/Users/Asus/Desktop/algoritms_pr/test.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

reference_name = "Alice"
reference_answers = {item["qnumber"]: item["description"] for item in data[reference_name]}

def similarity(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

for name, answers in data.items():
    if name == reference_name:
        continue

    for ans in answers:
        q = ans['qnumber']
        desc = ans['description']
        ref_desc = reference_answers.get(q)

        sim = similarity(desc, ref_desc)

        if sim >= 0.8 :
            print(f"\n🔍 moghayese {name} ba {reference_name} soal({q}):")
            # agar shart if sim >= 0.8  ro hazf konim darsad tashaboh hame soala barresy mishe 
            status = "⛔ copy" if sim >= 0.97 else "📛 taghalob" if sim >= 0.87 else "❗ shebahat_ziad" if sim >= 0.77 else "❓ shabih" if sim >= 0.67 else "⏩ nesbatan_motefavet"
            if not desc:
                status = "🪦  bedone javab"
            print(f"    {status} (shebahat: %{(sim*100):.2f})")
            print(f"        - javab {name}: {desc}")
            print(f"        - javab {reference_name}: {ref_desc}")

