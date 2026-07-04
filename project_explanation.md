# شرح تفصيلي كامل لمشروع Cryptocraft

**المطور:** Mohannad Al-Majidi  
**اللغة:** Python 3.12  
**المكتبة الرئيسية:** CustomTkinter

---

## الفكرة العامة للمشروع

Cryptocraft هو تطبيق مكتبي (Desktop GUI Application) مبني بلغة Python يُتيح للمستخدم تشفير وفك تشفير نصوص باستخدام خمس خوارزميات مختلفة. الهدف الأساسي للمشروع ليس فقط تطبيق خوارزميات التشفير، بل بناؤها بطريقة معمارية احترافية قابلة للتطوير والصيانة.

---

## الهيكل الكامل للمشروع

```
Encryption Algorithms/
│
├── main.py                    # نقطة تشغيل التطبيق
├── requirements.txt           # قائمة المكتبات المطلوبة
├── .gitignore                 # تجاهل الملفات المؤقتة عند الرفع لـ GitHub
├── README.md                  # توثيق المشروع
│
├── core/                      # طبقة المنطق الجوهري (خوارزميات التشفير)
│   ├── __init__.py
│   ├── base_cipher.py         # الفئة الأساسية المجردة + نموذج النتيجة
│   ├── caesar_cipher.py
│   ├── vigenere_cipher.py
│   ├── hill_cipher.py
│   ├── des_cipher.py
│   └── aes_cipher.py
│
├── controllers/               # طبقة التحكم (الجسر بين الواجهة والمنطق)
│   ├── __init__.py
│   └── cipher_controller.py
│
├── ui/                        # طبقة الواجهة
│   ├── __init__.py
│   ├── app_window.py          # النافذة الرئيسية والمنسق العام
│   ├── views/
│   │   ├── __init__.py
│   │   ├── selection_view.py  # شاشة اختيار الخوارزمية
│   │   └── cipher_view.py     # شاشة العمل والتشفير
│   └── widgets/
│       ├── __init__.py
│       └── algorithm_card.py  # مكوّن البطاقة التفاعلية
│
└── utils/                     # أدوات مساعدة مشتركة
    ├── __init__.py
    ├── theme.py               # نظام التصميم والألوان
    └── clipboard.py           # النسخ إلى الحافظة
```

---

## البنية المعمارية (Architecture Pattern)

المشروع مبني على نمط معماري مُقسَّم إلى 3 طبقات واضحة متمايزة:

```
[ Presentation Layer (ui/) ]
         ↕
[ Controller Layer (controllers/) ]
         ↕
[ Core Logic Layer (core/) ]
```

**لماذا هذه البنية؟**
- الطبقة الأولى (UI) لا تعرف أي شيء عن رياضيات التشفير.
- الطبقة الثالثة (Core) لا تعرف أي شيء عن CustomTkinter أو الواجهات.
- طبقة التحكم هي الوحيدة التي تعرف الاثنتين وتنسق بينهما.
- هذا يعني أنك تستطيع تغيير أي طبقة بالكامل دون أن تؤثر على الأخرى.

---

## تفصيل كل ملف

---

### main.py

**الغرض:** نقطة دخول التطبيق الوحيدة.

```python
def main() -> None:
    app = AppWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
```

- تُنشئ `main()` كائناً واحداً من `AppWindow` وتبدأ حلقة الأحداث `mainloop()`.
- حلقة `mainloop()` هي حلقة لا نهائية تستمع لأحداث النظام (نقر، كتابة، تغيير حجم نافذة) حتى يُغلق المستخدم التطبيق.

---

### utils/theme.py

**الغرض:** تعريف نظام التصميم المركزي للتطبيق (Design Tokens System).

```python
@dataclass(frozen=True)
class AppTheme:
    bg_primary: tuple   = ("#F8FAFC", "#0D0F1A")
    bg_secondary: tuple = ("#FFFFFF", "#13162B")
    ...
```

