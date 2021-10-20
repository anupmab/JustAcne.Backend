import graphene
import traceback
import random
import string
import stripe

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from graphql_jwt.decorators import login_required
from graphql_jwt.exceptions import PermissionDenied
from graphql_auth.bases import Output
from graphene.types.generic import GenericScalar

from users.models import AuthUser, UserImage
from users.utils import UserUtils
from users.relay import ObtainJSONWebToken, RefreshToken, RevokeToken, Register, PasswordSet

stripe.api_key = "sk_test_51JPz90LTGfmZPVsyzxRyjPFCmr63y6R5ORVW0OnUEA9qT53s79yMQvfgeyVFTriJmW9RJCjOPFaKZnLWfvMlsrhJ00E4W3yw70"


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


class ProfileImageMutation(graphene.relay.ClientIDMutation, Output):

    profile_url = graphene.String()

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):

        try:
            user = info.context.user
            if info.context.FILES.get("image", None):
                user.profile_image = info.context.FILES["image"]
                user.save()
                return ProfileImageMutation(success=True, errors=None, profile_url=f"{settings.BE_DOMAIN}{user.profile_image.url}")
            else:
                return ProfileImageMutation(
                    success=False,
                    errors={"message": 'Profile Image not provided'},
                    profile_url=None,
                )
        except Exception as e:
            return ProfileImageMutation(
                False,
                errors={"message": traceback.format_exc()},
                profile_url=None,
            )


class StripeCheckoutMutation(graphene.relay.ClientIDMutation, Output):
    class Input:
        email = graphene.String()
        success_url = graphene.String()
        failure_url = graphene.String()

    checkout_url = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        success_url = kwargs.get("success_url", None)
        failure_url = kwargs.get("failure_url", None)
        email = kwargs.get("email", None)

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Just Acne Shipping Charge',
                    },
                    'unit_amount': 1000,
                },
                'quantity': 1,
            }],
            mode='payment',
            billing_address_collection='required',
            phone_number_collection={
                'enabled': True,
            },
            shipping_address_collection={
                'allowed_countries': ['US', 'CA'],
            },
            customer_email=email,
            success_url=success_url,
            cancel_url=failure_url,
        )
        return StripeCheckoutMutation(success=True, errors=None, checkout_url=session.url )


class CheckoutCompleteMutation(graphene.relay.ClientIDMutation, Output):
    class Input:
        session_id = graphene.String()
        email = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        session_id = kwargs.get("session_id", None)
        email = kwargs.get("email", None)
        user = AuthUser.objects.get(email=email)

        session = stripe.checkout.Session.retrieve(session_id)
        intent = stripe.PaymentIntent.retrieve(session["payment_intent"], expand=["payment_method"])
        user.billing_address = intent['payment_method']['billing_details']['address']
        user.shipping_address = session["shipping"]["address"]
        user.phone_number = session["customer_details"]["phone"]

        user.email_token = ''.join(random.choices(string.ascii_uppercase+string.ascii_uppercase+string.digits, k=128))
        user.is_active = True
        user.save()

        msg = EmailMessage(
            'Thanks for your purchase!',
            (f'Thanks for your purchase. Someone will reach out to schedule a consult soon.<br>'
             f'Please reach out with any questions at info@justacne.com.<br><br>'
             f'You can set your password and login to dashboard using following link:<br>'
             f'https://justacne.com/set-password/{user.email_token}'),

            'Just Acne <justacne@mab-development.com>',
            [user.email]
        )
        msg.content_subtype = "html"
        msg.send()

        return CheckoutCompleteMutation(
            success=True,
            errors=None
        )


class PasswordResetMutation(graphene.relay.ClientIDMutation, Output):
    class Input:
        token = graphene.String()
        password = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        token = kwargs.get("token", None)
        password = kwargs.get("password", None)
        user = AuthUser.objects.filter(email_token=token).first()
        if not user:
            return PasswordResetMutation(success=False, errors={"message": "Invalid Token"})
        user.set_password(password)
        user.email_token = ''.join(
            random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=128))
        user.save()
        return PasswordResetMutation(success=True, errors=None)


class PasswordResetEmailMutation(graphene.relay.ClientIDMutation, Output):
    class Input:
        email = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **kwargs):
        email = kwargs.get("email", None)
        user = AuthUser.objects.filter(email=email).first()
        if not user:
            return PasswordResetEmailMutation(success=False, errors={"message": "Invalid Email"})

        user.email_token = ''.join(
            random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=128))
        user.save()

        msg = EmailMessage(
            'Password Reset',
            (f'You are receiving this email because you or someone else has requested a password for your user account.'
             f'<br>It can be safely ignored if you did not request a password reset.<br><br>'
             f'Click the link below to reset your password:<br>'
             f'https://justacne.com/reset-password/{user.email_token}'),

            'Just Acne <justacne@mab-development.com>',
            [user.email]
        )
        msg.content_subtype = "html"
        msg.send()
        return PasswordResetEmailMutation(success=True, errors=None)


class UserMutation(graphene.ObjectType):
    user_image = ImageMutation.Field()
    profile_image = ProfileImageMutation.Field()
    stripe_checkout = StripeCheckoutMutation.Field()
    checkout_complete = CheckoutCompleteMutation.Field()
    login = ObtainJSONWebToken.Field()
    send_password_reset_email = PasswordResetEmailMutation.Field()
    reset_password = PasswordResetMutation.Field()
    refresh_token = RefreshToken.Field()
    logout = RevokeToken.Field()


class UserQuery(graphene.ObjectType):
    user_list = graphene.List(GenericScalar, limit=graphene.Int(100), offset=graphene.Int(0), user_id=graphene.Int(0))
    me = GenericScalar()

    @login_required
    def resolve_user_list(self, info, limit, offset, user_id):
        user = info.context.user
        if user.access_type != "ADMIN":
            return PermissionDenied()
            return {"success": False, 'errors': {"message": "You do not have permission to perform this actiona"}}
        user_list = []
        if user_id:
            users = AuthUser.objects.filter(id=user_id)
        else:
            users = AuthUser.objects.filter(access_type="USER").order_by('-date_joined')[offset:offset + limit]
        for user in users:
            user_list.append(UserUtils.get_user_data(user))
        return user_list

    @login_required
    def resolve_me(self, info):
        user = info.context.user
        return UserUtils.get_user_data(user)
