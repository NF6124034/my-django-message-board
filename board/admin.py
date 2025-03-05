from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'message', 'created_at')  # 顯示哪些欄位
    search_fields = ('name', 'message')  # 可以搜尋哪些欄位
    list_filter = ('created_at',)  # 可以用哪些欄位篩選
    ordering = ('-created_at',)  # 預設排序（最新留言在最上）
