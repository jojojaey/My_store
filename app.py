from datetime import datetime
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for

# إنشاء تطبيق الويب باستخدام مكتبة فلاسك
app = Flask(__name__)

# قائمة مؤقتة لتخزين الطلبات التي يرسلها الزبائن
orders = []


# 1. الصفحة الرئيسية (التي يفتحها الزبون ليرى متجر الاشتراكات)
@app.route("/")
def index():
  return render_template("index.html")


# 2. مسار استقبال الطلب (عندما يضغط الزبون "إتمام الطلب")
@app.route("/submit_order", methods=["POST"])
def submit_order():
  # جلب بيانات الزبون التي كتبها في الاستمارة
  customer_name = request.form.get("name")
  customer_phone = request.form.get("phone")
  item_name = request.form.get("item")

  # إنشاء رقم تسلسلي للطلب
  order_id = len(orders) + 1

  # ترتيب بيانات الطلب بداخل قالب بيانات (قاموس)
  new_order = {
      "id": order_id,
      "name": customer_name,
      "phone": customer_phone,
      "item": item_name,
      "status": "جاري الطلب",  # الحالة الابتدائية
      "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
  }

  # إضافة الطلب للقائمة
  orders.append(new_order)

  # طباعة تنبيه في السيرفر بأن هناك طلباً جديداً وصل
  print(
      f"[طلب جديد] من الزبون: {customer_name}, الهاتف: {customer_phone}, طلب:"
      f" {item_name}"
  )

  # إرسال رد للزبون بأن طلبه تم بنجاح
  return jsonify(
      {
          "success": True,
          "message": (
              "تم إرسال طلبك بنجاح! سيتم التواصل معك للدفع عند الاستلام قريباً."
          ),
      }
  )


# 3. لوحة التحكم الخاصة بكِ (لرؤية الطلبات)
@app.route("/admin")
def admin_panel():
  return render_template("admin.html", orders=orders)


# 4. زر تغيير حالة الطلب إلى "تم التجهيز"
@app.route("/mark_ready/<int:order_id>", methods=["POST"])
def mark_ready(order_id):
  for order in orders:
    if order["id"] == order_id:
      order["status"] = "تم تجهيز الطلب والتسليم"
      break
  return redirect(url_for("admin_panel"))


# تشغيل التطبيق على السيرفر بالمنفذ المخصص
if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
  
