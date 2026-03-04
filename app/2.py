import frida

# 获取远程设备（你的手机）
rdev = frida.get_remote_device()

# 调用 enumerate_processes() 方法，获取正在运行的进程列表
progress = rdev.enumerate_processes() # <--- 看这里，加上了圆括号！

# 遍历并打印出每一个进程的信息
for p in progress:
    print(p)