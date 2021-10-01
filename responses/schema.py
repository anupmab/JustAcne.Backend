import traceback
from datetime import datetime
import graphene
from graphql_auth.bases import Output
from graphene import relay, ObjectType
from users.models import CustomUserManager, AuthUser
from responses.models import UserResponse
from users.utils import UserUtils
from graphene.types.generic import GenericScalar


class QuestionResponseInput(graphene.InputObjectType):
    question_id = graphene.String(required=True)
    answers = graphene.List(graphene.String)


class ResponseMutation(relay.ClientIDMutation, Output):
    class Input:
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        dob = graphene.String()
        state = graphene.String()
        question_responses = graphene.List(QuestionResponseInput)

    user_data = GenericScalar()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        try:
            email = kwargs.get("email", None)
            if not email:
                return ResponseMutation(success=False, errors={"message": "Email not provided"}, user_data=None)

            first_name = kwargs.get("first_name", None)
            last_name = kwargs.get("last_name", None)
            state = kwargs.get("state", None)
            dob = kwargs.get("dob", None)
            question_responses = kwargs.get("question_responses", [])

            user, created = AuthUser.objects.get_or_create(email=email, username=email)
            user.set_password('123456') # FOR TESTING
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if dob:
                user.dob = datetime.strptime(dob, "%m-%d-%Y")
            if state:
                user.state = state
            user.save()

            for response in question_responses:
                user_response, created = UserResponse.objects.get_or_create(user=user,
                                                                            question_id=response['question_id'])
                user_response.answers = response['answers']
                user_response.save()

            return ResponseMutation(success=True, errors=None, user_data=UserUtils.get_user_data(user))
        except Exception as e:
            return ResponseMutation(
                False,
                {"message": traceback.format_exc()},
                None
            )


class UserResponseMutation(ObjectType):
    user_response = ResponseMutation.Field()

