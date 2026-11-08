# کوردیی پەتی (Kurdî Petî)

**دروستکەر:** ئاوارە ق. محەمەد (Awara Q. Muhammad)

پلگینێک بۆ Claude و ChatGPT کە وا لە ژیریی دەستکرد دەکات هەموو دەق، بەرنامە، وێبسایت و پڕۆژەیەکی بەرنامەسازی بە **کوردیی سۆرانیی سەد لە سەد پەتی** بنووسێت.

## ئەم پلگینە چی دەکات؟
<!-- kurdi-peti-ignore-start -->

- وشەی عەرەبی، فارسی، تورکی و ئینگلیزی دەگۆڕێت بە کوردیی پەتی: «مەسەلە» ← «پرس»، «فایل» ← «پەڕگە».
- ڕێنووسی یونیکۆدی دروست بەکاردەهێنێت: ک نەک ك، ی نەک ي، ە نەک ه، ڕ لە سەرەتای وشەدا.
<!-- kurdi-peti-ignore-end -->
- لە پڕۆژەی بەرنامەسازیدا، ڕووکار و نامەکان، README و لێدوانەکانی کۆد بە کوردی دەنووسێت، بەڵام ناوی گۆڕاو و پەڕگەکان بە ئینگلیزی دەهێڵێتەوە تا کۆدەکە کار بکات.
- ئامرازێکی پشکنینی هەیە (`check.py`) کە هەڵەکان دەدۆزێتەوە.

## دامەزراندن

سەرەتا پاکێجەکان دروست بکە:

```
python build.py
```

### Claude.ai (وێب، دێسکتۆپ، مۆبایل)

1. `dist/kurdi-peti-skill.zip` دابگرە.
2. لە Claude.ai بڕۆ بۆ **Settings ← Capabilities ← Skills**.
3. **Upload skill** هەڵبژێرە و پەڕگەکە باربکە.
4. ئەگەر code execution چالاک بێت، Claude دەتوانێت پشکەرەکەش بەکاربهێنێت.

### Claude Code

```
/plugin marketplace add Araawara/kurdi-peti
/plugin install kurdi-peti@kurdi-peti
```

### ChatGPT (Custom GPT)

1. **Explore GPTs ← Create ← Configure**.
2. ناوەڕۆکی `dist/chatgpt/instructions.md` بخەرە ناو **Instructions**.
3. لە **Knowledge**دا ئەم چوار پەڕگەیە باربکە: `glossary.json`، `rules.md`، `software.md`، `check.py`.
4. **Code Interpreter & Data Analysis** چالاک بکە.
5. بە **Anyone with the link** یان **GPT Store** بڵاوی بکەرەوە، بۆ ئەوەی هەموو کەس بەکاری بهێنێت.

### Connector (Claude.ai و ChatGPT)

بەستەری ڕاژەکار: **https://kurdi-peti.vercel.app/mcp**

- **Claude.ai:** Settings ← Connectors ← Add custom connector ← بەستەرەکە دابنێ.
- **ChatGPT:** Settings ← Apps & Connectors ← Advanced ← Developer mode چالاک بکە ← Create ← بەستەرەکە دابنێ، Authentication: No authentication.

ئامرازەکان: `search_word` (گەڕان لە فەرهەنگ)، `check_text` (پشکنینی دەق)، `get_guide` (ڕێنمایی)، `search` و `fetch`.

بڵاوکردنەوەی وەشانی نوێ: `python build.py` ئینجا لە بوخچەی `mcp`: `npx vercel deploy --prod`

ڕێنماییی تەواو: https://kurdi-peti.vercel.app/docs.html

### بۆ گەشەپێدەران (بێ ژیریی دەستکرد)

```
python skills/kurdi-peti/scripts/check.py src/ locales/ README.md
python skills/kurdi-peti/scripts/check.py --fix locales/ckb.json
```

ئەگەر هەڵە هەبێت، کۆدی دەرچوون `1`ە، بۆیە دەتوانیت لە CIدا بەکاری بهێنیت.

## پێکهاتە

```
skills/kurdi-peti/          سەرچاوەی هاوبەش
  SKILL.md                  ڕێنمایی بۆ Claude
  references/glossary.json  فەرهەنگ (تەنها ئەمە دەستکاری بکە)
  references/glossary.md    خۆکارانە دروست دەکرێت
  references/rules.md       یاساکانی ڕێنووس و ڕێزمان
  references/software.md    بەرنامە، وێبسایت، RTL، فەرهەنگی ڕووکار
  scripts/check.py          پشکنەر
chatgpt/instructions.md     ڕێنمایی بۆ Custom GPT
.claude-plugin/             پلگینی Claude Code
build.py                    دروستکردنی dist/
```

## بەشداریکردن

مامۆستایان، نووسەران و هەر کەسێک کە کوردی دەزانێت دەتوانێت یارمەتی بدات، بێ ئەوەی بەرنامەسازی بزانێت:

1. بڕۆ بۆ [Issues ← New issue](https://github.com/Araawara/kurdi-peti/issues/new/choose).
2. فۆڕمی **پێشنیاری وشەی نوێ** یان **ڕاستکردنەوەی وشەیەک** پڕ بکەرەوە.
3. دوای پەسەندکردن، وشەکە بە شێوەیەکی خۆکار دەخرێتە ناو فەرهەنگەکە و connectorەکە.

ڕێنماییی تەواو: [CONTRIBUTING.md](CONTRIBUTING.md)

## ڕێگەپێدان

© ٢٠٢٦ ئاوارە ق. محەمەد (Awara Q. Muhammad) و بەشداربووان.

- **فەرهەنگ و ڕێنماییەکان** (`skills/kurdi-peti/references/`، `SKILL.md`، `chatgpt/instructions.md`): [CC BY 4.0](LICENSE-DATA.md). هەر کەسێک دەتوانێت بەکاری بهێنێت، تەنانەت بۆ فێرکردنی ژیری دەستکرد، بەو مەرجەی ناوی سەرچاوەکە بهێنێت.
- **کۆد:** [MIT](LICENSE).
- ناوی «کوردیی پەتی» و ئاڵاکەی تایبەتن بەم پڕۆژەیە. ئەگەر وەشانێکی گۆڕاو بڵاو دەکەیتەوە، ناوێکی تری لێ بنێ.

---

**English:** Kurdî Petî makes Claude, ChatGPT and other AI tools write pure Central Kurdish (Sorani). Connector URL: `https://kurdi-peti.vercel.app/mcp` (no login). Glossary and guides are licensed CC BY 4.0, code is MIT. Suggest words via [Issues](https://github.com/Araawara/kurdi-peti/issues/new/choose); see [CONTRIBUTING.md](CONTRIBUTING.md).
