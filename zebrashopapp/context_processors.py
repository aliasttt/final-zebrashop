# def user_info(request):
#     if request.user.is_authenticated:
#         return {
#             'user': {
#                 'name': request.user.first_name,
#                 'lastname': request.user.last_name
#             }
#         }
#     return {}