from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class ScoresView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, _):
        score_data = {
            'team_a': {
                'score': 1600,
                'users': {
                    'user_1': 0,
                    'user_2': 100,
                    'user_3': 500,
                    'user_4': 1000
                }
            },
            'team_b': {
                'score': 0,
                'users': {
                    'user_5': 0,
                    'user_6': 0,
                    'user_7': 0,
                    'user_8': 0
                }
            },
            'team_c': {
                'score': 0,
                'users': {
                    'user_9': 0,
                    'user_10': 0,
                    'user_11': 0,
                    'user_12': 0
                }
            },
            'team_d': {
                'score': 0,
                'users': {
                    'user_13': 0,
                    'user_14': 0,
                    'user_15': 0,
                    'user_16': 0
                }
            },
            'team_e': {
                'score': 0,
                'users': {
                    'user_17': 0,
                    'user_18': 0,
                    'user_19': 0,
                    'user_20': 0
                }
            }
        }
        return Response(data=score_data, status=status.HTTP_200_OK)


class QuestionsView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, _):
        questions_data = {
            'levels': [
                {
                    'id': 'easy',
                    'label': 'Easy',
                    'score': 100
                },
                {
                    'id': 'normal',
                    'label': 'Normal',
                    'score': 200
                },
                {
                    'id': 'hard',
                    'label': 'Hard',
                    'score': 300
                }
            ],
            'questions': [
                {
                    'id': 1,
                    'levelId': 'easy'
                },
                {
                    'id': 2,
                    'levelId': 'easy'
                },
                {
                    'id': 3,
                    'levelId': 'easy'
                },
                {
                    'id': 4,
                    'levelId': 'easy'
                },
                {
                    'id': 5,
                    'levelId': 'easy'
                },
                {
                    'id': 6,
                    'levelId': 'normal'
                },
                {
                    'id': 7,
                    'levelId': 'normal'
                },
                {
                    'id': 8,
                    'levelId': 'normal'
                },
                {
                    'id': 9,
                    'levelId': 'normal'
                },
                {
                    'id': 10,
                    'levelId': 'normal'
                },
                {
                    'id': 11,
                    'levelId': 'hard'
                },
                {
                    'id': 12,
                    'levelId': 'hard'
                },
                {
                    'id': 13,
                    'levelId': 'hard'
                },
                {
                    'id': 14,
                    'levelId': 'hard'
                },
                {
                    'id': 15,
                    'levelId': 'hard'
                }
            ]
        }
        return Response(data=questions_data, status=status.HTTP_200_OK)
