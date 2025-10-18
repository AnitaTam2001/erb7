
import os
import sys
import django
import json
import random
from datetime import datetime, timedelta
from faker import Faker

# 设置Django环境
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files import File
from doctors.models import Doctor
from listings.models import Subject, Listing
from taggit.models import Tag

# 初始化Faker
fake = Faker('zh_TW')
Faker.seed(42)  # 确保每次生成相同的数据

class DataManager:
    def __init__(self):
        self.sample_data = {}
        self.exported_data = {}
        
        # 模拟choices数据（根据您的choices.py）
        self.district_choices = {
            'Zhongzheng': '中正區',
            'Da-an': '大安區', 
            'Xinyi': '信義區',
            'Songshan': '松山區',
            'Zhongshan': '中山區',
            'Wanhua': '萬華區',
            'Datong': '大同區',
            'Shilin': '士林區',
            'Beitou': '北投區',
            'Neihu': '內湖區',
            'Nangang': '南港區',
            'Wenshan': '文山區'
        }
        
        self.room_choices = {
            'consultation': '診療室',
            'surgery': '手術室', 
            'examination': '檢查室',
            'recovery': '恢復室',
            'emergency': '急診室'
        }
        
        self.rooms_choices = {
            '1': '1間',
            '2': '2間',
            '3': '3間', 
            '4': '4間',
            '5+': '5間以上'
        }

    def clean_existing_data(self):
        """清理现有数据"""
        print("正在清理现有数据...")
        Listing.objects.all().delete()
        Doctor.objects.all().delete() 
        Subject.objects.all().delete()
        Tag.objects.all().delete()
        print("数据清理完成")

    def generate_sample_data(self):
        """生成样本数据"""
        print("正在生成样本数据...")
        
        # 生成Subject数据
        subjects_data = [
            '心臟內科', '神經外科', '兒科', '婦產科', '眼科',
            '牙科', '皮膚科', '精神科', '復健科', '急診醫學科'
        ]
        
        subjects = []
        for subject_name in subjects_data:
            subject, created = Subject.objects.get_or_create(name=subject_name)
            subjects.append(subject)
            print(f"創建科目: {subject_name}")
        
        # 生成Doctor数据 (8位醫生)
        doctors = []
        for i in range(8):
            doctor = Doctor(
                name=fake.name(),
                description=fake.text(max_nb_chars=200),
                phone=fake.phone_number(),
                email=fake.unique.email(),
                is_mvp=fake.boolean(chance_of_getting_true=30),
                hire_date=fake.date_time_between(start_date='-5y', end_date='now')
            )
            # 注意：照片字段需要实际文件，这里暂时留空
            doctor.save()
            doctors.append(doctor)
            print(f"創建醫生: {doctor.name}")
        
        # 生成Listing数据 (12個診所列表)
        services_list = [
            '門診服務', '急診服務', '健康檢查', '疫苗接種', '手術服務',
            '復健治療', '牙科服務', '眼科檢查', '產前檢查', '兒童保健'
        ]
        
        listings = []
        for i in range(12):
            # 随机选择医生
            doctor = random.choice(doctors)
            
            # 随机选择专业科目 (1-3个)
            selected_subjects = random.sample(subjects, random.randint(1, 3))
            
            listing = Listing(
                doctor=doctor,
                title=f"{doctor.name}醫師的{fake.company_suffix()}診所",
                address=fake.address(),
                district=random.choice(list(self.district_choices.keys())),
                description=fake.text(max_nb_chars=300),
                service=random.randint(1, 10),
                room_type=random.choice(list(self.room_choices.keys())),
                screen=random.randint(1, 5),
                professional=random.randint(1, 10),
                rooms=random.choice(list(self.rooms_choices.keys())),
                is_published=fake.boolean(chance_of_getting_true=80),
                list_date=fake.date_time_between(
                    start_date='-1y', end_date='now'
                )
            )
            
            listing.save()
            
            # 添加多对多关系
            listing.professionals.set(selected_subjects)
            
            # 添加标签服务
            selected_services = random.sample(services_list, random.randint(2, 5))
            for service in selected_services:
                listing.services.add(service)
            
            listings.append(listing)
            print(f"創建診所列表: {listing.title}")
        
        self.sample_data = {
            'subjects': subjects,
            'doctors': doctors, 
            'listings': listings
        }
        
        print(f"樣本數據生成完成:")
        print(f"- 科目: {len(subjects)} 個")
        print(f"- 醫生: {len(doctors)} 位") 
        print(f"- 診所列表: {len(listings)} 個")

    def format_data_for_export(self):
        """格式化数据用于导出"""
        print("正在格式化數據用於導出...")
        
        formatted_data = {
            'export_time': datetime.now().isoformat(),
            'subjects': [],
            'doctors': [],
            'listings': []
        }
        
        # 格式化Subject数据
        for subject in Subject.objects.all():
            formatted_data['subjects'].append({
                'id': subject.id,
                'name': subject.name
            })
        
        # 格式化Doctor数据
        for doctor in Doctor.objects.all():
            formatted_data['doctors'].append({
                'id': doctor.id,
                'name': doctor.name,
                'description': doctor.description,
                'phone': doctor.phone,
                'email': doctor.email,
                'is_mvp': doctor.is_mvp,
                'hire_date': doctor.hire_date.isoformat()
            })
        
        # 格式化Listing数据
        for listing in Listing.objects.all():
            formatted_data['listings'].append({
                'id': listing.id,
                'doctor_id': listing.doctor.id,
                'title': listing.title,
                'address': listing.address,
                'district': listing.district,
                'description': listing.description,
                'service': listing.service,
                'room_type': listing.room_type,
                'screen': listing.screen,
                'professional': listing.professional,
                'rooms': listing.rooms,
                'is_published': listing.is_published,
                'list_date': listing.list_date.isoformat(),
                'professionals': [subj.id for subj in listing.professionals.all()],
                'services': [tag.name for tag in listing.services.all()]
            })
        
        self.exported_data = formatted_data
        return formatted_data

    def export_to_json(self, filename='django_sample_data.json'):
        """导出数据到JSON文件"""
        if not self.exported_data:
            self.format_data_for_export()
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.exported_data, f, ensure_ascii=False, indent=2)
        
        print(f"數據已導出到: {filename}")

    def import_from_json(self, filename='django_sample_data.json'):
        """从JSON文件导入数据"""
        print(f"正在從 {filename} 導入數據...")
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"文件 {filename} 不存在")
            return
        
        # 清理现有数据
        self.clean_existing_data()
        
        # 导入Subject数据
        subject_map = {}
        for subject_data in data['subjects']:
            subject = Subject.objects.create(
                id=subject_data['id'],
                name=subject_data['name']
            )
            subject_map[subject_data['id']] = subject
        
        # 导入Doctor数据
        doctor_map = {}
        for doctor_data in data['doctors']:
            doctor = Doctor.objects.create(
                id=doctor_data['id'],
                name=doctor_data['name'],
                description=doctor_data['description'],
                phone=doctor_data['phone'],
                email=doctor_data['email'],
                is_mvp=doctor_data['is_mvp'],
                hire_date=datetime.fromisoformat(doctor_data['hire_date'])
            )
            doctor_map[doctor_data['id']] = doctor
        
        # 导入Listing数据
        for listing_data in data['listings']:
            listing = Listing.objects.create(
                id=listing_data['id'],
                doctor=doctor_map[listing_data['doctor_id']],
                title=listing_data['title'],
                address=listing_data['address'],
                district=listing_data['district'],
                description=listing_data['description'],
                service=listing_data['service'],
                room_type=listing_data['room_type'],
                screen=listing_data['screen'],
                professional=listing_data['professional'],
                rooms=listing_data['rooms'],
                is_published=listing_data['is_published'],
                list_date=datetime.fromisoformat(listing_data['list_date'])
            )
            
            # 添加多对多关系
            professional_ids = listing_data['professionals']
            professionals = [subject_map[pid] for pid in professional_ids]
            listing.professionals.set(professionals)
            
            # 添加标签
            for service in listing_data['services']:
                listing.services.add(service)
        
        print("數據導入完成")

    def display_statistics(self):
        """显示数据统计"""
        print("\n=== 數據統計 ===")
        print(f"科目數量: {Subject.objects.count()}")
        print(f"醫生數量: {Doctor.objects.count()}")
        print(f"診所列表數量: {Listing.objects.count()}")
        
        # 显示一些样本数据
        print("\n=== 最近創建的3個診所 ===")
        recent_listings = Listing.objects.all().order_by('-list_date')[:3]
        for listing in recent_listings:
            print(f"- {listing.title} (醫生: {listing.doctor.name})")