**الفكرة الجوهرية:**
- `@dataclass(frozen=True)` تعني أن الكائن ثابت لا يتغير (Immutable). لا يمكن لأي مكون في التطبيق تعديل قيم المظهر بالخطأ.
- كل قيمة لونية عبارة عن Tuple من قيمتين: `(لون_المظهر_الفاتح, لون_المظهر_الداكن)`.
- CustomTkinter يقرأ هذا التنسيق تلقائياً ويختار اللون المناسب حسب الوضع النشط (Dark/Light).
- جميع الأرقام (المسافات، أحجام الخطوط) مركزية هنا أيضاً مثل `font_size_lg`, `pad_md`.

**أبرز الدوال:**

| الدالة | الغرض |
|--------|--------|
| `algorithm_colors` (property) | تُعيد قاموساً يربط اسم كل خوارزمية بلونها المخصص |
| `get_algorithm_color(name)` | تأخذ اسم الخوارزمية وتُعيد لونها أو اللون الافتراضي |

---

### utils/clipboard.py

**الغرض:** نسخ نص إلى حافظة النظام.

```python
def copy_to_clipboard(widget: ctk.CTk, text: str) -> None:
    widget.clipboard_clear()
    widget.clipboard_append(text)
    widget.update()
```

- نستخدم `widget.clipboard_clear()` أولاً لمسح أي نص سابق في الحافظة.
- ثم `widget.clipboard_append(text)` لوضع النص الجديد.
- `widget.update()` ضروري على Windows لضمان أن النظام يستلم النص قبل إغلاق التطبيق.

---

### core/base_cipher.py

**الغرض:** تعريف العقد البرمجي (Contract) الذي يجب أن تلتزم به كل خوارزمية.

**يحتوي على نوعين:**

#### 1. CipherResult (نموذج النتيجة)

```python
@dataclass
class CipherResult:
    success: bool
    output: str
    error_message: Optional[str] = None
    algorithm_name: str = ""
    operation: str = ""
```

**لماذا نستخدم CipherResult بدل استثناءات Exception؟**
- بدلاً من رمي `Exception` عند خطأ في المفتاح، كل عملية تُعيد دائماً `CipherResult`.
- الواجهة تتحقق من `result.success` وتعرض إما النتيجة أو رسالة الخطأ.
- هذا يمنع انهيار التطبيق ويعطي المستخدم رسائل واضحة.

#### 2. BaseCipher (الفئة المجردة)

```python
class BaseCipher(ABC):
    @property @abstractmethod
    def name(self) -> str: ...

    @property @abstractmethod
    def description(self) -> str: ...

    @property @abstractmethod
    def key_hint(self) -> str: ...

    @abstractmethod
    def encrypt(self, plaintext: str, key: str) -> CipherResult: ...

    @abstractmethod
    def decrypt(self, ciphertext: str, key: str) -> CipherResult: ...

    @abstractmethod
    def generate_key(self) -> str: ...
```

- `ABC` هو اختصار Abstract Base Class. يمنع إنشاء كائن مباشرة من `BaseCipher`.
- كل خوارزمية جديدة تُضاف للمشروع يجب أن تُنفذ جميع هذه الدوال وإلا يُرفع خطأ Python فوراً عند التشغيل.

**الدوال المساعدة المُضمَّنة (Helpers في BaseCipher):**

```python
def _make_success(self, output, operation) -> CipherResult:
    # تُنشئ كائن نتيجة ناجحة بسهولة
    
def _make_error(self, message, operation) -> CipherResult:
    # تُنشئ كائن نتيجة فاشلة بسهولة
```

هذان الاثنان يُوفران الكتابة المتكررة ويضمنان اتساق النتائج عبر كل الخوارزميات.

---

### core/caesar_cipher.py

**الفكرة الرياضية:** إزاحة كل حرف بمقدار ثابت في الأبجدية.
مثال: الحرف A مع مفتاح 3 يصبح D.

