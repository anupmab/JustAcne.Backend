import traceback
import graphene
from graphql_auth.bases import Output
from graphene import relay, ObjectType


class ResponseInput(graphene.InputObjectType):
    question_id = graphene.String(required=True)
    answers = graphene.List(graphene.String)


class ResponseMutation(relay.ClientIDMutation, Output):
    class Input:
        user = graphene.String()
        response = graphene.List(ResponseInput)

    @classmethod
    # @login_required
    def mutate_and_get_payload(cls, root, info, **kwargs):
        # user = info.context.user
        try:
            user = kwargs.get("email", None)
            response = kwargs.get("response", None)

            print(response)



            # if not email:
            #     raise ValueError("Response must have an associated email")

            # exchange = Exchange.objects.get(pk=from_global_id(exchange_id)[1])
            # exchange_connection = UserExchangeConnection.objects.get(exchange=exchange, user=user)
            # preference = UserConnectionPreference.objects.get(user_exchange_connection=exchange_connection)
            # purchase_order = PurchaseOrderUtils.create_purchase_order(user, exchange, preference.investment_asset,
            #                                                           amount, PurchaseOrder.QUICK_BUY)
            # ExchangePurchaseUtils.exchange_purchase(purchase_order)
            return ResponseMutation(success=True, errors=None)
        except Exception as e:
            return ResponseMutation(
                False,
                {
                    "message": traceback.format_exc(),
                },
            )


class UserResponseMutation(ObjectType):
    user_response = ResponseMutation.Field()

