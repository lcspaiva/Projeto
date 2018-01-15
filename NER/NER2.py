import pt_core_news_sm


with open("doc1.txt", "r") as docs:
    data = docs.read().replace('\n', '')


parser = pt_core_news_sm.load()
parsedEx = parser(data)

print("-------------- entidades ---------------")
ents = list(parsedEx.ents)
for entity in ents:
    print(entity.label_, ' '.join(t.orth_ for t in entity))