**الثابت:**
```python
ALPHABET_SIZE = 26
```

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `encrypt(plaintext, key)` | تتحقق من المفتاح ثم تُطبق الإزاحة الموجبة |
| `decrypt(ciphertext, key)` | تطبق نفس الإزاحة لكن سالبة `(-shift)` |
| `generate_key()` | تُعيد رقماً عشوائياً بين 1 و 25 |
| `_parse_key(key)` | تتحقق أن المفتاح رقم صحيح بين 1 و 25 |
| `_shift_text(text, shift)` | التحويل الفعلي - تمر على كل حرف وتُزيحه |

**قلب الخوارزمية:**
```python
shifted = (ord(char) - base + shift) % ALPHABET_SIZE
```
- `ord(char)` تُحوّل الحرف إلى رقم ASCII.
- `base` هو رقم `A` (65) أو `a` (97) حسب حالة الحرف.
- عملية `% 26` تضمن الدوران (Z + 1 يرجع لـ A).

---

### core/vigenere_cipher.py

**الفكرة الرياضية:** خوارزمية Caesar لكن بدلاً من مفتاح رقمي واحد، نستخدم كلمة مفتاحية تتكرر على طول النص.

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `encrypt(plaintext, key)` | تنظف المفتاح ثم تُشفر |
| `decrypt(ciphertext, key)` | تنظف المفتاح ثم تفك التشفير |
| `generate_key()` | تُولد كلمة عشوائية من الحروف الكبيرة طولها 6-10 |
| `_sanitize_key(key)` | تزيل كل ما ليس حرفاً وتحوله لأحرف كبيرة |
| `_process(text, key, mode)` | التحويل الفعلي |

**قلب الخوارزمية في `_process`:**
```python
key_shift = ord(key[key_index % len(key)]) - ord('A')
```
- `key_index % len(key)` يضمن تكرار الكلمة المفتاحية بشكل دائري.
- `key_index` يزداد فقط عند معالجة حرف أبجدي (الأرقام والمسافات تُترك كما هي).

---

### core/hill_cipher.py

**الفكرة الرياضية:** تشفير الجبر الخطي (Linear Algebra). يتم تمثيل النص كمتجه أرقام ثم ضربه في مصفوفة مفتاح مع عملية Modulo 26.

**المكتبة:** `numpy` لعمليات المصفوفات.

**الثابت:**
```python
MOD = 26
```

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `encrypt(plaintext, key)` | تحلل المصفوفة وتُطبق الضرب |
| `decrypt(ciphertext, key)` | تحسب المصفوفة العكسية وتُطبقها |
| `generate_key()` | تُولد مصفوفة 2×2 عشوائية قابلة للعكس |
| `_parse_key_matrix(key)` | تحوّل النص المُدخل إلى مصفوفة numpy وتتحقق من صحتها |
| `_matrix_mod_inverse(matrix, n)` | تحسب المصفوفة المعكوسة modulo 26 |
| `_apply_matrix(text, matrix, n)` | تُقسم النص لكتل وتضرب كل كتلة في المصفوفة |
| `_extract_letters(text)` | تُبقي الحروف الأبجدية فقط (Hill لا تعمل على أرقام) |
| `_pad_text(text, block_size)` | تُضيف X حتى يكون طول النص مضاعفاً للنظام |
| `_gcd(a, b)` | خوارزمية القاسم المشترك الأكبر (Euclidean Algorithm) |
| `_mod_inverse(a, m)` | المعكوس الضربي modulo 26 |

**لماذا يجب أن تكون المصفوفة قابلة للعكس؟**
```python
det = int(round(np.linalg.det(matrix))) % 26
if det == 0 or gcd(det, 26) != 1:
    return error("Matrix is not invertible mod 26")
```
بدون هذا الشرط لن يكون فك التشفير ممكناً رياضياً.

---

### core/des_cipher.py

