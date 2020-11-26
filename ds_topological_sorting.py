# 20-2 Data Structure
# Programming Report 2) 위상 정렬(Topological Sorting)
# 1607057 정소진

# txt형식의 데이터 파일 불러오기
def get_data():
    from collections import defaultdict     # 데이터를 dictionary형태로 입력받기 위한 모듈 호출
    from ast import literal_eval            # 문자열을 dictionary형태로 변환시키기 위한 모듈 호출
    
    with open('./resource/dag1.txt', 'r', encoding='utf-8-sig') as data:    # 파일 호출
        dag_dict_temp = defaultdict(dict)   # txt 파일의 데이터를 dictionary형태로 입력받기 위한 변수 선언
        dag_dict = {}                       # 정렬 처리에 필요한 최종 형태의 데이터를 담을 변수 선언

        for line in data:                   # txt 파일의 데이터를 한 줄씩 불러온다.
            first_v, second_v = line.strip().split(" ") # " " 공백을 기준으로 잘라 변수에 담아준다.
            dag_dict_temp.setdefault(int(first_v), []).append(int(second_v)) 
            # txt 파일의 데이터 에지 <Vn, Vm>은 정점 Vn에서 Vm으로 향하는 방향 에지를 의미한다..
            # 따라서 Vn은 dictionary의 key에, Vm은 dictionary의 value에 담을 수 있다.
            # 이때, Vn은 2개 이상의 Vm을 가질 수도 있으므로 .setdefault()을 이용하여 처리해준다.

        # 위에서 처리된 데이터는 collections.setdefault 자료형으로 저장되므로 
        # 문자열 형태로 바꾼뒤, 에지를 표현한 부분만 슬라이싱해준다.
        result = str(dag_dict_temp) 
        result = result[28:-1]

        dag_dict = literal_eval(result)     # 문자열 형태의 데이터를 dict 형태로 변환해준다.
        
        # 정점, 에지의 개수 추출하기
        vertices = []                       # vertices[0] : 정점의 개수
        edges = []                          # edges[0] : 에지의 개수
        for v in dag_dict.keys():
            vertices.append(v)
        for e in dag_dict.values():
            edges.append(e) 
        
        del dag_dict[vertices[0]]           # 위상 정렬을 위해 정점의 수를 키값으로 가지는 항목 삭제

        # 위의 과정을 통해 처리된 데이터는 방향 에지를 가지지 않는 정점은 포함되지 않지만 필요하므로
        # 변수 dag_dict에 추가하여 할당 한다.
        if len(dag_dict) < vertices[0]:         # key의 개수가 정점의 개수보다 보다 작으면,
            for a in range(int(vertices[0])):   # 정점의 개수만큼 value가 없는 key 값을 추가
                if a not in dag_dict:
                    dag_dict[a] = []

    return dag_dict                         # 연산하기 쉽게 정리된 데이터를 반환해 준다.


# linked list로 Stack 구현
class Stack_Node:                           # 스택에 담길 노드 구현
    def __init__(self, data):
        self.data = data
        self.next = None
            
class Stack:                                # 스택 기능 구현
    def __init__(self):                     # 초기화 함수
        self.head = None 
        
    def is_empty(self):                     # 스택이 비어있는지 확인하는 함수
        if not self.head:
            return True
        return False

    def push(self, data):                   # 스택에 항목을 삽입하는 함수
        new_node = Stack_Node(data)
        new_node.next = self.head
        self.head = new_node

    def pop(self):                  # 스택의 가장 마지막에 삽입된 항목을 삭제하고 출력하는 함수
        if self.is_empty():
            return None
        pop_data = self.head.data
        self.head = self.head.next
        return pop_data


# linked list로 Queue 구현
class Queue_Node:                       # queue에 담길 노드 구현 및 초기화
    def __init__(self, data):
        self.data = data
        self.next = None
    
class Queue:                            # queue 기능 구현
    def __init__(self):                 # 초기화 함수
        self.head = None
        self.tail = None
    
    def is_empty(self):                 # 큐가 비어있는지 확인하는 함수
        if not self.head:
            return True
        return False
    
    def enqueue(self, data):            # enqueue 기능 구현 
        new_node = Queue_Node(data)     # : 큐에 새로운 노드를 삽입하는 함수

        if self.is_empty():
            self.head = new_node
            self.tail = new_node
            return

        else:
            self.tail.next = new_node
            self.tail = new_node
    
    def dequeue(self):                  # dequeue 기능 구현
        if self.is_empty():             # : 큐에 가장 먼저에 들어온 노드를 반환하고 삭제
            return None

        v = self.head.data
        self.head = self.head.next
        return v

