Set WshShell = CreateObject("WScript.Shell")
pythonExe = """D:\project\gitee\py\py-script\.venv\Scripts\python.exe"""
scriptPath = """D:\project\gitee\snb2025\snbBook\imageScript\main.py"""
WshShell.Run pythonExe & " " & scriptPath, 0
Set WshShell = Nothing