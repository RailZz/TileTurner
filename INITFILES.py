for i in range(1, 101):
    fopen = open('levels/score' + str(i) + '.pavel', 'w')
    print(0, file = fopen)
    fopen.close()
fopen = open('levelToPlayDoc.txt', 'w')
print(1, file = fopen)
fopen.close()
    