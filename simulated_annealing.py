import random
import math

def initialize_solution(N, M, b, reviewers_per_paper):
    """
    Khởi tạo giải pháp ban đầu một cách tham lam:
    - Với mỗi bài báo, chọn b chuyên gia có tải trọng thấp nhất từ danh sách L(i).
    """
    solution = []
    load = [0] * (M + 1)  # Tải trọng của các chuyên gia, index từ 1 đến M
    
    for i in range(1, N + 1):
        available_reviewers = reviewers_per_paper[i]
        # Sắp xếp các chuyên gia theo tải trọng hiện tại (thấp đến cao)
        available_reviewers.sort(key=lambda r: load[r])
        # Chọn b chuyên gia có tải trọng thấp nhất
        assigned = available_reviewers[:b]
        for r in assigned:
            load[r] += 1  # Tăng tải trọng của chuyên gia được chọn
        solution.append(assigned)
    
    return solution, load

def evaluate_max_load(load):
    """
    Đánh giá tải trọng tối đa hiện tại của các chuyên gia.
    """
    return max(load)

def simulated_annealing(N, M, b, reviewers_per_paper, initial_temp=100, cooling_rate=0.95, max_iterations=1000):
    """
    Tối ưu hóa giải pháp bằng Simulated Annealing:
    - Thử thay đổi ngẫu nhiên và chấp nhận thay đổi xấu hơn với xác suất nhất định.
    - Xác suất chấp nhận giảm dần theo nhiệt độ.
    """
    # Khởi tạo giải pháp ban đầu
    solution, load = initialize_solution(N, M, b, reviewers_per_paper)
    
    best_solution = [row[:] for row in solution]
    best_load = load[:]
    best_max_load = evaluate_max_load(load)
    
    current_solution = [row[:] for row in solution]
    current_load = load[:]
    current_max_load = best_max_load
    
    temp = initial_temp
    iteration = 0
    
    while temp > 1 and iteration < max_iterations:
        iteration += 1
        
        # Chọn ngẫu nhiên một bài báo
        paper_idx = random.randint(0, N-1)
        
        # Chọn ngẫu nhiên một reviewer để thay thế
        reviewer_idx = random.randint(0, b-1)
        old_reviewer = current_solution[paper_idx][reviewer_idx]
        
        # Chọn ngẫu nhiên một reviewer mới hợp lệ
        available_new = [r for r in reviewers_per_paper[paper_idx+1] if r != old_reviewer 
                         and r not in current_solution[paper_idx]]
        if not available_new:
            continue
            
        new_reviewer = random.choice(available_new)
        
        # Thực hiện thay đổi
        current_solution[paper_idx][reviewer_idx] = new_reviewer
        current_load[old_reviewer] -= 1
        current_load[new_reviewer] += 1
        
        # Đánh giá thay đổi
        new_max_load = evaluate_max_load(current_load)
        delta = new_max_load - current_max_load
        
        # Quyết định chấp nhận thay đổi
        accept_change = False
        
        if delta <= 0:  # Thay đổi tốt hơn hoặc bằng
            accept_change = True
            
            # Nếu tốt hơn giải pháp tốt nhất, cập nhật giải pháp tốt nhất
            if new_max_load < best_max_load:
                best_solution = [row[:] for row in current_solution]
                best_load = current_load[:]
                best_max_load = new_max_load
        else:  # Thay đổi xấu hơn
            # Chấp nhận với xác suất dựa trên nhiệt độ
            acceptance_prob = math.exp(-delta / temp)
            if random.random() < acceptance_prob:
                accept_change = True
        
        if accept_change:
            current_max_load = new_max_load
        else:
            # Hoàn tác thay đổi
            current_solution[paper_idx][reviewer_idx] = old_reviewer
            current_load[old_reviewer] += 1
            current_load[new_reviewer] -= 1
        
        # Giảm nhiệt độ
        temp *= cooling_rate
    
    return best_solution, best_load

def main():
    # Đọc input từ người dùng
    N, M, b = map(int, input().split())
    reviewers_per_paper = {}
    
    for i in range(1, N + 1):
        data = list(map(int, input().split()))
        reviewers_per_paper[i] = data[1:]  # Lấy danh sách chuyên gia từ sau số k
    
    # Tối ưu hóa bằng Simulated Annealing
    solution, load = simulated_annealing(N, M, b, reviewers_per_paper)
    
    # In output theo định dạng yêu cầu
    print(N)
    for reviewers in solution:
        print(b, *reviewers)
    
    # In thêm thông tin tải trọng tối đa để theo dõi
    print(f"Max load: {evaluate_max_load(load)}")

if __name__ == "__main__":
    main()