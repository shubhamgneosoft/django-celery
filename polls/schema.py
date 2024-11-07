import datetime

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


class QuestionInput(graphene.InputObjectType):
    id = graphene.ID()
    question_text = graphene.String()
    pub_date = graphene.DateTime()


class CreateQuestion(graphene.Mutation):
    class Arguments:
        question_data = QuestionInput(required=True)

    question = graphene.Field(QuestionSchema)

    @staticmethod
    def mutate(root, info, question_data=None):
        q_instance = Question(
            question_text=question_data.question_text,
            pub_date=datetime.datetime.now(),
        )
        q_instance.save()
        return CreateQuestion(question=q_instance)


class UpdateQuestion(graphene.Mutation):
    class Arguments:
        question_data = QuestionInput(required=True)

    question = graphene.Field(QuestionSchema)

    @staticmethod
    def mutate(root, info, question_data=None):
        print(question_data.question_text)
        q_instance = Question.objects.get(pk=question_data.id)
        if q_instance:
            q_instance.question_text = question_data.question_text
            q_instance.save()
            return UpdateQuestion(question=q_instance)
        return UpdateQuestion(book=None)


class DeleteQuestion(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    question = graphene.Field(QuestionSchema)

    @staticmethod
    def mutate(root, info, id):
        question_instance = Question.objects.get(pk=id)
        question_instance.delete()

        return None


class Mutation(graphene.ObjectType):
    create_question = CreateQuestion.Field()
    update_question = UpdateQuestion.Field()
    delete_question = DeleteQuestion.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)