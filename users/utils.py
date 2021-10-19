from datetime import datetime
from django.conf import settings
from responses.models import UserResponse
from users.models import UserImage


class UserUtils:

    @staticmethod
    def get_user_data(user):
        user_data = {'dob':''}
        user_data['id'] = user.id
        user_data['email'] = user.email
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        if user.dob:
            user_data['dob'] = user.dob.strftime("%m-%d-%Y")
        user_data['phone_number'] = user.phone_number
        user_data['state'] = user.state
        user_data['billing_address'] = user.billing_address
        user_data['shipping_address'] = user.shipping_address
        user_data['access_type'] = user.access_type
        user_data['checkout_completed'] = user.is_active
        user_data['date_joined'] = user.date_joined.strftime("%m-%d-%Y")
        if user.user.profile_image:
            user_data['profile_image'] = f"{settings.BE_DOMAIN}{user.profile_image.url}"
        else:
            user_data['profile_image'] = None

        images = UserImage.objects.filter(user=user)
        user_data['images'] = [{'url': f"{settings.BE_DOMAIN}{image.image.url}",
                                'date': image.date_created.strftime("%m-%d-%Y")} for image in images]

        responses = UserResponse.objects.filter(user=user)
        question_responses = {}
        for response in responses:
            question_responses[response.question_id] = response.answers
        user_data['question_responses'] = question_responses
        return user_data

