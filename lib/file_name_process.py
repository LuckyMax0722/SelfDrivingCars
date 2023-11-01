import csv

# 读取原始CSV文件
input_file = '/home/jiachen/SelfDrivingCars/data_D/driving_log.csv'
output_file = '/home/jiachen/SelfDrivingCars/data_D/re.csv'

with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
    csv_reader = csv.reader(input_csv)
    csv_writer = csv.writer(output_csv)

    for row in csv_reader:
        # 检查是否有足够的列数（至少3列）
        if len(row) >= 3:
            # 在第一列的字符串前添加'/home/jiachen/SelfDrivingCars/data/'
            row[0] = f'/home/jiachen/SelfDrivingCars/data/{row[0]}'
            # 删除第二和第三列的字符串的第一个字符
            row[1] = row[1][1:]
            row[1] = f'/home/jiachen/SelfDrivingCars/data/{row[1]}'
            row[1] = f' {row[1]}'
            row[2] = row[2][1:]
            row[2] = f'/home/jiachen/SelfDrivingCars/data/{row[2]}'
            row[2] = f' {row[2]}'

        csv_writer.writerow(row)

print(f'已修改第一列前缀和删除第二列和第三列的第一个字符，结果保存到 {output_file}')
