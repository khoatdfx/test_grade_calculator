import re
import numpy as np
import pandas as pd

# Tạo biến file_name để lưu trữ input của người dùng
# lower case biến file_name để đảm bảo chỉ cần đúng tên file thì sẽ đọc được, không quan trọng người dùng có sử dụng Caps Lock
file_name = input('Enter a class to grade (i.e. class1 for class1.txt): ').lower()
answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
key_list = answer_key.split(',')

# Đọc file với try except
try:
    with open(f'./Data/{file_name}.txt', 'r') as file:

        # Thông báo đọc file thành công
        print(f'{file_name}.txt successfully opened')

        # Đọc tất cả các dòng trong file và lưu và list file_data
        file_data = file.readlines()

        # Tạo các biến để đếm số data hợp lệ, không hợp lệ, danh sách các data hợp lệ và không hợp lệ
        valid_data_count = 0
        invalid_data_count = 0
        valid_data_list = []
        invalid_data_list = []

        for i in range(len(file_data)):

            # Tách từng dòng trong data thành các list tương ứng
            stud_data = file_data[i].split(',')
            stud_data[-1] = stud_data[-1].strip()

            # Tạo RegEx để kiểm tra tính hợp lệ của số ID của sinh viên
            stud_id_regex = '^N+\d{8}'
            stud_id_check = re.match(stud_id_regex, file_data[i])

            '''
            Kiểm tra tính hợp lệ của ID sinh viên
            Nếu hợp lệ thì biến valid_data_count sẽ tăng thêm 1
            Nếu không hợp lệ thì biến invalid_data_count tăng thêm 1 
            và đưa các dòng không hợp lệ vào biến danh sách invalid_data_list
            '''
            if len(stud_data) == 26 and len(stud_data[0]) == 9 and stud_id_check:
                valid_data_count += 1
                valid_data_list.append(stud_data)
            else:
                invalid_data_count += 1
                invalid_data_list.append(stud_data)
        
        # Hiển thị thông tin phân tích và báo cáo về file dữ liệu
        print('\n**** ANALYZING ****\n')
        if len(invalid_data_list) == 0:
            print('No errors found!\n')
        else:
            # Duyệt qua danh sách invalid_data_list và in ra các dòng theo các lỗi
            for i in invalid_data_list:
                if len(i) != 26 :
                    print('Invalid line of data: does not contain exactly 26 values')
                    print(','.join(map(str, i)), '\n')
                else:
                    print('Invalid line of data: N# is invalid')
                    print(','.join(map(str, i)), '\n')

        print('**** REPORT ****')
        print(f'\nTotal lines of data: {len(file_data)}')
        print(f'Total valid lines of data: {valid_data_count}')
        print(f'Total invalid lines of data: {invalid_data_count}')
        
        

        '''
        Zip đáp án và câu trả lời của sinh viên thành các tuple và đưa vào list
        Duyệt qua từng phần tử trong bộ dữ liệu đã được zip và so đáp án với câu trả lời của sinh viên
        Nếu câu trả lời giống với đáp án thì được 4 điểm, bỏ trống thì 0 điểm và trả lời sai thì bị -1 điểm
        Tính tổng điểm của từng sinh viên và đưa vào score_list để tính các giá trị thống kê
        '''
        answer_list = [valid_data_list[i][1:] for i in range(len(valid_data_list))]
        stud_id_list = [valid_data_list[i][0] for i in range(len(valid_data_list))]
        score_list = []

        for j in range(len(answer_list)):
            s = 0
            zip_data = list(zip(key_list, answer_list[j]))
            for i in zip_data:
                total_correct = []
                total_empty = []
                total_wrong = []
                total = 0
                if i[0] == i[1]:
                    total_correct.append(i[0])
                elif i[1] == '':
                    total_empty.append(i[1])
                elif i[0] != i[1]:
                    total_wrong.append(i[1])
                total = 4 * len(total_correct) + 0 * len(total_empty) + (-1) * len(total_wrong)
                s += total
            score_list.append(s)

        print(f'\nAverage score: {round(np.mean(score_list), 2)}')
        print(f'Highest score: {np.max(score_list)}')
        print(f'Lowest score: {np.min(score_list)}')
        print(f'Range scores: {np.max(score_list) - np.min(score_list)}')
        print(f'Median score: {np.median(score_list)}')

        # Lưu thông tin gồm ID sinh viên và điểm vào một dataframe
        score_df = pd.DataFrame(
            {
                'StudentID': stud_id_list,
                'Score': score_list
            }
        )

        # Sử dụng numpy để ghi file kết quả của từng lớp kết hợp try except để bắt lỗi
        try:
            np.savetxt(f'./Result/{file_name}_grades.txt', score_df.values, fmt = '%s', delimiter = ',', newline = '\n')
            print(f'\n{file_name}.txt successfully wrote to txt file')
        except Exception as e:
            print('An error occurred ', e)

# Thông báo file nhập không tồn tại
except FileNotFoundError as e:
    print('File does not exist: ', e)

# Thông báo lỗi khác khi chạy chương trình 
except Exception as e:
    print('An error occurred ', e)