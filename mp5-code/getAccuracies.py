import subprocess
train = ["brown-training.txt", "masc-training.txt", "both-training.txt"]
test = ["brown-dev.txt", "masc-dev.txt", "both-dev.txt"]
for trainer in train:
    for tester in test:
        f = open("output.txt", "a")
        f.write(trainer)
        f.write(", ")
        f.write(tester)
        result = subprocess.run(['python3', 'mp5.py', '--train', trainer,'--test', tester, '--viterbi'], stdout=open('output.txt', 'a'))
        f.write("\n\n")
f.close()