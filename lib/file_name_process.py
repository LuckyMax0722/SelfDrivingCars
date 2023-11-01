import csv

# 读取原始CSV文件
input_file = '/home/jiachen/SelfDrivingCars/data/driving_log.csv'
output_file = '/home/jiachen/SelfDrivingCars/data/re.csv'

with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
    csv_reader = csv.reader(input_csv)
    csv_writer = csv.writer(output_csv)

    for row in csv_reader:
        # 检查是否有足够的列数（至少3列）
        if len(row) >= 3:
            row[0] = row[0].replace('/home/jiachen', '/home/tum')
            row[1] = row[1].replace(' /home/jiachen', ' /home/tum')
            row[2] = row[2].replace(' /home/jiachen', ' /home/tum')

        csv_writer.writerow(row)

print(f'已修改第一列前缀和删除第二列和第三列的第一个字符，结果保存到 {output_file}')
