import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import time

class FloydWarshallApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mô phỏng Giải thuật Floyd-Warshall")
        self.root.geometry("1600x900")
        self.root.configure(bg="#2c3e50")
        self.root.state('zoomed')
        
        self.INF = 999
        self.current_step = 0
        self.steps = []
        self.is_running = False
        self.speed = 1000
        self.graph_history = []
        self.current_example_index = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        # Thanh tiêu đề hiện đại
        title_frame = tk.Frame(self.root, bg="#34495e", height=70)
        title_frame.pack(fill=tk.X, pady=(0, 5))
        title_frame.pack_propagate(False)
        
        title_container = tk.Frame(title_frame, bg="#34495e")
        title_container.pack(expand=True)
        
        title_label = tk.Label(title_container, text="🔗 MÔ PHỎNG GIẢI THUẬT FLOYD-WARSHALL",
                               font=("Segoe UI", 22, "bold"), bg="#34495e", fg="#ecf0f1")
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(title_container, text="Tìm đường đi ngắn nhất giữa tất cả các cặp đỉnh",
                                 font=("Segoe UI", 11), bg="#34495e", fg="#bdc3c7")
        subtitle_label.pack()
        
        # Khung chính
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Panel trái - Nhập liệu (Rộng hơn để chứa tất cả nút)
        left_panel = tk.Frame(main_frame, bg="#ecf0f1", relief=tk.FLAT, bd=0, width=340)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8), pady=5)
        left_panel.pack_propagate(False)
        
        # Phần nhập liệu hiện đại
        input_header = tk.Frame(left_panel, bg="#3498db", height=50)
        input_header.pack(fill=tk.X)
        input_header.pack_propagate(False)
        
        input_label = tk.Label(input_header, text="⚙️ THIẾT LẬP MA TRẬN", 
                              font=("Segoe UI", 12, "bold"), bg="#3498db", fg="white")
        input_label.pack(pady=12)
        
        # Nội dung nhập liệu
        input_content = tk.Frame(left_panel, bg="#ecf0f1")
        input_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Số đỉnh
        node_frame = tk.Frame(input_content, bg="#ecf0f1")
        node_frame.pack(pady=(0, 15))
        
        tk.Label(node_frame, text="Số đỉnh:", font=("Segoe UI", 11, "bold"), 
                bg="#ecf0f1", fg="#2c3e50").pack(side=tk.LEFT, padx=(0, 10))
        
        self.node_entry = tk.Entry(node_frame, width=8, font=("Segoe UI", 11),
                                  relief=tk.FLAT, bd=5, bg="white", fg="#2c3e50")
        self.node_entry.insert(0, "4")
        self.node_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        create_btn = tk.Button(node_frame, text="Tạo Ma trận", command=self.create_matrix,
                               bg="#27ae60", fg="white", font=("Segoe UI", 10, "bold"),
                               relief=tk.FLAT, bd=0, padx=15, pady=8, cursor="hand2")
        create_btn.pack(side=tk.LEFT)
        
        # Khung nhập ma trận
        matrix_container = tk.Frame(input_content, bg="#ecf0f1")
        matrix_container.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        self.matrix_frame = tk.Frame(matrix_container, bg="white", relief=tk.FLAT, bd=1)
        self.matrix_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Hướng dẫn hiện đại
        inst_frame = tk.Frame(input_content, bg="#f8f9fa", relief=tk.FLAT, bd=1)
        inst_frame.pack(fill=tk.X, pady=(0, 15))
        
        inst_text = """💡 Hướng dẫn sử dụng:
• Nhập số đỉnh (2-10) và tạo ma trận
• Nhập trọng số cạnh (999 = vô cực)
• Nhấn "▶ Bắt đầu" để mô phỏng
• Cuộn xuống để xem các bước chi tiết"""
        
        inst_label = tk.Label(inst_frame, text=inst_text, 
                             font=("Segoe UI", 9), bg="#f8f9fa", 
                             justify=tk.LEFT, fg="#34495e")
        inst_label.pack(pady=12, padx=12)
        
        # Nút điều khiển hiện đại
        control_frame = tk.Frame(input_content, bg="#ecf0f1")
        control_frame.pack(fill=tk.X)
        
        # Kiểu dáng nút
        btn_style = {
            "font": ("Segoe UI", 9, "bold"),
            "relief": tk.FLAT,
            "bd": 0,
            "padx": 10,
            "pady": 8,
            "cursor": "hand2"
        }
        
        self.start_btn = tk.Button(control_frame, text="▶ Bắt đầu", 
                                   command=self.start_algorithm,
                                   bg="#95a5a6", fg="white", state=tk.DISABLED, **btn_style)
        self.start_btn.pack(fill=tk.X, pady=(0, 3))
        
        self.pause_btn = tk.Button(control_frame, text="⏸ Tạm dừng", 
                                   command=self.pause_algorithm,
                                   bg="#f39c12", fg="white", 
                                   state=tk.DISABLED, **btn_style)
        self.pause_btn.pack(fill=tk.X, pady=(0, 3))
        
        self.next_btn = tk.Button(control_frame, text="⏭ Bước tiếp", 
                                 command=self.next_step,
                                 bg="#3498db", fg="white", 
                                 state=tk.DISABLED, **btn_style)
        self.next_btn.pack(fill=tk.X, pady=(0, 3))
        
        self.reset_btn = tk.Button(control_frame, text="↻ Đặt lại", 
                                   command=self.reset_algorithm,
                                   bg="#e74c3c", fg="white", **btn_style)
        self.reset_btn.pack(fill=tk.X, pady=(0, 12))
        
        # Điều khiển tốc độ hiện đại
        speed_frame = tk.Frame(input_content, bg="#f8f9fa", relief=tk.FLAT, bd=1)
        speed_frame.pack(fill=tk.X)
        
        tk.Label(speed_frame, text="⚡ Tốc độ mô phỏng:", font=("Segoe UI", 10, "bold"), 
                bg="#f8f9fa", fg="#2c3e50").pack(pady=(10, 5))
        
        self.speed_scale = tk.Scale(speed_frame, from_=100, to=2000, 
                                    orient=tk.HORIZONTAL, length=250,
                                    command=self.update_speed, bg="#f8f9fa",
                                    font=("Segoe UI", 9), fg="#2c3e50")
        self.speed_scale.set(1000)
        self.speed_scale.pack(pady=(0, 10))
        
        # Panel giữa - Hiển thị có thể cuộn hiện đại
        middle_panel = tk.Frame(main_frame, bg="white", relief=tk.FLAT, bd=0)
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=5)
        
        # Tạo canvas chính có thể cuộn dọc
        main_canvas = tk.Canvas(middle_panel, bg="white", highlightthickness=0)
        main_scrollbar = tk.Scrollbar(middle_panel, orient=tk.VERTICAL, command=main_canvas.yview,
                                     bg="#bdc3c7", troughcolor="#ecf0f1", width=12)
        self.scrollable_frame = tk.Frame(main_canvas, bg="white")
        
        # Đóng gói scrollbar và canvas
        main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Tạo cửa sổ trong canvas
        main_canvas_window = main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Cấu hình cuộn
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        def configure_scroll_region(event=None):
            main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        
        def configure_main_canvas(event):
            canvas_width = event.width
            main_canvas.itemconfig(main_canvas_window, width=canvas_width)
        
        self.scrollable_frame.bind("<Configure>", configure_scroll_region)
        main_canvas.bind("<Configure>", configure_main_canvas)
        
        # Liên kết con lăn chuột
        def on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def bind_mousewheel(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel(child)
        
        main_canvas.bind("<MouseWheel>", on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", on_mousewheel)
        middle_panel.bind("<MouseWheel>", on_mousewheel)
        
        def bind_to_mousewheel(event):
            bind_mousewheel(event.widget)
        
        self.scrollable_frame.bind("<Map>", bind_to_mousewheel)
        
        # === PHẦN 1: ĐỒ THỊ CHÍNH ===
        graph_header = tk.Frame(self.scrollable_frame, bg="#2980b9", height=50)
        graph_header.pack(fill=tk.X, pady=(0, 10))
        graph_header.pack_propagate(False)
        
        vis_label = tk.Label(graph_header, text="📊 ĐỒ THỊ HIỆN TẠI", 
                            font=("Segoe UI", 14, "bold"), bg="#2980b9", fg="white")
        vis_label.pack(pady=12)
        
        graph_container = tk.Frame(self.scrollable_frame, bg="#ecf0f1", relief=tk.FLAT, bd=2)
        graph_container.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        self.canvas_frame = tk.Frame(graph_container, bg="white", height=450)
        self.canvas_frame.pack(fill=tk.X, padx=5, pady=5)
        self.canvas_frame.pack_propagate(False)
        
        # === PHẦN 2: CÁC BƯỚC GIẢI CHI TIẾT ===
        separator = tk.Frame(self.scrollable_frame, height=4, bg="#e67e22")
        separator.pack(fill=tk.X, padx=20, pady=15)
        
        steps_header_frame = tk.Frame(self.scrollable_frame, bg="#e67e22", height=60)
        steps_header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        steps_header_frame.pack_propagate(False)
        
        steps_content = tk.Frame(steps_header_frame, bg="#e67e22")
        steps_content.pack(expand=True)
        
        steps_label = tk.Label(steps_content, text="🔍 CÁC BƯỚC GIẢI CHI TIẾT", 
                              font=("Segoe UI", 14, "bold"), bg="#e67e22", fg="white")
        steps_label.pack(side=tk.LEFT, pady=15, padx=20)
        
        scroll_btn = tk.Button(steps_content, text="👇 Cuộn xuống xem chi tiết", 
                              command=self.scroll_to_steps,
                              bg="#d35400", fg="white", font=("Segoe UI", 10, "bold"),
                              relief=tk.FLAT, bd=0, padx=15, pady=8, cursor="hand2")
        scroll_btn.pack(side=tk.RIGHT, pady=15, padx=20)
        
        self.steps_container = tk.Frame(self.scrollable_frame, bg="white")
        self.steps_container.pack(fill=tk.X, padx=10, pady=(0, 20))
        
        initial_container = tk.Frame(self.steps_container, bg="#f8f9fa", relief=tk.FLAT, bd=1)
        initial_container.pack(fill=tk.X, padx=20, pady=20)
        
        self.initial_message = tk.Label(initial_container, 
                                       text="🚀 Nhấn 'Bắt đầu' để xem các bước giải chi tiết...",
                                       font=("Segoe UI", 12), bg="#f8f9fa", fg="#7f8c8d",
                                       pady=30)
        self.initial_message.pack()
        
        self.main_canvas = main_canvas
        
        # Panel phải - Hiển thị Log và Ma trận hiện đại
        right_panel = tk.Frame(main_frame, bg="#ecf0f1", relief=tk.FLAT, bd=0, width=420)
        right_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(8, 0), pady=5)
        right_panel.pack_propagate(False)
        
        # Hiển thị ma trận hiện đại
        matrix_header = tk.Frame(right_panel, bg="#8e44ad", height=45)
        matrix_header.pack(fill=tk.X)
        matrix_header.pack_propagate(False)
        
        matrix_label = tk.Label(matrix_header, text="📋 MA TRẬN HIỆN TẠI", 
                               font=("Segoe UI", 11, "bold"), bg="#8e44ad", fg="white")
        matrix_label.pack(pady=10)
        
        matrix_container = tk.Frame(right_panel, bg="white", relief=tk.FLAT, bd=1)
        matrix_container.pack(fill=tk.X, padx=8, pady=(0, 8))
        
        self.matrix_display = tk.Text(matrix_container, width=38, height=10, 
                                      font=("Consolas", 9), bg="white", fg="#2c3e50",
                                      relief=tk.FLAT, bd=0, padx=8, pady=8)
        self.matrix_display.pack(fill=tk.X, padx=4, pady=4)
        
        # Hiển thị đường đi ngắn nhất
        paths_header = tk.Frame(right_panel, bg="#e67e22", height=45)
        paths_header.pack(fill=tk.X, pady=(8, 0))
        paths_header.pack_propagate(False)
        
        paths_label = tk.Label(paths_header, text="🛤️ ĐƯỜNG ĐI NGẮN NHẤT", 
                              font=("Segoe UI", 11, "bold"), bg="#e67e22", fg="white")
        paths_label.pack(pady=10)
        
        paths_container = tk.Frame(right_panel, bg="white", relief=tk.FLAT, bd=1)
        paths_container.pack(fill=tk.X, padx=8, pady=(0, 8))
        
        self.paths_display = scrolledtext.ScrolledText(paths_container, width=38, height=7, 
                                                       font=("Consolas", 8), bg="white", fg="#2c3e50",
                                                       relief=tk.FLAT, bd=0, padx=8, pady=8)
        self.paths_display.pack(fill=tk.X, padx=4, pady=4)
        
        # Hiển thị log hiện đại
        log_header = tk.Frame(right_panel, bg="#16a085", height=45)
        log_header.pack(fill=tk.X)
        log_header.pack_propagate(False)
        
        log_label = tk.Label(log_header, text="📝 NHẬT KÝ THỰC HIỆN", 
                            font=("Segoe UI", 11, "bold"), bg="#16a085", fg="white")
        log_label.pack(pady=10)
        
        log_container = tk.Frame(right_panel, bg="white", relief=tk.FLAT, bd=1)
        log_container.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        
        self.log_text = scrolledtext.ScrolledText(log_container, width=38, height=15, 
                                                  font=("Consolas", 8), bg="white", fg="#2c3e50",
                                                  relief=tk.FLAT, bd=0, padx=8, pady=8)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        
        # Thanh trạng thái hiện đại
        self.status_label = tk.Label(self.root, text="🟢 Sẵn sàng", 
                                     font=("Segoe UI", 10, "bold"), bg="#34495e", 
                                     fg="#ecf0f1", anchor=tk.W, padx=15, height=2)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Tạo ma trận ban đầu
        self.create_matrix()
    def create_matrix(self):
        try:
            n = int(self.node_entry.get())
            if n < 2 or n > 10:
                messagebox.showerror("Lỗi", "Số đỉnh phải từ 2 đến 10!")
                return
            
            self.current_example_index = 0
                
            # Xóa ma trận trước đó
            for widget in self.matrix_frame.winfo_children():
                widget.destroy()
            
            self.matrix_entries = []
            
            # Tạo tiêu đề
            tk.Label(self.matrix_frame, text="", width=3, bg="white").grid(row=0, column=0)
            for j in range(n):
                tk.Label(self.matrix_frame, text=str(j), width=6, 
                        font=("Segoe UI", 10, "bold"), bg="white", fg="#2c3e50").grid(row=0, column=j+1)
            
            # Tạo các ô nhập ma trận
            for i in range(n):
                tk.Label(self.matrix_frame, text=str(i), width=3, 
                        font=("Segoe UI", 10, "bold"), bg="white", fg="#2c3e50").grid(row=i+1, column=0)
                row_entries = []
                for j in range(n):
                    entry = tk.Entry(self.matrix_frame, width=6, font=("Segoe UI", 10),
                                   justify=tk.CENTER, relief=tk.FLAT, bd=2)
                    if i == j:
                        entry.insert(0, "0")
                        entry.config(state=tk.DISABLED, bg="#ecf0f1", fg="#7f8c8d")
                    else:
                        entry.insert(0, str(self.INF))
                        entry.config(bg="white", fg="#2c3e50")
                        entry.bind('<KeyRelease>', self.on_matrix_change)
                        entry.bind('<FocusOut>', self.on_matrix_change)
                    entry.grid(row=i+1, column=j+1, padx=3, pady=3)
                    row_entries.append(entry)
                self.matrix_entries.append(row_entries)
            
            # Nút tải ví dụ
            example_btn = tk.Button(self.matrix_frame, text="🎯 Tạo đồ thị mẫu", 
                                   command=self.load_example,
                                   bg="#9b59b6", fg="white", 
                                   font=("Segoe UI", 9, "bold"), 
                                   relief=tk.FLAT, bd=0, padx=15, pady=8, cursor="hand2")
            example_btn.grid(row=n+1, column=0, columnspan=n+1, pady=15)
            
            self.log_message(f"Đã tạo ma trận {n}x{n}")
            self.draw_initial_placeholder()
            self.update_start_button_state()
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên hợp lệ!")
    
    def on_matrix_change(self, event=None):
        self.update_start_button_state()
    
    def update_start_button_state(self):
        try:
            if not hasattr(self, 'matrix_entries') or not self.matrix_entries:
                self.start_btn.config(state=tk.DISABLED, bg="#95a5a6")
                return
            
            has_valid_edge = False
            n = len(self.matrix_entries)
            
            for i in range(n):
                for j in range(n):
                    if i != j:
                        try:
                            value_str = self.matrix_entries[i][j].get().strip()
                            if value_str and value_str != str(self.INF):
                                value = int(value_str)
                                if value < self.INF:
                                    has_valid_edge = True
                                    break
                        except:
                            continue
                if has_valid_edge:
                    break
            
            if has_valid_edge and not self.is_running:
                self.start_btn.config(state=tk.NORMAL, bg="#27ae60")
            else:
                self.start_btn.config(state=tk.DISABLED, bg="#95a5a6")
                
        except Exception as e:
            print(f"Error updating start button state: {e}")
            self.start_btn.config(state=tk.DISABLED, bg="#95a5a6")
    
    def load_example(self):
        try:
            import random
            
            n = len(self.matrix_entries)
            if n < 2:
                messagebox.showinfo("Thông báo", "Cần tạo ma trận trước!")
                return
            
            # Xóa ma trận hiện tại
            for i in range(n):
                for j in range(n):
                    if i != j:
                        self.matrix_entries[i][j].delete(0, tk.END)
            
            # Các dạng đồ thị khác nhau
            graph_types = [
                "complete", "cycle", "path", "star", "negative_cycle", "random"
            ]
            
            graph_type = graph_types[self.current_example_index % len(graph_types)]
            matrix = self.create_graph_by_type(n, graph_type)
            
            if not matrix or len(matrix) != n:
                raise Exception("Ma trận không hợp lệ")
            
            # Cập nhật giao diện
            for i in range(n):
                for j in range(n):
                    if i != j:
                        value = matrix[i][j] if matrix[i][j] != self.INF else self.INF
                        self.matrix_entries[i][j].insert(0, str(value))
            
            self.current_example_index += 1
            graph_name = self.get_graph_type_name(graph_type)
            self.log_message(f"Đã tạo đồ thị {graph_name} #{self.current_example_index} cho {n} đỉnh")
            
            self.root.after(100, self.update_display_after_load)
            
        except Exception as e:
            print(f"Error in load_example: {e}")
            self.log_message(f"Lỗi khi tạo đồ thị: {e}")
            self.create_simple_fallback_graph()
    
    def update_display_after_load(self):
        try:
            matrix_data = self.get_matrix()
            if matrix_data:
                n = len(matrix_data)
                self.draw_graph(np.array(matrix_data), -1, -1, -1)
                self.update_matrix_display(np.array(matrix_data), -1, -1, -1)
                
                next_matrix = np.full((n, n), -1, dtype=int)
                for i in range(n):
                    for j in range(n):
                        if i != j and matrix_data[i][j] < self.INF:
                            next_matrix[i][j] = j
                self.update_paths_display(np.array(matrix_data), next_matrix)
            
            self.update_start_button_state()
            
        except Exception as e:
            print(f"Error updating display: {e}")
            self.create_simple_fallback_graph()
    
    def create_simple_fallback_graph(self):
        try:
            import random
            n = len(self.matrix_entries)
            
            for i in range(n):
                for j in range(n):
                    if i != j:
                        self.matrix_entries[i][j].delete(0, tk.END)
            
            for i in range(n):
                for j in range(n):
                    if i != j:
                        if j == (i + 1) % n:
                            weight = random.randint(1, 8)
                            self.matrix_entries[i][j].insert(0, str(weight))
                        elif random.random() < 0.3:
                            weight = random.randint(1, 12)
                            self.matrix_entries[i][j].insert(0, str(weight))
                        else:
                            self.matrix_entries[i][j].insert(0, str(self.INF))
            
            self.log_message("Đã tạo đồ thị đơn giản (fallback)")
            self.root.after(100, self.update_display_after_load)
            
        except Exception as e:
            print(f"Error in fallback: {e}")
            self.log_message("Lỗi khi tạo đồ thị fallback")
    
    def create_graph_by_type(self, n, graph_type):
        try:
            import random
            
            matrix = [[self.INF if i != j else 0 for j in range(n)] for i in range(n)]
            
            if graph_type == "complete":
                for i in range(n):
                    for j in range(n):
                        if i != j:
                            matrix[i][j] = random.randint(1, 10)
            
            elif graph_type == "cycle":
                for i in range(n):
                    next_vertex = (i + 1) % n
                    matrix[i][next_vertex] = random.randint(1, 8)
                    if random.random() < 0.4:
                        matrix[next_vertex][i] = random.randint(1, 8)
                for _ in range(min(2, n // 2)):
                    i, j = random.sample(range(n), 2)
                    matrix[i][j] = random.randint(5, 12)
            
            elif graph_type == "path":
                for i in range(n - 1):
                    matrix[i][i + 1] = random.randint(1, 6)
                    if random.random() < 0.5:
                        matrix[i + 1][i] = random.randint(1, 6)
                for _ in range(min(2, n // 2)):
                    i, j = random.sample(range(n), 2)
                    if abs(i - j) > 1:
                        matrix[i][j] = random.randint(8, 15)
            
            elif graph_type == "star":
                center = 0
                for i in range(1, n):
                    matrix[center][i] = random.randint(1, 5)
                    matrix[i][center] = random.randint(1, 5)
                if n > 3:
                    for _ in range(min(2, n // 3)):
                        i, j = random.sample(range(1, n), 2)
                        matrix[i][j] = random.randint(6, 12)
            
            elif graph_type == "negative_cycle":
                # Tạo chu trình cơ bản
                for i in range(n - 1):
                    matrix[i][i + 1] = random.randint(1, 5)
                matrix[n - 1][0] = random.randint(1, 5)
                
                # Thêm chu trình âm
                if n >= 3:
                    matrix[0][1] = 5
                    matrix[1][2] = 3
                    matrix[2][0] = -10  # Chu trình âm
                
                for _ in range(min(2, n // 2)):
                    i, j = random.sample(range(n), 2)
                    if matrix[i][j] == self.INF:
                        matrix[i][j] = random.randint(1, 8)
            
            else:  # random
                edge_probability = 0.4
                for i in range(n):
                    for j in range(n):
                        if i != j and random.random() < edge_probability:
                            matrix[i][j] = random.randint(1, 12)
            
            if graph_type != "negative_cycle":
                self.ensure_connectivity(matrix, n)
            
            return matrix
            
        except Exception as e:
            print(f"Error creating graph: {e}")
            import random
            matrix = [[self.INF if i != j else 0 for j in range(n)] for i in range(n)]
            for i in range(n - 1):
                matrix[i][i + 1] = random.randint(1, 8)
            return matrix
    
    def ensure_connectivity(self, matrix, n):
        import random
        for i in range(n - 1):
            if matrix[i][i + 1] == self.INF and matrix[i + 1][i] == self.INF:
                matrix[i][i + 1] = random.randint(1, 8)
    
    def get_graph_type_name(self, graph_type):
        names = {
            "complete": "Đầy đủ",
            "cycle": "Chu trình", 
            "path": "Đường đi",
            "star": "Hình sao",
            "negative_cycle": "Chu trình âm (Test)",
            "random": "Ngẫu nhiên"
        }
        return names.get(graph_type, "Ngẫu nhiên")
    
    def get_matrix(self):
        if not hasattr(self, 'matrix_entries') or not self.matrix_entries:
            messagebox.showwarning("Cảnh báo", "Vui lòng tạo ma trận trước!")
            return None
            
        n = len(self.matrix_entries)
        matrix = []
        try:
            for i in range(n):
                row = []
                for j in range(n):
                    value_str = self.matrix_entries[i][j].get().strip()
                    if not value_str:
                        messagebox.showerror("Lỗi", f"Ô [{i}][{j}] không được để trống!")
                        return None
                    
                    try:
                        value = int(value_str)
                        row.append(value)
                    except ValueError:
                        messagebox.showerror("Lỗi", f"Giá trị tại [{i}][{j}] phải là số nguyên!\nGiá trị hiện tại: '{value_str}'")
                        return None
                        
                matrix.append(row)
            return matrix
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi khi đọc ma trận: {str(e)}")
            return None
    def start_algorithm(self):
        if not hasattr(self, 'matrix_entries') or not self.matrix_entries:
            messagebox.showwarning("Cảnh báo", "Vui lòng tạo ma trận trước khi bắt đầu!")
            return
        
        matrix = self.get_matrix()
        if matrix is None:
            return
        
        if not self.validate_matrix(matrix):
            return
        
        self.steps = []
        self.current_step = 0
        self.compute_floyd_warshall(matrix)
        
        if len(self.steps) > 0:
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.DISABLED)
            self.log_message("Bắt đầu mô phỏng giải thuật Floyd-Warshall")
            self.run_next_step()
    
    def validate_matrix(self, matrix):
        n = len(matrix)
        
        for row in matrix:
            if len(row) != n:
                messagebox.showerror("Lỗi", "Ma trận phải là ma trận vuông!")
                return False
        
        for i in range(n):
            if matrix[i][i] != 0:
                messagebox.showerror("Lỗi", f"Phần tử d[{i}][{i}] phải bằng 0!")
                return False
        
        has_edge = False
        for i in range(n):
            for j in range(n):
                if i != j and matrix[i][j] < self.INF:
                    has_edge = True
                    break
            if has_edge:
                break
        
        if not has_edge:
            messagebox.showwarning("Cảnh báo", 
                                 "Đồ thị không có cạnh nào! Vui lòng nhập ít nhất một cạnh hoặc tạo ví dụ ngẫu nhiên.")
            return False
        
        return True
    
    def compute_floyd_warshall(self, graph):
        n = len(graph)
        dist = np.array(graph, dtype=float)
        next_node = np.full((n, n), -1, dtype=int)
        
        # Khởi tạo ma trận next_node
        for i in range(n):
            for j in range(n):
                if i != j and dist[i][j] < self.INF:
                    next_node[i][j] = j
        
        # Trạng thái ban đầu
        self.steps.append({
            'matrix': dist.copy(),
            'next_matrix': next_node.copy(),
            'k': -1, 'i': -1, 'j': -1,
            'message': 'Khởi tạo ma trận ban đầu D⁰',
            'explanation': 'Ma trận ban đầu chứa khoảng cách trực tiếp giữa các đỉnh. Nếu không có cạnh trực tiếp thì giá trị là ∞.',
            'updated': False,
            'negative_cycle': False
        })
        
        algorithm_stopped = False
        negative_cycle_detected = False
        
        for k in range(n):
            if algorithm_stopped:
                break
            
            # Thêm bước bắt đầu xét đỉnh k
            self.steps.append({
                'matrix': dist.copy(),
                'next_matrix': next_node.copy(),
                'k': k, 'i': -1, 'j': -1,
                'message': f'Bắt đầu xét đỉnh trung gian k = {k}',
                'explanation': f'Xét đỉnh {k} làm đỉnh trung gian. Kiểm tra xem có thể cải thiện đường đi từ i đến j bằng cách đi qua đỉnh {k} không.',
                'updated': False,
                'negative_cycle': False
            })
                
            # Thực hiện các cập nhật cho k hiện tại
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        old_value = dist[i][j]
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_node[i][j] = next_node[i][k]
                        
                        # Tạo giải thích chi tiết cho việc cập nhật
                        if old_value >= self.INF:
                            explanation = f'Tìm thấy đường đi mới từ {i} đến {j} qua đỉnh {k}:\n' \
                                        f'• Trước: không có đường đi (∞)\n' \
                                        f'• Qua đỉnh {k}: {dist[i][k]:.0f} + {dist[k][j]:.0f} = {dist[i][j]:.0f}\n' \
                                        f'• Kết quả: cập nhật d[{i}][{j}] = {dist[i][j]:.0f}'
                        else:
                            explanation = f'Cải thiện đường đi từ {i} đến {j} qua đỉnh {k}:\n' \
                                        f'• Đường đi cũ: {old_value:.0f}\n' \
                                        f'• Qua đỉnh {k}: {dist[i][k]:.0f} + {dist[k][j]:.0f} = {dist[i][j]:.0f}\n' \
                                        f'• So sánh: {dist[i][j]:.0f} < {old_value:.0f} ✓\n' \
                                        f'• Kết quả: cập nhật d[{i}][{j}] = {dist[i][j]:.0f}'
                        
                        self.steps.append({
                            'matrix': dist.copy(),
                            'next_matrix': next_node.copy(),
                            'k': k, 'i': i, 'j': j,
                            'message': f'Cập nhật d[{i}][{j}] qua đỉnh {k}: {old_value:.0f} → {dist[i][j]:.0f}',
                            'explanation': explanation,
                            'updated': True,
                            'negative_cycle': False
                        })
            
            # Thêm bước tổng kết sau khi xét xong đỉnh k
            self.steps.append({
                'matrix': dist.copy(),
                'next_matrix': next_node.copy(),
                'k': k, 'i': -1, 'j': -1,
                'message': f'Hoàn thành xét đỉnh trung gian k = {k}',
                'explanation': f'Đã kiểm tra tất cả các cặp đỉnh (i,j) với đỉnh trung gian k = {k}. ' \
                             f'Ma trận hiện tại chứa đường đi ngắn nhất qua các đỉnh từ 0 đến {k}.',
                'updated': False,
                'negative_cycle': False
            })
            
            # Kiểm tra chu trình âm sau mỗi bước lặp k
            negative_cycle_vertices = []
            for i in range(n):
                if dist[i][i] < 0:
                    negative_cycle_vertices.append(i)
            
            if negative_cycle_vertices and not negative_cycle_detected:
                negative_cycle_detected = True
                
                warning_message = f'⚠️ PHÁT HIỆN CHU TRÌNH ÂM sau bước k={k}!\nCác đỉnh: {negative_cycle_vertices}\nKết quả sẽ không còn chính xác.'
                warning_explanation = f'Phát hiện chu trình âm tại các đỉnh {negative_cycle_vertices}!\n\n' \
                                    f'Chu trình âm là một chu trình mà tổng trọng số các cạnh < 0.\n' \
                                    f'Khi có chu trình âm, ta có thể đi vòng vô hạn để giảm khoảng cách.\n\n' \
                                    f'Điều này làm cho khái niệm "đường đi ngắn nhất" không còn ý nghĩa.\n' \
                                    f'Thuật toán Floyd-Warshall không thể xử lý đồ thị có chu trình âm.'
                
                self.steps.append({
                    'matrix': dist.copy(),
                    'next_matrix': next_node.copy(),
                    'k': k, 'i': -1, 'j': -1,
                    'message': warning_message,
                    'explanation': warning_explanation,
                    'updated': False,
                    'negative_cycle': True,
                    'affected_vertices': negative_cycle_vertices,
                    'requires_user_decision': True
                })
                
                # Đảm bảo cửa sổ chính không che messagebox
                self.root.update()
                self.root.lift()
                self.root.attributes('-topmost', False)
                
                try:
                    user_choice = messagebox.askyesno(
                        "Phát hiện chu trình âm", 
                        f"Phát hiện chu trình âm tại các đỉnh: {negative_cycle_vertices}\n"
                        f"sau khi xử lý đỉnh trung gian k={k}.\n\n"
                        f"Kết quả sẽ không còn chính xác nếu tiếp tục.\n\n"
                        f"Bạn có muốn tiếp tục các bước còn lại không?",
                        icon='warning',
                        parent=self.root
                    )
                except Exception as e:
                    print(f"Error showing messagebox: {e}")
                    user_choice = False
                
                if not user_choice:
                    algorithm_stopped = True
                    self.steps.append({
                        'matrix': dist.copy(),
                        'next_matrix': next_node.copy(),
                        'k': k, 'i': -1, 'j': -1,
                        'message': f'🛑 Thuật toán đã dừng theo yêu cầu người dùng tại k={k}',
                        'explanation': f'Người dùng đã chọn dừng thuật toán tại bước k={k} do phát hiện chu trình âm.\n\n' \
                                     f'Đây là quyết định đúng đắn vì:\n' \
                                     f'• Chu trình âm làm cho kết quả không chính xác\n' \
                                     f'• Tiếp tục sẽ tạo ra các giá trị âm vô cực (-∞)\n' \
                                     f'• Ma trận hiện tại vẫn chứa thông tin hữu ích về đường đi ngắn nhất',
                        'updated': False,
                        'negative_cycle': True,
                        'algorithm_stopped': True
                    })
                    break
                else:
                    self.steps.append({
                        'matrix': dist.copy(),
                        'next_matrix': next_node.copy(),
                        'k': k, 'i': -1, 'j': -1,
                        'message': f'▶️ Tiếp tục thuật toán (kết quả có thể không chính xác)',
                        'explanation': f'Người dùng đã chọn tiếp tục thuật toán mặc dù có chu trình âm.\n\n' \
                                     f'Lưu ý:\n' \
                                     f'• Kết quả có thể không chính xác\n' \
                                     f'• Một số khoảng cách có thể trở thành -∞\n' \
                                     f'• Đây chỉ nên dùng cho mục đích học tập và quan sát',
                        'updated': False,
                        'negative_cycle': True,
                        'user_continued': True
                    })
        
        # Trạng thái cuối
        if algorithm_stopped:
            final_message = f'Thuật toán đã dừng sớm do chu trình âm'
            final_explanation = f'Thuật toán Floyd-Warshall đã dừng sớm do phát hiện chu trình âm.\n\n' \
                              f'Kết quả hiện tại:\n' \
                              f'• Ma trận chứa đường đi ngắn nhất đã tính được\n' \
                              f'• Các giá trị này vẫn chính xác cho các cặp đỉnh không bị ảnh hưởng\n' \
                              f'• Chu trình âm làm cho một số đường đi không có ý nghĩa'
        else:
            final_negative_vertices = [i for i in range(n) if dist[i][i] < 0]
            if final_negative_vertices:
                final_message = f'Hoàn thành với chu trình âm tại các đỉnh: {final_negative_vertices}'
                final_explanation = f'Thuật toán đã hoàn thành nhưng phát hiện chu trình âm.\n\n' \
                                  f'Kết quả:\n' \
                                  f'• Một số khoảng cách có giá trị -∞\n' \
                                  f'• Điều này có nghĩa là có thể giảm khoảng cách vô hạn\n' \
                                  f'• Ma trận không thể hiện đường đi ngắn nhất thực sự\n\n' \
                                  f'📝 Lưu ý quan trọng:\n' \
                                  f'• Chu trình âm làm cho bài toán đường đi ngắn nhất không có nghiệm\n' \
                                  f'• Trong thực tế, cần kiểm tra và loại bỏ chu trình âm trước khi áp dụng thuật toán\n' \
                                  f'• Kết quả hiện tại chỉ mang tính chất minh họa cho mục đích học tập'
                
                for k in range(n):
                    for i in range(n):
                        for j in range(n):
                            if dist[i][k] + dist[k][j] < dist[i][j]:
                                dist[i][j] = float('-inf')
            else:
                final_message = 'Hoàn thành! Ma trận đường đi ngắn nhất'
                final_explanation = f'Thuật toán Floyd-Warshall đã hoàn thành thành công!\n\n' \
                                  f'Kết quả:\n' \
                                  f'• Ma trận D chứa khoảng cách ngắn nhất giữa mọi cặp đỉnh\n' \
                                  f'• Độ phức tạp: O(V³) với V = {n} đỉnh\n' \
                                  f'• Đã thực hiện {n} vòng lặp chính (k từ 0 đến {n-1})\n' \
                                  f'• Mỗi vòng lặp kiểm tra {n}×{n} = {n*n} cặp đỉnh'
        
        self.steps.append({
            'matrix': dist.copy(),
            'next_matrix': next_node.copy(),
            'k': -1, 'i': -1, 'j': -1,
            'message': final_message,
            'explanation': final_explanation,
            'updated': False,
            'negative_cycle': any(dist[i][i] < 0 for i in range(n)),
            'algorithm_stopped': algorithm_stopped
        })
    
    def get_path(self, next_matrix, start, end):
        if next_matrix[start][end] == -1:
            return []
        
        path = [start]
        current = start
        while current != end:
            current = next_matrix[current][end]
            if current == -1:
                return []
            path.append(current)
        return path
    
    def update_paths_display(self, matrix, next_matrix):
        self.paths_display.delete(1.0, tk.END)
        n = len(matrix)
        
        # Kiểm tra chu trình âm
        has_negative_cycle = any(matrix[i][i] < 0 for i in range(n))
        
        if has_negative_cycle:
            self.paths_display.insert(tk.END, "⚠️ CẢNH BÁO CHU TRÌNH ÂM!\n")
            self.paths_display.insert(tk.END, "=" * 45 + "\n\n")
            
            negative_vertices = []
            for i in range(n):
                if matrix[i][i] < 0:
                    negative_vertices.append(i)
            
            self.paths_display.insert(tk.END, f"Các đỉnh có chu trình âm: {negative_vertices}\n\n")
            
            start_idx = "1.0"
            end_idx = "3.0"
            self.paths_display.tag_add("warning", start_idx, end_idx)
            self.paths_display.tag_config("warning", foreground="#e74c3c", font=("Consolas", 10, "bold"))
            
            self.paths_display.insert(tk.END, "Một số khoảng cách có thể là -∞\n")
            self.paths_display.insert(tk.END, "do ảnh hưởng của chu trình âm.")
            
        else:
            self.paths_display.insert(tk.END, "ĐƯỜNG ĐI NGẮN NHẤT XA NHẤT:\n")
            self.paths_display.insert(tk.END, "=" * 45 + "\n\n")
            
            max_distance = -1
            best_start = -1
            best_end = -1
            best_path = []
            
            for i in range(n):
                for j in range(n):
                    if i != j and matrix[i][j] < self.INF and matrix[i][j] != float('-inf'):
                        if matrix[i][j] > max_distance:
                            max_distance = matrix[i][j]
                            best_start = i
                            best_end = j
                            best_path = self.get_path(next_matrix, i, j)
            
            if best_start != -1 and best_end != -1:
                self.paths_display.insert(tk.END, f"Đường đi xa nhất trong đồ thị:\n")
                self.paths_display.insert(tk.END, f"Từ đỉnh {best_start} đến đỉnh {best_end}: ")
                
                start_idx = self.paths_display.index(tk.END)
                self.paths_display.insert(tk.END, f"[{int(max_distance)}] ")
                end_idx = self.paths_display.index(tk.END)
                self.paths_display.tag_add("distance", start_idx, end_idx)
                self.paths_display.tag_config("distance", foreground="#e74c3c", font=("Consolas", 10, "bold"))
                
                if best_path and len(best_path) > 1:
                    path_str = " → ".join(map(str, best_path))
                    self.paths_display.insert(tk.END, f"\n{path_str}\n\n")
                else:
                    self.paths_display.insert(tk.END, "\nTrực tiếp\n\n")
            else:
                self.paths_display.insert(tk.END, "Không có đường đi nào trong đồ thị.")
        
        self.paths_display.see(tk.END)
    def run_next_step(self):
        if not self.is_running or self.current_step >= len(self.steps):
            self.pause_algorithm()
            if self.current_step >= len(self.steps):
                self.status_label.config(text="Hoàn thành!")
                messagebox.showinfo("Hoàn thành", "Giải thuật đã hoàn thành!")
            return
        
        self.display_step(self.current_step)
        self.current_step += 1
        
        self.root.after(self.speed, self.run_next_step)
    
    def next_step(self):
        if self.current_step < len(self.steps):
            self.display_step(self.current_step)
            self.current_step += 1
        
        if self.current_step >= len(self.steps):
            self.status_label.config(text="Hoàn thành!")
            messagebox.showinfo("Hoàn thành", "Giải thuật đã hoàn thành!")
    
    def display_step(self, step_idx):
        if step_idx >= len(self.steps):
            return
        
        step = self.steps[step_idx]
        
        # Update status với màu sắc khác nhau
        if step.get('negative_cycle', False):
            if step.get('requires_user_decision', False):
                status_text = f"⚠️ Bước {step_idx + 1}: CẢNH BÁO CHU TRÌNH ÂM!"
                self.status_label.config(text=status_text, bg="#e74c3c", fg="white")
            elif step.get('algorithm_stopped', False):
                status_text = f"🛑 Bước {step_idx + 1}: THUẬT TOÁN ĐÃ DỪNG"
                self.status_label.config(text=status_text, bg="#8b0000", fg="white")
            elif step.get('user_continued', False):
                status_text = f"▶️ Bước {step_idx + 1}: TIẾP TỤC THỰC HIỆN"
                self.status_label.config(text=status_text, bg="#f39c12", fg="white")
            else:
                status_text = f"⚠️ Bước {step_idx + 1}: {step['message']}"
                self.status_label.config(text=status_text, bg="#e67e22", fg="white")
        else:
            status_text = f"Bước {step_idx + 1}: {step['message']}"
            self.status_label.config(text=status_text, bg="#34495e", fg="#ecf0f1")
        
        # Log message
        if step.get('negative_cycle', False):
            self.log_message(f"[Bước {step_idx + 1}] ⚠️ {step['message']}")
        else:
            self.log_message(f"[Bước {step_idx + 1}] {step['message']}")
        
        # Kiểm tra nếu đây là bước cuối và có chu trình âm
        if (step_idx == len(self.steps) - 1 and 
            any(step['matrix'][i][i] < 0 for i in range(len(step['matrix'])))):
            self.log_message("=" * 50)
            self.log_message("📝 KẾT LUẬN VỀ CHU TRÌNH ÂM:")
            self.log_message("• Đồ thị chứa chu trình âm - không có đường đi ngắn nhất")
            self.log_message("• Kết quả chỉ mang tính chất minh họa")
            self.log_message("• Trong thực tế cần loại bỏ chu trình âm trước")
            self.log_message("=" * 50)
        
        # Cập nhật hiển thị
        self.update_matrix_display(step['matrix'], step['i'], step['j'], step['k'])
        
        if 'next_matrix' in step:
            self.update_paths_display(step['matrix'], step['next_matrix'])
        
        self.draw_graph(step['matrix'], step['k'], step['i'], step['j'])
        self.add_step_detail(step_idx, step)
    
    def update_matrix_display(self, matrix, i=-1, j=-1, k=-1):
        self.matrix_display.delete(1.0, tk.END)
        n = len(matrix)
        
        # Tiêu đề
        header = "    " + "  ".join([f"{x:^6}" for x in range(n)]) + "\n"
        self.matrix_display.insert(tk.END, header)
        self.matrix_display.insert(tk.END, "  " + "-" * (n * 8) + "\n")
        
        for row_idx in range(n):
            row_str = f"{row_idx} | "
            for col_idx in range(n):
                val = matrix[row_idx][col_idx]
                if val == float('-inf'):
                    val_str = "-∞"
                elif val >= self.INF:
                    val_str = "∞"
                else:
                    val_str = f"{int(val)}"
                
                row_str += f"{val_str:^6}  "
            
            start_idx = self.matrix_display.index(tk.END)
            self.matrix_display.insert(tk.END, row_str + "\n")
            
            # Làm nổi bật ô được cập nhật
            if row_idx == i and j >= 0:
                line_num = int(start_idx.split('.')[0])
                col_start = 4 + j * 8
                self.matrix_display.tag_add("highlight", 
                                           f"{line_num}.{col_start}", 
                                           f"{line_num}.{col_start + 6}")
                self.matrix_display.tag_config("highlight", background="yellow", 
                                              foreground="red", font=("Courier", 10, "bold"))
            
            # Làm nổi bật chu trình âm
            if row_idx == col_idx and matrix[row_idx][col_idx] < 0:
                line_num = int(start_idx.split('.')[0])
                col_start = 4 + col_idx * 8
                self.matrix_display.tag_add("negative_cycle", 
                                           f"{line_num}.{col_start}", 
                                           f"{line_num}.{col_start + 6}")
                self.matrix_display.tag_config("negative_cycle", background="red", 
                                              foreground="white", font=("Courier", 10, "bold"))
    
    def draw_initial_placeholder(self):
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(7, 6), dpi=100)
        ax = fig.add_subplot(111)
        
        ax.text(0.5, 0.5, '🎯 Tạo đồ thị mẫu\nhoặc nhập ma trận\nvà bắt đầu mô phỏng',
                ha='center', va='center', fontsize=12, 
                bbox=dict(boxstyle='round', facecolor='#e8f4f8', alpha=0.8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    def draw_graph(self, matrix, k=-1, i=-1, j=-1):
        try:
            # Xóa canvas trước đó
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
            
            # Tạo figure
            fig = Figure(figsize=(7, 6), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)
            
            G = nx.DiGraph()
            n = len(matrix)
            
            # Thêm tất cả các đỉnh trước
            for node in range(n):
                G.add_node(node)
            
            # Thêm cạnh - bỏ qua các giá trị -∞
            for row in range(n):
                for col in range(n):
                    if (row != col and 
                        matrix[row][col] < self.INF and 
                        matrix[row][col] != float('-inf')):
                        try:
                            weight = int(matrix[row][col])
                            G.add_edge(row, col, weight=weight)
                        except (ValueError, OverflowError):
                            continue
            
            # Bố cục - nhiều hình dạng khác nhau
            if n == 3:
                pos = {0: (0, 1), 1: (-0.866, -0.5), 2: (0.866, -0.5)}
            elif n == 4:
                pos = {0: (-1, 1), 1: (1, 1), 2: (1, -1), 3: (-1, -1)}
            elif n == 5:
                import math
                pos = {}
                for i in range(5):
                    angle = 2 * math.pi * i / 5 - math.pi/2
                    pos[i] = (2 * math.cos(angle), 2 * math.sin(angle))
            elif n == 6:
                import math
                pos = {}
                for i in range(6):
                    angle = 2 * math.pi * i / 6
                    pos[i] = (2 * math.cos(angle), 2 * math.sin(angle))
            elif n == 7:
                import math
                pos = {}
                for i in range(7):
                    angle = 2 * math.pi * i / 7 - math.pi/2
                    pos[i] = (2.2 * math.cos(angle), 2.2 * math.sin(angle))
            elif n == 8:
                import math
                pos = {}
                for i in range(8):
                    angle = 2 * math.pi * i / 8
                    pos[i] = (2.3 * math.cos(angle), 2.3 * math.sin(angle))
            else:
                pos = nx.spring_layout(G, k=3, iterations=100, scale=2.5)
            
            # Vẽ cạnh
            edge_colors = []
            edge_widths = []
            for edge in G.edges():
                if (edge[0] == i and edge[1] == j) or (edge[0] == i and edge[1] == k) or (edge[0] == k and edge[1] == j):
                    edge_colors.append('#FF1744')
                    edge_widths.append(4)
                else:
                    edge_colors.append('#757575')
                    edge_widths.append(2)
            
            for idx, edge in enumerate(G.edges()):
                nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color=[edge_colors[idx]], 
                                      arrows=True, arrowsize=25, 
                                      arrowstyle='-|>', ax=ax, width=edge_widths[idx],
                                      connectionstyle='arc3,rad=0.1', alpha=0.8)
            
            # Vẽ đỉnh
            for idx, node in enumerate(G.nodes()):
                has_negative_cycle_at_node = False
                try:
                    if (node < len(matrix) and 
                        node < len(matrix[node]) and
                        matrix[node][node] < 0):
                        has_negative_cycle_at_node = True
                except (IndexError, TypeError, ValueError):
                    has_negative_cycle_at_node = False
                
                if has_negative_cycle_at_node:
                    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#8B0000', 
                                          node_size=1800, ax=ax, node_shape='X',
                                          edgecolors='#000000', linewidths=5)
                elif node == k:
                    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#FF4444', 
                                          node_size=1600, ax=ax, node_shape='o',
                                          edgecolors='#C0392B', linewidths=4)
                elif node == i:
                    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#FFD700', 
                                          node_size=1400, ax=ax, node_shape='s',
                                          edgecolors='#F39C12', linewidths=3)
                elif node == j:
                    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#FFA500', 
                                          node_size=1400, ax=ax, node_shape='^',
                                          edgecolors='#E67E22', linewidths=3)
                else:
                    nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#4CAF50', 
                                          node_size=1200, ax=ax, node_shape='o',
                                          edgecolors='#27AE60', linewidths=2)
            
            # Vẽ nhãn
            nx.draw_networkx_labels(G, pos, font_size=18, font_weight='bold', 
                                   font_color='white', ax=ax)
            
            # Vẽ nhãn cạnh
            edge_labels = nx.get_edge_attributes(G, 'weight')
            if edge_labels:
                label_pos = {}
                for edge in edge_labels:
                    x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2
                    y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2
                    angle = np.arctan2(pos[edge[1]][1] - pos[edge[0]][1], 
                                      pos[edge[1]][0] - pos[edge[0]][0])
                    x += 0.15 * np.cos(angle + np.pi/2)
                    y += 0.15 * np.sin(angle + np.pi/2)
                    label_pos[edge] = (x, y)
                
                for edge, (x, y) in label_pos.items():
                    weight = edge_labels[edge]
                    try:
                        if weight == float('-inf'):
                            weight_str = "-∞"
                            color = '#8B0000'
                            bbox_props = dict(boxstyle='round,pad=0.5', facecolor='#FFB6C1', 
                                             edgecolor='#8B0000', linewidth=2)
                            size = 11
                        elif (edge[0] == i and edge[1] == j) or (edge[0] == i and edge[1] == k) or (edge[0] == k and edge[1] == j):
                            weight_str = str(int(weight))
                            bbox_props = dict(boxstyle='round,pad=0.5', facecolor='#FFEB3B', 
                                             edgecolor='#FF5722', linewidth=2)
                            color = '#D32F2F'
                            size = 13
                        else:
                            weight_str = str(int(weight))
                            bbox_props = dict(boxstyle='round,pad=0.4', facecolor='white', 
                                             edgecolor='gray', linewidth=1.5)
                            color = 'black'
                            size = 11
                        
                        ax.text(x, y, weight_str, fontsize=size, fontweight='bold',
                               ha='center', va='center', color=color,
                               bbox=bbox_props, zorder=10)
                    except (ValueError, OverflowError):
                        continue
            
            # Tiêu đề
            if k >= 0:
                title = f"🔴 Đỉnh trung gian: k={k}"
                if i >= 0 and j >= 0:
                    title += f"  |  🟡 Cập nhật: d[{i}][{j}]"
            else:
                title = "📊 Đồ thị ban đầu"
            
            ax.set_title(title, fontsize=16, fontweight='bold', pad=20, color='#1976D2')
            
            # Chú giải
            legend_elements = [
                plt.Line2D([0], [0], marker='X', color='w', markerfacecolor='#8B0000', 
                          markersize=16, label='Chu trình âm', markeredgecolor='#000000', markeredgewidth=3),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF4444', 
                          markersize=14, label='Đỉnh trung gian (k)', markeredgecolor='#C0392B', markeredgewidth=3),
                plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#FFD700', 
                          markersize=12, label='Đỉnh nguồn (i)', markeredgecolor='#F39C12', markeredgewidth=2),
                plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='#FFA500', 
                          markersize=12, label='Đỉnh đích (j)', markeredgecolor='#E67E22', markeredgewidth=2),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4CAF50', 
                          markersize=10, label='Đỉnh khác', markeredgecolor='#27AE60', markeredgewidth=2)
            ]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=9,
                     framealpha=0.95, edgecolor='gray', fancybox=True, shadow=True)
            
            ax.axis('off')
            ax.set_xlim(-3, 3)
            ax.set_ylim(-3, 3)
            
            # Nhúng vào tkinter
            canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"Error in draw_graph: {e}")
            import traceback
            traceback.print_exc()
            
            # Xóa canvas và hiển thị thông báo lỗi
            for widget in self.canvas_frame.winfo_children():
                widget.destroy()
                
            error_label = tk.Label(self.canvas_frame, 
                                  text="Lỗi hiển thị đồ thị với chu trình âm\nVui lòng đặt lại và thử lại", 
                                  bg="white", fg="red", 
                                  font=("Arial", 12), justify=tk.CENTER)
            error_label.pack(expand=True)
    def bind_mousewheel_to_widget(self, widget):
        def on_mousewheel(event):
            self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        widget.bind("<MouseWheel>", on_mousewheel)
        try:
            for child in widget.winfo_children():
                self.bind_mousewheel_to_widget(child)
        except:
            pass
    
    def add_step_detail(self, step_idx, step):
        try:
            print(f"Adding step detail for step {step_idx + 1}")
            
            if step_idx == 0 and hasattr(self, 'initial_message') and self.initial_message.winfo_exists():
                self.initial_message.destroy()
            
            # Quyết định có vẽ đồ thị hay không (chỉ vẽ cho các bước quan trọng)
            should_draw_graph = (
                step_idx == 0 or  # Bước đầu
                step_idx == len(self.steps) - 1 or  # Bước cuối
                step.get('updated', False) or  # Có cập nhật ma trận
                step.get('negative_cycle', False) or  # Phát hiện chu trình âm
                (step['k'] >= 0 and step['i'] == -1 and step['j'] == -1)  # Bắt đầu/kết thúc xét đỉnh k
            )
            
            if should_draw_graph:
                # Tạo step frame đầy đủ với đồ thị
                step_frame = tk.Frame(self.steps_container, bg="#f8f9fa", relief=tk.RAISED, bd=2)
                step_frame.pack(fill=tk.X, padx=5, pady=5)
            else:
                # Tạo step frame đơn giản chỉ có text
                step_frame = tk.Frame(self.steps_container, bg="#f8f9fa", relief=tk.FLAT, bd=1)
                step_frame.pack(fill=tk.X, padx=5, pady=2)
            
            self.bind_mousewheel_to_widget(step_frame)
            
            # Header với chiều cao khác nhau
            header_height = 40 if should_draw_graph else 30
            header_frame = tk.Frame(step_frame, bg="#3498db", height=header_height)
            header_frame.pack(fill=tk.X)
            header_frame.pack_propagate(False)
            
            # Tiêu đề bước với màu sắc khác nhau
            if step.get('negative_cycle', False):
                if step.get('requires_user_decision', False):
                    title_text = f"⚠️ Bước {step_idx + 1}: PHÁT HIỆN CHU TRÌNH ÂM!"
                    header_color = "#e74c3c"
                elif step.get('algorithm_stopped', False):
                    title_text = f"🛑 Bước {step_idx + 1}: Thuật toán đã dừng"
                    header_color = "#8b0000"
                elif step.get('user_continued', False):
                    title_text = f"▶️ Bước {step_idx + 1}: Tiếp tục thực hiện"
                    header_color = "#f39c12"
                else:
                    title_text = f"⚠️ Bước {step_idx + 1}: Chu trình âm"
                    header_color = "#e67e22"
            elif step['k'] >= 0:
                if step['updated']:
                    title_text = f"🔄 Bước {step_idx + 1}: Cập nhật d[{step['i']}][{step['j']}] qua đỉnh {step['k']}"
                else:
                    title_text = f"📊 Bước {step_idx + 1}: Xét đỉnh trung gian k = {step['k']}"
                header_color = "#3498db"
            else:
                if step_idx == 0:
                    title_text = f"🚀 Bước {step_idx + 1}: Khởi tạo ma trận ban đầu"
                else:
                    title_text = f"✅ Bước {step_idx + 1}: Hoàn thành thuật toán"
                header_color = "#3498db"
            
            def on_mousewheel_local(event):
                self.main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            
            header_frame.config(bg=header_color)
            font_size = 11 if should_draw_graph else 10
            title_label = tk.Label(header_frame, text=title_text,
                                  font=("Arial", font_size, "bold"), bg=header_color, fg="white")
            title_label.pack(pady=8 if should_draw_graph else 5)
            title_label.bind("<MouseWheel>", on_mousewheel_local)
            
            if should_draw_graph:
                # Tạo nội dung đầy đủ với đồ thị
                content_frame = tk.Frame(step_frame, bg="#f8f9fa")
                content_frame.pack(fill=tk.X, padx=10, pady=10)
                
                left_frame = tk.Frame(content_frame, bg="#f8f9fa")
                left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
                
                right_frame = tk.Frame(content_frame, bg="#f8f9fa")
                right_frame.pack(side=tk.RIGHT, fill=tk.Y)
                
                # === ĐỒ THỊ NHỎ ===
                graph_label = tk.Label(left_frame, text="Đồ thị:", 
                                      font=("Arial", 10, "bold"), bg="#f8f9fa")
                graph_label.pack(anchor=tk.W)
                graph_label.bind("<MouseWheel>", on_mousewheel_local)
                
                graph_frame = tk.Frame(left_frame, bg="white", relief=tk.SUNKEN, bd=1)
                graph_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
                
                # Vẽ đồ thị nhỏ
                fig = Figure(figsize=(4, 3), dpi=80, facecolor='white')
                ax = fig.add_subplot(111)
                
                G = nx.DiGraph()
                n = len(step['matrix'])
                
                for node in range(n):
                    G.add_node(node)
                
                for row in range(n):
                    for col in range(n):
                        if row != col and step['matrix'][row][col] < self.INF:
                            G.add_edge(row, col, weight=int(step['matrix'][row][col]))
                
                # Layout
                if n == 3:
                    pos = {0: (0, 0.8), 1: (-0.7, -0.4), 2: (0.7, -0.4)}
                elif n == 4:
                    pos = {0: (-0.8, 0.8), 1: (0.8, 0.8), 2: (0.8, -0.8), 3: (-0.8, -0.8)}
                elif n == 5:
                    import math
                    pos = {}
                    for i in range(5):
                        angle = 2 * math.pi * i / 5 - math.pi/2
                        pos[i] = (0.9 * math.cos(angle), 0.9 * math.sin(angle))
                elif n == 6:
                    import math
                    pos = {}
                    for i in range(6):
                        angle = 2 * math.pi * i / 6
                        pos[i] = (0.9 * math.cos(angle), 0.9 * math.sin(angle))
                else:
                    pos = nx.spring_layout(G, k=1.5, iterations=50, scale=0.9)
                
                # Vẽ cạnh
                edge_colors = []
                for edge in G.edges():
                    if ((edge[0] == step['i'] and edge[1] == step['j']) or 
                        (edge[0] == step['i'] and edge[1] == step['k']) or 
                        (edge[0] == step['k'] and edge[1] == step['j'])):
                        edge_colors.append('#FF1744')
                    else:
                        edge_colors.append('#757575')
                
                if G.edges():
                    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, 
                                          arrows=True, arrowsize=15, width=2,
                                          arrowstyle='-|>', ax=ax, alpha=0.8)
                
                # Vẽ đỉnh
                for idx, node in enumerate(G.nodes()):
                    has_negative_cycle_at_node = step['matrix'][node][node] < 0 if hasattr(step['matrix'], '__getitem__') else False
                    
                    if has_negative_cycle_at_node:
                        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#8B0000', 
                                              node_size=500, ax=ax, node_shape='X',
                                              edgecolors='#000000', linewidths=4)
                    elif node == step['k']:
                        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#FF4444', 
                                              node_size=450, ax=ax, node_shape='o',
                                              edgecolors='#C0392B', linewidths=3)
                    elif node == step['i']:
                        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#FFD700', 
                                              node_size=400, ax=ax, node_shape='s',
                                              edgecolors='#F39C12', linewidths=2)
                    elif node == step['j']:
                        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#FFA500', 
                                              node_size=400, ax=ax, node_shape='^',
                                              edgecolors='#E67E22', linewidths=2)
                    else:
                        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color='#4CAF50', 
                                              node_size=350, ax=ax, node_shape='o',
                                              edgecolors='#27AE60', linewidths=2)
                
                nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold', 
                                       font_color='white', ax=ax)
                
                # Vẽ trọng số cạnh
                edge_labels = nx.get_edge_attributes(G, 'weight')
                if edge_labels:
                    for edge, weight in edge_labels.items():
                        x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2
                        y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2
                        
                        if ((edge[0] == step['i'] and edge[1] == step['j']) or 
                            (edge[0] == step['i'] and edge[1] == step['k']) or 
                            (edge[0] == step['k'] and edge[1] == step['j'])):
                            bbox_props = dict(boxstyle='round,pad=0.3', facecolor='#FFEB3B', 
                                             edgecolor='#FF5722', linewidth=2)
                            color = '#D32F2F'
                            size = 9
                        else:
                            bbox_props = dict(boxstyle='round,pad=0.2', facecolor='white', 
                                             edgecolor='gray', linewidth=1)
                            color = 'black'
                            size = 8
                        
                        ax.text(x, y, str(weight), fontsize=size, fontweight='bold',
                               ha='center', va='center', color=color,
                               bbox=bbox_props, zorder=10)
                
                ax.axis('off')
                ax.set_xlim(-1.3, 1.3)
                ax.set_ylim(-1.3, 1.3)
                
                canvas = FigureCanvasTkAgg(fig, master=graph_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
                
                # === MA TRẬN ===
                matrix_label = tk.Label(right_frame, text="Ma trận khoảng cách:", 
                                       font=("Arial", 10, "bold"), bg="#f8f9fa")
                matrix_label.pack(anchor=tk.W)
                matrix_label.bind("<MouseWheel>", on_mousewheel_local)
                
                matrix_text = tk.Text(right_frame, width=25, height=8, 
                                     font=("Courier", 9), bg="white", relief=tk.SUNKEN, bd=1)
                matrix_text.pack(pady=(5, 0))
                matrix_text.bind("<MouseWheel>", on_mousewheel_local)
                
                # Hiển thị ma trận
                n = len(step['matrix'])
                header = "   " + "  ".join([f"{x:^4}" for x in range(n)]) + "\n"
                matrix_text.insert(tk.END, header)
                matrix_text.insert(tk.END, " " + "-" * (n * 6) + "\n")
                
                for row_idx in range(n):
                    row_str = f"{row_idx}| "
                    for col_idx in range(n):
                        val = step['matrix'][row_idx][col_idx]
                        if val == float('-inf'):
                            val_str = "-∞"
                        elif val >= self.INF:
                            val_str = "∞"
                        else:
                            val_str = f"{int(val)}"
                        row_str += f"{val_str:^4}  "
                    
                    start_idx = matrix_text.index(tk.END)
                    matrix_text.insert(tk.END, row_str + "\n")
                    
                    # Highlight updated cell
                    if row_idx == step['i'] and step['j'] >= 0:
                        line_num = int(start_idx.split('.')[0])
                        col_start = 3 + step['j'] * 6
                        matrix_text.tag_add("highlight", 
                                           f"{line_num}.{col_start}", 
                                           f"{line_num}.{col_start + 4}")
                        matrix_text.tag_config("highlight", background="yellow", 
                                              foreground="red", font=("Courier", 9, "bold"))
                    
                    # Highlight negative cycle
                    if row_idx == col_idx and step['matrix'][row_idx][col_idx] < 0:
                        line_num = int(start_idx.split('.')[0])
                        col_start = 3 + col_idx * 6
                        matrix_text.tag_add("negative_cycle", 
                                           f"{line_num}.{col_start}", 
                                           f"{line_num}.{col_start + 4}")
                        matrix_text.tag_config("negative_cycle", background="red", 
                                              foreground="white", font=("Courier", 9, "bold"))
                
                matrix_text.config(state=tk.DISABLED)
                
                # === ĐƯỜNG ĐI NGẮN NHẤT ===
                if 'next_matrix' in step:
                    paths_label = tk.Label(right_frame, text="Đường đi ngắn nhất:", 
                                          font=("Segoe UI", 10, "bold"), bg="#f8f9fa")
                    paths_label.pack(anchor=tk.W, pady=(10, 0))
                    paths_label.bind("<MouseWheel>", on_mousewheel_local)
                    
                    paths_text = tk.Text(right_frame, width=25, height=6, 
                                        font=("Consolas", 8), bg="white", relief=tk.SUNKEN, bd=1)
                    paths_text.pack(pady=(5, 0))
                    paths_text.bind("<MouseWheel>", on_mousewheel_local)
                    
                    # Hiển thị đường đi xa nhất duy nhất trong đồ thị
                    n = len(step['matrix'])
                    
                    # Kiểm tra chu trình âm
                    has_negative_cycle = any(step['matrix'][i][i] < 0 for i in range(n))
                    
                    if has_negative_cycle:
                        paths_text.insert(tk.END, "⚠️ Chu trình âm!\n")
                        negative_vertices = [i for i in range(n) if step['matrix'][i][i] < 0]
                        paths_text.insert(tk.END, f"Đỉnh: {negative_vertices}")
                    else:
                        paths_text.insert(tk.END, "Đường đi xa nhất:\n")
                        
                        # Tìm đường đi xa nhất trong toàn bộ đồ thị
                        max_distance = -1
                        best_start = -1
                        best_end = -1
                        best_path = []
                        
                        for i in range(n):
                            for j in range(n):
                                if (i != j and step['matrix'][i][j] < self.INF and 
                                    step['matrix'][i][j] != float('-inf')):
                                    if step['matrix'][i][j] > max_distance:
                                        max_distance = step['matrix'][i][j]
                                        best_start = i
                                        best_end = j
                                        try:
                                            best_path = self.get_path(step['next_matrix'], i, j)
                                        except:
                                            best_path = []
                        
                        # Hiển thị đường đi xa nhất duy nhất
                        if best_start != -1 and best_end != -1:
                            if best_path and len(best_path) > 1:
                                path_str = "→".join(map(str, best_path))
                                paths_text.insert(tk.END, f"{best_start}→{best_end}: [{int(max_distance)}]\n{path_str}")
                            else:
                                paths_text.insert(tk.END, f"{best_start}→{best_end}: [{int(max_distance)}]\nTrực tiếp")
                        else:
                            paths_text.insert(tk.END, "Chưa có đường đi")
                    
                    paths_text.config(state=tk.DISABLED)
            else:
                # Tạo nội dung đơn giản chỉ có text (không có đồ thị)
                content_frame = tk.Frame(step_frame, bg="#f8f9fa")
                content_frame.pack(fill=tk.X, padx=10, pady=5)
                
                # Chỉ hiển thị thông tin cơ bản
                if step['k'] >= 0 and step['i'] >= 0 and step['j'] >= 0:
                    info_text = f"Kiểm tra: d[{step['i']}][{step['j']}] qua đỉnh {step['k']}"
                    if step.get('updated', False):
                        info_text += f" → Cập nhật thành {step['matrix'][step['i']][step['j']]:.0f}"
                    else:
                        info_text += " → Không thay đổi"
                else:
                    info_text = step['message']
                
                info_label = tk.Label(content_frame, text=info_text, 
                                     font=("Arial", 9), bg="#f8f9fa", fg="#34495e",
                                     wraplength=600, justify=tk.LEFT)
                info_label.pack(anchor=tk.W)
                info_label.bind("<MouseWheel>", on_mousewheel_local)
            
            # === GIẢI THÍCH (cho cả hai loại) ===
            if step['message'] and should_draw_graph:
                explain_label = tk.Label(step_frame, text=f"💡 {step['message']}", 
                                        font=("Arial", 10, "bold"), bg="#f8f9fa", fg="#2c3e50",
                                        wraplength=600, justify=tk.LEFT)
                explain_label.pack(pady=(0, 5), padx=10)
                explain_label.bind("<MouseWheel>", on_mousewheel_local)
            
            # === CHI TIẾT GIẢI THÍCH (chỉ cho các bước quan trọng) ===
            if step.get('explanation') and should_draw_graph:
                detail_frame = tk.Frame(step_frame, bg="#e8f5e8", relief=tk.FLAT, bd=1)
                detail_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
                
                detail_label = tk.Label(detail_frame, text="📝 Chi tiết:", 
                                       font=("Arial", 9, "bold"), bg="#e8f5e8", fg="#27ae60")
                detail_label.pack(anchor=tk.W, padx=8, pady=(8, 0))
                detail_label.bind("<MouseWheel>", on_mousewheel_local)
                
                explanation_text = tk.Text(detail_frame, height=4, width=70, 
                                         font=("Arial", 9), bg="#e8f5e8", fg="#2c3e50",
                                         relief=tk.FLAT, bd=0, wrap=tk.WORD)
                explanation_text.pack(fill=tk.X, padx=8, pady=(2, 8))
                explanation_text.insert(tk.END, step['explanation'])
                explanation_text.config(state=tk.DISABLED)
                explanation_text.bind("<MouseWheel>", on_mousewheel_local)
            
            # Lưu vào danh sách
            canvas_obj = canvas if should_draw_graph else None
            self.graph_history.append({
                'step_idx': step_idx,
                'widget': step_frame,
                'canvas': canvas_obj,
                'has_graph': should_draw_graph
            })
            
            # Cập nhật scroll region
            self.root.after(100, self.update_main_scroll)
            
            print(f"Added step detail ({'full' if should_draw_graph else 'simple'}), total: {len(self.graph_history)}")
            
        except Exception as e:
            print(f"Error adding step detail: {e}")
            import traceback
            traceback.print_exc()
    
    def scroll_to_steps(self):
        try:
            self.main_canvas.yview_moveto(0.3)
        except Exception as e:
            print(f"Error scrolling to steps: {e}")
    
    def update_main_scroll(self):
        try:
            self.scrollable_frame.update_idletasks()
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        except Exception as e:
            print(f"Error updating main scroll: {e}")
    
    def pause_algorithm(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL)
        self.log_message("Đã tạm dừng")
    
    def reset_algorithm(self):
        self.is_running = False
        self.current_step = 0
        self.steps = []
        
        # Xóa lịch sử đúng cách
        for item in self.graph_history:
            if item['widget'].winfo_exists():
                item['widget'].destroy()
        self.graph_history = []
        
        self.start_btn.config(state=tk.NORMAL, bg="#27ae60")
        self.pause_btn.config(state=tk.DISABLED)
        self.next_btn.config(state=tk.DISABLED)
        
        self.update_start_button_state()
        
        self.matrix_display.delete(1.0, tk.END)
        self.paths_display.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        self.status_label.config(text="Đã đặt lại")
        
        # Xóa canvas chính
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Xóa container các bước
        for widget in self.steps_container.winfo_children():
            widget.destroy()
        
        # Tạo lại thông báo ban đầu
        initial_container = tk.Frame(self.steps_container, bg="#f8f9fa", relief=tk.FLAT, bd=1)
        initial_container.pack(fill=tk.X, padx=20, pady=20)
        
        self.initial_message = tk.Label(initial_container, 
                                       text="🚀 Nhấn 'Bắt đầu' để xem các bước giải chi tiết...",
                                       font=("Segoe UI", 12), bg="#f8f9fa", fg="#7f8c8d",
                                       pady=30)
        self.initial_message.pack()
        
        # Đặt lại vị trí cuộn
        self.main_canvas.yview_moveto(0.0)
        
        self.log_message("Đã đặt lại ứng dụng")
        self.draw_initial_placeholder()
    
    def update_speed(self, value):
        self.speed = int(value)
    
    def log_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

def main():
    root = tk.Tk()
    app = FloydWarshallApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()