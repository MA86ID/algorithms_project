import json

def read_json_file(file_path):
    try:
        # تلاش برای باز کردن و خواندن فایل
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                # تلاش برای تجزیه محتوای JSON
                data = json.load(file)
                return data
            except json.JSONDecodeError as json_error:
                print(f"خطا در تجزیه فایل JSON: {json_error}")
                return None
    except FileNotFoundError:
        print(f"فایل '{file_path}' پیدا نشد.")
        return None
    except PermissionError:
        print("خطا: دسترسی به فایل امکان‌پذیر نیست.")
        return None
    except Exception as e:
        print(f"خطای غیرمنتظره: {str(e)}")
        return None

# استفاده از تابع
file_path = 'results.json'  # مسیر فایل JSON خود را اینجا وارد کنید
result = read_json_file(file_path)

if result is not None:
    print("محتوای فایل JSON:")
    print(result)