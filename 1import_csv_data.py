import os
import django
import csv

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from doctors.models import Doctor
from listings.models import Subject, Listing

def clear_data():
    """清理現有資料"""
    print("清理現有資料...")
    Listing.objects.all().delete()
    Doctor.objects.all().delete()
    Subject.objects.all().delete()
    print("✓ 資料清理完成")

def import_doctors_from_csv(csv_file='doctors.csv'):
    """從 CSV 導入醫生資料"""
    print(f"導入醫生資料從 {csv_file}...")
    
    doctor_id_mapping = {}
    doctor_count = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                original_id = int(row['id'])
                doctor, created = Doctor.objects.get_or_create(
                    email=row['email'],
                    defaults={
                        'name': row['name'],
                        'description': row.get('description', ''),
                        'phone': row.get('phone', '00000000'),
                        'is_mvp': row.get('is_mvp', 'True').lower() == 'true'
                    }
                )
                doctor_id_mapping[original_id] = doctor.id
                doctor_count += 1
                status = "✓" if created else "↻"
                print(f"{status} 建立醫生: {doctor.name} (ID: {doctor.id})")
                
        print(f"✓ 成功導入 {doctor_count} 位醫生")
        print(f"醫生 ID 對照表: {doctor_id_mapping}")
        return doctor_id_mapping
        
    except FileNotFoundError:
        print(f"✗ 找不到檔案: {csv_file}")
        return {}
    except Exception as e:
        print(f"✗ 導入醫生資料時發生錯誤: {e}")
        return {}

def import_subjects_from_csv(csv_file='subjects.csv'):
    """從 CSV 導入科目資料"""
    print(f"\n導入科目資料從 {csv_file}...")
    
    subject_id_mapping = {}
    subject_count = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                original_id = int(row['id'])
                subject, created = Subject.objects.get_or_create(
                    name=row['name']
                )
                subject_id_mapping[original_id] = subject.id
                subject_count += 1
                status = "✓" if created else "↻"
                print(f"{status} 建立科目: {subject.name} (ID: {subject.id})")
                
        print(f"✓ 成功導入 {subject_count} 個科目")
        return subject_id_mapping
        
    except FileNotFoundError:
        print(f"✗ 找不到檔案: {csv_file}")
        return {}
    except Exception as e:
        print(f"✗ 導入科目資料時發生錯誤: {e}")
        return {}

def import_listings_from_csv(csv_file='listings.csv', doctor_id_mapping=None):
    """從 CSV 導入診所資料"""
    print(f"\n導入診所列表資料從 {csv_file}...")
    
    if doctor_id_mapping is None:
        doctor_id_mapping = {}
    
    listing_id_mapping = {}
    listing_count = 0
    error_count = 0
    
    # 顯示醫生 ID 對照表
    print("醫生 ID 對照表:")
    for original_id, db_id in doctor_id_mapping.items():
        doctor = Doctor.objects.get(id=db_id)
        print(f"  CSV ID: {original_id} → 資料庫 ID: {db_id} - 姓名: {doctor.name}")
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                original_listing_id = int(row['id'])
                original_doctor_id = int(row['doctor_id'])
                
                # 使用映射表找到正確的醫生 ID
                if original_doctor_id in doctor_id_mapping:
                    actual_doctor_id = doctor_id_mapping[original_doctor_id]
                    
                    try:
                        doctor = Doctor.objects.get(id=actual_doctor_id)
                        
                        listing, created = Listing.objects.get_or_create(
                            title=row['title'],
                            doctor=doctor,
                            defaults={
                                'address': row['address'],
                                'district': row['district'],
                                'description': row.get('description', ''),
                                'service': int(row.get('service', 0)),
                                'room_type': row.get('room_type', ''),
                                'screen': int(row.get('screen', 0)),
                                'professional': int(row.get('professional', 0)),
                                'rooms': row.get('rooms', '1'),
                                'is_published': row.get('is_published', 'True').lower() == 'true'
                            }
                        )
                        
                        listing_id_mapping[original_listing_id] = listing.id
                        listing_count += 1
                        status = "✓" if created else "↻"
                        print(f"{status} 建立診所: {listing.title} (醫生: {doctor.name})")
                        
                    except Doctor.DoesNotExist:
                        print(f"✗ 資料庫中找不到醫生 ID: {actual_doctor_id}，對應診所: {row['title']}")
                        error_count += 1
                else:
                    print(f"✗ 找不到醫生 ID: {original_doctor_id}，對應診所: {row['title']}")
                    error_count += 1
                    
        print(f"✓ 成功導入 {listing_count} 間診所")
        if error_count > 0:
            print(f"⚠  {error_count} 個診所導入失敗")
        return listing_id_mapping
        
    except FileNotFoundError:
        print(f"✗ 找不到檔案: {csv_file}")
        return {}
    except Exception as e:
        print(f"✗ 導入診所資料時發生錯誤: {e}")
        return {}

