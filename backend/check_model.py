# backend/check_models.py
import google.generativeai as genai
import os

# 把你的 API Key 貼在這裡
API_KEY = "AIzaSyBMOSuY5F-H_pPPp485y5Rw9YsGTIaHr6g" 
genai.configure(api_key=API_KEY)

print("正在查詢可用模型...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"發生錯誤: {e}")