"""
LuxeCart Backend API & Static Web Server
Runs on Python standard library without external dependencies.
"""
import http.server
import socketserver
import json
import urllib.parse
import os
import sys

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

PRODUCTS_DATA = [
    {
        "id": 1,
        "title": "سماعات الأذن اللاسلكية برو زيرو",
        "title_en": "Pro Zero Wireless Headphones",
        "category": "electronics",
        "price": 199.99,
        "originalPrice": 249.99,
        "rating": 4.8,
        "reviewsCount": 128,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=600&auto=format&fit=crop&q=80",
        "badge": "الأكثر مبيعاً",
        "description": "سماعات فائقة الجودة تتميز بخاصية إلغاء الضوضاء النشط، وعمر بطارية يدوم حتى 40 ساعة من الاستماع المتواصل.",
        "specs": ["إلغاء الضوضاء النشط (ANC)", "بطارية 40 ساعة", "بلوتوث 5.3", "مقاوم للماء IPX5"]
    },
    {
        "id": 2,
        "title": "ساعة ذكية تيتانيوم إكس",
        "title_en": "Titanium X Smartwatch",
        "category": "electronics",
        "price": 299.99,
        "originalPrice": 349.99,
        "rating": 4.9,
        "reviewsCount": 94,
        "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=600&auto=format&fit=crop&q=80",
        "badge": "جديد",
        "description": "ساعة رياضية وأنيقة بهيكل من التيتانيوم الصلب وشاشة AMOLED مع تتبع دقيق للصحة والأنشطة الرياضية.",
        "specs": ["شاشة AMOLED 1.43 بوصة", "تتبع نبضات القلب و SpO2", "هيكل تيتانيوم مقاوم للصدمات", "بطارية تدوم 14 يوماً"]
    },
    {
        "id": 3,
        "title": "حقيبة ظهر جلدية كلاسيكية",
        "title_en": "Classic Leather Backpack",
        "category": "fashion",
        "price": 129.50,
        "originalPrice": 160.00,
        "rating": 4.7,
        "reviewsCount": 64,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=80",
        "badge": "خصم 20%",
        "description": "حقيبة من الجلد الطبيعي الفاخر تتسع للاب توب بحجم 15.6 بوصة مع جيب مقاوم للماء وتصميم فاخر للعمل والسفر.",
        "specs": ["جلد طبيعي 100%", "مقصورة لاب توب 15.6 بوصة", "مقاومة للماء", "ضمان لمدة سنتين"]
    },
    {
        "id": 4,
        "title": "كاميرا فورية ريترو سينس",
        "title_en": "Retro Sense Instant Camera",
        "category": "electronics",
        "price": 149.00,
        "originalPrice": 179.99,
        "rating": 4.6,
        "reviewsCount": 52,
        "image": "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=600&auto=format&fit=crop&q=80",
        "badge": "مميز",
        "description": "سجل لحظاتك المميزة فوراً بطابع كلاسيكي، مع مرآة سيلفي مدمجة وعدسة تقريب دقيقة.",
        "specs": ["طباعة فورية في ثوانٍ", "فلاش أوتوماتيكي", "وضع السيلفي المطور", "بطارية قابلة للشحن"]
    },
    {
        "id": 5,
        "title": "نظارة شمسية كلاسيك بولاريزد",
        "title_en": "Classic Polarized Sunglasses",
        "category": "fashion",
        "price": 79.99,
        "originalPrice": 99.99,
        "rating": 4.5,
        "reviewsCount": 87,
        "image": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=600&auto=format&fit=crop&q=80",
        "badge": "الأعلى تقييماً",
        "description": "حماية كاملة من أشعة الشمس UV400 مع عدسات بولاريزد لمنع الانعكاسات ومظهر عصري جذاب.",
        "specs": ["حماية UV400", "عدسات Polarized", "إطار معدني خفيف الوزن", "حافظة جلدية فاخرة"]
    },
    {
        "id": 6,
        "title": "مصباح مكتب ذكي LED minimalist",
        "title_en": "Smart Minimalist LED Desk Lamp",
        "category": "home",
        "price": 89.00,
        "originalPrice": 110.00,
        "rating": 4.8,
        "reviewsCount": 43,
        "image": "https://images.unsplash.com/photo-1534073828943-f801091bb18c?w=600&auto=format&fit=crop&q=80",
        "badge": "",
        "description": "مصباح مكتب بتصميم حديث يدعم التحكم باللمس ومستويات إضاءة متعددة مع شاحن لاسلكي مدمج للهاتف.",
        "specs": ["شاحن لاسلكي 15W", "5 درجات حرارة للون", "تحكم باللمس", "مؤقت إيقاف تلقائي"]
    },
    {
        "id": 7,
        "title": "زجاجة مياه حرارية ستانلس ستيل",
        "title_en": "Insulated Thermal Water Bottle",
        "category": "accessories",
        "price": 34.99,
        "originalPrice": 45.00,
        "rating": 4.9,
        "reviewsCount": 210,
        "image": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80",
        "badge": "الأكثر طلباً",
        "description": "تحفظ المشروبات باردة لمدة 24 ساعة وساخنة لمدة 12 ساعة بفضل تكنولوجيا العزل الفراغي المزدوج.",
        "specs": ["عزل مزدوج Double-Wall", "سعة 750 مل", "خالية من BPA", "غطاء مقاوم للتسريب"]
    },
    {
        "id": 8,
        "title": "حذاء رياضي أنيق بلس",
        "title_en": "Aero Comfort Sneakers",
        "category": "fashion",
        "price": 119.99,
        "originalPrice": 149.99,
        "rating": 4.7,
        "reviewsCount": 156,
        "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80",
        "badge": "خصم 20%",
        "description": "حذاء جري يومي مصمم ببطانة ممتصة للصدمات وخامات شبكية مريحة لتهوية القدمين طوال اليوم.",
        "specs": ["نعل مرن ممتص للصدمات", "قماش خفيف متهوي", "تصميم عصري ديناميكي", "مقاسات متعددة"]
    }
]

