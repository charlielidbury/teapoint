from wordfreq import word_frequency
from collections import Counter

def extract_keywords(messages):

    words = []
    for message in messages:
        message = clean_text(message)
        words.extend(message.split(' '))
        
    total_words = len(words)
    word_frequencies = { w: (count / total_words) for w, count in Counter(words).items() }

    # now we normalize the frequencies
    for word, freq in word_frequencies.items():
        if word_frequency(word, 'en') == 0:
            word_frequencies[word] = 0
        else:
            word_frequencies[word] = word_frequencies[word] / word_frequency(word, 'en')
            
    return word_frequencies

def get_ranked_keywords(messages):
    uids = set([m[3] for m in messages])
    ranked_keywords = dict()
    for uid in uids:
      target_messages = [m[4] for m in messages if m[3] == uid]
      word_frequencies = extract_keywords(target_messages)
      ranked_keywords[uid] = dict(sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)[:100])
    return ranked_keywords

def clean_text(message):
    return message
