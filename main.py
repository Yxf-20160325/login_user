import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox
import os
import yagmail

# ====================== 数据操作函数 ======================
def load_users():
    """加载用户数据(user.txt格式: 用户名,密码)"""
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

def load_security_questions():
    """加载安全问题"""
    if not os.path.exists("user_问题.txt"):
        return {}  # 直接返回空字典，避免递归
        
    questions = {}
    with open("user_问题.txt", "r", encoding='utf-8') as f:  # 确保只读
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
    return questions  # 确保这里是纯数据加载，不调用其他函数


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

# ====================== 界面函数 ======================
def create_login_window():
    """登录窗口"""
    root = tk.Tk()
    root.title("系统登录")
    root.geometry("600x600")
    
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
    
     if not username or not password:
        messagebox.showerror("错误", "用户名和密码不能为空")
        return
        
     users = load_users()
     if username == "superadmin" and password == "superadmin":
        # 先创建新窗口
        create_admin_panel()
        # 然后销毁原窗口
        root.destroy()
        superadmin()
        def superadmin():
            create_admin_panel()
            
            
     if username == "admin" and password == "admin":
        # 先创建新窗口
        create_admin_panel()
        # 然后销毁原窗口
        root.destroy()
     elif username in users and users[username] == password:
        # 先创建新窗口
        create_user_panel(username)
        # 然后销毁原窗口
        root.destroy()
     else:
        messagebox.showerror("错误", "用户名或密码错误")
    def email():
        root_telephone = tk.Tk()
        root_telephone.title("联系我们")
        root_telephone.geometry("400x300")
        ttk.Label(root_telephone, text="我们的邮箱地址：Yxf52013141@outlook.com").pack(pady=10)
        root_telephone.mainloop()
    ttk.Button(button_frame, text="登录", command=login, width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="注册", command=lambda: create_register_window(root), width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="找回密码", command=create_recover_window, width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="退出", command=root.destroy, width=10).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="联系我们", command=email, width=10).pack(side=tk.LEFT, padx=5)
    root.mainloop()