COUPONS = {
    "LUXE10": 0.10,
    "SAVE20": 0.20,
    "PROMO30": 0.30
}

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/products":
            self.send_json_response(PRODUCTS_DATA)
        elif path.startswith("/api/products/"):
            prod_id = path.split("/")[-1]
            try:
                prod_id = int(prod_id)
                product = next((p for p in PRODUCTS_DATA if p["id"] == prod_id), None)
                if product:
                    self.send_json_response(product)
                else:
                    self.send_json_response({"error": "Product not found"}, status=404)
            except ValueError:
                self.send_json_response({"error": "Invalid Product ID"}, status=400)
        elif path == "/api/categories":
            categories = list(set(p["category"] for p in PRODUCTS_DATA))
            self.send_json_response(categories)
        else:
            super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b'{}'
        
        try:
            body = json.loads(post_data.decode('utf-8'))
        except Exception:
            body = {}

        if path == "/api/coupon":
            code = body.get("code", "").strip().upper()
            if code in COUPONS:
                discount = COUPONS[code]
                self.send_json_response({
                    "valid": True,
                    "code": code,
                    "discountRate": discount,
                    "message": f"تم تطبيق الخصم بنجاح ({int(discount*100)}%)"
                })
            else:
                self.send_json_response({
                    "valid": False,
                    "message": "كود الخصم غير صالح أو منتهي الصلاحية"
                }, status=400)

        elif path == "/api/checkout":
            items = body.get("items", [])
            total = body.get("total", 0)
            customer = body.get("customer", {})
            order_id = f"ORD-{int(os.times().system * 100000) % 899999 + 100000}"
            
            self.send_json_response({
                "success": True,
                "orderId": order_id,
                "message": "تم استلام الطلب بنجاح! شكراً لتسوقك معنا.",
                "total": total,
                "customer": customer
            })
        else:
            self.send_json_response({"error": "Endpoint not found"}, status=404)

    def send_json_response(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
    print(f"==================================================")
    print(f"🚀 LuxeCart Store Server is running!")
    print(f"🌐 Open in your browser: http://localhost:{PORT}")
    print(f"==================================================")
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped successfully.")
