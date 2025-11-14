from datetime import datetime
import os
import shutil

# Читаем файл подписок
subscriptions_file = 'subscriptions.txt'

if not os.path.exists(subscriptions_file):
    print("No subscriptions file found")
    exit(0)

with open(subscriptions_file, 'r') as f:
    lines = f.readlines()

current_date = datetime.now().strftime('%Y-%m-%d')
updated_lines = []

for line in lines:
    if line.strip() and ':' in line:
        try:
            username, email, expiry_date, txt_filename = line.strip().split(':')
            
            # Проверяем дату окончания
            if current_date <= expiry_date:
                # Подписка активна - оставляем
                updated_lines.append(line)
            else:
                # Подписка истекла - перемещаем файл
                source_path = f"codes/{txt_filename}"
                dest_path = f"expired/{txt_filename}"
                
                if os.path.exists(source_path):
                    shutil.move(source_path, dest_path)
                    print(f"Moved expired: {txt_filename}")
                else:
                    print(f"File not found: {txt_filename}")
                    
        except ValueError as e:
            print(f"Error parsing line: {line} - {e}")
            updated_lines.append(line)  # Оставляем проблемные строки

# Сохраняем обновленный файл подписок
with open(subscriptions_file, 'w') as f:
    f.writelines(updated_lines)

print("Subscription check completed!")