**الفكرة:** DES هو خوارزمية تشفير صناعية قياسية (بلوك سيفر). نستخدم مكتبة `pycryptodome` لتطبيقه بدلاً من إعادة اختراعه.

**الثوابت:**
```python
KEY_LENGTH = 8       # 8 بايت = 64 بت
BLOCK_SIZE = 8       # حجم البلوك 64 بت
IV = b'\x00' * 8    # Initialization Vector ثابت للبساطة
```

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `encrypt(plaintext, key)` | تُشفر النص وتُعيد النتيجة بتنسيق Hex |
| `decrypt(ciphertext, key)` | تحوّل Hex إلى بايتات ثم تفك التشفير |
| `generate_key()` | تُولد 8 أحرف عشوائية alphanumeric |
| `_validate_and_encode_key(key)` | تتحقق أن طول المفتاح بالضبط 8 أحرف |

**لماذا CBC Mode؟**
- CBC (Cipher Block Chaining) أكثر أماناً من ECB لأن كل بلوك يعتمد على نتيجة البلوك السابق.

**لماذا تنسيق Hex؟**
- الناتج المشفر بيانات ثنائية (Binary) لا يمكن عرضها كنص عادي، لذا نحولها لـ Hex لعرضها.

---

### core/aes_cipher.py

**الفكرة:** AES هو المعيار الذهبي للتشفير الحديث، أسرع وأقوى من DES. البنية مشابهة لـ DES مع اختلاف في أحجام المفاتيح والبلوكات.

**الثوابت:**
```python
VALID_KEY_LENGTHS = {16, 24, 32}  # 128, 192, 256 بت
BLOCK_SIZE = 16                    # 128 بت
IV = b'\x00' * 16
```

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `encrypt(plaintext, key)` | تُشفر بـ AES-CBC وتُعيد Hex |
| `decrypt(ciphertext, key)` | تُحوّل Hex وتفك التشفير |
| `generate_key()` | تُولد 32 حرفاً عشوائياً (256 بت) |
| `_validate_and_encode_key(key)` | تتحقق أن الطول 16 أو 24 أو 32 |

---

### controllers/cipher_controller.py

**الغرض:** الجسر الذي ينسق بين الواجهة وطبقة الخوارزميات. الواجهة لا تستورد أي شيء من `core/` مباشرة.

**الخصائص الداخلية:**
```python
self._registry: Dict[str, BaseCipher]  # قاموس: اسم الخوارزمية → كائنها
self._active_cipher_name: Optional[str]  # اسم الخوارزمية النشطة حالياً
```

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `_build_registry()` | يُنشئ كائناً واحداً من كل خوارزمية ويضعها في القاموس |
| `get_algorithm_names()` | يُعيد قائمة بأسماء الخوارزميات |
| `select_algorithm(name)` | يُحدد الخوارزمية النشطة |
| `active_cipher` (property) | يُعيد كائن الخوارزمية النشطة أو None |
| `encrypt(plaintext, key)` | يُمرر طلب التشفير للخوارزمية النشطة |
| `decrypt(ciphertext, key)` | يُمرر طلب فك التشفير للخوارزمية النشطة |
| `get_active_key_hint()` | يُعيد تلميح المفتاح من الخوارزمية النشطة |
| `get_active_description()` | يُعيد وصف الخوارزمية النشطة |
| `get_active_name()` | يُعيد اسم الخوارزمية النشطة |
| `generate_active_key()` | يستدعي `generate_key()` من الخوارزمية النشطة |
| `_get_active_or_error(operation)` | مساعدة خاصة - تُعيد الخوارزمية أو خطأ إذا لم يُختر شيء |

---

### ui/app_window.py

**الغرض:** الطبقة العليا التي تمتلك كل شيء وتنسّق بين الشاشات. لا تعرف شيئاً عن رياضيات التشفير، تتعامل فقط مع التحكم (CipherController) والشاشات.

**الثوابت:**
```python
WINDOW_TITLE = "Encryption Algorithms Suite"
WINDOW_SIZE  = "920x680"
MIN_SIZE     = (820, 580)
```

