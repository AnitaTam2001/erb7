import os
import django
import random
from datetime import datetime, timedelta
from faker import Faker

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import transaction
from django.core.files import File
from doctors.models import Doctor
from listings.models import Subject, Listing

# 初始化Faker
fake = Faker('zh-TW')

class DataImporter:
    def __init__(self):
        self.doctors_created = 0
        self.subjects_created = 0
        self.listings_created = 0
    
    def cleanup_data(self):
        """清理现有数据 - 修复外键约束问题"""
        print("正在清理现有数据...")
        
        # 按照依赖关系顺序删除数据
        # 先删除有外键依赖的表
        Listing.objects.all().delete()
        print("已删除所有诊所列表记录")
        
        # 然后删除被依赖的表
        Subject.objects.all().delete()
        print("已删除所有科目记录")
        
        Doctor.objects.all().delete()
        print("已删除所有医生记录")
        
        print("数据清理完成!")
    
    def create_sample_data(self):
        """创建样本数据"""
        self.create_subjects()
        self.create_doctors()
        self.create_listings()
    
    def create_subjects(self):
        """创建科目数据"""
        print("正在创建科目数据...")
        subjects_data = [
            "內科", "外科", "兒科", "婦產科", "眼科", 
            "耳鼻喉科", "牙科", "皮膚科", "精神科", "復健科",
            "心臟科", "神經科", "泌尿科", "骨科", "家庭醫學科"
        ]
        
        for subject_name in subjects_data:
            subject, created = Subject.objects.get_or_create(name=subject_name)
            if created:
                self.subjects_created += 1
        
        print(f"已创建 {self.subjects_created} 个科目")
        return Subject.objects.all()
    
    def create_doctors(self):
        """创建医生数据"""
        print("正在创建医生数据...")
        
        doctors_data = [
            {
                'name': '陳大明',
                'description': '資深內科醫師，擁有20年臨床經驗，專長於心血管疾病治療。',
                'phone': '0223456789',
                'email': 'chendaming@hospital.com'
            },
            {
                'name': '林小美',
                'description': '專業兒科醫師，對兒童疾病有深入研究，親切耐心的診療風格。',
                'phone': '0223456790',
                'email': 'linxiaomei@hospital.com'
            },
            {
                'name': '王建國',
                'description': '外科手術專家，擅長微創手術，完成超過千例成功手術。',
                'phone': '0223456791',
                'email': 'wangjianguo@hospital.com'
            },
            {
                'name': '張美麗',
                'description': '婦產科主任醫師，接生經驗豐富，專精高危險妊娠處理。',
                'phone': '0223456792',
                'email': 'zhangmeili@hospital.com'
            },
            {
                'name': '李聰明',
                'description': '眼科權威，專精白內障手術，引進最新雷射治療技術。',
                'phone': '0223456793',
                'email': 'licongming@hospital.com'
            },
            {
                'name': '黃小龍',
                'description': '牙科醫師，提供全方位牙齒護理，專精植牙與矯正治療。',
                'phone': '0223456794',
                'email': 'huangxiaolong@hospital.com'
            },
            {
                'name': '劉德華',
                'description': '皮膚科專家，對各種皮膚疾病有獨到見解與治療方案。',
                'phone': '0223456795',
                'email': 'liudehua@hospital.com'
            },
            {
                'name': '周杰倫',
                'description': '復健科醫師，結合中西醫治療，幫助患者恢復最佳狀態。',
                'phone': '0223456796',
                'email': 'jaychou@hospital.com'
            }
        ]
        
        for doctor_info in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                email=doctor_info['email'],
                defaults={
                    'name': doctor_info['name'],
                    'description': doctor_info['description'],
                    'phone': doctor_info['phone'],
                    'is_mvp': random.choice([True, False])
                }
            )
            if created:
                self.doctors_created += 1
        
        print(f"已创建 {self.doctors_created} 位医生")
        return Doctor.objects.all()
    
    def create_listings(self):
        """创建诊所列表数据"""
        print("正在创建诊所列表数据...")
        
        districts = ['中正區', '大同區', '中山區', '松山區', '大安區', '萬華區', '信義區', '士林區', '北投區', '內湖區']
        room_types = ['診療室', '手術室', '檢查室', '治療室', '諮詢室']
        services_list = ['一般診療', '健康檢查', '疫苗接種', '慢性病管理', '急診服務', '手術服務', '復健治療', '心理諮詢', '醫學影像', ' laboratory檢驗']
        
        doctors = list(Doctor.objects.all())
        subjects = list(Subject.objects.all())
        
        if not doctors:
            print("错误: 没有可用的医生数据")
            return
        if not subjects:
            print("错误: 没有可用的科目数据")
            return
        
        clinic_names = [
            "安心診所", "康健醫療中心", "仁愛醫院", "和平診所", "陽光醫療",
            "希望診所", "慈濟醫療", "惠民診所", "安康醫療中心", "德仁醫院"
        ]
        
        for i in range(20):  # 创建20个诊所记录
            doctor = random.choice(doctors)
            selected_subjects = random.sample(subjects, min(3, len(subjects)))
            clinic_name = random.choice(clinic_names)
            
            listing = Listing.objects.create(
                doctor=doctor,
                title=f"{clinic_name} - {doctor.name}醫師",
                address=f"{random.choice(districts)}{fake.street_address()}",
                district=random.choice(districts),
                description=fake.text(max_nb_chars=200),
                service=random.randint(1, 10),
                room_type=random.choice(room_types),
                screen=random.randint(1, 5),
                professional=random.randint(1, 10),
                rooms=random.choice(['1', '2', '3', '4+']),
                is_published=random.choice([True, False]),
                list_date=fake.date_time_between(
                    start_date='-1y', 
                    end_date='now'
                )
            )
            
            # 添加多对多关系
            listing.professionals.set(selected_subjects)
            
            # 添加标签服务
            selected_services = random.sample(services_list, min(4, len(services_list)))
            for service in selected_services:
                listing.services.add(service)
            
            self.listings_created += 1
            print(f"已创建诊所: {listing.title}")
        
        print(f"已创建 {self.listings_created} 个诊所列表")
    
    def export_data_summary(self):
        """导出数据摘要"""
        print("\n" + "="*50)
        print("数据导入摘要:")
        print("="*50)
        print(f"医生数量: {Doctor.objects.count()}")
        print(f"科目数量: {Subject.objects.count()}")
        print(f"诊所列表数量: {Listing.objects.count()}")
        
        # 显示一些样本数据
        print("\n样本数据预览:")
        print("医生列表:")
        for doctor in Doctor.objects.all()[:3]:
            print(f"  - {doctor.name} ({doctor.email})")
        
        print("\n科目列表:")
        for subject in Subject.objects.all()[:5]:
            print(f"  - {subject.name}")
        
        print("\n诊所列表:")
        for listing in Listing.objects.all()[:3]:
            print(f"  - {listing.title} ({listing.district})")
        
        print("="*50)
    
    @transaction.atomic
    def run_import(self):
        """运行完整导入流程 - 使用事务确保数据一致性"""
        print("开始数据导入流程...")
        
        try:
            # a) 清理原始数据
            self.cleanup_data()
            
            # b) 格式化并创建数据集
            self.create_sample_data()
            
            # c) 数据已自动导入数据库
            print("数据已成功导入Django数据库!")
            
            # d) 显示最终结果摘要
            self.export_data_summary()
            
            print("\n请在Django管理面板中检查数据:")
            print("- 访问 /admin/doctors/doctor/ 查看医生数据")
            print("- 访问 /admin/listings/subject/ 查看科目数据")
            print("- 访问 /admin/listings/listing/ 查看诊所列表数据")
            
        except Exception as e:
            print(f"数据导入过程中发生错误: {e}")
            # 事务会自动回滚

if __name__ == "__main__":
    importer = DataImporter()
    importer.run_import()