import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
import os
import webbrowser
import time

# ====================== 数据操作函数 ======================
def load_users():
    """加载用户数据(格式: 用户名,密码)"""
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as f:
            pass  # 创建空文件
        
    users = {}
    with open("user.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 2:
                users[parts[0]] = parts[1]
    return users
def web():
    root_web = tk.Tk()
    root_web.title("浏览器")
    root_web.geometry("600x600")
    label = tk.Label(root_web, text="输入网址:")
    label.pack()
    entry = tk.Entry(root_web)
    entry.pack()
    def open_web():
        url = entry.get()
        webbrowser.open(url,new=1)
    ttk.Button(root_web,text="打开",command=open_web).pack()
    label2 = ttk.Label(root_web,text="搜索:")
    label2.pack()
    entry2 = ttk.Entry(root_web)
    entry2.pack()
    def search():
        search_1 = entry2.get()
        webbrowser.open("https://cn.bing.com/search?pglt=2339&q=" + search_1,new=1)
    ttk.Button(root_web,text="搜索",command=search).pack()
    root_web.mainloop()
def load_security_questions():
    """加载安全问题"""
    if not os.path.exists("user_问题.txt"):
        return {}  # 直接返回空字典
        
    questions = {}
    with open("user_问题.txt", "r", encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) == 3:
                questions[parts[0]] = {
                    "question": parts[1],
                    "answer": parts[2]
                }
    return questions
def load_banned_users():
    """加载禁止登录的用户列表和原因"""
    banned_users = {}
    try:
        with open("banned_users.txt", "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:  # 跳过空行
                    parts = line.split(",", 1)  # 只分割第一个逗号
                    if len(parts) == 1:
                        banned_users[parts[0]] = "无具体原因"  # 只有用户名没有原因
                    elif len(parts) == 2:
                        banned_users[parts[0]] = parts[1]  # 用户名和原因
    except FileNotFoundError:
        with open("banned_users.txt", "w", encoding='utf-8') as f:
            pass  # 创建空文件
    return banned_users
    


def load_banned_names():
    """加载禁止注册的用户名"""
    banned_names = []
    try:
        with open("banned_names.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line:  # 跳过空行
                    banned_names.append(line)
    except FileNotFoundError:
        with open("banned_names.txt", "w") as f:
            pass  # 创建空文件
    return banned_names

def ban_user(username, reason="无具体原因"):
    """添加用户到禁止登录列表并记录原因"""
    banned_users = load_banned_users()
    if username in banned_users:
        return False  # 用户已在禁止列表中
        
    try:
        with open("banned_users.txt", "a", encoding='utf-8') as f:
            f.write(f"{username},{reason}\n")
        return True
    except Exception as e:
        print(f"禁止用户失败: {e}")
        return False
def unban_user(username):
    """从禁止登录列表中移除用户"""
    banned_users = load_banned_users()
    if username not in banned_users:
        return False  # 用户不在禁止列表中
        
    try:
        banned_users.pop(username)
        with open("banned_users.txt", "w", encoding='utf-8') as f:
            for user, reason in banned_users.items():
                f.write(f"{user},{reason}\n")
        return True
    except Exception as e:
        print(f"解除禁止失败: {e}")
        return False

def ban_name(name):
    """添加名称到禁止注册列表"""
    banned_names = load_banned_names()
    if name.lower() in [n.lower() for n in banned_names]:
        return False  # 名称已在禁止列表中
        
    try:
        with open("banned_names.txt", "a") as f:
            f.write(f"{name}\n")
        return True
    except Exception as e:
        print(f"禁止名称失败: {e}")
        return False

def unban_name(name):
    """从禁止注册列表中移除名称"""
    banned_names = load_banned_names()
    if name.lower() not in [n.lower() for n in banned_names]:
        return False  # 名称不在禁止列表中
        
    try:
        banned_names = [n for n in banned_names if n.lower() != name.lower()]
        with open("banned_names.txt", "w") as f:
            for name in banned_names:
                f.write(f"{name}\n")
        return True
    except Exception as e:
        print(f"解除名称禁止失败: {e}")
        return False

def save_user(username, password):
    """保存用户信息"""
    with open("user.txt", "a") as f:
        f.write(f"{username},{password}\n")

def save_security_question(username, question, answer):
    """保存安全问题"""
    with open("user_问题.txt", "a", encoding='utf-8') as f:
        f.write(f"{username},{question},{answer}\n")

def delete_user(username):
    """删除用户及其安全信息"""
    # 删除用户
    users = load_users()
    if username in users:
        del users[username]
        with open("user.txt", "w") as f:
            for uname, pwd in users.items():
                f.write(f"{uname},{pwd}\n")
    
    # 删除安全问题
    questions = load_security_questions()
    if username in questions:
        del questions[username]
        with open("user_问题.txt", "w", encoding='utf-8') as f:
            for uname, data in questions.items():
                f.write(f"{uname},{data['question']},{data['answer']}\n")

def is_valid_username(username):
    """验证用户名合法性"""
    banned_names = load_banned_names()
    if username.lower() in [name.lower() for name in banned_names]:
        return False, "该用户名已被禁止注册"
    
    return True, ""

def is_valid_password(password):
    """验证密码强度""" 
    return True, ""

# ====================== 界面函数 ======================
def open_debug_window(level):
    """打开调试窗口"""
    debug = tk.Tk()
    debug.geometry("700x700")
    debug.title("debug")
    if level == "admin":
        tk.Label(debug,text="你好，管理员").pack()
    else:
        tk.Label(debug,text="你好，用户").pack()
    tk.Label(debug,text="调试:").pack()
    def open_admin_windows():
        """打开admin窗口"""
        debug_1 = tk.Tk()
        debug_1.geometry("700x700")
        debug_1.title("身份验证")
        tk.Label(debug_1,text="输入admin密码:").pack()
        entry = tk.Entry(debug_1,show="*")
        entry.pack()
        def login():
            # 验证密码
            if entry.get() == "admin":
                create_admin_panel()
            else:
                messagebox.showerror("错误","密码错误")
        tk.Button(debug_1,text="验证",command=lambda:login()).pack()
        
    tk.Button(debug,text="打开管理员窗口",command=open_admin_windows).pack()
    def admin_change_password_2():
        """修改密码"""
        debug_2 = tk.Tk()
        debug_2.geometry("700x700")
        debug_2.title("修改密码")
        tk.Label(debug_2,text="输入admin密码:").pack()
        entry = tk.Entry(debug_2,show="*")
        entry.pack()
        def login_2():
            # 验证密码
            if entry.get() == "admin":
                admin_change_password_1()
            else:
                messagebox.showerror("错误","密码错误")
        tk.Button(debug_2,text="验证",command=lambda:login_2()).pack()
    def login_3():
            """删除用户"""
            debug_3 = tk.Tk()
            debug_3.geometry("700x700")
            debug_3.title("删除用户")
            tk.Label(debug_3,text="输入admin密码:").pack()
            entry_1 = tk.Entry(debug_3,show="*")
            entry_1.pack()
            def login_3_1():
             # 验证密码
             if entry_1.get() == "admin":
                tk.Label(debug_3,text="输入用户名:").pack()
                entry_2 = tk.Entry(debug_3)
                entry_2.pack()
                tk.Button(debug_3,text="删除",command=lambda:delete_user(username=entry_2.get())).pack()
            tk.Button(debug_3,text="验证",command=lambda:login_3_1()).pack()
    tk.Button(debug,command=lambda:admin_change_password_2(),text="修改密码").pack()
    tk.Button(debug,text="删除用户",command=lambda:login_3()).pack()
    def login_4():
        """封禁用户"""
        debug_4 = tk.Tk()
        debug_4.geometry("700x700")
        debug_4.title("封禁用户")
        tk.Label(debug_4,text="输入admin密码:").pack()
        entry_1 = tk.Entry(debug_4,show="*")
        entry_1.pack()
        ttk.Button(debug_4,text="验证",command=lambda:login_4_1()).pack()
        def login_4_1():
            # 验证密码
            if entry_1.get() == "admin":
                tk.Label(debug_4,text="输入用户名:").pack()
                entry_2 = tk.Entry(debug_4)
                entry_2.pack()
                tk.Label(debug_4,text="输入封禁原因:").pack()
                entry_3 = tk.Entry(debug_4)
                entry_3.pack()
                tk.Button(debug_4,text="封禁",command=lambda:ban_user(username=entry_2.get(),reason=entry_3.get())).pack()
    ttk.Button(debug,command=lambda:login_4(),text="封禁用户").pack()
    def login_5():
        """进入用户页面"""
        debug_5 = tk.Tk()
        debug_5.geometry("700x700")
        debug_5.title("进入用户页面")
        ttk.Button(debug_5,text="进入",command=lambda:create_user_panel(username="debug_user",pwd="test_debug")).pack()
    ttk.Button(debug,command=lambda:login_5(),text="进入用户页面").pack()
    debug.mainloop()

def create_login_window():
    """登录窗口"""
    root = tk.Tk()
    root.title("登录")
    root.geometry("800x800")
    
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(frame, text="用户登录", font=("Arial", 14, "bold")).pack(pady=10)
    
    # 用户名
    ttk.Label(frame, text="用户名:").pack(pady=5)
    entry_username = ttk.Entry(frame)
    entry_username.pack(pady=5, fill=tk.X)
    
    # 密码
    ttk.Label(frame, text="密码:").pack(pady=5)
    entry_password = ttk.Entry(frame, show="*")
    entry_password.pack(pady=5, fill=tk.X)
    
    # 按钮区域
    button_frame = ttk.Frame(frame)
    button_frame.pack(pady=15, fill=tk.X)
    
    def login():
        username = entry_username.get().strip()
        password = entry_password.get().strip()
        if username == "debug":
            open_debug_window(level="user")
        if not username:
            messagebox.showerror("错误", "用户名不能为空")
            return
            
        # 检查是否被禁止登录
        banned_users = load_banned_users()
        lowercase_banned = {k.lower(): v for k, v in banned_users.items()}
        if username.lower() in lowercase_banned:
          reason = lowercase_banned[username.lower()]
          messagebox.showerror("禁止登录", 
                           f"该账号已被禁止登录\n\n"
                           f"封禁原因: {reason}\n\n"
                           f"如需申诉，请联系管理员\n\n"
                           f"其他信息:\n"
                           f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                           f"{time.localtime()}")
          return False
            
        users = load_users()
        
        # 管理员检查
        if username == "superadmin" and password == "superadmin":
            create_admin_panel()
            root.destroy()
            return
            
        if username == "admin" and password == "admin":
            create_admin_panel()
            root.destroy()
        elif username in users and users[username] == password:
            create_user_panel(username,pwd=password)
            root.destroy()
        else:
            messagebox.showerror("错误", "用户名或密码错误")
    def delate_username_pwd():
        """删除用户名和密码"""
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    def show_contact():
        """显示联系信息"""
        contact_win = tk.Toplevel(root)
        contact_win.title("联系我们")
        contact_win.geometry("400x300")
        
        frame = ttk.Frame(contact_win, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="邮箱:", font=('Arial', 12)).pack()
        ttk.Label(frame, text="Yxf52013141@outlook.com", font=('Arial', 12, 'bold')).pack(pady=10)
        ttk.Button(frame, text="关闭", command=contact_win.destroy).pack(pady=20)
    ttk.Button(button_frame, text="清除所有内容", command=delate_username_pwd, width=10).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="登录", command=login, width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="注册", command=lambda:create_register_window(root), width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="找回密码", command=create_recover_window, width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="退出", command=root.destroy, width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="联系我们", command=show_contact, width=10).pack(side=tk.LEFT, padx=5)
    # debug
    ttk.Button(button_frame, text="admin", command=lambda:create_admin_panel(), width=10).pack(side=tk.LEFT, padx=5)
    # 底部信息
    ttk.Label(frame, text="© 2025 系统登录").pack(pady=10)
    ttk.Label(frame, text="版本号：2.0.1.50501").pack(pady=5)
    
    root.mainloop()

def create_user_panel(username,pwd):
    """用户主页"""
    user_window = tk.Tk()
    user_window.title(f"用户中心 - {username}")
    user_window.geometry("500x400")
    
    main_frame = ttk.Frame(user_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(main_frame, text=f"欢迎您，{username}！", font=("Arial", 14, "bold")).pack(pady=20)
    ttk.Label(main_frame, text=f"你的密码是:{pwd}").pack(pady=10)
    # 用户功能区域
    button = ttk.Button(main_frame,text="浏览器",command=web)
    button.pack(pady=10)
    button2 = ttk.Button(main_frame, text="修改密码", command=lambda:admin_change_password(username))
    button2.pack(pady=10)
    button3 = ttk.Button(main_frame, text="退出登录", command=user_window.destroy)
    button3.pack(pady=20)
    if username == "debug_user":
        return False
    else:
     questions = load_security_questions()
     if len(questions) == 0:
        button.config(state=tk.DISABLED)
        button2.config(state=tk.DISABLED)
        label = ttk.Label(main_frame, text="你还没有设置安全问题，所有功能已禁用", font=("Arial", 12, "bold"), foreground="red")
        ban_user(username,reason="没有设置安全问题")
        label.pack(pady=10)
        messagebox.showerror("错误-自动封禁系统", "你还没有设置安全问题，所有功能已禁用\n\n"
                           f"封禁原因: 没有设置安全问题\n\n"
                           f"如需申诉，请联系管理员\n\n"
                           f"reason: no security question\n\n"
                           f"其他信息:\n"
                           f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                           f"{time.localtime()}")
    if len(pwd) < 6:
        button.config(state=tk.DISABLED)
        button2.config(state=tk.DISABLED)
        label = ttk.Label(main_frame, text="你的密码过短，所有功能已禁用", font=("Arial", 12, "bold"), foreground="red")
        label.pack(pady=10)
        ban_user(username,reason="密码过短")
        messagebox.showerror("错误-自动封禁系统", "你的密码过短，所有功能已禁用\n\n"
                           f"封禁原因: 密码过短\n"
                           f"如需申诉，请联系管理员\n"
                           f"reason: password too short\n\n"
                           f"其他信息:\n"
                           f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                           f"{time.localtime()}")
    if len(username) > 10:
        button.config(state=tk.DISABLED)
        button2.config(state=tk.DISABLED)
        label = ttk.Label(main_frame, text="你的用户名过长，所有功能已禁用", font=("Arial", 12, "bold"), foreground="red")
        label.pack(pady=10)
        ban_user(username,reason="用户名过长")
        messagebox.showerror("错误-自动封禁系统", "你的用户名过长，所有功能已禁用\n\n"
                           f"封禁原因: 用户名过长\n"
                           f"如需申诉，请联系管理员\n"
                           f"reason: username too long\n\n"
                           f"其他信息:\n"
                           f"当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                           f"{time.localtime()}")
        
    user_window.mainloop()

def create_admin_panel():
    """管理员控制台"""
    admin_window = tk.Tk()
    admin_window.title("管理员控制台")
    admin_window.geometry("1000x1000")
    
    main_frame = ttk.Frame(admin_window, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(main_frame, text="管理员控制台", font=("Arial", 16, "bold")).pack(pady=10)
    
    # 用户列表显示区域
    list_frame = ttk.Frame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=True)
    
    scroll_y = ttk.Scrollbar(list_frame)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_area = tk.Text(list_frame, yscrollcommand=scroll_y.set, wrap=tk.WORD)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scroll_y.config(command=text_area.yview)
    text_area.config(state=tk.DISABLED)
    
    def load_all_users():
        """加载用户数据到文本框"""
        users = load_users()
        questions = load_security_questions()
        banned_users = load_banned_users()
        
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        
        if not users:
            text_area.insert(tk.END, "当前没有用户数据")
            text_area.config(state=tk.DISABLED)
            return
            
        text_area.insert(tk.END, f"共 {len(users)} 位用户\n\n")
        text_area.insert(tk.END, "="*60 + "\n\n")
        
        for username, pwd in users.items():
            text_area.insert(tk.END, f"用户名: {username}\n")
            text_area.insert(tk.END, f"密码: {pwd}\n")
            text_area.insert(tk.END, f"密码位数: {len(pwd)}\n")
            text_area.insert(tk.END, f"状态: {'🚫 禁用' if username in banned_users else '✅ 正常'}\n")
            
            if username in questions:
                text_area.insert(tk.END, f"安全问题: {questions[username]['question']}\n")
                text_area.insert(tk.END, f"安全答案: {questions[username]['answer']}\n")
            else:
                text_area.insert(tk.END, "安全提示: 未设置安全问题\n")
                text_area.insert(tk.END, "建议封禁,账户名: "+ username+ "\n")
                
            text_area.insert(tk.END, "-"*60 + "\n\n")
        
        text_area.config(state=tk.DISABLED)
    
    def refresh_list():
        load_all_users()
    refresh_list()
    def delete_all_users():
        """删除所有用户"""
        if messagebox.askyesno("确认", "确定要删除所有用户吗？"):
            open("user.txt", "w").close()
            open("user_问题.txt", "w").close()
            messagebox.showinfo("提示", "删除成功")   
            refresh_list()        
    
    # 控制按钮区域
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=5)
    
    ttk.Button(button_frame, text="刷新列表", command=refresh_list).pack(side=tk.LEFT, padx=5)
    
    def open_ban_management():
     """封禁管理窗口"""
     ban_win = tk.Toplevel()
     ban_win.title("封禁管理系统")
     ban_win.geometry("800x600")
    
     # 主框架
     main_frame = ttk.Frame(ban_win, padding=15)
     main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 搜索和添加区域
     search_frame = ttk.Frame(main_frame)
     search_frame.pack(fill=tk.X, pady=10)
    
     ttk.Label(search_frame, text="搜索用户:").pack(side=tk.LEFT)
     search_entry = ttk.Entry(search_frame)
     search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
    
    # 操作按钮区域
     action_frame = ttk.Frame(search_frame)
     action_frame.pack(side=tk.RIGHT, padx=5)
    
     ttk.Button(action_frame, text="封禁用户", style="danger.TButton", command=lambda: show_ban_dialog()).pack(side=tk.LEFT, padx=2)
     ttk.Button(action_frame, text="解封用户", style="success.TButton", command=lambda: unban_selected()).pack(side=tk.LEFT, padx=2)
    
    # 封禁用户列表
     list_frame = ttk.Frame(main_frame)
     list_frame.pack(fill=tk.BOTH, expand=True)
    
     columns = ("username", "reason")
     tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
    
    # 设置列
     tree.heading("username", text="用户名", anchor="w")
     tree.heading("reason", text="封禁原因", anchor="w")
     tree.column("username", width=150)
     tree.column("reason", width=400, stretch=True)
    
     vsb = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
     hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=tree.xview)
     tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
     tree.grid(row=0, column=0, sticky="nsew")
     vsb.grid(row=0, column=1, sticky="ns")
     hsb.grid(row=1, column=0, sticky="ew")
    
     list_frame.grid_rowconfigure(0, weight=1)
     list_frame.grid_columnconfigure(0, weight=1)
    
    # 详情区域
     detail_frame = ttk.LabelFrame(main_frame, text="封禁详情", padding=10)
     detail_frame.pack(fill=tk.X, pady=10)
    
     detail_text = tk.Text(detail_frame, height=4, wrap="word")
     detail_text.pack(fill=tk.X)
     detail_text.config(state="disabled")
    
    # 底部按钮
     bottom_frame = ttk.Frame(main_frame)
     bottom_frame.pack(fill=tk.X, pady=10)
     ttk.Button(bottom_frame, text="刷新列表", command=lambda:refresh_list()).pack(side=tk.LEFT, padx=5)
     ttk.Button(bottom_frame, text="导出列表", command=lambda:export_list()).pack(side=tk.LEFT, padx=5)
     ttk.Button(bottom_frame, text="关闭", command=ban_win.destroy).pack(side=tk.RIGHT)
    
    # 功能函数
     def refresh_list():
        """刷新封禁用户列表"""
        for item in tree.get_children():
            tree.delete(item)
            
        banned_users = load_banned_users()
        for username, reason in banned_users.items():
            tree.insert("", "end", values=(username, reason))
        detail_text.config(state="normal")
        detail_text.delete("1.0", "end")
        detail_text.config(state="disabled")
     def show_ban_dialog():
        """显示封禁用户对话框"""
        dialog = tk.Toplevel(ban_win)
        dialog.title("封禁用户")
        dialog.geometry("600x600")
        dialog.resizable(False, False)
        
        center_frame = ttk.Frame(dialog, padding=20)
        center_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(center_frame, text="用户名:").pack(anchor="w", pady=5)
        username_entry = ttk.Entry(center_frame)
        username_entry.pack(fill=tk.X, pady=5)
        
        ttk.Label(center_frame, text="封禁原因:").pack(anchor="w", pady=5)
        reason_entry = ttk.Entry(center_frame)
        reason_entry.pack(fill=tk.X, pady=5)
        
        status_label = ttk.Label(center_frame, text="", foreground="red")
        status_label.pack(pady=5)
        
        button_frame = ttk.Frame(center_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        def confirm_ban():
            username = username_entry.get().strip()
            reason = reason_entry.get().strip()
            
            if not username:
                status_label.config(text="请输入用户名")
                return
                
            if not reason:
                reason = "违反用户规定"
                
            if ban_user(username, reason):
                refresh_list()
                dialog.destroy()
                messagebox.showinfo("成功", f"已封禁用户 {username}", parent=ban_win)
            else:
                status_label.config(text=f"封禁失败: 用户可能已被封禁")
        
        ttk.Button(button_frame, text="确认封禁", style="danger.TButton", command=confirm_ban).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="取消", command=dialog.destroy).pack(side=tk.RIGHT)
        
        dialog.transient(ban_win)
        dialog.grab_set()
        dialog.wait_window(ban_win)
    
     def unban_selected():
        """解封选中的用户"""
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("警告", "请先选择要解封的用户", parent=ban_win)
            return
            
        username = tree.item(selected[0], "values")[0]
        if messagebox.askyesno("确认", f"确定要解封用户 {username} 吗?", parent=ban_win):
            if unban_user(username):
                refresh_list()
                messagebox.showinfo("成功", f"已解封用户 {username}", parent=ban_win)
            else:
                messagebox.showerror("错误", f"解封用户 {username} 失败", parent=ban_win)
    
     def update_details(event):
        """更新详情区域"""
        selected = tree.selection()
        if selected:
            values = tree.item(selected[0], "values")
            detail_text.config(state="normal")
            detail_text.delete("1.0", "end")
            detail_text.insert("end", f"用户名: {values[0]}\n")
            detail_text.insert("end", f"封禁原因: {values[1]}")
            detail_text.config(state="disabled")
    
     def search_users():
        """搜索用户"""
        query = search_entry.get().lower()
        if not query:
            refresh_list()
            return
            
        for item in tree.get_children():
            values = tree.item(item, "values")
            if query in values[0].lower() or query in values[1].lower():
                tree.selection_set(item)
                tree.see(item)
                break
    
     def export_list():
        """导出封禁列表"""
        with open("banned_users_export.txt", "w", encoding="utf-8") as f:
            for item in tree.get_children():
                username, reason = tree.item(item, "values")
                f.write(f"{username},{reason}\n")
        messagebox.showinfo("导出成功", "封禁列表已导出为 banned_users_export.txt", parent=ban_win)
    
    # 绑定事件
     tree.bind("<<TreeviewSelect>>", update_details)
     search_entry.bind("<KeyRelease>", lambda e: search_users())
    
    # 初始加载
     refresh_list()
    
     ban_win.mainloop()

    # 封禁管理按钮
    ttk.Button(button_frame, text="封禁管理", command=open_ban_management).pack(side=tk.LEFT, padx=5)
    def admin_create_user_panel(username,pwd):
     """管理员用户主页"""
     user_window = tk.Tk()
     user_window.title(f"用户中心 - {username}")
     user_window.geometry("500x400")
    
     main_frame = ttk.Frame(user_window, padding="20")
     main_frame.pack(fill=tk.BOTH, expand=True)
    
     ttk.Label(main_frame, text=f"欢迎您，{username}！", font=("Arial", 14, "bold")).pack(pady=20)
     ttk.Label(main_frame, text=f"你的密码是:{pwd}").pack(pady=10)
    # 用户功能区域
     ttk.Button(main_frame,text="浏览器",command=web).pack(pady=10)
     ttk.Button(main_frame, text="修改密码", command=lambda:print("NameError"),state="disabled").pack(pady=10)
     ttk.Button(main_frame, text="退出登录", command=user_window.destroy).pack(pady=20)
    
     user_window.mainloop()
    # 删除用户区域
    delete_frame = ttk.Frame(main_frame)
    delete_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(delete_frame, text="删除用户:").pack(side=tk.LEFT, padx=5)
    entry_delete = ttk.Entry(delete_frame)
    entry_delete.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    def delete_selected():
        """删除指定用户"""
        username = entry_delete.get().strip()
        
        if not username:
            messagebox.showerror("错误", "请输入要删除的用户名")
            return
            
        if username == "admin":
            messagebox.showerror("错误", "不能删除管理员账户")
            return
            
        users = load_users()
        if username not in users:
            messagebox.showerror("错误", "用户不存在")
            return
            
        if messagebox.askyesno("确认", f"确定要删除用户 {username} 吗？"):
            delete_user(username)
    def delete_selected():
        """删除指定用户"""
        username = entry_delete.get().strip()
        
        if not username:
            messagebox.showerror("错误", "请输入要删除的用户名")
            return
            
        if username == "admin":
            messagebox.showerror("错误", "不能删除管理员账户")
            return
            
        users = load_users()
        if username not in users:
            messagebox.showerror("错误", "用户不存在")
            return
            
        if messagebox.askyesno("确认", f"确定要删除用户 {username} 吗？"):
            delete_user(username)
            messagebox.showinfo("成功", "用户已删除")
            entry_delete.delete(0, tk.END)
            refresh_list()
    def admin_more():
        """打开更多功能窗口"""
        more_win = tk.Toplevel(admin_window)
        more_win.title("更多功能")
        more_win.geometry("500x400")
        ttk.Button(more_win, text="进入用户页面", command=lambda:admin_create_user_panel(username="admin_test_user_12345",pwd="test")).pack(pady=10)
        ttk.Button(more_win, text="debug", command=lambda:open_debug_window(level="admin")).pack(pady=10)
        ttk.Button(more_win, text="关闭", command=more_win.destroy).pack(pady=10)
    
    ttk.Button(delete_frame, text="删除用户", command=delete_selected, style="danger.TButton").pack(side=tk.LEFT, padx=5)
    ttk.Button(delete_frame, text="删除所有用户", command=delete_all_users, style="danger.TButton").pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="更多功能", command=admin_more).pack(side=tk.LEFT, padx=5)
    # 禁止名称管理功能
    def open_ban_names_management():
        """打开禁止名称管理窗口"""
        name_win = tk.Toplevel(admin_window)
        name_win.title("禁止注册管理")
        name_win.geometry("500x400")
        
        frame = ttk.Frame(name_win, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # 当前禁止名称列表
        banned_names = load_banned_names()
        ttk.Label(frame, text="禁止注册的名称:", font=('Arial', 12, 'bold')).pack()
        
        listbox = tk.Listbox(frame)
        for name in banned_names:
            listbox.insert(tk.END, name)
        listbox.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 添加/移除区域
        manage_frame = ttk.Frame(frame)
        manage_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(manage_frame, text="名称:").pack(side=tk.LEFT)
        entry_name = ttk.Entry(manage_frame)
        entry_name.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=5)
        
        def on_add_ban():
            name = entry_name.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入名称", parent=name_win)
                return
                
            if ban_name(name):
                listbox.insert(tk.END, name)
                entry_name.delete(0, tk.END)
                messagebox.showinfo("成功", f"已禁止注册名称: {name}", parent=name_win)
            else:
                messagebox.showinfo("提示", f"{name} 已在禁止列表中", parent=name_win)
        
        def on_remove_ban():
            name = entry_name.get().strip()
            if not name:
                messagebox.showerror("错误", "请输入名称", parent=name_win)
                return
                
            if unban_name(name):
                items = listbox.get(0, tk.END)
                for i, item in enumerate(items):
                    if item.lower() == name.lower():
                        listbox.delete(i)
                        break
                entry_name.delete(0, tk.END)
                messagebox.showinfo("成功", f"已允许注册名称: {name}", parent=name_win)
            else:
                messagebox.showinfo("提示", f"{name} 不在禁止列表中", parent=name_win)
        
        ttk.Button(button_frame, text="添加禁止", command=on_add_ban, style="danger.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="移除禁止", command=on_remove_ban, style="success.TButton").pack(side=tk.RIGHT, padx=5)
        
        name_win.mainloop()
    ttk.Button(button_frame, text="注册新用户", command=create_register_window).pack(side=tk.LEFT, padx=5)
    # 禁止名称管理按钮
    ttk.Button(button_frame, text="禁止注册管理", command=open_ban_names_management).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="修改密码", command=admin_change_password_1).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="退出", command=admin_window.destroy).pack(side=tk.RIGHT, padx=5)
