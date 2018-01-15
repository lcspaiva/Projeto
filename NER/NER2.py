import pt_core_news_sm

with open("doc1.txt", "r") as docs:
    data = docs.read().replace('\n', '')

parser = pt_core_news_sm.load()
parsedEx = parser(data)

dict={}
'''
print("------------Tudo--------------")
for token in parsedEx:
    print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")
'''

print("-------------- entidades ---------------")
ents = list(parsedEx.ents)
for entity in ents:
    aux = (entity.label_, ' '.join(t.orth_ for t in entity))
    if dict.get(aux,0) == 0:
        dict[aux] = 1
    else:
        pass

#print(dict.items())
for items in dict:
    print(items)
