You are curating the "کوردیی پەتی" pure Central Kurdish (Sorani) glossary in this folder, in bulk mode.
Work only inside this folder. Only use the commands below. Do not ask questions; finish the whole run.
Do not create helper scripts.

1. Run `python grow.py todo 200 wiki`. It writes 200 candidate words from Kurdish Wikipedia to data/todo.txt.
2. Read skills/kurdi-peti/references/rules.md (loanword policy) and data/todo.txt.
3. Decide EVERY candidate. Each one must end up either accepted or rejected:
   - ACCEPT only a real Arabic / Turkish / English / Persian-only loanword used in Sorani, when you are
     confident of an established pure Kurdish replacement. Prefer scientific and technical words.
     Use the base form as `loan` and add common spelling variants (with/without doubled letters, ة/ە, ھ/ه).
     Internationalisms with no Kurdish word in real use (کۆمپیوتەر، ئینتەرنێت، فیزیک، کیمیا) are not loans: reject.
   - REJECT personal or place names, Quranic or classical Arabic phrases, religious terms with no real
     replacement, words that are actually Kurdish, words so assimilated they have no replacement (قسە، خەیاڵ)،
     inflected verb forms, and anything you are unsure about.
4. Write accepted entries to data/batch-wiki-HHMM.txt (HHMM = current time), one per line:
   `loan|variant1,variant2|pure1,pure2|core|ar|wiki`  (level core or strict; origin ar/fa/tr/en).
   Write EVERY rejected candidate exactly as it appears in todo.txt, one per line, to data/reject-wiki-HHMM.txt.
   Run `python grow.py merge data/batch-wiki-HHMM.txt` and `python grow.py reject data/reject-wiki-HHMM.txt`.
5. Run `python grow.py fp data/batch-wiki-HHMM.txt`. If an entry matches genuine Kurdish words
   (a short loan + suffix forming a native word), fix it in glossary.json: add "exact": true, drop the bad
   variant, or remove that entry. Do not change entries you did not add in this run.
6. Run `python grow.py stats` and finish with one line: accepted, rejected, total.