def admin_change_password_1():
    """第一步：输入要修改密码的用户名"""
    password_win = tk.Toplevel()
    password_win.title("修改密码 - 输入用户名")
    password_win.geometry("400x300")
    password_win.resizable(False, False)
    
    main_frame = ttk.Frame(password_win, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 标题
    ttk.Label(main_frame, text="修改用户密码", font=("Arial", 16, "bold")).pack(pady=10)
    
    # 用户名输入部分
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(pady=20, fill=tk.X)
    
    ttk.Label(input_frame, text="请输入要修改的用户名:").pack(anchor="w")
    username_var = tk.StringVar()
    entry_username = ttk.Entry(input_frame, textvariable=username_var, width=25)
    entry_username.pack(pady=10, fill=tk.X)
    
    # 用户名验证状态显示
    status_label = ttk.Label(input_frame, text="", foreground="red")
    status_label.pack(anchor="w")
    
    # 按钮区域
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)
    
    def verify_username():
        username = username_var.get().strip()
        users = load_users()
        
        if not username:
            status_label.config(text="用户名不能为空", foreground="red")
            return
        
        if username.lower() not in [u.lower() for u in users]:
            status_label.config(text="用户名不存在", foreground="red")
            return
        
        # 用户存在，打开密码修改窗口
        password_win.destroy()
        admin_change_password(username)
    
    ttk.Button(button_frame, text="下一步", command=verify_username, width=15).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="取消", command=password_win.destroy, width=15).pack(side=tk.RIGHT, padx=5)

