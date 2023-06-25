from func import calculate_pi_leibniz,calculate_sum

def combine():
    List = [1,2,3,4,5,6,7,8,9,10]
    PI = calculate_pi_leibniz(100)
    Sum = []
    for i in List:
        Sum.append(PI*i**2)
    ans = calculate_sum(Sum)
    print(f"the ans is : {ans:.2f}")
    return ans

if __name__ == "__main__":
    combine()