def create_user_panel(username):
    """用户主页"""
    user_window = tk.Tk()
    user_window.title(f"用户中心 - {username}")
    user_window.geometry("500x400")
    
    main_frame = ttk.Frame(user_window, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(main_frame, text=f"欢迎您，{username}！", font=("Arial", 14, "bold")).pack(pady=20)
    
    # 用户功能区域
    ttk.Button(main_frame, text="退出登录", command=user_window.destroy).pack(pady=20)
    
    user_window.mainloop()

def create_admin_panel():
    """管理员控制台"""
    admin_window = tk.Tk()
    admin_window.title("管理员控制台")
    admin_window.geometry("900x800")
    
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
            text_area.insert(tk.END, f"密码: {(pwd)}\n")
            
            if username in questions:
                text_area.insert(tk.END, f"安全问题: {questions[username]['question']}\n")
                text_area.insert(tk.END, f"安全答案: {questions[username]['answer']}\n")
            else:
                text_area.insert(tk.END, "安全提示: 未设置安全问题\n")
            
            text_area.insert(tk.END, "-"*60 + "\n\n")
        
        text_area.config(state=tk.DISABLED)
    
    def refresh_list():
        """刷新用户列表"""
        load_all_users()
    
    def delate_all_user():
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
            messagebox.showinfo("成功", f"用户 {username} 已删除")
            entry_delete.delete(0, tk.END)
            refresh_list()
            
    ttk.Button(delete_frame, text="删除", command=delete_selected, style="danger.TButton").pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="删除所有用户", command=delate_all_user).pack(side=tk.RIGHT, padx=5)
    
    # 初始加载用户列表
    refresh_list()
    
    ttk.Button(main_frame, text="退出", command=admin_window.destroy, style="primary.TButton").pack(pady=10)
    
    admin_window.mainloop()

    def refresh_list():
        load_users
    def delate_all_user():
        if messagebox.askyesno("确认", "确定要删除所有用户吗？"):
          open("user.txt", "w").close()
          open("user_问题.txt", "w").close()
          messagebox.showinfo("提示", "删除成功")   
          refresh_list()         
    # 控制按钮区域
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=5)
    
    ttk.Button(button_frame, text="刷新列表", command=refresh_list).pack(side=tk.LEFT, padx=5)
    
    # 删除用户区域
    delete_frame = ttk.Frame(main_frame)
    delete_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(delete_frame, text="删除用户:").pack(side=tk.LEFT, padx=5)
    entry_delete = ttk.Entry(delete_frame)
    entry_delete.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    def delete_selected():
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
            messagebox.showinfo("成功", f"用户 {username} 已删除")
            entry_delete.delete(0, tk.END)
            refresh_list()
            
    ttk.Button(delete_frame, text="删除", command=delete_selected, style="danger.TButton").pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="删除所有用户", command=delate_all_user).pack(side=tk.RIGHT, padx=5)
    # 初始加载用户列表
    refresh_list()
    
    ttk.Button(main_frame, text="退出", command=admin_window.destroy, style="primary.TButton").pack(pady=10)
    
    admin_window.mainloop()


    def refresh_list():
        load_all_users(text_area)
        
    ttk.Button(button_frame, text="刷新列表", command=refresh_list).pack(side=tk.LEFT, padx=5)
    
    # 删除用户区域
    delete_frame = ttk.Frame(main_frame)
    delete_frame.pack(fill=tk.X, pady=5)
    
    ttk.Label(delete_frame, text="删除用户:").pack(side=tk.LEFT, padx=5)
    entry_delete = ttk.Entry(delete_frame)
    entry_delete.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
    
    def delete_selected():
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
            messagebox.showinfo("成功", f"用户 {username} 已删除")
            entry_delete.delete(0, tk.END)
            refresh_list()
    
    ttk.Button(delete_frame, text="删除", command=delete_selected, style="danger.TButton").pack(side=tk.RIGHT, padx=5)
    
    # 用户列表显示区域
    list_frame = ttk.Frame(main_frame)
    list_frame.pack(fill=tk.BOTH, expand=True)
    
    scroll_y = ttk.Scrollbar(list_frame)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    
    text_area = tk.Text(list_frame, yscrollcommand=scroll_y.set, wrap=tk.WORD)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    scroll_y.config(command=text_area.yview)
    
    def load_all_users(text_widget):
        """加载用户数据到文本框"""
        users = load_users()
        questions = load_security_questions()
        
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        
        if not users:
            text_widget.insert(tk.END, "当前没有用户数据")
            return
            
        text_widget.insert(tk.END, f"共 {len(users)} 位用户\n\n")
        text_widget.insert(tk.END, "="*60 + "\n\n")
        
        for username, pwd in users.items():
            text_widget.insert(tk.END, f"用户名: {username}\n")
            text_widget.insert(tk.END, f"密码: {'*'*len(pwd)}\n")
            
            if username in questions:
                text_widget.insert(tk.END, f"安全问题: {questions[username]['question']}\n")
            else:
                text_widget.insert(tk.END, "安全提示: 未设置安全问题\n")
            
            text_widget.insert(tk.END, "-"*60 + "\n\n")
        
        text_widget.config(state=tk.DISABLED)
    
    # 初始加载用户列表
    refresh_list()
    
    ttk.Button(main_frame, text="退出", command=admin_window.destroy, style="primary.TButton").pack(pady=10)
    
    admin_window.mainloop()
def load_all_users(text_widget):
        """加载用户数据到文本框"""
        users = load_users()
        questions = load_security_questions()
        
        text_widget.config(state=tk.NORMAL)
        text_widget.delete(1.0, tk.END)
        
        if not users:
            text_widget.insert(tk.END, "当前没有用户数据")
            return
            
        text_widget.insert(tk.END, f"共 {len(users)} 位用户\n\n")
        text_widget.insert(tk.END, "="*60 + "\n\n")
        
        for username, pwd in users.items():
            text_widget.insert(tk.END, f"用户名: {username}\n")
            text_widget.insert(tk.END, f"密码: {'*'*len(pwd)}\n")
            
            if username in questions:
                text_widget.insert(tk.END, f"安全问题: {questions[username]['question']}\n")
            else:
                text_widget.insert(tk.END, "安全提示: 未设置安全问题\n")
            
            text_widget.insert(tk.END, "-"*60 + "\n\n")
        
        text_widget.config(state=tk.DISABLED)
