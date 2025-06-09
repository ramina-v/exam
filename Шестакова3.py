import math

# pi/4 = 4*arctg(1/5) - arctg(1/239)
# pi   = 4* (4*arctg(1/5) - arctg(1/239))

U = math.ulp(1.0) / 2.0

# глобальная переменная-хранилище значения ошибок
total_error = 0

def gamma(n):
    return (n * U / (1 - n * U))

# функция вычисления арктангенса и ошибок 
def arctg(x, nMax):
    
    sum = x

	# погрешность округления каждого члена
    # нужно ли домножать на U здесь? вроде нет
    second_error = abs(sum)
  
    # хранилище для суммы модулей членов ряда для вычисления ошибки суммирования
    third_error_buffer = abs(sum)

    # числитель, в нём копятся степени х и знак
    numerator = x
    # знаменатель
    denominator = 3.
    
    for k in range(1, nMax):
        
        numerator *= -x * x
        term = numerator / denominator
        
        # погрешность округления каждого члена
        # Банников сказал gamma(4k + 2)    (?)
        second_error += abs(term) * gamma(4*k +2)

        third_error_buffer += abs(term)
        
        denominator += 2
        sum += term
    
    # остаточный член ряда
    first_error = abs(term * x * x / denominator)
    first_error += math.ulp(first_error)
    
    # погрешность суммирования с ростом оценки суммирования
    third_error = gamma(nMax1 - 1) * third_error_buffer
	
  	# как было со второй ошибкой:
    #second_error *= U# Банников сказал неправильно
	
    # ошибка представления числа
    fourth_error = sum * (1.0 + U)
    
    global total_error
    total_error += first_error + second_error + third_error + fourth_error
    
    return sum
#

x1 = 1/5.
# int(1022/math.log(5, 2)) = 440
nMax1 = 440
arctg1 = arctg(x1, nMax1)
total_error *= 4

x2 = 1/239.
# int(1022/math.log(239, 2)) = 129
nMax2 = 129
arctg2 = arctg(x2, nMax2)
total_error *= 4

piMy = 4 * (4 * arctg1 - arctg2)

# прибавляем ошибку разности вычисления piMy по формуле
total_error += abs(piMy) * U

# ошибка ulp
total_error_in_ulp = total_error / math.ulp(piMy)

print("pi =", f"{piMy:.60}")
print("PI =", f"{math.pi:.60}")
#print("total_error =", f"{total_error:.60}")
print("total_error_in_ulp =", f"{total_error_in_ulp:.60}")


