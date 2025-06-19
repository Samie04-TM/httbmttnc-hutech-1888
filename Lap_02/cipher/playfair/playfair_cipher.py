class PlayFairCipher:
    def __init__(self) -> None: # Giữ lại một __init__
        pass

    # def __init__(self): # Xóa __init__ trùng lặp
    #     pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace("J", "I")
        matrix_chars = []
        # Thêm các ký tự duy nhất từ khóa (giữ nguyên thứ tự)
        for char_in_key in key:
            if char_in_key not in matrix_chars and char_in_key.isalpha():
                matrix_chars.append(char_in_key)

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ" # Bảng chữ cái không có 'J'
        for letter_in_alphabet in alphabet:
            if letter_in_alphabet not in matrix_chars:
                matrix_chars.append(letter_in_alphabet)
        
        # Đảm bảo matrix_chars có đúng 25 ký tự trước khi tạo ma trận 5x5
        # Logic ở trên nên đảm bảo điều này nếu key và alphabet hợp lệ
        playfair_matrix = [matrix_chars[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for r, row_list in enumerate(matrix):
            if letter in row_list:
                c = row_list.index(letter)
                return r, c
        return None, None # Trả về None nếu không tìm thấy

    # Sửa lỗi thụt lề: playfair_encrypt phải ở cùng cấp với các phương thức khác
    def _preprocess_text(self, text, is_encrypt=True):
        text = text.upper().replace("J", "I")
        # Loại bỏ các ký tự không phải chữ cái
        text = ''.join(filter(str.isalpha, text))
        
        if not is_encrypt: # Đối với giải mã, không cần xử lý X hoặc độ dài
            return text

        # Xử lý cho mã hóa
        processed_text = []
        i = 0
        while i < len(text):
            char1 = text[i]
            processed_text.append(char1)
            if i + 1 < len(text):
                char2 = text[i+1]
                if char1 == char2:
                    processed_text.append('X')
                    # i không tăng, để char1 (của cặp tiếp theo) là char2 hiện tại
                else:
                    processed_text.append(char2)
                    i += 1 # Đã xử lý char2, tăng i
            else: # Ký tự cuối cùng, cần thêm 'X' nếu độ dài là lẻ
                pass # Xử lý độ dài lẻ ở cuối
            i += 1
            
        final_text = "".join(processed_text)
        if len(final_text) % 2 != 0:
            final_text += 'X'
        return final_text

    def playfair_encrypt(self, plain_text, matrix):
        processed_plain_text = self._preprocess_text(plain_text, is_encrypt=True)
        encrypted_text = ""

        if not processed_plain_text:
            return ""

        for i in range(0, len(processed_plain_text), 2):
            pair = processed_plain_text[i:i+2]
            # Đảm bảo cặp luôn có 2 ký tự (đã được xử lý bởi _preprocess_text)
            
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 is None or col1 is None or row2 is None or col2 is None:
                # Điều này không nên xảy ra nếu ma trận và văn bản hợp lệ
                print(f"Lỗi: Ký tự không tìm thấy trong ma trận cho cặp mã hóa: {pair}")
                continue 

            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    # Sửa lỗi thụt lề: playfair_decrypt phải ở cùng cấp với các phương thức khác
    def playfair_decrypt(self, cipher_text, matrix):
        # Ciphertext đã được chuẩn hóa (uppercase, J->I, không có ký tự đặc biệt, độ dài chẵn)
        # bởi quá trình mã hóa đúng cách.
        # Nếu cipher_text đến từ nguồn bên ngoài, cần tiền xử lý tương tự.
        cipher_text = self._preprocess_text(cipher_text, is_encrypt=False) # Chỉ UPPERCASE và J->I
        decrypted_text_chars = []

        if not cipher_text or len(cipher_text) % 2 != 0:
            # print("Lỗi: Ciphertext không hợp lệ để giải mã.")
            return "" # Hoặc raise ValueError

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 is None or col1 is None or row2 is None or col2 is None:
                # print(f"Lỗi: Ký tự không tìm thấy trong ma trận cho cặp giải mã: {pair}")
                continue

            if row1 == row2:
                decrypted_text_chars.append(matrix[row1][(col1 - 1 + 5) % 5])
                decrypted_text_chars.append(matrix[row2][(col2 - 1 + 5) % 5])
            elif col1 == col2:
                decrypted_text_chars.append(matrix[(row1 - 1 + 5) % 5][col1])
                decrypted_text_chars.append(matrix[(row2 - 1 + 5) % 5][col2])
            else:
                decrypted_text_chars.append(matrix[row1][col2])
                decrypted_text_chars.append(matrix[row2][col1])
        
        # Xử lý loại bỏ 'X'
        # Logic này đơn giản hơn: loại bỏ 'X' nếu nó nằm giữa hai ký tự giống hệt nhau
        # và loại bỏ 'X' ở cuối nếu nó là ký tự đệm.
        
        final_decrypted_text = []
        temp_text = "".join(decrypted_text_chars)
        
        i = 0
        while i < len(temp_text):
            char = temp_text[i]
            # Kiểm tra mẫu LXL -> LL
            if char != 'X' and i + 2 < len(temp_text) and temp_text[i+1] == 'X' and temp_text[i+2] == char:
                final_decrypted_text.append(char) # Thêm L
                final_decrypted_text.append(char) # Thêm L thứ hai
                i += 2 # Bỏ qua X và L thứ hai (đã được thêm)
            else:
                final_decrypted_text.append(char)
            i += 1
            
        result = "".join(final_decrypted_text)
        
        # Loại bỏ 'X' không cần thiết (ví dụ: X giữa các ký tự khác nhau, hoặc X cuối làm đệm)
        # Đây là phần phức tạp và phụ thuộc vào quy ước.
        # Một cách tiếp cận đơn giản là loại bỏ 'X' nếu nó không thay đổi ý nghĩa.
        # Ví dụ: "HELXLOXWORLDX" -> "HELLOWORLD"
        # Logic dưới đây cố gắng loại bỏ 'X' nếu nó không phải là một phần của cặp ký tự giống nhau (đã xử lý ở trên)
        # và không phải là ký tự thực sự của thông điệp.
        
        # Tinh chỉnh lại việc loại bỏ X
        # Bỏ qua X nếu nó không phải là ký tự thực sự
        # Ví dụ: nếu có "AXB", X không bị bỏ. Nếu "AXA" đã thành "AA".
        # Nếu "ABXCD", X cuối có thể là đệm.
        
        # Logic đơn giản hóa:
        clean_result_list = []
        idx = 0
        while idx < len(result):
            current_char = result[idx]
            # Xử lý trường hợp LX L (đã được chuyển thành L L X L trong result)
            # hoặc trường hợp X được chèn giữa hai ký tự khác nhau (ít phổ biến hơn)
            # hoặc X ở cuối làm ký tự đệm.
            
            # Nếu ký tự hiện tại là X, kiểm tra xem nó có phải là đệm không
            if current_char == 'X':
                # Nếu X ở cuối cùng
                if idx == len(result) - 1:
                    # Có thể là đệm, không thêm
                    pass
                # Nếu X đứng giữa hai ký tự khác nhau (ví dụ A X B)
                # hoặc X đứng giữa ký tự và cuối (A X)
                # Trong Playfair chuẩn, X thường chỉ được chèn giữa 2 ký tự giống nhau hoặc cuối để làm chẵn.
                # Logic này giả định X không phải là ký tự thực của thông điệp nếu nó không theo quy tắc trên.
                elif idx > 0 and idx < len(result) -1 and result[idx-1] != result[idx+1]:
                     clean_result_list.append(current_char) # Giữ lại X nếu nó có vẻ là ký tự thực
                # Các trường hợp khác (ví dụ X ở đầu, hoặc X mà logic trên không bắt) thì giữ lại
                # Tuy nhiên, với Playfair, X thường không phải là ký tự thực trừ khi nó là một phần của thông điệp gốc.
                # Để đơn giản, nếu X không phải là phần của LXL (đã xử lý) và không phải ở cuối, thì có thể nó là ký tự thực.
                # Logic này cần được kiểm tra kỹ lưỡng với nhiều trường hợp.
                # Hiện tại, chỉ loại bỏ X ở cuối nếu nó là ký tự cuối cùng.
                # Và LXL đã được xử lý.
                else:
                    clean_result_list.append(current_char)


            else: # Không phải X
                clean_result_list.append(current_char)
            idx += 1
            
        final_output = "".join(clean_result_list)
        # Loại bỏ X ở cuối nếu nó là ký tự đệm duy nhất còn sót lại
        if final_output.endswith('X') and len(final_output) % 2 != 0 : # Kiểm tra lại điều kiện này
             # Nếu sau khi xử lý, độ dài vẫn lẻ và kết thúc bằng X, có thể X đó là đệm
             # Tuy nhiên, nếu thông điệp gốc thực sự kết thúc bằng X thì sao?
             # Đây là một điểm khó của Playfair.
             # Giả định: nếu X ở cuối và nó làm cho độ dài tổng thể của các cặp giải mã là lẻ,
             # thì nó có thể là ký tự đệm được thêm vào plaintext ban đầu.
             # Cách an toàn nhất là không tự động xóa X cuối trừ khi có quy tắc rõ ràng.
             # Với logic hiện tại, LXL đã được xử lý.
             # Nếu X cuối cùng không phải là phần của LXL và làm cho độ dài lẻ, có thể bỏ.
             # Ví dụ: HELLOX -> HELLO
             # Nhưng nếu là MEETX -> MEETX (nếu X là ký tự thực)
             # Giữ nguyên X ở cuối nếu nó không rõ ràng là đệm.
             pass


        return final_output