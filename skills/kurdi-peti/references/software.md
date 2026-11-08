# بەرنامە و وێبسایت بە کوردیی پەتی

## ١. ڕێکخستنی بنەڕەتی

- کۆدی زمان: `ckb` (یان `ckb-IQ` و `ckb-IR`)
- ئاراستە: لە ڕاستەوە بۆ چەپ (RTL)

```html
<html lang="ckb" dir="rtl">
```

```css
/* بەکارهێنانی logical properties تا RTL و LTR هەردووکیان کار بکەن */
.card { margin-inline-start: 1rem; padding-inline-end: 0.5rem; text-align: start; }
body { font-family: "Vazirmatn", "Noto Naskh Arabic", "Noto Sans Arabic", sans-serif; }
```

- فۆنتێک هەڵبژێرە کە پیتەکانی ڕ ڵ ێ ۆ ڤ ە پشتگیری بکات، و بە دەقێکی ڕاستەقینە تاقی بکەرەوە.
- ئایکۆنی ئاراستەدار (تیر، «دواتر»، «پێشوو») لە RTLدا پێچەوانە بکەرەوە.
- خانەی تێنووسین: `dir="auto"` بۆ ئەوەی دەقی تێکەڵی کوردی و ئینگلیزی دروست پیشان بدرێت.

## ٢. وەرگێڕانی ڕووکار (i18n)

کلیلەکان ئینگلیزی دەمێننەوە و تەنها بەهاکان کوردین:

```json
{
  "save": "پاشەکەوتی بکە",
  "cancel": "هەڵیوەشێنەوە",
  "delete_confirm": "دڵنیایت دەتەوێت ئەم پەڕگەیە بسڕیتەوە؟",
  "files_count": "{count} پەڕگە"
}
```

- دوای ژمارە ناو تاکە: «{count} پەڕگە». پێویست بە کۆ نییە.
- ژمارە و ڕێکەوت: `new Intl.NumberFormat('ckb').format(n)` و `Intl.DateTimeFormat('ckb')`. دەرئەنجامەکە لە وێبگەڕەکانی ئامانجتدا تاقی بکەرەوە.

## ٣. فەرهەنگی ڕووکار

| ئینگلیزی | کوردیی پەتی |
|---|---|
| Save | پاشەکەوتکردن |
| Cancel | هەڵوەشاندنەوە |
| Delete | سڕینەوە |
| Edit | دەستکاریکردن |
| Add | زیادکردن |
| Search | گەڕان |
| Filter | پاڵاوتن |
| Sort | ڕیزکردن |
| Settings | ڕێکخستنەکان |
| Log in | چوونەژوورەوە |
| Log out | چوونەدەرەوە |
| Sign up | خۆتۆمارکردن |
| Username | ناوی بەکارهێنەر |
| Password | وشەی نهێنی |
| Forgot password? | وشەی نهێنیت لەبیرچووە؟ |
| Account | هەژمار |
| Profile | پەڕەی کەسی |
| Home | سەرەکی |
| Menu | پێڕست |
| Notifications | ئاگادارکردنەوەکان |
| Messages | نامەکان |
| Send | ناردن |
| Submit | ناردن |
| Next / Back | دواتر / گەڕانەوە |
| Continue | بەردەوامبوون |
| Close / Open | داخستن / کردنەوە |
| Yes / No | بەڵێ / نەخێر |
| OK | باشە |
| Confirm | پشتڕاستکردنەوە |
| Upload / Download | بارکردن / داگرتن |
| Share | هاوبەشکردن |
| Copy / Paste / Cut | لەبەرگرتنەوە / لکاندن / بڕین |
| Undo / Redo | پاشگەزبوونەوە / دووبارەکردنەوە |
| Select all | هەمووی هەڵبژێرە |
| Help / About | یارمەتی / دەربارە |
| Language | زمان |
| Dark mode | ڕووکاری تاریک |
| Loading… | چاوەڕێ بکە… |
| Error / Warning / Success | هەڵە / ئاگاداری / سەرکەوتوو بوو |
| Try again | دووبارە هەوڵ بدەرەوە |
| Required field | ئەم خانەیە پێویستە |
| Invalid | نادروستە |
| Page not found | پەڕەکە نەدۆزرایەوە |
| File / Folder | پەڕگە / بوخچە |
| Link | بەستەر |
| Button | دوگمە |
| Version / Update | وەشان / نوێکردنەوە |
| Comment | لێدوان |
| Feedback | ڕاوبۆچوون |
| Date / Time | ڕێکەوت / کات |
| Today / Yesterday | ئەمڕۆ / دوێنێ |
| Price / Total | نرخ / کۆی گشتی |
| Cart | سەبەتە |
| Order | داواکاری |
| Payment | پارەدان |
| Address | ناونیشان |
| Server | ڕاژەکار |
| Database | بنکەدراو |
| Software / Hardware | نەرمەکاڵا / ڕەقەکاڵا |
| Network | تۆڕ |
| Online | سەرهێڵ |
| Task | ئەرک |
| Feature | تایبەتمەندی |

## ٤. کۆد

- ناوی گۆڕاو، فەنکشن، پەڕگە و بوخچە بە ئینگلیزی بن.
- لێدوانەکانی ناو کۆد (comments) و commit message بە کوردیی پەتی بن:

```python
# پشکنینی وشەی نهێنی پێش پاشەکەوتکردن
def validate_password(password: str) -> bool:
    return len(password) >= 8
```

- دەقی ڕووکار ڕاستەوخۆ لە ناو کۆددا مەنووسە. بیخەرە ناو پەڕگەی وەرگێڕان (`ckb.json`).
- پاش تەواوبوون: `python scripts/check.py src/ locales/ README.md`
