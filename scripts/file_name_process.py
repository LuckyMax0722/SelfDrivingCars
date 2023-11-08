import csv

# 读取原始CSV文件
input_file = '/data/tumdriving/SelfDrivingCars/data/driving_log.csv'
output_file = '/data/tumdriving/SelfDrivingCars/data/driving_log_c.csv'

with open(input_file, 'r') as input_csv, open(output_file, 'w', newline='') as output_csv:
    csv_reader = csv.reader(input_csv)
    csv_writer = csv.writer(output_csv)

    
    for row in csv_reader:
        row[0] = row[0].replace('/home/jiachen', '/data/tumdriving')
        row[1] = row[1].replace(' /home/jiachen', ' /data/tumdriving')
        row[2] = row[2].replace(' /home/jiachen', ' /data/tumdriving')
        csv_writer.writerow(row)
    '''
    for row in csv_reader:
        row[0] = row[0].replace('/home/jiachen/SelfDrivingCars/data_val/', '/data/tumdriving/SelfDrivingCars/data/')
        row[1] = row[1].replace(' /home/jiachen/SelfDrivingCars/data_val/', ' /data/tumdriving/SelfDrivingCars/data/')
        row[2] = row[2].replace(' /home/jiachen/SelfDrivingCars/data_val/', ' /data/tumdriving/SelfDrivingCars/data/')
        csv_writer.writerow(row)
    '''

print('Finish file name preprocessing')
