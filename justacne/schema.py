import graphene
#from apps.users.schema import UsersQuery, UsersMutation
from responses.schema import UserResponseMutation
from users.schema import UserImageMutation
from graphql_auth.schema import UserQuery, MeQuery


# class Query(
#     ConnectionsQuery,
#     BaseQuery,
#     UsersQuery,
#     NotificationsQuery,
#     StripePriceQuery,
#     PlaidAccountQuery,
#     RoundupHistoryQuery,
#     graphene.ObjectType,
# ):
#     pass

class Query(UserQuery, MeQuery, graphene.ObjectType):
    pass


class Mutation(UserResponseMutation, UserImageMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)