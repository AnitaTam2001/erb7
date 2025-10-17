import os
import django
import csv

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from doctors.models import Doctor
from listings.models import Subject, Listing

def quick_export_all():
    """快速导出所有模型数据"""
    
    # 导出医生数据
    with open('doctors_export.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', '姓名', '邮箱', '电话', '描述', 'MVP', '雇佣日期'])
        
        for doctor in Doctor.objects.all():
            writer.writerow([
                doctor.id,
                doctor.name,
                doctor.email,
                doctor.phone,
                doctor.description or '',
                '是' if doctor.is_mvp else '否',
                doctor.hire_date.strftime('%Y-%m-%d') if doctor.hire_date else ''
            ])
    print("医生数据导出完成: doctors_export.csv")
    
    # 导出科目数据
    with open('subjects_export.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', '科目名称'])
        
        for subject in Subject.objects.all():
            writer.writerow([subject.id, subject.name])
    print("科目数据导出完成: subjects_export.csv")
    
    # 导出诊所列表数据
    with open('listings_export.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', '标题', '医生', '地址', '区域', '房间类型', '是否发布'])
        
        for listing in Listing.objects.all().select_related('doctor'):
            writer.writerow([
                listing.id,
                listing.title,
                listing.doctor.name,
                listing.address,
                listing.district,
                listing.room_type,
                '是' if listing.is_published else '否'
            ])
    print("诊所列表数据导出完成: listings_export.csv")

if __name__ == "__main__":
    quick_export_all()