def import_listing_professionals_from_csv(csv_file='listing_professionals.csv', listing_id_mapping=None, subject_id_mapping=None):
    """從 CSV 導入診所-科目關係"""
    print(f"\n導入診所-科目關係從 {csv_file}...")
    
    if listing_id_mapping is None:
        listing_id_mapping = {}
    if subject_id_mapping is None:
        subject_id_mapping = {}
    
    relationship_count = 0
    error_count = 0
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                original_listing_id = int(row['listing_id'])
                original_subject_id = int(row['subject_id'])
                
                # 使用映射表找到正確的 ID
                if (original_listing_id in listing_id_mapping and 
                    original_subject_id in subject_id_mapping):
                    
                    actual_listing_id = listing_id_mapping[original_listing_id]
                    actual_subject_id = subject_id_mapping[original_subject_id]
                    
                    try:
                        listing = Listing.objects.get(id=actual_listing_id)
                        subject = Subject.objects.get(id=actual_subject_id)
                        
                        # 檢查關係是否已存在
                        if not listing.professionals.filter(id=subject.id).exists():
                            listing.professionals.add(subject)
                            relationship_count += 1
                            print(f"✓ 建立關係: {listing.title} - {subject.name}")
                        else:
                            print(f"↻ 關係已存在: {listing.title} - {subject.name}")
                        
                    except Listing.DoesNotExist:
                        print(f"✗ 找不到診所 ID: {actual_listing_id}")
                        error_count += 1
                    except Subject.DoesNotExist:
                        print(f"✗ 找不到科目 ID: {actual_subject_id}")
                        error_count += 1
                else:
                    missing = []
                    if original_listing_id not in listing_id_mapping:
                        missing.append(f"診所 ID: {original_listing_id}")
                    if original_subject_id not in subject_id_mapping:
                        missing.append(f"科目 ID: {original_subject_id}")
                    print(f"✗ 找不到映射的 ID - {', '.join(missing)}")
                    error_count += 1
                    
        print(f"✓ 成功建立 {relationship_count} 個診所-科目關係")
        if error_count > 0:
            print(f"⚠  {error_count} 個關係建立失敗")
        return relationship_count
        
    except FileNotFoundError:
        print(f"✗ 找不到檔案: {csv_file}")
        return 0
    except Exception as e:
        print(f"✗ 導入診所-科目關係時發生錯誤: {e}")
        return 0

def check_csv_files():
    """檢查 CSV 檔案是否存在"""
    required_files = ['doctors.csv', 'subjects.csv', 'listings.csv', 'listing_professionals.csv']
    missing_files = []
    
    print("檢查 CSV 檔案...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ 找到檔案: {file}")
        else:
            print(f"✗ 找不到檔案: {file}")
            missing_files.append(file)
    
    return missing_files

def display_summary():
    """顯示導入總結"""
    print("\n" + "="*60)
    print("📊 資料導入總結")
    print("="*60)
    
    doctors_count = Doctor.objects.count()
    subjects_count = Subject.objects.count()
    listings_count = Listing.objects.count()
    
    # 計算診所-科目關係總數
    total_relationships = 0
    for listing in Listing.objects.all():
        total_relationships += listing.professionals.count()
    
    print(f"👨‍⚕️  醫生數量: {doctors_count}")
    print(f"📚 科目數量: {subjects_count}")
    print(f"🏥 診所數量: {listings_count}")
    print(f"🔗 診所-科目關係: {total_relationships}")
    
    # 顯示診所列表
    print(f"\n🏥 診所列表:")
    for listing in Listing.objects.all():
        subjects = ", ".join([subject.name for subject in listing.professionals.all()])
        print(f"  • {listing.title} (醫生: {listing.doctor.name})")
        print(f"    科目: {subjects}")
    
    print("="*60)

def main():
    """主執行函數"""
    print("開始從 CSV 檔案導入資料...")
    print("="*60)
    
    # 檢查 CSV 檔案
    missing_files = check_csv_files()
    if missing_files:
        print(f"\n❌ 缺少必要的 CSV 檔案: {missing_files}")
        print("請確保以下檔案存在於相同目錄:")
        print("  - doctors.csv")
        print("  - subjects.csv") 
        print("  - listings.csv")
        print("  - listing_professionals.csv")
        return
    
    # 清理現有資料
    clear_data()
    
    # 導入資料
    print("\n開始導入資料...")
    doctor_id_mapping = import_doctors_from_csv()
    
    if not doctor_id_mapping:
        print("❌ 醫生資料導入失敗，中止程序")
        return
        
    subject_id_mapping = import_subjects_from_csv()
    
    if not subject_id_mapping:
        print("❌ 科目資料導入失敗，中止程序")
        return
        
    listing_id_mapping = import_listings_from_csv(doctor_id_mapping=doctor_id_mapping)
    
    if not listing_id_mapping:
        print("❌ 診所資料導入失敗，中止程序")
        return
        
    relationship_count = import_listing_professionals_from_csv(
        listing_id_mapping=listing_id_mapping,
        subject_id_mapping=subject_id_mapping
    )
    
    # 顯示總結
    display_summary()
    
    print("\n🎉 CSV 資料導入完成！")
    print("您可以在 Django Admin 中檢視所有導入的資料")

if __name__ == "__main__":
    main()