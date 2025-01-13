import pandas as pd
import os

# Hàm tạo HTML mẫu từ dữ liệu trong bảng
def generate_html_from_data(data):
    html_questions = []
    for index, row in data.iterrows():
        question_id = f"q{index + 1}"
        question_text = row['Question Text']
        options = [row['Option 1'], row['Option 2'], row['Option 3'], row['Option 4']]
        correct_answer = row['Correct Answer']
        
        # Khởi tạo thẻ <div> chứa câu hỏi
        question_html = f'<div class="question">\n'
        question_html += f'  <h3>Question {index + 1}</h3>\n'
        question_html += f'  <p>{question_text}</p>\n'
        
        # Thêm các lựa chọn (option)
        for i, option in enumerate(options, start=1):
            if pd.notna(option):  # Chỉ thêm các lựa chọn không rỗng
                is_correct = ' class="correct"' if i == correct_answer else ''
                question_html += (
                    f'  <label><br>\n'
                    f'  <input type="radio" name="{question_id}" value="{chr(96 + i)}"{is_correct}>\n'
                    f'  {option}\n'
                    f'  </label><br>\n'
                )
        
        # Đóng thẻ <div>
        question_html += '</div>\n'
        html_questions.append(question_html)
    
    return "\n".join(html_questions)

# Đường dẫn tới tệp Excel
file_path = 'data/listQuiz_XDQLDACNTT _Part2_101-211.xlsx'

# Kiểm tra xem tệp có tồn tại không
if not os.path.exists(file_path):
    print(f"Lỗi: Tệp không tồn tại tại đường dẫn {file_path}")
else:
    try:
        # Đọc dữ liệu từ tệp Excel
        sheet_data = pd.ExcelFile(file_path).parse(0)  # Đọc sheet đầu tiên
        
        # Lọc và chuẩn bị dữ liệu từ các cột cần thiết
        columns_to_keep = ['Question Text', 'Option 1', 'Option 2', 'Option 3', 'Option 4', 'Correct Answer']
        filtered_data = sheet_data[columns_to_keep].dropna(subset=['Question Text', 'Correct Answer'])

        # Đổi giá trị đáp án về số nguyên
        filtered_data['Correct Answer'] = pd.to_numeric(filtered_data['Correct Answer'], errors='coerce')

        # Tạo HTML từ dữ liệu
        html_output = generate_html_from_data(filtered_data)

        # Lưu HTML vào file
        output_file_path = 'quiz_output.html'
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(html_output)

        print(f"HTML được lưu tại: {output_file_path}")
    except Exception as e:
        print(f"Lỗi khi xử lý tệp: {e}")