def admin_change_password(username):
    """管理员修改用户密码"""
    password_win = tk.Toplevel()
    password_win.title(f"修改密码 - {username}")
    password_win.geometry("600x600")

    main_frame = ttk.Frame(password_win, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 标题
    ttk.Label(main_frame, text=f"正在修改 {username} 的密码", font=("Arial", 14, "bold")).pack(pady=10)
    
    # 密码输入部分
    input_frame = ttk.Frame(main_frame)
    input_frame.pack(pady=10, fill=tk.X)
    
    # 新密码
    ttk.Label(input_frame, text="新密码 (至少6位):").pack(anchor="w")
    password_var = tk.StringVar()
    entry_password = ttk.Entry(input_frame, textvariable=password_var, show="*", width=25)
    entry_password.pack(pady=5, fill=tk.X)
    
    # 密码强度显示
    password_strength = ttk.Label(input_frame, text="", foreground="red")
    password_strength.pack(anchor="w")
    
    # 确认密码
    ttk.Label(input_frame, text="确认新密码:").pack(anchor="w", pady=(10, 0))
    confirm_var = tk.StringVar()
    entry_confirm = ttk.Entry(input_frame, textvariable=confirm_var, show="*", width=25)
    entry_confirm.pack(pady=5, fill=tk.X)
    
    # 密码匹配状态
    confirm_status = ttk.Label(input_frame, text="", foreground="red")
    confirm_status.pack(anchor="w")
    
    # 状态显示
    status_label = ttk.Label(main_frame, text="", foreground="red")
    status_label.pack(pady=10)
    
    def check_password():
        """实时检查密码强度"""
        password = password_var.get()
        
        if not password:
            password_strength.config(text="密码不能为空", foreground="red")
            return False
        
        if len(password) < 6:
            password_strength.config(text="密码至少需要6位", foreground="red")
            return False
        
        password_strength.config(text="✔ 密码强度合格", foreground="green")
        return True
    
    def check_match():
        """检查密码是否匹配"""
        password = password_var.get()
        confirm = confirm_var.get()
        
        if password and confirm and password == confirm:
            confirm_status.config(text="✔ 密码匹配", foreground="green")
            return True
        elif confirm:
            confirm_status.config(text="两次输入的密码不一致", foreground="red")
            return False
        else:
            confirm_status.config(text="请再次输入密码", foreground="red")
            return False
    
    # 实时验证
    password_var.trace_add("write", lambda *args: (check_password(), check_match()))
    confirm_var.trace_add("write", lambda *args: check_match())
    
    # 按钮区域
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)
    
    def save_new_password():
        """保存新密码"""
        if not (check_password() and check_match()):
            status_label.config(text="请检查密码设置是否正确", foreground="red")
            return
        
        try:
            # 加载现有用户
            users = load_users()
            
            # 更新密码
            users[username] = password_var.get()
            
            # 保存到文件
            with open("user.txt", "w") as f:
                for user, pwd in users.items():
                    f.write(f"{user},{pwd}\n")
            
            status_label.config(text="密码修改成功!", foreground="green")
            password_win.after(1500, password_win.destroy)
        except Exception as e:
            status_label.config(text=f"保存失败: {str(e)}", foreground="red")
    
    ttk.Button(button_frame, text="确认修改", command=save_new_password, width=15, style="success.TButton").pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="取消", command=password_win.destroy, width=15).pack(side=tk.RIGHT, padx=5)
    
