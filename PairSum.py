import math

# pi/4 = 4*arctg(1/5) - arctg(1/239)
# pi   = 4* (4*arctg(1/5) - arctg(1/239))

U = math.ulp(1.0) / 2.0

# глобальная переменная-хранилище значения ошибок
total_error = 0

def gamma(n):
    return (n * U / (1 - n * U))

# функция попарного суммирования
def pairSum(terms):
    while(len(terms) > 1):
        termsPaired = []
        l = len(terms)
        buffer = 0
        for i in range(0, len(terms)):
            if (i%2):
                buffer += terms[i]
                termsPaired.append(buffer)
            else:
                buffer = terms[i]
        
        if (len(terms) % 2 ==1):
            termsPaired.append(buffer)
            
        terms = termsPaired.copy()
    return terms[0]
#

# функция вычисления арктангенса и ошибок 
def arctg(x, nMax):
    terms = []
    terms.append(x)
    sum = x
    second_error = abs(x) * U
    third_error_buffer = abs(x)

    # числитель, в нём копятся степени х и знак
    numerator = x
    # знаменатель
    denominator = 3.
    
    for k in range(1, nMax):

        numerator *= -x * x
        term = numerator / denominator
        terms.append(term)
        # погрешность округления каждого члена
        second_error += abs(term) * gamma(4*k +2)
        # Банников сказал gamma(4k + 2)

        third_error_buffer += abs(term)
        
        denominator += 2
        sum += term
        
    
    # остаточный член ряда
    first_error = abs(term * x * x / denominator)
    first_error += math.ulp(first_error)
    
    # погрешность суммирования с ростом оценки суммирования
    third_error = gamma(math.log(nMax, 2)) * third_error_buffer
    #second_error *= U#

    # ошибка представления числа
    fourth_error = sum * (1.0 + U)
    
    global total_error
    total_error += first_error + second_error + third_error + fourth_error
    
    
    return pairSum(terms)
#

x1 = 1/5.
# int(1022/math.log(5, 2)) = 440
nMax1 = 2565
arctg1 = arctg(x1, nMax1)

arctg1 *= 4
total_error *= 4


x2 = 1/239.
# int(1022/math.log(239, 2)) = 129
nMax2 = 8
arctg2 = arctg(x2, nMax2)
total_error *= 4

piMy = 4 * (arctg1 - arctg2)

# прибавляем ошибку разности вычисления piMy по формуле
total_error += abs(piMy) * U


total_error_in_ulp = total_error / math.ulp(piMy)

print("pi =", f"{piMy:.60}")
print("PI =", f"{math.pi:.60}")
#print("total_error =", f"{total_error:.60}")
print("total_error_in_ulp =", f"{total_error_in_ulp:.60}")











