# بەشداریکردن لە «کوردیی پەتی»

سوپاس بۆ یارمەتیدانت! هەر وشەیەک کە زیاد دەکەیت، یارمەتی Claude، ChatGPT و هەموو کەسێک دەدات کوردییەکی پەتیتر بنووسن.

## ڕێگای ئاسان: فۆڕمی پێشنیار (بێ زانینی بەرنامەسازی)

1. هەژمارێکی بێبەرامبەری GitHub دروست بکە، ئەگەر نیتە.
2. بڕۆ بۆ بەشی [Issues](https://github.com/Araawara/kurdi-peti/issues/new/choose).
3. یەکێک لەم دوو فۆڕمە هەڵبژێرە:
   - **پێشنیاری وشەی نوێ:** وشەیەکی بیانی و جێگرەوە کوردییەکەی.
   - **ڕاستکردنەوەی وشەیەک:** ئەگەر وشەیەک لە فەرهەنگەکەدا هەڵەیە.
4. فۆڕمەکە پڕ بکەرەوە و بینێرە.

دوای ئەوە:

- خاوەنی پڕۆژە پێشنیارەکە دەخوێنێتەوە.
- ئەگەر پەسەندی بکات، نیشانەی «پەسەندکراو» دەخاتە سەری، و وشەکە بە شێوەیەکی خۆکار دەخرێتە ناو فەرهەنگەکە.
- دوای چەند خولەکێک لە ڕاژەکارەکەشدا (connector) بەردەست دەبێت.

## ڕێگای بەرنامەسازان

1. پڕۆژەکە fork بکە.
2. لە `skills/kurdi-peti/references/glossary.json` بۆ هەر وشەیەک ڕیزێک زیاد بکە:

<!-- kurdi-peti-ignore-start -->
```json
{"loan": "مەسەلە", "variants": ["مەسئەلە"], "origin": "ar", "pure": ["پرس", "بابەت"], "level": "core"}
```
<!-- kurdi-peti-ignore-end -->

   | کلیل | واتا |
   |---|---|
   | `loan` | وشە بیانییەکە |
   | `variants` | شێوەکانی تری نووسینی |
   | `origin` | `ar` عەرەبی، `fa` فارسی، `tr` تورکی، `en` ئینگلیزی یان ئەورووپی |
   | `pure` | وشە کوردییە پەتییەکان، باشترینیان یەکەم |
   | `level` | `core` هەمیشە بگۆڕدرێت، `strict` تەنها بۆ کوردیی سەد لە سەد پەتی |
   | `exact` | `true` ئەگەر تەنها شێوەی ساکاری وشەکە بگیرێت، بێ پاشگر |
   | `source` | سەرچاوە، بۆ نموونە `community` |
   | `review` | `true` ئەگەر هێشتا پێداچوونەوەی دەوێت |

3. پشکنین: `python tools/validate_glossary.py`
4. pull request بنێرە. پشکنینە خۆکارەکان لە GitHub بە شێوەیەکی خۆبەخۆ جێبەجێ دەبن.

`glossary.md` و `mcp/api/kp_data.py` دەستکاری مەکە؛ دوای پەسەندکردن خۆکارانە دروست دەکرێنەوە.

## یاساکانی وشە

<!-- kurdi-peti-ignore-start -->
- تەنها ئەلفوبێی کوردی: ک نەک ك، ی نەک ي، ە نەک ة، ڕ لە سەرەتای وشەدا.
<!-- kurdi-peti-ignore-end -->
- وشەکە دەبێت لە کوردیدا بەکاربێت یان لە ڕەگی کوردی دروست کرابێت.
- لە فەرهەنگێکی چاپکراو بە کۆمەڵ لەبەر مەگرەوە. وشەی تاک بە تاک و زانیاریی خۆت باشە.
- وشەی سووکایەتی یان ڕامیاری نابێت.

## ڕێگەپێدان

بە ناردنی هەر پێشنیارێک، ڕازی دەبیت کە:

- وشە و دەقەکان بە **CC BY 4.0** بڵاو بکرێنەوە (بڕوانە `LICENSE-DATA.md`)،
- و کۆد بە **MIT** (بڕوانە `LICENSE`).

ناوی هەموو بەشداربووان لە مێژووی پڕۆژەکەدا لە GitHub دەمێنێتەوە.

---

# Contributing (English)

- **No coding needed:** open an issue with the "پێشنیاری وشەی نوێ" (new word) or "ڕاستکردنەوەی وشەیەک" (fix) form. When the maintainer adds the "پەسەندکراو" (approved) label, a pull request adding the word is created automatically.
- **Developers:** edit `skills/kurdi-peti/references/glossary.json` (one entry per line), run `python tools/validate_glossary.py`, and open a pull request. Do not edit generated files (`glossary.md`, `mcp/api/kp_data.py`).
- Do not copy dictionaries wholesale.
- By contributing you agree to license your contribution under CC BY 4.0 (glossary and docs) and MIT (code).
