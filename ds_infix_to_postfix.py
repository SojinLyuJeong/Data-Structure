# 2020 Data Structure
# Infix to Postfix
# SojinLyuJeong

class OperatorStack:                        # list로 연산자 스택 구현한 클래스
    def __init__(self):                     # 초기화 함수
        self.operator_stack = list()        # 원소들이 담길 operator_stack을 초기화해준다.
        self.top = -1                       # 스택의 항목이 추가되고 제거되는 부분으로, 초기값 -1을 정해준다.

    def empty(self):                        # 스택이 비었는지 확인하는 함수
        return True if self.top == -1 else False 
        # top이 -1이면 True를 반환하고, -1이 아니면 Fals를 반환

    def push(self, data):                   # 스택에 항목을 삽입하는 연산
        self.top += 1                       # top을 1 증가시켜주고
        self.operator_stack.append(data)    # operator_stack에 항목을 추가한다.
 
    def pop(self):                          # 스택에서 가장 마지막에 들어간 항목을 삭제하고 출력해주는 연산
        if self.empty():                    # 스택이 비었으면 삭제할 항목도 없으므로 None을 반환한다.
            return None
        
        data = self.operator_stack[self.top] # 스택의 가장 마지막 항목을 data변수에 담아주고
        del self.operator_stack[self.top]    # 삭제한다.
        self.top -= 1                        # top을 1 감소시켜준다.
        return data                          # 스택의 가장 마지막 항목을 반환한다.
    
    def peek(self):                          # 스택의 가장 마지막 항목을 출력해주는 함수
        if self.empty():                     # 스택이 비었으면 None을 반환한다.
            return None
        return self.operator_stack[self.top] # 가장 top에 있는 값을 반환한다.

# linked list로 피연산자 스택 구현
class Node:                                 # 스택에 담길 노드 구현
    def __init__(self, data):               # 초기화 함수
        self.data = data                    # 데이터 필드 초기화
        self.next = None                    # 링크 필드 초기화
            
class OperandStack:                         # 스택 기능 구현
    def __init__(self):                     # 초기화 함수
        self.head = None 
        
    def is_empty(self):                     # 스택이 비어있는지 확인하는 함수
        if not self.head:
            return True
        return False

    def push(self, data):           # 스택에 항목을 삽입하는 함수
        new_node = Node(data)       # 새로운 노드를 만들어주고
        new_node.next = self.head   # 새로운 노드의 링크가 head가 가르키고 있던 노드를 가르키도록 한다.
        self.head = new_node        # head가 새로운 노드를 가르키도록 한다.

    def pop(self):                  # 스택의 가장 마지막에 삽입된 항목을 삭제하고 출력하는 함수
        if self.is_empty():         # 비어있는지 확인
            return None
        pop_data = self.head.data   # head가 가르키고 있던 데이터를 pop_data에 담는다.
        self.head = self.head.next  # head는 head의 링크가 가르키고 있던 항목을 가르키도록 한다.
        return pop_data             # pop_data를 반환한다.
        
    def peek(self,data):            # 스택의 가장 최근에 삽입된 항목을 반환한다.
        if self.is_empty():         # 비어있는지 확인
            return None
        return self.head.data       # head가 가르키는 항목을 반환


# 파일 불러오기
def get_data():
    with open('./resource/infix1.txt', 'r') as file:    # 샘플 데이터 파일 읽어오기
        infix_data = []                                 # 샘플 데이터를 저장할 리스트 선언
        for l in file:                                  # 파일을 한 줄씩 읽고 리스트 형태로 저장
            infix_data.append(l)
            
        n = int(infix_data[0])                          # 입력으로 들어올 수식의 개수 저장
        infix_data = infix_data[1:]                     # 변환할 수식만 따로 저장

        # 샘플 데이터에는 연산자와 피연산자가 구분없이 붙어있으므로
        # 연산하기 위해 한 글자씩 분리하여 리스트에 담아준다.
        refined_infix_data = []
        for i in infix_data:
            refined_infix_data.append(list(i))

    return n, refined_infix_data                # 튜플 형식으로 항목 수와 데이터가 담긴 리스트를 반환


# 연산자와 그 우선 순위 전역변수 선언
OPERATORS = set(['+', '-', '*', '/', '%', '^', '(', ')', ';'])  # 연산자 정의
ICP = {'+':1, '-':1, '*':2, '/':2, '%':2, '^':4, '(':10, ';':0} # 스택에 진입할 때의 우선순위 (In-Comming Priority)
ISP = {'+':1, '-':1, '*':2, '/':2, '%':2, '^':3, '(':0, ';':0}  # 스택 안에서의 우선 순위 (In-Stack Priority)