# 스택을 사용하는 위상 정렬 함수
def topsort_stack():                    
    dag_dict = get_data()               # get_data()에서 dictionary형태로 정리한 데이터를 불러온다
    stack = Stack()                     # 스택 생성
    in_degree = [0] * len(dag_dict)     # 각 정점의 진입차수를 저장하기 위한 리스트 변수를 할당
    sorted_result = []                  # 최종적으로 정렬한 결과를 담기 위한 변수 할당

    for i in range(len(dag_dict)):      # 각 정점의 진입차수 계산
        for j in range(len(dag_dict)):  # dictionary를 순회하며 각 
            temp = dag_dict[j]          # 각 정점과 같은 value가 나올때 마다
            for k in range(len(temp)):  # in_degree[i]에 1씩 증가시켜준다.
                if temp[k] == i:        
                    in_degree[i] += 1

    for i in range(len(in_degree)):     # 진입차수가 0이면 스택에 삽입한다.
        if in_degree[i] == 0:
            stack.push(i)

    while not stack.is_empty():         # 진입차수가 0인 정점들이 담긴 스택이 빌때까지
        vertex = stack.pop()            # 스택을 pop하여 변수 vertex에 할당하고
        sorted_result.append(vertex)    # 변수 vertex에 할당된 정점을 sorted_result에 추가한다.

        for i in range(len(dag_dict[vertex])):  # vertex에 할당된 변수를 key로 가지는 정점을 순회하여
            index = dag_dict[vertex][i]         # 해당 정점과 인접한 에지를 찾아서
            in_degree[index] -= 1               # 진입차수를 하나씩 감소시킨다.
            if in_degree[index] == 0:           # 인접한 정점의 진입 차수가 0이 되면
                stack.push(index)               # 스택에 push해준다.
    
    if len(sorted_result) < len(in_degree) and stack.is_empty():
        return 'impossible'
        # 모든 정점을 출력하지 않았는데, 진입 차수가 0인 정점이 없는 경우
        # 위상 정렬이 불가능하므로, 'impossible'이라는 메세지를 출력해준다.

    return sorted_result # 위상 정렬이 완료된 결과를 반환

# 큐를 사용하는 위상 정렬 함수
def topsort_queue():
    dag_dict = get_data()               # get_data()에서 dictionary형태로 정리한 데이터를 불러온다
    queue = Queue()                     # 큐 생성
    in_degree = [0] * len(dag_dict)     # 진입 차수를 계산하여 담아줄 변수 생성
    sorted_result = []                  # 위상 정렬된 결과를 담아줄 변수 생성

    for i in range(len(dag_dict)):      # 각 정점의 진입차수 계산하여 리스트 변수 in_degree에 담아준다.
        for j in range(len(dag_dict)):
            temp = dag_dict[j]
            for k in range(len(temp)):
                if temp[k] == i:
                    in_degree[i] += 1

    for i in range(len(in_degree)):     # 진입차수가 0이면 스택에 삽입한다.
        if in_degree[i] == 0:
            queue.enqueue(i)

    while not queue.is_empty():         # 진입차수가 0인 정점들이 담긴 큐가 빌때까지
        vertex = queue.dequeue()        # 큐를 dequeue해주고, 변수 vertex에 할당해준다.
        sorted_result.append(vertex)    # 정점이 할당된 vertex를 sorted_result에 담아준다.

        for i in range(len(dag_dict[vertex])):  # vertex에 할당된 변수를 key로 가지는 정점을 순회하여
            index = dag_dict[vertex][i]         # 해당 정점과 인접한 에지를 찾아서
            in_degree[index] -= 1               # 진입차수를 하나씩 감소시킨다.
            if in_degree[index] == 0:           # 인접한 정점의 진입차수가 0이되면
                queue.enqueue(index)            # 큐에 enqueue해 준다.
    
    if len(sorted_result) < len(in_degree) and queue.is_empty():
        return 'impossible'
        # 모든 정점을 출력하지 않았는데, 진입 차수가 0인 정점이 없는 경우
        # 위상 정렬이 불가능하므로, 'impossible'이라는 메세지를 출력해준다.

    return sorted_result                # 위상정렬된 결과가 담긴 리스트를 반환해준다.

# 실행
data = get_data()               # 변수에 함수 실행 결과를 할당
topsort_stack = topsort_stack()
topsort_queue = topsort_queue()

# topsort_stack과 topsort_queue의 실행 결과, 위상정렬이 불가능하면 impossible이라는 메세지를 띄워준다.
if topsort_stack == 'impossible' or topsort_queue == 'impossible':
    print('------------------------------ result ------------------------------\n')
    print('                           * impossible *')
    print('\n--------------------------------------------------------------------')

# topsort_stack과 topsort_queue의 실행 결과를 각 정점 사이에 빈칸을 하나씩 삽입하여 출력한다.
else: 
    str_int_stack = [str(int) for int in topsort_stack]
    str_int_queue = [str(int) for int in topsort_queue]
    print('------------------------------ result ------------------------------\n')
    print("* 스택 사용 위상정렬 결과 = ", ' '.join(str_int_stack))
    print("* 큐 사용 위상정렬 결과 = ", ' '.join(str_int_queue))
    print('\n--------------------------------------------------------------------')
