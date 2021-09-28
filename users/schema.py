import graphene
import traceback
from django.conf import settings
from graphql_auth import mutations, relay
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth.bases import Output
from graphene_django import DjangoObjectType

from users.models import AuthUser, UserImage


class AuthMutation(graphene.ObjectType):
    #register = mutations.Register.Field()
    #verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_change = mutations.PasswordChange.Field()


class ImageMutation(graphene.relay.ClientIDMutation, Output):
    class Input:
        email = graphene.String()

    image_url = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):

        try:
            email = kwargs.get("email", None)
            if not email:
                return ImageMutation(success=False, errors=["Email not provided"], image_url=None)
            if info.context.FILES.get("image", None):
                user = AuthUser.objects.get(email=email)
                user_image = UserImage.objects.create(user=user)
                user_image.image = info.context.FILES["image"]
                user_image.save()
                return ImageMutation(success=True, errors=None, image_url=f"{settings.BE_DOMAIN}{user_image.image.url}")
            else:
                return ImageMutation(
                    success=False,
                    errors=['image info not provided'],
                    image_url=None,
                )
        except Exception as e:
            return ImageMutation(
                False,
                errors=[traceback.format_exc()],
                image_url=None,
            )


class UserImageMutation(graphene.ObjectType):
    user_image = ImageMutation.Field()

# class UserDetailsNode(DjangoObjectType):
#     class Meta:
#         model = AuthUser
#         fields = ("id", "first_name", "last_name", "email", "username")
#         interfaces = (graphene.relay.Node,)
#
#     def resolve_verified(self, info):
#         return self.status.verified
#
# class ExchangeQuickBuyMutation(relay.ClientIDMutation, Output):
#     class Input:
#         email = graphene.String()
#         amount = graphene.
#
#     @classmethod
#     @login_required
#     def mutate_and_get_payload(cls, root, info, **kwargs):
#         user = info.context.user
#         try:
#             exchange_id = kwargs.get("exchange_id", None)
#             amount = kwargs.get("amount", None)
#
#             exchange = Exchange.objects.get(pk=from_global_id(exchange_id)[1])
#             exchange_connection = UserExchangeConnection.objects.get(exchange=exchange, user=user)
#             preference = UserConnectionPreference.objects.get(user_exchange_connection=exchange_connection)
#             purchase_order = PurchaseOrderUtils.create_purchase_order(user, exchange, preference.investment_asset,
#                                                                       amount, PurchaseOrder.QUICK_BUY)
#             ExchangePurchaseUtils.exchange_purchase(purchase_order)
#             return ExchangeQuickBuyMutation(success=True, errors=None)
#         except Exception as e:
#             kwargs = {
#                 "raw_error": traceback.format_exc(),
#                 "user_friendly_error": "Exchange Quick Buy Error",
#                 "operation_name": "EXCHANGE_QUICK_BUY",
#                 "user": user,
#             }
#             ErrorLog.log_to_db(**kwargs)
#             return ExchangeQuickBuyMutation(
#                 False,
#                 {
#                     "exchange_quick_buy": [
#                         {
#                             "message": _(getattr(e, "message", str(e))),
#                             "code": _(getattr(e, "code", "exchange_quick_buy_error")),
#                         }
#                     ]
#                 },
#             )


class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)