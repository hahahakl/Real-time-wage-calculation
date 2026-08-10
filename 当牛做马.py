#
# import tkinter as tk
# from tkinter import font, Menu
# import datetime
# import calendar
# import chinese_calendar
# import json
# import os
#
#
# class MinimizableWindow:
#     def __init__(self, root):
#         self.root = root
#         self.taskbar_icon = None
#         self.is_minimized = False
#         self.root.protocol("WM_DELETE_WINDOW", self.on_close)
#
#     def minimize(self):
#         if self.is_minimized:
#             return
#         self.root.withdraw()
#         self.taskbar_icon = tk.Toplevel(self.root)
#         self.taskbar_icon.title("🐮 牛马费计算器")
#         self.taskbar_icon.geometry("1x1+-1000+-1000")
#         self.taskbar_icon.attributes("-alpha", 0.0)
#         self.taskbar_icon.bind("<FocusIn>", self.restore)
#         self.is_minimized = True
#
#     def restore(self, event=None):
#         if not self.is_minimized:
#             return
#         if self.taskbar_icon:
#             self.taskbar_icon.destroy()
#             self.taskbar_icon = None
#         self.root.deiconify()
#         self.root.lift()
#         self.root.attributes("-topmost", True)
#         self.root.after_idle(self.root.attributes, '-topmost', False)
#         self.is_minimized = False
#
#     def on_close(self):
#         if self.taskbar_icon:
#             self.taskbar_icon.destroy()
#         self.root.quit()
#
#
# class NiumaCalculator:
#     def __init__(self, root):
#         self.root = root
#         self.minimizer = MinimizableWindow(root)
#
#         # 配置文件路径
#         self.config_file = "niuma_config.json"
#
#         # --- 缩放核心配置 ---
#         self.base_width = 320
#         self.base_height = 200
#         self.current_width = 320
#         self.current_height = 200
#
#         # 缩放限制
#         self.min_scale = 0.5
#         self.max_scale = 2.0
#         self.min_font_size = 6
#         self.max_font_size = 100
#
#         self.root.overrideredirect(True)
#         self.root.attributes("-topmost", True)
#         self.root.attributes("-alpha", 0.95)
#         self.root.geometry(f"{self.base_width}x{self.base_height}")
#
#         # 颜色配置
#         self.bg_color = "#1e1e1e"
#         self.money_color = "#00d68f"
#         self.total_color = "#f1c40f"
#         self.status_color = "#bdc3c7"
#         self.root.configure(bg=self.bg_color)
#
#         # 薪资配置 (先设默认值，稍后从文件加载)
#         self.monthly_salary = 5300
#         self.work_hours_per_day = 6.5
#
#         # 存储需要缩放的组件信息
#         self.scalable_widgets = []
#
#         self._load_config()  # 👈 启动时加载配置
#         self._create_widgets()
#         self._bind_events()
#         self.update_display()
#
#     def _load_config(self):
#         """从本地文件加载配置"""
#         if os.path.exists(self.config_file):
#             try:
#                 with open(self.config_file, 'r', encoding='utf-8') as f:
#                     config = json.load(f)
#                     self.monthly_salary = config.get('monthly_salary', 5300)
#                     self.work_hours_per_day = config.get('work_hours_per_day', 6.5)
#                     print(f"✅ 已加载配置: 月薪 {self.monthly_salary}, 时长 {self.work_hours_per_day}h")
#             except Exception as e:
#                 print(f"⚠️ 配置加载失败: {e}")
#
#     def _save_config(self):
#         """将当前配置保存到本地文件"""
#         config = {
#             'monthly_salary': self.monthly_salary,
#             'work_hours_per_day': self.work_hours_per_day
#         }
#         try:
#             with open(self.config_file, 'w', encoding='utf-8') as f:
#                 json.dump(config, f)
#             print(f"💾 配置已保存")
#         except Exception as e:
#             print(f"❌ 配置保存失败: {e}")
#
#     def _register_widget(self, widget, base_size, family="Microsoft YaHei", weight="normal"):
#         self.scalable_widgets.append({
#             'widget': widget,
#             'base_size': base_size,
#             'family': family,
#             'weight': weight
#         })
#
#     def _update_fonts(self):
#         scale = self.current_width / self.base_width
#         scale = max(self.min_scale, min(self.max_scale, scale))
#
#         for item in self.scalable_widgets:
#             new_size = int(item['base_size'] * scale)
#             new_size = max(self.min_font_size, min(self.max_font_size, new_size))
#             new_font = font.Font(family=item['family'], size=new_size, weight=item['weight'])
#             item['widget'].config(font=new_font)
#
#     def _create_widgets(self):
#         # 1. 状态标签
#         self.status_label = tk.Label(self.root, text="加载中...",
#                                      bg=self.bg_color, fg=self.status_color,
#                                      anchor="w")
#         self.status_label.pack(fill="x", padx=15, pady=(15, 5))
#         self._register_widget(self.status_label, 10, "Microsoft YaHei")
#
#         # 2. 金钱大字
#         self.money_label = tk.Label(self.root, text="¥ 0.00",
#                                     bg=self.bg_color, fg=self.money_color)
#         self.money_label.pack(pady=5)
#         self._register_widget(self.money_label, 36, "Arial", "bold")
#
#         # 3. 本月累计
#         self.total_label = tk.Label(self.root, text="月挣：¥ 0.00",
#                                     bg=self.bg_color, fg=self.total_color)
#         self.total_label.pack(pady=(0, 2))  # 间距调小
#         self._register_widget(self.total_label, 14, "Microsoft YaHei")
#
#         # 4. 底部信息
#         self.info_label = tk.Label(self.root, text="",
#                                    bg=self.bg_color, fg="#7f8c8d",
#                                    anchor="center")
#         self.info_label.pack(fill="x", padx=15, pady=(2, 15))  # 间距调小
#         self._register_widget(self.info_label, 8, "Microsoft YaHei")
#
#         self._update_fonts()
#
#     def _bind_events(self):
#         self.root.bind("<ButtonPress-1>", self.start_drag)
#         self.root.bind("<B1-Motion>", self.do_drag)
#         self.root.bind("<Button-3>", self.show_context_menu)
#         self.root.bind("<MouseWheel>", self.on_mouse_wheel)
#         self.root.bind("<Button-4>", self.on_mouse_wheel)
#         self.root.bind("<Button-5>", self.on_mouse_wheel)
#
#     def start_drag(self, event):
#         self.x = event.x
#         self.y = event.y
#
#     def do_drag(self, event):
#         deltax = event.x - self.x
#         deltay = event.y - self.y
#         x = self.root.winfo_x() + deltax
#         y = self.root.winfo_y() + deltay
#         self.root.geometry(f"+{x}+{y}")
#
#     def on_mouse_wheel(self, event):
#         direction = 0
#         if hasattr(event, 'delta'):
#             direction = int(event.delta / 120)
#         elif hasattr(event, 'num'):
#             if event.num == 4:
#                 direction = 1
#             elif event.num == 5:
#                 direction = -1
#
#         if direction != 0:
#             scale_step = 1.1 if direction > 0 else 0.9
#             new_w = int(self.current_width * scale_step)
#             new_h = int(self.current_height * scale_step)
#             potential_scale = new_w / self.base_width
#
#             if self.min_scale <= potential_scale <= self.max_scale:
#                 self.current_width = new_w
#                 self.current_height = new_h
#                 self.root.geometry(f"{self.current_width}x{self.current_height}")
#                 self._update_fonts()
#
#     def show_context_menu(self, event):
#         menu = Menu(self.root, tearoff=0, bg="#333", fg="white", activebackground="#555")
#         menu.add_command(label="📉 最小化到任务栏", command=self.minimizer.minimize)
#         menu.add_command(label="⚙️ 设置薪资", command=self.open_settings)
#         menu.add_separator()
#         menu.add_command(label="❌ 退出程序", command=self.minimizer.on_close)
#         try:
#             menu.tk_popup(event.x_root, event.y_root)
#         finally:
#             menu.grab_release()
#
#     def open_settings(self):
#         settings_win = tk.Toplevel(self.root)
#         settings_win.title("⚙️ 薪资设置")
#         settings_win.geometry("300x200")
#         settings_win.configure(bg="#2c2c2c")
#         settings_win.attributes("-topmost", True)
#
#         settings_win.update_idletasks()
#         x = self.root.winfo_x() + (self.root.winfo_width() - 300) // 2
#         y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
#         settings_win.geometry(f"+{x}+{y}")
#
#         tk.Label(settings_win, text="月薪 (元):", bg="#2c2c2c", fg="white").pack(pady=(20, 5))
#         salary_var = tk.StringVar(value=str(self.monthly_salary))
#         entry_salary = tk.Entry(settings_win, textvariable=salary_var, justify="center")
#         entry_salary.pack(pady=5)
#
#         tk.Label(settings_win, text="每日工作时长 (小时):", bg="#2c2c2c", fg="white").pack(pady=(10, 5))
#         hours_var = tk.StringVar(value=str(self.work_hours_per_day))
#         entry_hours = tk.Entry(settings_win, textvariable=hours_var, justify="center")
#         entry_hours.pack(pady=5)
#
#         def save_settings():
#             try:
#                 new_salary = float(salary_var.get())
#                 new_hours = float(hours_var.get())
#                 if new_salary > 0 and new_hours > 0:
#                     # 更新内存中的变量
#                     self.monthly_salary = new_salary
#                     self.work_hours_per_day = new_hours
#
#                     # 👇 关键：保存到文件
#                     self._save_config()
#
#                     self.update_display()
#                     settings_win.destroy()
#                 else:
#                     raise ValueError
#             except:
#                 print("输入无效")
#
#         btn_save = tk.Button(settings_win, text="保存并应用", command=save_settings,
#                              bg="#00d68f", fg="white", relief="flat", padx=10, pady=5)
#         btn_save.pack(pady=20)
#
#     def get_workdays_in_month(self, year, month):
#         workdays = 0
#         days_in_month = calendar.monthrange(year, month)[1]
#         for day in range(1, days_in_month + 1):
#             current_date = datetime.date(year, month, day)
#             if chinese_calendar.is_workday(current_date):
#                 workdays += 1
#         return workdays
#
#     def update_display(self):
#         now = datetime.datetime.now()
#         current_time = now.time()
#         is_today_workday = chinese_calendar.is_workday(now.date())
#
#         workdays = self.get_workdays_in_month(now.year, now.month)
#         daily_wage = self.monthly_salary / workdays if workdays > 0 else 0
#         secondly_wage = daily_wage / (self.work_hours_per_day * 3600)
#
#         morning_start = datetime.time(8, 0)
#         morning_end = datetime.time(11, 30)
#         afternoon_start = datetime.time(14, 30)
#         afternoon_end = datetime.time(17, 30)
#
#         earned_today = 0.0
#         status_text = ""
#         is_working = False
#
#         if is_today_workday:
#             if morning_start <= current_time <= morning_end:
#                 is_working = True
#                 start_of_work = now.replace(hour=8, minute=0, second=0, microsecond=0)
#                 worked_seconds = (now - start_of_work).total_seconds()
#                 earned_today = worked_seconds * secondly_wage
#                 status_text = "上午搬砖中... 💪"
#             elif afternoon_start <= current_time <= afternoon_end:
#                 is_working = True
#                 morning_work_seconds = (
#                         datetime.datetime.combine(now.date(), morning_end) - datetime.datetime.combine(now.date(),
#                                                                                                        morning_start)).total_seconds()
#                 start_of_afternoon = now.replace(hour=14, minute=30, second=0, microsecond=0)
#                 afternoon_worked_seconds = (now - start_of_afternoon).total_seconds()
#                 total_worked_seconds = morning_work_seconds + afternoon_worked_seconds
#                 earned_today = total_worked_seconds * secondly_wage
#                 status_text = "下午搬砖中... 💪"
#             else:
#                 if current_time < morning_start:
#                     status_text = "还没到点，再睡会儿... 😴"
#                 elif morning_end < current_time < afternoon_start:
#                     status_text = "午休充电中... 🔋"
#                 elif current_time > afternoon_end:
#                     status_text = "今日搬砖结束，自由人！ 🎉"
#                     earned_today = daily_wage
#         else:
#             holiday_name = chinese_calendar.get_holiday_detail(now.date())[1]
#             status_text = f"免费劳动力上线 ({holiday_name or '休息日'}) 🆓"
#
#         past_workdays = 0
#         for day in range(1, now.day):
#             if chinese_calendar.is_workday(datetime.date(now.year, now.month, day)):
#                 past_workdays += 1
#         total_earned_month = (past_workdays * daily_wage) + earned_today
#
#         self.status_label.config(text=status_text)
#
#         if is_working:
#             self.money_label.config(text=f"¥ {earned_today:.3f}")
#         else:
#             if not is_today_workday:
#                 self.money_label.config(text="¥ 0.00")
#             else:
#                 self.money_label.config(text=f"¥ {earned_today:.3f}")
#
#         self.total_label.config(text=f"月挣：¥ {total_earned_month:.3f}")
#         self.info_label.config(text=f"本月 {workdays} 个工作日 | 每秒进账 ¥{secondly_wage:.4f}")
#
#         self.root.after(1000, self.update_display)
#
#
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = NiumaCalculator(root)
#     root.mainloop()