**الخصائص الداخلية:**
```python
self._theme: AppTheme           # كائن المظهر الوحيد
self._controller: CipherController  # كائن المتحكم الوحيد
self._active_view: CTkFrame    # الشاشة المعروضة حالياً
```

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `_configure_window()` | تعيين العنوان والحجم وتمركز النافذة على الشاشة |
| `_build_background()` | بناء إطار الحاوية الرئيسية |
| `_show_selection_view()` | تدمير الشاشة الحالية وعرض شاشة الاختيار |
| `_show_cipher_view()` | تدمير الشاشة الحالية وعرض مساحة العمل |
| `_clear_active_view()` | تدمير الشاشة الحالية لتحرير الذاكرة |
| `_handle_algorithm_selected(name)` | يُبلغ المتحكم باختيار خوارزمية |
| `_handle_encrypt(text, key)` | يُرسل طلب تشفير للمتحكم ويعرض النتيجة |
| `_handle_decrypt(text, key)` | يُرسل طلب فك تشفير للمتحكم ويعرض النتيجة |
| `_handle_copy(text)` | يستدعي دالة النسخ للحافظة |
| `_handle_generate_key()` | يطلب من المتحكم مفتاحاً جديداً ويُعيده للشاشة |
| `toggle_theme()` | يتحقق من الوضع الحالي ويُبدله عبر `ctk.set_appearance_mode()` |
| `_refresh_cipher_view_header()` | يُحدث ترويسة شاشة العمل بمعلومات الخوارزمية المختارة |
| `_get_cipher_description(name)` | يُعيد وصف خوارزمية محددة دون تغيير الاختيار النشط |

---

### ui/views/selection_view.py

**الغرض:** الشاشة الأولى التي تظهر للمستخدم. تعرض بطاقات الخوارزميات وتنتقل فوراً عند الضغط.

**البنية البصرية:**
```
┌─────────────────────────────────────────────┐
│  [Lock Icon] Encryption Suite    [☀️ / 🌙]  │
│  Select a cipher algorithm...               │
│  ─────────────────────────────────────────  │
│  [ Caesar Cipher ]    [ Vigenère Cipher ]   │
│  [ Hill Cipher   ]    [ DES              ]  │
│  [ AES           ]                          │
└─────────────────────────────────────────────┘
```

**المعلمات في الـ init:**

| المعلمة | الغرض |
|---------|--------|
| `algorithm_names` | قائمة بأسماء الخوارزميات |
| `algorithm_descriptions` | قاموس: اسم → وصف |
| `on_algorithm_selected` | Callback يُستدعى عند اختيار خوارزمية |
| `on_continue` | Callback للانتقال لشاشة العمل |
| `on_toggle_theme` | Callback لزر تبديل المظهر |
| `theme` | كائن AppTheme |

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `_build_ui(names, descriptions)` | بناء الشاشة الكاملة (الترويسة + الشبكة + البطاقات) |
| `_build_header()` | بناء الجزء العلوي (عنوان + أيقونة + زر المظهر + فاصل) |
| `_handle_selection(name)` | تُبلغ المتحكم باختيار خوارزمية وتنتقل فوراً لشاشة العمل |

---

### ui/views/cipher_view.py

**الغرض:** مساحة العمل الرئيسية للتشفير وفك التشفير.

**البنية البصرية:**
```
┌─────────────────────────────────────────────┐
│  [← Back]  Caesar Cipher          [☀️ / 🌙] │
│  ─────────────────────────────────────────  │
│  [●] Caesar Cipher                          │
│      Shifts each letter by a fixed...       │
│  ─────────────────────────────────────────  │
│  [Key Input Field] [⚡ Generate]            │
│  ℹ Enter a number (1-25)                    │
│                     [Input Text Area]        │
│  ─────────────────────────────────────────  │
│  [ ⚡ Encrypt ]     [ 🔓 Decrypt ]          │
│  ─────────────────────────────────────────  │
│  [Output] [Status Badge]        [Copy]      │
│  ─────────────────────────────────────────  │
│  Output text here...                        │
└─────────────────────────────────────────────┘
```

