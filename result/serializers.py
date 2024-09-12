# serializers.py
from rest_framework import serializers
from .models import ExamType, Result, Syllabus



class SyllabusSerializer(serializers.ModelSerializer):
    get_data = serializers.CharField(source='get_dataa', read_only=True)

    class Meta:
        model = Syllabus
        fields = ['id', 'classroom', 'subject', 'teacher', 'get_data']

    def validate(self, data):
        teacher = data.get('teacher')
        subject = data.get('subject')
        classroom = data.get('classroom')

        if Syllabus.objects.filter(classroom=classroom, subject=subject, teacher=teacher).exists():
            raise serializers.ValidationError(
                "This combination of classroom, subject, and teacher already exists."
            )

        if not teacher.subject.filter(id=subject.id).exists():
            raise serializers.ValidationError("This Teacher does not teach the selected subject.")

        return data

    def __init__(self, *args, **kwargs):
        super(SyllabusSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = '__all__'

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(ResultSerializer, self).__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and request.method == "POST":
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2