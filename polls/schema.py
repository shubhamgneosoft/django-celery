import graphene
from graphene_django import DjangoObjectType

from .models import Question, Choice


class QuestionSchema(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "question_text", "pub_date")


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = ("id", "question", "choice_text", "votes")


class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionSchema)
    choice_by_choice_text = graphene.Field(ChoiceType, choice_text=graphene.String(required=True))

    def resolve_all_questions(root, info):
        # We can easily optimize query count in the resolve method
        return Question.objects.all()

    def resolve_choice_by_choice_text(root, info, choice_text):
        try:
            return Choice.objects.get(choice_text=choice_text)
        except Choice.DoesNotExist:
            return None


schema = graphene.Schema(query=Query)