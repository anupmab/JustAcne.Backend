import graphene
import traceback

from django.conf import settings
from graphql_jwt.decorators import login_required
from graphql_auth.bases import Output
from graphene.types.generic import GenericScalar

from users.models import AuthUser, UserImage
from users.utils import UserUtils
from users.relay import ObtainJSONWebToken, RefreshToken, RevokeToken


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


class UserMutation(graphene.ObjectType):
    user_image = ImageMutation.Field()
    checkout_complete = CheckoutCompleteMutation.Field()

    login = ObtainJSONWebToken.Field()
    refresh_token = RefreshToken.Field()
    logout = RevokeToken.Field()


class UserQuery(graphene.ObjectType):
    user_list = graphene.List(GenericScalar, limit=graphene.Int(100), offset=graphene.Int(0))
    me = GenericScalar()

    @login_required
    def resolve_user_list(self, info, limit, offset):
        user_list = []
        users = AuthUser.objects.filter(access_type="USER").order_by('-date_joined')[offset:offset + limit]
        for user in users:
            user_list.append(UserUtils.get_user_data(user))
        return user_list

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        return UserUtils.get_user_data(user)