**المعلمات في الـ init:**

| المعلمة | الغرض |
|---------|--------|
| `on_encrypt` | Callback للتشفير (يستقبل النص + المفتاح) |
| `on_decrypt` | Callback لفك التشفير |
| `on_back` | Callback للرجوع |
| `on_copy` | Callback لنسخ النتيجة |
| `on_generate_key` | Callback لطلب مفتاح جديد (يُعيد str) |
| `on_toggle_theme` | Callback لزر المظهر |

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `_build_top_bar()` | بناء الشريط العلوي (← Back + العنوان + زر المظهر) |
| `_build_algorithm_info()` | بناء بطاقة معلومات الخوارزمية المختارة |
| `_build_input_section()` | بناء حقل المفتاح + زر Generate + حقل النص |
| `_build_output_section()` | بناء منطقة عرض النتيجة |
| `update_algorithm(name, desc, hint, color)` | تحديث جميع عناصر الشاشة عند تغيير الخوارزمية |
| `display_result(output, operation, success, error)` | عرض نتيجة التشفير/فك التشفير مع لون الحالة |
| `get_input_text()` | قراءة النص من حقل الإدخال |
| `get_key()` | قراءة المفتاح من حقل الإدخال |
| `get_output_text()` | قراءة النص من منطقة الإخراج |
| `_handle_encrypt()` | جمع النص والمفتاح واستدعاء `on_encrypt` |
| `_handle_decrypt()` | جمع النص والمفتاح واستدعاء `on_decrypt` |
| `_handle_generate_key()` | طلب مفتاح جديد ووضعه في حقل المفتاح |
| `_handle_copy()` | نسخ النتيجة وتغيير نص زر النسخ مؤقتاً |
| `_clear_output()` | مسح منطقة النتيجة |
| `_make_label(parent, text)` | دالة مساعدة لإنشاء Labels بنفس التنسيق |

---

### ui/widgets/algorithm_card.py

**الغرض:** المكوّن البصري الأساسي في شاشة الاختيار. كل بطاقة تمثل خوارزمية واحدة.

**بنية البطاقة:**
```
┌──┬─────────────────────────────────────────┐
│  │  Caesar Cipher (Bold, Large)            │
│  │  Shifts alphabetic characters...        │
└──┴─────────────────────────────────────────┘
 ↑
شريط لوني جانبي
```

**تحدي الأحداث في CustomTkinter:**
المشكلة كانت أن CustomTkinter يُنشئ داخلياً Canvas وLabel مدمجة، ونقرة المستخدم تُلتقط من هذه العناصر الداخلية ولا تصل للإطار الخارجي (البطاقة).

**الحل المُطبق:** ربط الأحداث مباشرة على جميع المكونات الظاهرة للمستخدم بشكل صريح باستخدام `*args` لتفادي أخطاء التوقيعات:

```python
for widget in [self, accent_bar, content_frame, name_label, desc_label]:
    widget.bind("<Button-1>", lambda *args: self._on_click())
    widget.bind("<Enter>",    lambda *args: self._on_hover())
    widget.bind("<Leave>",    lambda *args: self._on_leave())
```

**الدوال:**

| الدالة | الغرض |
|--------|--------|
| `_build_ui(description)` | بناء الشريط اللوني + إطار المحتوى + العنوان + الوصف |
| `_bind_explicit_events()` | ربط أحداث الماوس على كل المكونات |
| `_on_click()` | استدعاء `on_select(self._name)` عند النقر |
| `_on_hover()` | تغيير لون الخلفية عند مرور المؤشر |
| `_on_leave()` | إعادة اللون الأصلي عند مغادرة المؤشر (مع التحقق أن المؤشر خرج فعلاً) |
| `set_selected(selected)` | تلوين/إعادة البطاقة للوضع المحدد/غير المحدد |

