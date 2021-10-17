from requests import get


def get_question(topic: str = 'random'):
    url = 'https://qapi-api.ml'
    if topic != 'random':
        response = get(f'{url}/topic/{topic}/random-question').json()
    else:
        response = get(f'{url}/random-question').json()

    try:
        print(response)
        ok = True

        type = response['type']
        topic = response['topic'].capitalize()
        question = response['question']
        answer = response['answer']

        if type == 'multi':
            option1 = response['option1']
            option2 = response['option2']
            option3 = response['option3']
        else:
            option1 = None
            option2 = None
            option3 = None
    except Exception as e:
        print(e)
        return get_question()

    return type, topic, question, answer, option1, option2, option3, ok
