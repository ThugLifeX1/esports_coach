# إدارة الأصول والملفات

## هيكل المجلدات
```
Design_Assets/
├── 01_Brand/
│   ├── Logos/
│   ├── Colors/
│   ├── Fonts/
│   └── Brand_Guidelines/
├── 02_Social/
│   ├── Twitter/
│   ├── Instagram/
│   ├── TikTok/
│   └── YouTube/
├── 03_Stream/
│   ├── Overlays/
│   ├── Alerts/
│   ├── Screens/
│   └── Panels/
├── 04_Print/
│   ├── Business_Cards/
│   ├── Merch/
│   └── Certificates/
├── 05_Templates/
│   ├── Social_Templates/
│   ├── Stream_Templates/
│   └── Presentation_Templates/
├── 06_Archive/
│   └── [السنة]/
│       └── [الشهر]/
└── 07_WIP/ (Work In Progress)
```

## قواعد التسمية
| النوع | الصيغة | مثال |
|-------|--------|------|
| منشور سوشيال | `[المنصة]_[النوع]_[التاريخ]_[الإصدار]` | `IG_MatchResult_20260310_v2` |
| أوفرلاي | `Overlay_[البطولة]_[الإصدار]` | `Overlay_PMCO_v3` |
| قالب | `Template_[النوع]_[الإصدار]` | `Template_PlayerStats_v1` |
| شعار | `Logo_[النسخة]_[اللون]` | `Logo_Primary_Dark` |

## صيغ الملفات
| الاستخدام | الصيغة | ملاحظات |
|-----------|-------|---------|
| تصميم قابل للتعديل | .PSD / .AI / .AE | الاحتفاظ بالطبقات |
| استخدام نهائي رقمي | .PNG (شفاف) / .JPG | PNG للأوفرلاي |
| استخدام نهائي مطبوع | .PDF / .SVG | بدقة 300 DPI |
| فيديو/أنيميشن | .MP4 / .MOV | H.264 / ProRes |
| تصدير للويب | .SVG / .WebP | حجم صغير |

## نسخ احتياطية
- أسبوعي: نسخ مجلد WIP وآخر التصاميم
- شهري: نسخ كامل لمجلد الأصول
- التخزين: محلي + سحابي (Google Drive/OneDrive)