def create_register_window(parent=None):
    """注册新用户窗口"""
    register_win = tk.Toplevel(parent) if parent else tk.Tk()
    register_win.title("用户注册")
    register_win.geometry("700x700")
    
    main_frame = ttk.Frame(register_win, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(main_frame, text="新用户注册", font=("Arial", 16, "bold")).pack(pady=10)
    
    # 表单框架
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(fill=tk.BOTH, expand=True)
    
    # 用户名
    ttk.Label(form_frame, text="用户名(小于10字符):").pack(pady=2, anchor="w")
    entry_username = ttk.Entry(form_frame, width=30)
    entry_username.pack(pady=2, fill=tk.X)
    
    # 实时检查用户名可用性
    username_status = ttk.Label(form_frame, text="", foreground="red")
    username_status.pack(pady=2, anchor="w")
    
    def check_username_availability():
        username = entry_username.get().strip()
        if username == "debug_user":
            username_status.config(text="用户名已存在", foreground="red")
            return False
        if username == "admin":
            username_status.config(text="不能注册管理员账号", foreground="red")
            return False
        if len(username) > 10:
            username_status.config(text="用户名不能超过10个字符", foreground="red")
            return False
        if username == "superadmin":
            username_status.config(text="不能注册管理员账号", foreground="red")
            return False
        if not username:
            username_status.config(text="用户名不能为空", foreground="red")
            return False
        valid, msg = is_valid_username(username)
        if not valid:
            username_status.config(text=msg, foreground="red")
            return False
        users = load_users()
        if username.lower() in [u.lower() for u in users]:
            username_status.config(text="该用户名已被注册", foreground="red")
            return False
        username_status.config(text="✔ 该用户名可用", foreground="green")
        return True
    
    entry_username.bind("<KeyRelease>", lambda e: check_username_availability())
    
    # 密码
    ttk.Label(form_frame, text="密码(至少6位):").pack(pady=2, anchor="w")
    entry_password = ttk.Entry(form_frame, width=30, show="*")
    entry_password.pack(pady=2, fill=tk.X)
    
    password_status = ttk.Label(form_frame, text="", foreground="red")
    password_status.pack(pady=2, anchor="w")
    
    def check_password_strength():
        password = entry_password.get().strip()
        if not password:
            password_status.config(text="密码不能为空", foreground="red")
            return False
        valid, msg = is_valid_password(password)
        if not valid:
            password_status.config(text=msg, foreground="red")
            return False
        # 强化密码校验规则
        if len(password) < 6:
            password_status.config(text="密码长度至少为6位", foreground="red")
            return False
        password_status.config(text="✔ 密码强度合格", foreground="green")
        return True
    
    entry_password.bind("<KeyRelease>", lambda e: check_password_strength())
    
    # 确认密码
    ttk.Label(form_frame, text="确认密码:").pack(pady=2, anchor="w")
    entry_confirm = ttk.Entry(form_frame, width=30, show="*")
    entry_confirm.pack(pady=2, fill=tk.X)
    
    confirm_status = ttk.Label(form_frame, text="", foreground="red")
    confirm_status.pack(pady=2, anchor="w")
    
    def check_password_match():
        confirm = entry_confirm.get()
        password = entry_password.get()
        if password != confirm:
            confirm_status.config(text="两次输入的密码不一致", foreground="red")
            return False
        if confirm:
            confirm_status.config(text="✔ 密码匹配", foreground="green")
            return True
        confirm_status.config(text="请再次输入密码", foreground="red")
        return False
    
    entry_confirm.bind("<KeyRelease>", lambda e: check_password_match())
    
    # 安全问题
    ttk.Label(form_frame, text="安全问题 (用于找回密码):").pack(pady=(10,2), anchor="w")
    security_question = ttk.Combobox(form_frame, values=[
        "你的第一只宠物叫什么名字？",
        "你的出生地在哪？",
        "你的母亲姓氏是什么？",
        "你的中学名称？",
        "你的兴趣爱好是什么？",
        "你的生日是哪一天？",
        "你的父亲名字是什么？",
        "你的最好朋友叫什么名字？",
        "你的第一辆车是什么品牌？",
        "你的第一辆车的型号是什么？",
        "你的出生日期是什么？"
    ])
    security_question.pack(pady=2, fill=tk.X)
    
    ttk.Label(form_frame, text="安全答案:").pack(pady=2, anchor="w")
    security_answer = ttk.Entry(form_frame, width=30)
    security_answer.pack(pady=2, fill=tk.X)
    
    # 注册按钮
    def register():
        """注册新用户"""
        username = entry_username.get().strip()
        password = entry_password.get()
        confirm = entry_confirm.get()
        question = security_question.get()
        answer = security_answer.get().strip()
        
        # 验证所有输入是否合法
        if not (check_username_availability() and check_password_strength() and check_password_match()):
            messagebox.showerror("错误", "请检查填写内容是否正确", parent=register_win)
            return
        
        if not question:
            messagebox.showerror("错误", "请选择安全问题", parent=register_win)
            return
        
        if not answer:
            messagebox.showerror("错误", "安全答案不能为空", parent=register_win)
            return
        
        # 保存用户信息
        try:
            save_user(username, password)
            save_security_question(username, question, answer)
            messagebox.showinfo("成功", "注册成功！请牢记您的账号和安全信息", parent=register_win)
            register_win.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"注册失败: {str(e)}", parent=register_win)
    
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=20)
    
    ttk.Button(button_frame, text="注册新用户", command=register, width=15, style="success.TButton").pack(pady=5)
    
    if not parent:
        register_win.mainloop()

