# algorithms_project
هدف اصلی برنامه
بررسی شباهت پاسخ‌های افراد مختلف به سؤالات یکسان، با چشم‌پوشی از فاصله‌ها و علائم نگارشی و نمایش نتایج به‌صورت گرافیکی با امکان مشاهده و هایلایت بخش‌های مشابه.

 پاسخ‌ها در قالب یک فایل JSON وارد می‌شوند و الگوریتم با بررسی هر پاسخ، درصد شباهت آن را با سایر پاسخ‌ها محاسبه کرده و آن‌ها را دسته‌بندی می‌کند (Copy, Taghalob, …)، سپس نتایج را در رابط گرافیکی نمایش می‌دهد.
 
ساختار فایل ورودی JSON  
{
  "Alice": [
    {
      "qnumber": 1,
      "description": "The quick brown fox jumps over the lazy dog.",
      "time_taken": 30
    },
    {
      "qnumber": 2,
      "description": "Photosynthesis converts sunlight into energy.",
      "time_taken": 45
    } 
 ],
  "Bob": [
    {
      "qnumber": 1,
      "description": "The quick brown fox jumps over the lazy dog.",
      "time_taken": 32
    },
    {
      "qnumber": 2,
      "description": "Photosynthesis converts sunlight into energy.",
      "time_taken": 47
    }
  ]
}

تابع normalize_text(text)
پاک‌سازی پاسخ‌ها از علائم نگارشی و فاصله‌ها برای جلوگیری از تأثیر آن‌ها در محاسبه‌ی شباهت.


تابع similarity(a, b)

محاسبه درصد شباهت بین دو رشته(از difflib.SequenceMatcher  استفاده شده تا میزان شباهت بین دو پاسخ متنی (فارغ از حروف بزرگ و کوچک ) را به‌صورت عددی بین ۰ تا ۱ بازگرداند).

def similarity(a, b):
    if not a or not b:
        return 0.0
    norm_a = normalize_text(a)
    norm_b = normalize_text(b)
    return difflib.SequenceMatcher(None, norm_a, norm_b).ratio()تابع get_similarity_data(data)
    
میزان شباهت	وضعیت

≥ 97%	⛔ Copy
≥ 92%	📛 Taghalob
≥ 88%	❗ Shebahat Ziad
≥ 77%	❓ Shabih
< 77%	صرف‌نظر می‌شود

 این تابع پاسخ‌ها را بین همه‌ی شرکت‌کنندگان برای هر سوال مقایسه می‌کند. اگر شباهت از آستانه مشخصی بیشتر باشد، آن را دسته‌بندی می‌کند:



تابع load_file()

•	فایل JSON را با استفاده از پنجره‌ی انتخاب فایل (filedialog) باز می‌کند.

•	داده‌ها را می‌خواند و به  get_similarity_data می‌دهد.

•	در صورت خطا، پیغام هشدار نمایش می‌دهد.


تابع display_results(results)

نتایج محاسبه‌شده را در جدول  treeview نمایش می‌دهد:

•	ستون‌ها شامل شماره سوال، نام دو نفر، درصد شباهت، وضعیت تشخیص، و نسخه‌ی خلاصه‌شده‌ی پاسخ‌ها هستند.

•	با دابل‌کلیک روی یک ردیف، پنجره‌ای برای نمایش پاسخ‌های کامل و هایلایت‌شده باز می‌شود.

تابع open_highlight_popup(results)

با دابل‌کلیک کاربر اجرا می‌شود و پنجره‌ای با دو TextBox باز می‌کند:

•	پاسخ فرد A و فرد B را نمایش می‌دهد.

•	قسمت‌های مشابه بین این دو پاسخ، با استفاده از SequenceMatcher.get_matching_blocks() هایلایت می‌شوند.

•	پس از نمایش، TextBoxها غیرفعال (read-only) می‌شوند.

رابط کاربری (GUI)

•	با استفاده از tkinter ساخته شده.

•	دارای دکمه بارگذاری فایل، جدول نتایج، و پنجره پاپ‌آپ برای مقایسه پاسخ‌ها.

•	از فونت فارسی پشتیبانی می‌کند.

•	از رنگ‌بندی برای تمایز دیداری بین پاسخ‌ها استفاده شده.


✅ مزایا و قابلیت‌های مهم
•	پشتیبانی از داده‌های فارسی
•	هایلایت بخش‌های مشابه بین دو پاسخ
•	رابط کاربری ساده و تعاملی
•	دقت بالا در تشخیص مشابهت
