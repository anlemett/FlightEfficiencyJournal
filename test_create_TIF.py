def getTrafficImpactFactor(num, min_num, max_num):

    max_TIF = 10

    step = (max_num - min_num)/max_TIF
    
    if num == 0.7:
        print(step)
        print(num - min_num)
        print((num - min_num) / step)
        print((0.7)/(0.1))
        print(int((num - min_num) / step))
        print(int((num - min_num) / step) + 1)
      
    
    TIF = int(((num - min_num)*10) / (step*10)) + 1 if num!=max_num else max_TIF
    
    return TIF


numbers = [0, 0.05, 0.1, 0.7, 0.9, 1]

for number in numbers:
    tif = getTrafficImpactFactor(number, 0, 1)
    #print(tif)

