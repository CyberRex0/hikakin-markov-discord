import markovify

model = markovify.Text.from_json(open('model.json', 'r', encoding='utf8').read())

def mk_sentence(model):
    return model.make_sentence(tries=100).replace(' ', '')

for _ in range(10):
    print(mk_sentence(model))