**منطق `_on_leave` الذكي:**
```python
ptr_x, ptr_y = self.winfo_pointerxy()
still_inside = (card_x <= ptr_x <= card_x2) and (card_y <= ptr_y <= card_y2)
if not still_inside:
    self.configure(fg_color=self._theme.bg_secondary)
```
لأن التنقل بين المكونات الداخلية للبطاقة (من Label إلى Frame) يُطلق أحداث `<Leave>` زائفة، قمنا بالتحقق من الإحداثيات الحقيقية لمؤشر الماوس قبل إعادة اللون.

---

## تدفق بيانات مثال كامل (من النقر إلى النتيجة)

**المستخدم يريد تشفير كلمة HELLO بخوارزمية Caesar بمفتاح 3:**

```
1. المستخدم ينقر على بطاقة "Caesar Cipher" في SelectionView
      ↓
2. AlgorithmCard._on_click() تستدعي on_select("Caesar Cipher")
      ↓
3. SelectionView._handle_selection("Caesar Cipher") تستدعي:
   - on_algorithm_selected("Caesar Cipher")      ← تُبلغ AppWindow
   - on_continue()                               ← تطلب الانتقال
      ↓
4. AppWindow._handle_algorithm_selected("Caesar Cipher"):
   - controller.select_algorithm("Caesar Cipher")
      ↓
5. AppWindow._show_cipher_view() تبني CipherView وتعرضه
      ↓
6. AppWindow._refresh_cipher_view_header() يجلب البيانات من المتحكم
   ويُحدث cipher_view.update_algorithm(...)
      ↓
7. المستخدم يكتب "HELLO" في حقل النص و "3" في حقل المفتاح
      ↓
8. المستخدم ينقر زر "Encrypt"
      ↓
9. CipherView._handle_encrypt() تستدعي:
   on_encrypt("HELLO", "3")
      ↓
10. AppWindow._handle_encrypt("HELLO", "3") تستدعي:
    result = controller.encrypt("HELLO", "3")
      ↓
11. CipherController.encrypt() تستدعي:
    self.active_cipher.encrypt("HELLO", "3")
    (active_cipher هو CaesarCipher)
      ↓
12. CaesarCipher.encrypt("HELLO", "3"):
    - يُحلل المفتاح: shift = 3
    - يُطبق _shift_text("HELLO", 3)
    - H(7)+3 = K, E(4)+3 = H, L(11)+3 = O, L(11)+3 = O, O(14)+3 = R
    - يُعيد CipherResult(success=True, output="KHOOR")
      ↓
13. AppWindow._handle_encrypt() يستدعي:
    cipher_view.display_result(output="KHOOR", operation="encrypt", success=True)
      ↓
14. CipherView.display_result() تكتب "KHOOR" في منطقة النتيجة
    وتعرض شارة "✓ Encrypted" خضراء
```

---

## ملاحظات ختامية مهمة

1. **لا يوجد اتصال مباشر بين UI وCore:** الواجهة لا تعرف كيف تعمل Caesar، والخوارزمية لا تعرف شيئاً عن الأزرار.
2. **إضافة خوارزمية جديدة سهلة جداً:** كل ما تحتاجه هو إنشاء ملف جديد في `core/` يرث من `BaseCipher` وينفذ الدوال الست، ثم إضافته لـ `_build_registry` في المتحكم.
3. **تبديل المظهر لا يُعيد بناء الواجهة:** CustomTkinter يُحدّث الألوان تلقائياً على جميع الـ Widgets النشطة دون الحاجة لإعادة إنشائها.
4. **كل عملية تشفير آمنة من الانهيار:** استخدام `CipherResult` بدل الاستثناءات يضمن أن أي خطأ في المفتاح يظهر للمستخدم كرسالة واضحة لا كبرنامج منهار.