import tkinter as tk
from tkinter import font, Menu
import datetime
import calendar
import chinese_calendar
import json
import os


class MinimizableWindow:
    def __init__(self, root):
        self.root = root
        self.taskbar_icon = None
        self.is_minimized = False
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def minimize(self):
        if self.is_minimized:
            return
        self.root.withdraw()
        self.taskbar_icon = tk.Toplevel(self.root)
        self.taskbar_icon.title("🐮 牛马费计算器")
        self.taskbar_icon.geometry("1x1+-1000+-1000")
        self.taskbar_icon.attributes("-alpha", 0.0)
        self.taskbar_icon.bind("<FocusIn>", self.restore)
        self.is_minimized = True

    def restore(self, event=None):
        if not self.is_minimized:
            return
        if self.taskbar_icon:
            self.taskbar_icon.destroy()
            self.taskbar_icon = None
        self.root.deiconify()
        self.root.lift()
        self.root.attributes("-topmost", True)
        self.root.after_idle(self.root.attributes, '-topmost', False)
        self.is_minimized = False

    def on_close(self):
        if self.taskbar_icon:
            self.taskbar_icon.destroy()
        self.root.quit()


class NiumaCalculator:
    def __init__(self, root):
        self.root = root
        self.minimizer = MinimizableWindow(root)

        # 配置文件路径
        self.config_file = "niuma_config.json"

        # --- 缩放核心配置 ---
        self.base_width = 320
        self.base_height = 200
        self.current_width = 320
        self.current_height = 200

        # 缩放限制
        self.min_scale = 0.5
        self.max_scale = 2.0
        self.min_font_size = 6
        self.max_font_size = 100

        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.95)
        self.root.geometry(f"{self.base_width}x{self.base_height}")

        # 颜色配置
        self.bg_color = "#1e1e1e"
        self.money_color = "#00d68f"
        self.total_color = "#f1c40f"
        self.status_color = "#bdc3c7"
        self.root.configure(bg=self.bg_color)

        # 薪资与时间配置 (先设默认值，稍后从文件加载)
        self.monthly_salary = 5300

        # 默认工作时间段
        self.morning_start_str = "08:00"
        self.morning_end_str = "11:30"
        self.afternoon_start_str = "14:30"
        self.afternoon_end_str = "17:30"

        # 自动计算的工时
        self.work_hours_per_day = 6.5

        # 存储需要缩放的组件信息
        self.scalable_widgets = []

        self._load_config()  # 👈 启动时加载配置
        self._create_widgets()
        self._bind_events()
        self.update_display()

    def _calculate_work_hours(self):
        """根据时间段自动计算每日工作小时数"""
        try:
            am_start = datetime.datetime.strptime(self.morning_start_str, "%H:%M")
            am_end = datetime.datetime.strptime(self.morning_end_str, "%H:%M")
            pm_start = datetime.datetime.strptime(self.afternoon_start_str, "%H:%M")
            pm_end = datetime.datetime.strptime(self.afternoon_end_str, "%H:%M")

            morning_duration = (am_end - am_start).total_seconds() / 3600
            afternoon_duration = (pm_end - pm_start).total_seconds() / 3600

            total = morning_duration + afternoon_duration
            return max(0, total)  # 防止负数
        except:
            return 6.5  # 出错时返回默认值

    def _load_config(self):
        """从本地文件加载配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.monthly_salary = config.get('monthly_salary', 5300)

                    # 加载时间段配置
                    self.morning_start_str = config.get('morning_start', "08:00")
                    self.morning_end_str = config.get('morning_end', "11:30")
                    self.afternoon_start_str = config.get('afternoon_start', "14:30")
                    self.afternoon_end_str = config.get('afternoon_end', "17:30")

                    # 👇 关键：根据加载的时间段自动计算工时
                    self.work_hours_per_day = self._calculate_work_hours()

                    print(f"✅ 已加载配置: 月薪 {self.monthly_salary}, 自动计算工时 {self.work_hours_per_day:.2f}h")
            except Exception as e:
                print(f"⚠️ 配置加载失败: {e}")

    def _save_config(self):
        """将当前配置保存到本地文件"""
        # 👇 关键：保存前再次确保工时是最新计算的
        self.work_hours_per_day = self._calculate_work_hours()

        config = {
            'monthly_salary': self.monthly_salary,
            'work_hours_per_day': self.work_hours_per_day,  # 虽然自动计算，但也存一份方便查看
            'morning_start': self.morning_start_str,
            'morning_end': self.morning_end_str,
            'afternoon_start': self.afternoon_start_str,
            'afternoon_end': self.afternoon_end_str
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f)
            print(f"💾 配置已保存 (自动计算工时: {self.work_hours_per_day:.2f}h)")
        except Exception as e:
            print(f"❌ 配置保存失败: {e}")

    def _register_widget(self, widget, base_size, family="Microsoft YaHei", weight="normal"):
        self.scalable_widgets.append({
            'widget': widget,
            'base_size': base_size,
            'family': family,
            'weight': weight
        })

    def _update_fonts(self):
        scale = self.current_width / self.base_width
        scale = max(self.min_scale, min(self.max_scale, scale))

        for item in self.scalable_widgets:
            new_size = int(item['base_size'] * scale)
            new_size = max(self.min_font_size, min(self.max_font_size, new_size))
            new_font = font.Font(family=item['family'], size=new_size, weight=item['weight'])
            item['widget'].config(font=new_font)

    def _create_widgets(self):
        # 1. 状态标签
        self.status_label = tk.Label(self.root, text="加载中...",
                                     bg=self.bg_color, fg=self.status_color,
                                     anchor="w")
        self.status_label.pack(fill="x", padx=15, pady=(15, 5))
        self._register_widget(self.status_label, 10, "Microsoft YaHei")

        # 2. 金钱大字
        self.money_label = tk.Label(self.root, text="¥ 0.00",
                                    bg=self.bg_color, fg=self.money_color)
        self.money_label.pack(pady=5)
        self._register_widget(self.money_label, 36, "Arial", "bold")

        # 3. 本月累计
        self.total_label = tk.Label(self.root, text="月挣：¥ 0.00",
                                    bg=self.bg_color, fg=self.total_color)
        self.total_label.pack(pady=(0, 2))
        self._register_widget(self.total_label, 14, "Microsoft YaHei")

        # 4. 底部信息
        self.info_label = tk.Label(self.root, text="",
                                   bg=self.bg_color, fg="#7f8c8d",
                                   anchor="center")
        self.info_label.pack(fill="x", padx=15, pady=(2, 15))
        self._register_widget(self.info_label, 8, "Microsoft YaHei")

        self._update_fonts()

    def _bind_events(self):
        self.root.bind("<ButtonPress-1>", self.start_drag)
        self.root.bind("<B1-Motion>", self.do_drag)
        self.root.bind("<Button-3>", self.show_context_menu)
        self.root.bind("<MouseWheel>", self.on_mouse_wheel)
        self.root.bind("<Button-4>", self.on_mouse_wheel)
        self.root.bind("<Button-5>", self.on_mouse_wheel)

    def start_drag(self, event):
        self.x = event.x
        self.y = event.y

    def do_drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")

    def on_mouse_wheel(self, event):
        direction = 0
        if hasattr(event, 'delta'):
            direction = int(event.delta / 120)
        elif hasattr(event, 'num'):
            if event.num == 4:
                direction = 1
            elif event.num == 5:
                direction = -1

        if direction != 0:
            scale_step = 1.1 if direction > 0 else 0.9
            new_w = int(self.current_width * scale_step)
            new_h = int(self.current_height * scale_step)
            potential_scale = new_w / self.base_width

            if self.min_scale <= potential_scale <= self.max_scale:
                self.current_width = new_w
                self.current_height = new_h
                self.root.geometry(f"{self.current_width}x{self.current_height}")
                self._update_fonts()

    def show_context_menu(self, event):
        menu = Menu(self.root, tearoff=0, bg="#333", fg="white", activebackground="#555")
        menu.add_command(label="📉 最小化到任务栏", command=self.minimizer.minimize)
        menu.add_command(label="⚙️ 设置薪资", command=self.open_settings)
        menu.add_separator()
        menu.add_command(label="❌ 退出程序", command=self.minimizer.on_close)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("⚙️ 薪资与时间设置")
        settings_win.geometry("320x380")
        settings_win.configure(bg="#2c2c2c")
        settings_win.attributes("-topmost", True)

        settings_win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - 320) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 380) // 2
        settings_win.geometry(f"+{x}+{y}")

        # --- 薪资部分 ---
        tk.Label(settings_win, text="--- 薪资设置 ---", bg="#2c2c2c", fg="#aaa").pack(pady=(10, 5))

        tk.Label(settings_win, text="月薪 (元):", bg="#2c2c2c", fg="white").pack(pady=(5, 2))
        salary_var = tk.StringVar(value=str(self.monthly_salary))
        entry_salary = tk.Entry(settings_win, textvariable=salary_var, justify="center")
        entry_salary.pack(pady=2)

        # --- 时间段部分 ---
        tk.Label(settings_win, text="--- 工作时间段 (HH:MM) ---", bg="#2c2c2c", fg="#aaa").pack(pady=(15, 5))

        # 显示当前自动计算的工时提示
        current_hours = self._calculate_work_hours()
        tk.Label(settings_win, text=f"当前自动计算日工时: {current_hours:.2f} 小时",
                 bg="#2c2c2c", fg="#00d68f", font=("Microsoft YaHei", 9)).pack(pady=(0, 10))

        time_frame = tk.Frame(settings_win, bg="#2c2c2c")
        time_frame.pack(pady=5)

        tk.Label(time_frame, text="上午开始:", bg="#2c2c2c", fg="white").grid(row=0, column=0, padx=5)
        am_start_var = tk.StringVar(value=self.morning_start_str)
        tk.Entry(time_frame, textvariable=am_start_var, width=8, justify="center").grid(row=0, column=1, padx=5)

        tk.Label(time_frame, text="上午结束:", bg="#2c2c2c", fg="white").grid(row=1, column=0, padx=5)
        am_end_var = tk.StringVar(value=self.morning_end_str)
        tk.Entry(time_frame, textvariable=am_end_var, width=8, justify="center").grid(row=1, column=1, padx=5)

        tk.Label(time_frame, text="下午开始:", bg="#2c2c2c", fg="white").grid(row=2, column=0, padx=5, pady=(10, 0))
        pm_start_var = tk.StringVar(value=self.afternoon_start_str)
        tk.Entry(time_frame, textvariable=pm_start_var, width=8, justify="center").grid(row=2, column=1, padx=5,
                                                                                        pady=(10, 0))

        tk.Label(time_frame, text="下午结束:", bg="#2c2c2c", fg="white").grid(row=3, column=0, padx=5)
        pm_end_var = tk.StringVar(value=self.afternoon_end_str)
        tk.Entry(time_frame, textvariable=pm_end_var, width=8, justify="center").grid(row=3, column=1, padx=5)

        def save_settings():
            try:
                new_salary = float(salary_var.get())

                # 验证时间格式
                def parse_time(t_str):
                    h, m = map(int, t_str.split(':'))
                    return datetime.time(h, m)

                # 尝试解析以验证格式正确性
                parse_time(am_start_var.get())
                parse_time(am_end_var.get())
                parse_time(pm_start_var.get())
                parse_time(pm_end_var.get())

                if new_salary > 0:
                    # 更新内存中的变量
                    self.monthly_salary = new_salary

                    # 更新时间字符串
                    self.morning_start_str = am_start_var.get()
                    self.morning_end_str = am_end_var.get()
                    self.afternoon_start_str = pm_start_var.get()
                    self.afternoon_end_str = pm_end_var.get()

                    # 👇 关键：自动重新计算工时
                    self.work_hours_per_day = self._calculate_work_hours()

                    # 保存到文件
                    self._save_config()

                    self.update_display()
                    settings_win.destroy()
                else:
                    raise ValueError("薪资不能为负数或零")
            except ValueError as ve:
                print(f"输入错误: {ve}")
            except Exception as e:
                print(f"时间格式错误，请使用 HH:MM 格式 (例如 09:00)")

        btn_save = tk.Button(settings_win, text="保存并应用", command=save_settings,
                             bg="#00d68f", fg="white", relief="flat", padx=10, pady=5)
        btn_save.pack(pady=20)

    def get_workdays_in_month(self, year, month):
        workdays = 0
        days_in_month = calendar.monthrange(year, month)[1]
        for day in range(1, days_in_month + 1):
            current_date = datetime.date(year, month, day)
            if chinese_calendar.is_workday(current_date):
                workdays += 1
        return workdays

    def update_display(self):
        now = datetime.datetime.now()
        current_time = now.time()
        is_today_workday = chinese_calendar.is_workday(now.date())

        workdays = self.get_workdays_in_month(now.year, now.month)
        daily_wage = self.monthly_salary / workdays if workdays > 0 else 0

        # 使用自动计算的工时
        secondly_wage = daily_wage / (self.work_hours_per_day * 3600) if self.work_hours_per_day > 0 else 0

        # 使用动态加载的时间段
        morning_start = datetime.time(*map(int, self.morning_start_str.split(':')))
        morning_end = datetime.time(*map(int, self.morning_end_str.split(':')))
        afternoon_start = datetime.time(*map(int, self.afternoon_start_str.split(':')))
        afternoon_end = datetime.time(*map(int, self.afternoon_end_str.split(':')))

        earned_today = 0.0
        status_text = ""
        is_working = False

        if is_today_workday:
            if morning_start <= current_time <= morning_end:
                is_working = True
                start_of_work = now.replace(hour=morning_start.hour, minute=morning_start.minute, second=0,
                                            microsecond=0)
                worked_seconds = (now - start_of_work).total_seconds()
                earned_today = worked_seconds * secondly_wage
                status_text = "上午搬砖中... 💪"
            elif afternoon_start <= current_time <= afternoon_end:
                is_working = True
                morning_work_seconds = (
                        datetime.datetime.combine(now.date(), morning_end) - datetime.datetime.combine(now.date(),
                                                                                                       morning_start)).total_seconds()
                start_of_afternoon = now.replace(hour=afternoon_start.hour, minute=afternoon_start.minute, second=0,
                                                 microsecond=0)
                afternoon_worked_seconds = (now - start_of_afternoon).total_seconds()
                total_worked_seconds = morning_work_seconds + afternoon_worked_seconds
                earned_today = total_worked_seconds * secondly_wage
                status_text = "下午搬砖中... 💪"
            else:
                if current_time < morning_start:
                    status_text = "还没到点... 😴"
                elif morning_end < current_time < afternoon_start:
                    status_text = "午休充电中... 🔋"
                elif current_time > afternoon_end:
                    status_text = "今日搬砖结束，自由人！ 🎉"
                    earned_today = daily_wage
        else:
            holiday_name = chinese_calendar.get_holiday_detail(now.date())[1]
            status_text = f"免费劳动力上线 ({holiday_name or '休息日'}) 🆓"

        past_workdays = 0
        for day in range(1, now.day):
            if chinese_calendar.is_workday(datetime.date(now.year, now.month, day)):
                past_workdays += 1
        total_earned_month = (past_workdays * daily_wage) + earned_today

        self.status_label.config(text=status_text)

        if is_working:
            self.money_label.config(text=f"¥ {earned_today:.3f}")
        else:
            if not is_today_workday:
                self.money_label.config(text="¥ 0.00")
            else:
                self.money_label.config(text=f"¥ {earned_today:.3f}")

        self.total_label.config(text=f"月挣：¥ {total_earned_month:.3f}")
        self.info_label.config(text=f"本月 {workdays} 个工作日 | 每秒进账 ¥{secondly_wage:.4f}")

        self.root.after(1000, self.update_display)


if __name__ == "__main__":
    root = tk.Tk()
    app = NiumaCalculator(root)
    root.mainloop()
