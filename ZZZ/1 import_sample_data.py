import os
import django
import random
from datetime import datetime

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from doctors.models import Doctor
from listings.models import Subject, Listing
from listings.choices import district_choices, rooms_choices, room_choices

def clear_data():
    """清理現有資料（可選）"""
    Doctor.objects.all().delete()
    Subject.objects.all().delete()
    Listing.objects.all().delete()
    print("✅ 已清理現有資料")

def create_doctors():
    """建立醫生樣本資料"""
    doctors_data = [
        {
            "name": "陳大明",
            "photo": "doctors/2025/1016/dr_chen.jpg",
            "description": "資深內科醫師，專長為糖尿病與高血壓管理。",
            "phone": "0223456789",
            "email": "chen@example.com",
            "is_mvp": True,
        },
        {
            "name": "林小美",
            "photo": "doctors/2025/1016/dr_lin.jpg",
            "description": "小兒科醫師，親切細心，深受家長信賴。",
            "phone": "0223456790",
            "email": "lin@example.com",
            "is_mvp": True,
        },
        {
            "name": "王建國",
            "photo": "doctors/2025/1016/dr_wang.jpg",
            "description": "骨科專家，擅長關節置換手術。",
            "phone": "0223456791",
            "email": "wang@example.com",
            "is_mvp": False,
        },
        {
            "name": "黃雅婷",
            "photo": "doctors/2025/1016/dr_huang.jpg",
            "description": "眼科醫師，提供雷射手術與視力矯正服務。",
            "phone": "0223456792",
            "email": "huang@example.com",
            "is_mvp": True,
        },
        {
            "name": "劉偉豪",
            "photo": "doctors/2025/1016/dr_liu.jpg",
            "description": "心臟科主治醫師，專精於心血管疾病。",
            "phone": "0223456793",
            "email": "liu@example.com",
            "is_mvp": False,
        },
    ]

    for data in doctors_data:
        Doctor.objects.get_or_create(
            email=data["email"],
            defaults=data
        )
    print("✅ 醫生資料已建立")

def create_subjects():
    """建立科別資料"""
    subjects = ["內科", "小兒科", "骨科", "眼科", "心臟科", "家醫科", "皮膚科"]
    for name in subjects:
        Subject.objects.get_or_create(name=name)
    print("✅ 科別資料已建立")

def create_listings():
    """建立診所列表資料"""
    doctors = list(Doctor.objects.all())
    subjects = list(Subject.objects.all())

    listings_data = [
        {
            "doctor": random.choice(doctors),
            "title": "陽光診所",
            "address": "台北市信義區松高路100號",
            "district": "信義區",
            "description": "提供專業內科與家醫科服務，環境舒適。",
            "service": 5,
            "room_type": "診療室",
            "screen": 3,
            "professional": 2,
            "rooms": "3",
            "photo_main": "photos/2025/1016/clinic1.jpg",
            "is_published": True,
        },
        {
            "doctor": random.choice(doctors),
            "title": "安心兒科診所",
            "address": "新北市板橋區文化路200號",
            "district": "板橋區",
            "description": "專為兒童設計的醫療空間，親子友善。",
            "service": 4,
            "room_type": "兒童診間",
            "screen": 2,
            "professional": 1,
            "rooms": "2",
            "photo_main": "photos/2025/1016/clinic2.jpg",
            "is_published": True,
        },
        {
            "doctor": random.choice(doctors),
            "title": "明亮眼科中心",
            "address": "台中市西區公益路150號",
            "district": "西區",
            "description": "擁有先進設備的眼科診所，提供全面視力檢查。",
            "service": 6,
            "room_type": "檢查室",
            "screen": 4,
            "professional": 3,
            "rooms": "4",
            "photo_main": "photos/2025/1016/clinic3.jpg",
            "is_published": True,
        },
        {
            "doctor": random.choice(doctors),
            "title": "健骨聯合診所",
            "address": "高雄市前金區成功路300號",
            "district": "前金區",
            "description": "骨科與復健科聯合服務，專業團隊支援。",
            "service": 7,
            "room_type": "診療室",
            "screen": 5,
            "professional": 4,
            "rooms": "5",
            "photo_main": "photos/2025/1016/clinic4.jpg",
            "is_published": True,
        },
        {
            "doctor": random.choice(doctors),
            "title": "心悅心血管中心",
            "address": "台北市大安區仁愛路250號",
            "district": "大安區",
            "description": "心臟科專業診所，提供心血管健康管理。",
            "service": 5,
            "room_type": "檢查室",
            "screen": 3,
            "professional": 2,
            "rooms": "3",
            "photo_main": "photos/2025/1016/clinic5.jpg",
            "is_published": True,
        },
    ]

    for data in listings_data:
        listing = Listing.objects.create(**data)
        # 隨機加入科別
        listing.professionals.set(random.sample(subjects, 2))
        # 隨機加入服務標籤（需安裝 django-taggit）
        listing.services.add("門診", "預約制", "健保給付")
    print("✅ 診所列表資料已建立")

if __name__ == "__main__":
    clear_data()
    create_doctors()
    create_subjects()
    create_listings()
    print("🎉 所有樣本資料已成功匯入！請至 Django Admin 後台檢查。")