def main():
    """主函数"""
    manager = DataManager()
    
    while True:
        print("\n=== Django 數據管理系統 ===")
        print("1. 清理所有數據")
        print("2. 生成樣本數據")
        print("3. 導出數據到JSON")
        print("4. 從JSON導入數據")
        print("5. 顯示數據統計")
        print("6. 執行完整流程 (清理→生成→導出)")
        print("0. 退出")
        
        choice = input("請選擇操作: ").strip()
        
        if choice == '1':
            manager.clean_existing_data()
        elif choice == '2':
            manager.generate_sample_data()
        elif choice == '3':
            manager.export_to_json()
        elif choice == '4':
            filename = input("輸入JSON文件名 (回車使用默認): ").strip()
            if not filename:
                manager.import_from_json()
            else:
                manager.import_from_json(filename)
        elif choice == '5':
            manager.display_statistics()
        elif choice == '6':
            print("執行完整流程...")
            manager.clean_existing_data()
            manager.generate_sample_data()
            manager.export_to_json()
            manager.display_statistics()
            print("完整流程完成！")
        elif choice == '0':
            print("再見！")
            break
        else:
            print("無效選擇，請重新輸入")

if __name__ == "__main__":
    # 安装依赖提示
    try:
        import faker
    except ImportError:
        print("請先安裝所需依賴:")
        print("pip install faker")
        sys.exit(1)
    
    main()