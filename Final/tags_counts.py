import nltk

patterns=[(r'^-?[0-9]+(.[0-9]+)?$', 'CD')]
cnt=open("tags_counts","w")
regexp_tagger = nltk.RegexpTagger(patterns)

i1=0
i2=0
i3=0
i4=0
i5=0

for lines in open(r'citation_sentiment_corpus.txt'):
	wsj=nltk.pos_tag(nltk.word_tokenize(lines))
	for (word, tag) in wsj:
		print(str(tag))
		if(tag=='CD'):
			i5 += 1
		if tag.startswith('JJ'):
			i1 += 1
		if tag.startswith('RB'):
			i2 += 1
		if tag.startswith('CD'):
			i3 += 1
		if tag.startswith('PRP'):
			i4 += 1
		if tag.startswith('WP'):
			i4 +=1

print(i5)
cnt.write("ADJECTIVE "+ str(i1) + "\n")
cnt.write("ADVERB "+ str(i2) + "\n")
cnt.write("MODALS "+ str(i3) + "\n")
cnt.write("PRONOUNS "+ str(i4) + "\n")
cnt.write("CARDINALS "+ str(i5) + "\n")