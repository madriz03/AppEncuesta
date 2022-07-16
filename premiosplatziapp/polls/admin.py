from django.contrib import admin
from .models import Question, Choice

# Register your models here.

#Esta clase permite establecer cuantas respuestas se pueden mostrar y se vincula con la clase Question.
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1

#Esta clase nos permite personalizar como se va a ver el modelo Question en el administrador, hereda de la clase admin que se importo y se accede al modelo .ModelAdmin

class QuestionAdmin(admin.ModelAdmin):
    fields = ['pub_date', 'question_text']
    inlines = [ChoiceInline] #Vinculacion de choice y cuestion
    list_display = ('question_text', 'pub_date', 'was_published_recently') #Lo q se mostrara
    list_filter = ['pub_date'] #Lo que se filtrara
    search_fields = ['question_text'] #Barra de busqueda de preguntas


#Esta hereda de la clase anterior donde se definio el orden en que se mostraran los atributos del modelo en el administrador
admin.site.register(Question,QuestionAdmin) 
admin.site.register(Choice)