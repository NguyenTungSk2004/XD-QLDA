import pandas as pd
import random

# Hàm tạo HTML mẫu từ dữ liệu trong bảng
def generate_random_html_questions(data, num_questions=40):
    # Chọn ngẫu nhiên `num_questions` câu hỏi từ dữ liệu
    selected_questions = data.sample(n=num_questions).reset_index(drop=True)
    
    html_output = '<div class="bo_cau_hoi">\n'  # Mở thẻ bao đề thi
    for index, row in selected_questions.iterrows():
        question_id = f"q{index + 1}"  # Đánh số từ 1 đến num_questions
        question_text = row['Question Text']
        options = [row['Option 1'], row['Option 2'], row['Option 3'], row['Option 4']]
        correct_answer = row['Correct Answer']
        
        # Khởi tạo thẻ câu hỏi
        html_output += f'  <div class="question">\n'
        html_output += f'    <h3>Question {index + 1}</h3>\n'
        html_output += f'    <p>{question_text}</p>\n'
        
        # Thêm các lựa chọn
        for i, option in enumerate(options, start=1):
            if pd.notna(option):  # Chỉ thêm các lựa chọn không rỗng
                value = chr(96 + i)  # Tạo giá trị a, b, c, d
                is_correct = ' class="correct"' if i == correct_answer else ''
                html_output += (
                    f'    <label><br>\n'
                    f'    <input name="{question_id}" type="radio" value="{value}"{is_correct}> {option}</label><br>\n'
                )
        
        # Đóng thẻ câu hỏi
        html_output += '  </div>\n' 
    
    html_output += '</div>'  # Đóng thẻ bao đề thi
    return html_output

# Đọc dữ liệu từ file Excel
file_path = 'data/listQuiz_XDQLDACNTT _Part2_101-211.xlsx'
try:
    # Đọc dữ liệu từ Excel
    sheet_data = pd.ExcelFile(file_path).parse(0)  # Sheet đầu tiên
    columns_to_keep = ['Question Text', 'Option 1', 'Option 2', 'Option 3', 'Option 4', 'Correct Answer']
    filtered_data = sheet_data[columns_to_keep].dropna(subset=['Question Text', 'Correct Answer'])
    filtered_data['Correct Answer'] = pd.to_numeric(filtered_data['Correct Answer'], errors='coerce')

    # Tạo HTML
    html_output = generate_random_html_questions(filtered_data)

    # Lưu HTML vào file
    output_file_path = 'random_quiz.html'
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_output)

    print(f"HTML được lưu tại: {output_file_path}")
except Exception as e:
    print(f"Lỗi khi xử lý file: {e}")
