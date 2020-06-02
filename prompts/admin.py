from django.contrib import admin

# Register your models here.
from .models import Prompt, PromptLike, Template, TemplateTag, Tag

class TemplateTagAdmin(admin.TabularInline):
    model = TemplateTag

class TemplateAdmin(admin.ModelAdmin):
	inlines = [TemplateTagAdmin]
	class Meta:
		model = Template

class PromptLikeAdmin(admin.TabularInline):
    model = PromptLike

class PromptAdmin(admin.ModelAdmin):
    inlines = [PromptLikeAdmin]
    list_display = ['__str__', 'user']
    search_fields = ['content', 'user__username', 'user__email']
    class Meta:
        model = Prompt

admin.site.register(Prompt, PromptAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(Tag)