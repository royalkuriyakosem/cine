from django.contrib import admin
from .models import Production, Scene, Shot, BudgetLine, ScriptBreakdown

@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'owner')
    list_filter = ('status',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'production', 'location')
    list_filter = ('production',)
    search_fields = ('title',)

@admin.register(Shot)
class ShotAdmin(admin.ModelAdmin):
    list_display = ('shot_number', 'scene', 'status', 'assigned_to')
    list_filter = ('status', 'assigned_to')
    search_fields = ('description',)

@admin.register(BudgetLine)
class BudgetLineAdmin(admin.ModelAdmin):
    list_display = ('category', 'production', 'estimated_amount', 'actual_amount', 'approved')
    list_filter = ('approved', 'production')
    search_fields = ('category', 'vendor')

@admin.register(ScriptBreakdown)
class ScriptBreakdownAdmin(admin.ModelAdmin):
    list_display = ('production', 'created_at')
    list_filter = ('production', 'created_at')
    search_fields = ('notes',)