def create_recover_window():
    """找回密码窗口"""
    recover_win = tk.Toplevel()
    recover_win.title("找回密码")
    recover_win.geometry("600x500")
    
    main_frame = ttk.Frame(recover_win, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(main_frame, text="忘记密码", font=("Arial", 16, "bold")).pack(pady=10)
    
    # 步骤1：验证用户名
    step1_frame = ttk.LabelFrame(main_frame, text="第一步：验证账号", padding="10")
    step1_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(step1_frame, text="请输入您的用户名:").pack(anchor="w", pady=2)
    entry_username = ttk.Entry(step1_frame, width=30)
    entry_username.pack(fill=tk.X, pady=5)
    
    # 步骤2：验证安全问题
    step2_frame = ttk.LabelFrame(main_frame, text="第二步：验证身份", padding="10")
    step2_frame.pack_forget()  # 初始隐藏
    
    question_label = ttk.Label(step2_frame, text="安全问题:")
    question_label.pack(anchor="w", pady=2)
    
    answer_var = tk.StringVar()
    answer_entry = ttk.Entry(step2_frame, width=30, textvariable=answer_var)
    answer_entry.pack(fill=tk.X, pady=5)
    
    # 步骤3：设置新密码
    step3_frame = ttk.LabelFrame(main_frame, text="第三步：设置新密码", padding="10")
    step3_frame.pack_forget()  # 初始隐藏
    
    ttk.Label(step3_frame, text="新密码 (至少6位):").pack(anchor="w", pady=2)
    new_password_entry = ttk.Entry(step3_frame, width=30, show="*")
    new_password_entry.pack(fill=tk.X, pady=5)
    
    ttk.Label(step3_frame, text="确认新密码:").pack(anchor="w", pady=2)
    confirm_password_entry = ttk.Entry(step3_frame, width=30, show="*")
    confirm_password_entry.pack(fill=tk.X, pady=5)
    
    status_label = ttk.Label(main_frame, text="", foreground="red")
    status_label.pack(pady=10)
    
    current_username = None
    users = load_users()
    questions = load_security_questions()
    banned_users = load_banned_users()
    
    def on_step1():
        """验证用户名"""
        nonlocal current_username
        username = entry_username.get().strip()
        
        if not username:
            status_label.config(text="用户名不能为空", foreground="red")
            return
        
        # 检查是否被禁止
        if username.lower() in [u.lower() for u in banned_users]:
            status_label.config(text="该账号已被禁止登录", foreground="red")
            return
        
        # 检查用户是否存在
        if username.lower() not in [u.lower() for u in users]:
            status_label.config(text="用户名不存在", foreground="red")
            return
        
        # 检查是否设置过安全问题
        if username.lower() not in [u.lower() for u in questions]:
            status_label.config(text="该账号未设置安全问题，无法找回密码", foreground="red")
            return
        
        # 记录当前用户并显示安全问题
        current_username = next(u for u in questions if u.lower() == username.lower())
        question_label.config(text=f"安全问题: {questions[current_username]['question']}")
        
        step1_frame.pack_forget()
        step2_frame.pack(fill=tk.X, pady=5)
        status_label.config(text="", foreground="red")
    
    def on_step2():
        """验证安全问题"""
        answer = answer_var.get().strip()
        
        # 检查安全问题答案
        if answer.lower() != questions[current_username]['answer'].lower():
            status_label.config(text="安全答案错误", foreground="red")
            return
        
        step2_frame.pack_forget()
        step3_frame.pack(fill=tk.X, pady=5)
        status_label.config(text="", foreground="red")
    
    def on_step3():
        """设置新密码"""
        password = new_password_entry.get()
        confirm = confirm_password_entry.get()
        
        if not password or not confirm:
            status_label.config(text="密码不能为空", foreground="red")
            return
        
        if password != confirm:
            status_label.config(text="两次输入的密码不一致", foreground="red")
            return
        
        if len(password) < 6:
            status_label.config(text="密码至少需要6位", foreground="red")
            return
        
        # 更新密码
        try:
            # 先删除原用户
            del users[current_username]
            with open("user.txt", "w") as f:
                for user, pwd in users.items():
                    f.write(f"{user},{pwd}\n")
            
            # 添加新密码
            users[current_username] = password
            with open("user.txt", "a") as f:
                f.write(f"{current_username},{password}\n")
            
            status_label.config(text="密码重置成功！请使用新密码登录", foreground="green")
            recover_win.after(2000, recover_win.destroy)
        except Exception as e:
            status_label.config(text=f"操作失败: {str(e)}", foreground="red")
    
    # 按钮区域
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=10)
    
    ttk.Button(step1_frame, text="下一步", command=on_step1, width=15).pack(pady=5)
    ttk.Button(step2_frame, text="下一步", command=on_step2, width=15).pack(pady=5)
    
    button_frame2 = ttk.Frame(step3_frame)
    button_frame2.pack(pady=5)
    
    ttk.Button(button_frame2, text="确认修改", command=on_step3, width=15, style="success.TButton").pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame2, text="取消", command=recover_win.destroy, width=15).pack(side=tk.RIGHT, padx=5)
    
    recover_win.mainloop()
    
if __name__ == "__main__":
    create_login_window()
