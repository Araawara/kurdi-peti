---
name: kurdi-peti
description: Write 100% pure Central Kurdish (Sorani, ckb) with correct Unicode orthography and no Arabic, Persian, Turkish or English loanwords. Use whenever the user writes in Sorani Kurdish or asks for Kurdish text, translation, UI strings, docs, code comments, or an app/website in Kurdish. نووسینی کوردیی سۆرانیی پەتی بۆ دەق، وەرگێڕان، ئەپ، وێبسایت و پڕۆژەی بەرنامەسازی.
metadata:
  author: Awara Q. Muhammad
  version: 0.1.0
---

# کوردیی پەتی (Kurdî Petî)

Every human-readable word you produce must be pure Central Kurdish (Sorani) in Arabic script. Talk to the user in Sorani too.

## Scope in software projects

**Write in Kurdish:** UI text, buttons, error and success messages, notifications, README and docs, code comments, commit messages, test descriptions, sample/placeholder data, alt text, page titles, SEO meta.

**Keep in English ASCII:** identifiers (variables, functions, classes), file and folder names, package names, API routes, JSON/i18n keys, CSS classes, env vars, git branches. Never translate language keywords. Example: `"save_button": "پاشەکەوتی بکە"`.

## Workflow

1. Read `references/rules.md` once per conversation before writing Kurdish. For apps and websites, also read `references/software.md`.
2. When unsure whether a word is a loanword, look it up in `references/glossary.md`.
   For every UI string in an app or website (buttons, menus, labels, messages), look the English term up in
   `references/ui_terms.tsv` (1,400+ terms; grep the English word). Rows marked `kurdi-peti` are reviewed and
   win over `firefox` rows. If the connector's `ui_term` tool is available, it does the same lookup.
3. After writing files, if you can run code: `python scripts/check.py <files-or-folders>`. Fix every `[هەڵە]`; apply `[پێشنیار]` unless it is a false positive.
4. No pure word exists? In this order: (a) an established Kurdish coinage from the glossary; (b) a new word built from Kurdish roots, with the international term in parentheses on first use, e.g. ڕاژەکار (server); (c) the international term in Kurdish spelling. Never fall back to an Arabic or Persian word.

<!-- kurdi-peti-ignore-start: examples of wrong forms below -->
## Core rules

- **Letters:** ک not ك · ی not ي/ى · vowel «ە» (U+06D5), never ه or ة · ه only for consonant h · a word never starts with ر, write ڕ · use ڵ ڕ ێ ۆ ڤ.
- **Punctuation:** ، ؛ ؟ and «» quotes.
- **Numbers:** one system per project, either ٠١٢٣٤٥٦٧٨٩ or 0-9. After a number the noun stays singular: «٣ پەڕگە», not «٣ پەڕگەکان».
- **Grammar:** verb at the end (SOV). Write natural Kurdish sentences, not word-by-word English calques.
- **Iranian-root words** long established in Kurdish (بەرنامە، فەرهەنگ، هەفتە) are fine. Persian-only words (خوب، شاید، خەیلی، بیشتر) are not.
- **Allowed internationalisms** when no Kurdish word is in real use: کۆمپیوتەر، ئینتەرنێت، کۆد، ڤیدیۆ، کامێرا، تەلەفۆن، مۆبایل، ئەلیکترۆنی, and brand names.

## Most common replacements

| ❌ | ✅ | ❌ | ✅ |
|---|---|---|---|
| مەسەلە | پرس، بابەت | فایل | پەڕگە |
| ئیستیفادە | بەکارهێنان | فۆڵدەر | بوخچە |
| مەعلومات | زانیاری | پاسوۆرد | وشەی نهێنی |
| سوئال / جەواب | پرسیار / وەڵام | سەیڤ | پاشەکەوتکردن |
| موهیم / لازم | گرنگ / پێویست | دیلیت | سڕینەوە |
| وەخت / ساعەت | کات / کاتژمێر | سێرچ | گەڕان |
| موشکیلە / حەل | کێشە / چارەسەر | لینک | بەستەر |
| نەتیجە / سەبەب | ئەنجام / هۆ | سێتینگ | ڕێکخستنەکان |
| یەعنی / مەسەلەن | واتە / بۆ نموونە | ئێرۆر | هەڵە |
| تەرجەمە / کەلیمە | وەرگێڕان / وشە | ئەپدەیت / ڤێرژن | نوێکردنەوە / وەشان |

## Before you answer

- No word from the left column of `glossary.md` remains.
- No ك ي ى ة characters.
- No word starts with ر.
- Kurdish punctuation is used.
- Code identifiers are still English and the code still runs.
