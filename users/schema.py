import graphene
import traceback
import random
import string
from django.conf import settings
from graphql_auth import relay
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth.bases import Output
from graphene.types.generic import GenericScalar

from users.models import AuthUser, UserImage
from users.utils import UserUtils


class ImageMutation(graphene.relay.ClientIDMutation, Output):
    class Input:
        email = graphene.String()

    image_url = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):

        try:
            email = kwargs.get("email", None)
            if not email:
                return ImageMutation(success=False, errors={"message": "Email not provided"}, image_url=None)
            if info.context.FILES.get("image", None):
                user = AuthUser.objects.get(email=email)
                user_image = UserImage.objects.create(user=user)
                user_image.image = info.context.FILES["image"]
                user_image.save()
                return ImageMutation(success=True, errors=None, image_url=f"{settings.BE_DOMAIN}{user_image.image.url}")
            else:
                return ImageMutation(
                    success=False,
                    errors={"message": 'Image not provided'},
                    image_url=None,
                )
        except Exception as e:
            return ImageMutation(
                False,
                errors={"message": traceback.format_exc()},
                image_url=None,
            )


class CheckoutCompleteMutation(graphene.relay.ClientIDMutation, Output):
    class Input:
        session_id = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        session_id = kwargs.get("session_id", None)
        # session = stripe.checkout.Session.retrieve(session_id)
        # intent = stripe.SetupIntent.retrieve(session["setup_intent"], expand=["payment_method"])
        return CheckoutCompleteMutation(
            success=True,
            errors=None
        )


class LoginMutation(graphene.relay.ClientIDMutation, Output):
    class Input:
        email = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    user_data = GenericScalar()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        email = kwargs.get("email", None)
        password = kwargs.get("password", None)

        user = AuthUser.objects.filter(email=email).first()
        if not user:
            return LoginMutation(success=False, errors={"message": "Invalid Email"}, access_token=None, user_data=None)

        if user.check_password(password):
            user.access_token = ''.join(random.choices(string.ascii_uppercase + string.digits +
                                                       string.ascii_lowercase, k=128))
            user.save()
            return LoginMutation(success=True, errors=None, access_token=user.access_token,
                                 user_data=UserUtils.get_user_data(user))

        return LoginMutation(success=False, errors={"message": "Invalid Password"}, access_token=None, user_data=None)


class UserMutation(graphene.ObjectType):
    user_image = ImageMutation.Field()
    checkout_complete = CheckoutCompleteMutation.Field()
    login = LoginMutation.Field()


class UserQuery(UserQuery, MeQuery, graphene.ObjectType):
    pass
