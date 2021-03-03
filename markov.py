from random import randint

class MarkovLyrics:
    def __init__(self):
        self.chain = {}

    def populateChain(self, lyrics):
        for line in lyrics:
            words = line.split(" ")

            for i in range(len(words) - 1):
                word = words[i]

                next_word = words[i+1]
                if word in self.chain:
                    self.chain[word].append(next_word)
                else:
                    self.chain[word] = [next_word]
    def generateLyrics(self, length=500):
        n = len(self.chain)

        start_index = randint(0, n-1)
        keys = list(self.chain.keys())
        curr_word = keys[start_index].title()

        lyrics = curr_word + " "

        for _ in range(length):
            if curr_word not in self.chain:
                lyrics += 'NEWLINE'
                next_index = randint(0, n-1)
                curr_word = keys[next_index]
            else:
                next_words = self.chain[curr_word]
                next_index = randint(0, len(next_words) - 1)
                next_word = next_words[next_index]
                lyrics += next_word + " "
                curr_word = next_word
            
        return lyrics

        
