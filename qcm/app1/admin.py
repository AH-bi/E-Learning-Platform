from django.contrib import admin
from .models import Category,Domain,Question,Subcategory,CorrectAnswer,Score,Feedback
from django.forms import formset_factory
from .form import CorrectAnswerForm
from django.contrib.auth.models import Group 


# Register your models here.






admin.site.unregister(Group)


class ScoreAdmin(admin.ModelAdmin):
    list_display=('user','score','domain','subcategory','category')
        
    def domain(self, obj):
        return obj.domain if obj.domain else '-'
    domain.short_description = 'Domain'

    def category(self, obj):
        return obj.category if obj.category else '-'
    category.short_description = 'Category'

    def subcategory(self, obj):
        return obj.subcategory if obj.subcategory else '-'
    subcategory.short_description = 'Subcategory'


admin.site.register(Score,ScoreAdmin)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'description')

admin.site.register(Domain, DomainAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('domain', 'name', 'description')
    list_filter=('domain',)

admin.site.register(Category, CategoryAdmin)

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','category','description')
    list_filter=('category',)



    def description(self, obj):
        return obj.description if obj.description else '-'


admin.site.register(Subcategory, SubcategoryAdmin)










class CorrectAnswerInline(admin.TabularInline):
    model = CorrectAnswer
    form = CorrectAnswerForm
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [CorrectAnswerInline]
    list_display=['id','question','subcategory','category']
    list_filter =('domain', 'category', 'subcategory')
    
    
    def domain(self, obj):
        return obj.domain if obj.domain else '-'
    domain.short_description = 'Domain'

    def category(self, obj):
        return obj.category if obj.category else '-'
    category.short_description = 'Category'

    def subcategory(self, obj):
        return obj.subcategory if obj.subcategory else '-'
    subcategory.short_description = 'Subcategory'




admin.site.register(Question, QuestionAdmin)    


class CorrectAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

admin.site.register(CorrectAnswer, CorrectAnswerAdmin)



admin.site.register(Feedback)



admin.site.site_header="Quiz administration"


"""admin.site.register(Category)
admin.site.register(Domain)
admin.site.register(Subcategory)

class AnswerInline(admin.TabularInline):
    model=CorrectAnswer


class AdminQuestion(admin.ModelAdmin):
    inlines=[AnswerInline]
    list_display=['id','question','subcategory','category']






admin.site.register(Question,AdminQuestion)
admin.site.register(CorrectAnswer)









class QuestionAdmin(admin.ModelAdmin):
    list_display = ('domain', 'category', 'subcategory', 'question')
    list_filter =('domain', 'category', 'subcategory')

"""