# 중위 표기법을 후위표기법으로 바꾸는 함수
def infix_to_postfix():
    data = get_data()                           # get_data()에서 변환한 데이터 가져오기
    n = data[0]                                 # 항목 수
    infix_data = data[1]                        # 수식

    stack = OperatorStack()                     # 스택 생성
    postfix_result = []                         # 결과 저장하는 리스트 선언
    converted_result = []                       # 후위식 계산을 수월하게 하기 위해 postfix_result의 각 수식을 
                                                # 한 인덱스에 저장할 수 있는 리스트를 선언

                                                # 한 리스트 안에 여러개의 수식이 담겨있으므로 이중 for문을 사용한다.
    for i in range(n):                          # i는 한 줄의 수식을 순회한다.
        for j in infix_data[i]:                 # j는 한 줄의 수식 중 한 글자씩을 순회한다.
            if j not in OPERATORS:              # J가 연산자가 아니면(즉, 숫자이면)
                postfix_result.append(j)        # postfix_result에 삽입한다.
                if j == '\n':                   # 샘플 데이터를 가져오는 과정에서 '\n'도 추가되었는데 
                    postfix_result.pop()        # 필요 없으므로 pop해준다.

            elif j == '(':                      # 괄호를 먼저 계산해주어야 하므로 j가 '('이면 무조건 push한다.
                stack.push(j)
                
            elif j == ')':                      # j가 ')'이면 괄호가 닫혔다는 의미이므로 '('가 끝날 때 까지 
                                                # 스택의 연산자를 pop하여 결과에 저장한다.
                while not stack.empty() and stack.peek() != '(': # stack.peek()이 '('를 만날때 까지
                    temp = stack.pop()                           # 스택의 연산자를 pop하여
                    postfix_result.append(temp)                  # pop한 연산자를 postfix_result에 삽입한다.
                if not stack.empty() and stack.peek() != '(':    # 스택이 비거나 stack.peek()이 '('를 만나면
                    return -1                                    # -1을 반환
                else:
                    stack.pop()                                  # 그렇지 않으면 pop해준다.

            else:                                                           # j가 연산자이면
                while (not stack.empty() and ICP[j] <= ISP[stack.peek()]):  # 우선순위에 따라 pop 또는 push한다.
                    postfix_result.append(stack.pop())      # j와 스택의 top에 있는 연산자를 비교하여
                                                            # j가 스택의 top에 있는 연산자 보다 우선순위가 높다면
                                                            # 연산자 스택에 삽입하고,
                stack.push(j)                               # 같거나 작다면, 스택 상단에 있는 연산자를 출력한다.

        while not stack.empty():                            # 위의 과정에도 스택에 연산자가 남았다면, 스택이 빌때까지
            postfix_result.append(stack.pop())              # 연산자들을 pop하여 결과 리스트에 담아준다.
    
    # ostfix_result는 각 줄에 구분 없이 한 글자당 한 인덱스에 담겨 있다.
    # 예) ['4', '3','-', '6', '2', '/', '+', ';', '4', '3', '+', ';']
    # 아래 코드들은 converted_result에 수식 한 줄 마다 한 인덱스에 담기도록 한다.
    converted_result.append(' '.join(postfix_result))       # postfix_result의 원소들을 ' '(공백)을 사이에 두고
                                                            # converted_result에 저장
    converted_result = converted_result[-1].split(' ;')     # ' ;'를 기준으로 수식들을 분리
    converted_result = converted_result[:-1]                # 마지막에 공백이 저장되어 제거

    for k in range(0, len(converted_result)):               # 쓸모 없는 공백들을 제거
        converted_result[k] = converted_result[k] + ' ;'
        if converted_result[k][0] == ' ':
            converted_result[k] = converted_result[k][1:]
        elif converted_result[k][-1] == ' ':
            converted_result[k] = converted_result[k][:-1]

    return converted_result                                 # 정리된 결과를 반환해준다.


# 후위 표기법으로 표기된 수식을 계산해주는 함수
def calculate_postfix(converted_result):
    stack = OperandStack()                                      # 숫자들(피연산자들)이 저장될 스택을 선언
    cal_result = []                                             # 결과가 저장될 리스트 선언
    for i in range(len(converted_result)):          # 하나의 리스트에 여러개의 수식이 저장되어 있으므로 이중 for문을 사용
        for j in converted_result[i].split(' '):    # converted_result에 저장된 수식을 공백을 기준으로 분리하여 순회
                                                    # j가 피연산자이면 스택에 push해주고
                                                    # j가 연산자이면 피연산자 스택을 두번 pop하고
            if j == '+':                            # pop한 두 개의 숫자를 해당 연산에 따라 계산하여 스택에 push해준다.
                stack.push(int(stack.pop()) + int(stack.pop()))
            elif j == '-':
                stack.push(int(stack.pop()) - int(stack.pop()))
            elif j == '*':
                stack.push(int(stack.pop()) * int(stack.pop()))
            elif j == '/':
                stack.push(int(stack.pop()) / int(stack.pop()))
            elif j == '%':
                stack.push(int(stack.pop()) % int(stack.pop()))
            elif j == '^':
                stack.push(int(stack.pop()) ** int(stack.pop()))
            elif j == ';':                          # ';'는 수식의 가장 마지막에 위치하므로 연산을 끝내준다.
                break    
            else:
                stack.push(int(j))                       # j가 숫자이면 스택에 push해준다.
        cal_result.append(int(abs(stack.pop())))         # 가장 마지막까지 남은 숫자가 연산의 결과이므로 정수 형태로
    return cal_result                               # cal_result에 삽입하여 반환한다.

# 실행
data = get_data()                                   # 변수에 함수 실행 결과를 할당
postfix = infix_to_postfix()
value = calculate_postfix(postfix)

inf_data = data[1]                                  # data의 두번째 인덱스는 수식으로, inf_data에 담는다.
for k in range(len(inf_data)):                      # inf_data에는 불필요한 '\n'가 포함되므로 제거
    inf_data[k][:] = inf_data[k][:-1]

new_inf_data = []                                   # 새로운 리스트를 선언하여
for j in range(0, len(inf_data)):                   # 연산자/피연산자 사이에 빈칸을 하나씩 삽입함하여 할당해준다.
    new_inf_data.append(' '.join(inf_data[j]))

for i in range(0, data[0]):                         # 결과 출력
    print('------------------------test case {}-------------------------'.format(i+1))
    print('infix notation = {}'.format(new_inf_data[i]))
    print('postfix notation = {}'.format(postfix[i]))
    print('value = {}'.format(value[i]))
    print('------------------------------------------------------------\n')
# test 2