def create_register_window(parent):
    """注册窗口"""
    win = tk.Toplevel(parent)
    win.title("新用户注册")
    win.geometry("450x450")
    win.resizable(False, False)
    
    main_frame = ttk.Frame(win, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    ttk.Label(main_frame, text="新用户注册", font=('Arial', 14, 'bold')).pack(pady=(0, 15))
    
    # 表单区域
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(fill=tk.X, pady=5)
    
    # 用户名
    ttk.Label(form_frame, text="用户名:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
    entry_user = ttk.Entry(form_frame)
    entry_user.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
    
    # 密码
    ttk.Label(form_frame, text="密码(至少6位):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_pass = ttk.Entry(form_frame, show="*")
    entry_pass.grid(row=1, column=1, sticky='ew', padx=5, pady=5)
    
    # 安全问题
    ttk.Label(form_frame, text="安全问题:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
    security_questions = [
        "你的小学名称是什么？",
        "你的第一只宠物叫什么？",
        "你的出生城市是哪里？",
        "你母亲的名字是什么？",
        "你父亲的名字是什么？",
        "你最喜爱的电影是什么？",
        "你的第一辆车是哪一辆？",
        "你的理想工作是什么？",
        "你的最高学历是哪一层次？",
        "你的出生日期是多少？",
        "你的出生月份是什么？",
        "你的出生年份是多少？",
        "你的父亲的出生日期是多少？",
        "你的秘密是什么？",
        "你最喜爱的食物是什么？"

    ]
    question_var = tk.StringVar(value=security_questions[0])
    ttk.OptionMenu(form_frame, question_var, *security_questions).grid(row=2, column=1, sticky='ew', padx=5, pady=5)
    
    # 安全答案
    ttk.Label(form_frame, text="安全问题答案:").grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_answer = ttk.Entry(form_frame)
    entry_answer.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
    
    # 注册按钮
    def on_register():
        username = entry_user.get().strip()
        password = entry_pass.get()
        question = question_var.get()
        answer = entry_answer.get().strip()
        
        if not all([username, password, answer]):
            messagebox.showerror("错误", "所有字段都必须填写", parent=win)
            return
            
        if len(password) < 6:
            messagebox.showerror("错误", "密码长度不能少于6位", parent=win)
            return
            
        users = load_users()
        if username in users:
            messagebox.showerror("错误", "该用户名已被使用", parent=win)
            return
        if username == "admin":
            messagebox.showerror("错误", "用户名不能为admin", parent=win)
            return  
        # 保存用户数据
        save_user(username, password)
        
        # 保存安全问题
        save_security_question(username, question, answer)
        
        messagebox.showinfo("成功", "注册成功！", parent=win)
        win.destroy()
    
    ttk.Button(main_frame, text="立即注册", command=on_register, style='success.TButton').pack(pady=15)

def create_recover_window():
    """找回密码窗口"""
    win = tk.Toplevel()
    win.title("找回密码")
    win.geometry("450x350")
    win.resizable(False, False)
    
    main_frame = ttk.Frame(win, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    current_step = tk.IntVar(value=1)
    username = tk.StringVar()
    question = tk.StringVar()
    
    # 第1步：输入用户名
    def create_step1():
        frame = ttk.Frame(main_frame)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="找回密码 - 第一步", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        ttk.Label(frame, text="请输入您的用户名:").pack(pady=5)
        entry_user = ttk.Entry(frame, textvariable=username)
        entry_user.pack(pady=5, fill=tk.X)
        
        def next_step():
            uname = username.get().strip()
            if not uname:
                messagebox.showerror("错误", "请输入用户名", parent=win)
                return
                
            ques_data = load_security_questions()
            if uname not in ques_data:
                messagebox.showerror("错误", "该用户未设置安全问题/无此用户", parent=win)
                return
            if uname == "admin":
                messagebox.showerror("错误", "管理员账户无法找回密码", parent=win)
                return
            
            question.set(ques_data[uname]['question'])
            current_step.set(2)
            frame.destroy()
            create_step2()
        
        ttk.Button(frame, text="下一步", command=next_step).pack(pady=15)
        return frame
    
    # 第2步：验证安全问题
    def create_step2():
        frame = ttk.Frame(main_frame)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="找回密码 - 第二步", font=('Arial', 14, 'bold')).pack(pady=(0, 20))
        
        ttk.Label(frame, text=f"安全问题: {question.get()}").pack(pady=5)
        
        ttk.Label(frame, text="请输入您的答案:").pack(pady=5)
        entry_answer = ttk.Entry(frame)
        entry_answer.pack(pady=5, fill=tk.X)
        
        def verify():
            answer = entry_answer.get().strip()
            ques_data = load_security_questions()
            user_data = load_users()
            
            uname = username.get()
            if ques_data[uname]['answer'] == answer:
                if uname in user_data:
                    messagebox.showinfo("找回成功", 
                                      f"您的密码是: {user_data[uname]}", 
                                      parent=win)
                    messagebox.showinfo("提示", "请妥善保管您的密码", parent=win)
                    
                    win.destroy()
                   
                else:
                    messagebox.showerror("错误", "用户数据不完整", parent=win)
            else:
                messagebox.showerror("错误", "安全问题答案不正确", parent=win)
                
        ttk.Button(frame, text="上一步", command=lambda: current_step.set(1)).pack(side=tk.LEFT, padx=5, pady=15)
        ttk.Button(frame, text="验证", command=verify).pack(side=tk.RIGHT, padx=5, pady=15)
        return frame
    
    # 初始显示第一步
    create_step1()
    win.mainloop()

# ====================== 程序入口 ======================
if __name__ == "__main__":
    create_login_window()
