import graphene
from responses.schema import UserResponseMutation
from users.schema import UserMutation, UserQuery


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(UserResponseMutation, UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)