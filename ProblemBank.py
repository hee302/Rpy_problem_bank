import time
import random # 랜덤 선택을 위해 random 모듈 추가

# ==========================================================
# [문제 데이터베이스: 파이썬 기초 Part 1 (Page 1 ~ 9)]
# ==========================================================
import time
import copy # 딥 카피를 위해 copy 모듈 사용
import json

def load_quiz_data(file_path="quiz_data.json"):
    """JSON 파일에서 퀴즈 데이터를 불러오는 함수"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ {file_path}에서 {len(data)}개의 퀴즈 데이터를 성공적으로 불러왔습니다.")
        return data
    except FileNotFoundError:
        print(f"❌ 오류: {file_path} 파일을 찾을 수 없습니다. (경로 확인 필요)")
        return []
    except json.JSONDecodeError:
        print(f"❌ 오류: {file_path} 파일의 JSON 형식이 올바르지 않습니다.")
        return []

# ==========================================
# [퀴즈 실행 로직]
# ==========================================
def run_quiz_session(data, start_index=1, is_review=False):
    """
    실제 퀴즈 풀이를 진행하는 함수 (재활용을 위해 분리)
    """
    total = len(data)
    score = 0
    wrong_answers = []

    # 시작 인덱스를 0부터 시작하는 리스트 인덱스로 변환
    start_list_index = start_index - 1
    
    # 만약 재풀이라면, 인덱스 번호를 재조정하지 않음
    if is_review:
        print("\n🔄 [오답 노트] 틀린 문제 다시 풀기 시작합니다.")
        # 재풀이는 잘못된 문제 번호만 담긴 리스트를 기반으로 하므로,
        # 원본 인덱스 번호를 추적하는 로직이 필요합니다.
        # 이 예시에서는 단순화를 위해 'data'에 이미 틀린 문제만 있다고 가정합니다.
        
        # 재풀이에서는 처음부터 다시 시작
        start_list_index = 0
        total = len(data)
    else:
        print(f"✅ {start_index}번 문제부터 시작합니다.")

    # 퀴즈 루프 시작
    for i in range(start_list_index, total):
        item = data[i]
        
        # 원본 문제 번호를 추적 (재풀이 시에도 원래 번호를 보여주기 위함)
        original_idx = item.get('original_idx', i + 1)
        
        print(f"\n[문제 {original_idx}/{total}] {item['q']}")
        
        for option in item['options']:
            print(f"  {option}")

        while True:
            # 명령어 안내를 추가
            user_input = input("\n정답 입력 (a/b/c/d) 또는 [q, exit, s] > ").lower().strip()
            
            if user_input in ['exit', 'q']:
                print("\n[퀴즈를 중단하고 현재 점수를 확인합니다]")
                return score, total, wrong_answers, i + 1 # 현재 진행 상태 반환
            
            if user_input in ['s', 'score']:
                current_score = score
                current_total = i - start_list_index + 1 # 현재까지 푼 문제 수
                print("-" * 30)
                print(f"⭐ 현재 점수: {current_score} / {current_total}")
                if current_total > 0:
                    print(f"📊 정답률: {(current_score/current_total)*100:.1f}%")
                print("-" * 30)
                continue # 점수 확인 후 다시 정답 입력 대기

            if user_input in ['a', 'b', 'c', 'd']:
                break
            else:
                print("⚠️ a, b, c, d 중 하나만 입력하거나, 명령어를 입력해주세요.")
        
        # 정답 체크
        if user_input == item['a']:
            print("✅ 정답입니다!")
            score += 1
        else:
            print(f"❌ 틀렸습니다. 정답은 '{item['a']}' 입니다.")
            
            # 틀린 문제는 원본 데이터와 인덱스 번호를 저장하여 재풀이 목록에 추가
            if not is_review:
                # 딥 카피를 사용하여 원본 데이터 구조를 유지
                wrong_item = copy.deepcopy(item)
                wrong_item['original_idx'] = original_idx
                wrong_answers.append(wrong_item)
            
        time.sleep(0.3)

    return score, total, wrong_answers, total + 1 # 퀴즈 완료 시 반환

def run_quiz(quiz_data):
    print("="*60)
    print(f"🚀 [파이썬 기초 Part 1] 문제 풀이 (Page 1 ~ 9)")
    print(f"📄 총 {len(quiz_data)}문항")
    print("="*60)
    time.sleep(1)

    full_quiz_data = quiz_data
    max_q = len(full_quiz_data)
    
    quiz_data_to_use = []
    initial_total = 0
    start_index = 1
    
    # 1. 풀이할 문제 개수 선택 및 랜덤 모드 결정
    while True:
        try:
            count_input = input(f"❓ 총 몇 문제(1 ~ {max_q}개)를 푸시겠습니까? (전체 풀이: Enter) > ").strip()
            
            if not count_input:
                # 전체 문제 풀이 선택 (기존 순서대로)
                
                # 1-1. 시작 번호 선택 (기존 로직 유지)
                while True:
                    try:
                        start_num_input = input(f"❓ 몇 번 문제(1 ~ {max_q})부터 시작하시겠습니까? (기본값: 1) > ").strip()
                        if not start_num_input:
                            start_index = 1
                            break
                        start_index = int(start_num_input)
                        if 1 <= start_index <= max_q:
                            break
                        else:
                            print(f"⚠️ 1과 {max_q} 사이의 숫자를 입력해주세요.")
                    except ValueError:
                        print("⚠️ 유효한 숫자를 입력해주세요.")
                
                quiz_data_to_use = full_quiz_data
                initial_total = max_q
                break
            
            num_to_solve = int(count_input)
            
            if 1 <= num_to_solve <= max_q:
                # 랜덤 문제 풀이 선택
                
                # random.sample을 사용하여 N개의 문제를 무작위로 추출
                quiz_data_to_use = random.sample(full_quiz_data, num_to_solve)
                
                initial_total = len(quiz_data_to_use)
                start_index = 1 # 랜덤 모드에서는 항상 1번부터 시작
                print(f"\n✨ {initial_total}개의 랜덤 문제를 준비했습니다. (순서대로 1번부터 시작)")
                break
            else:
                print(f"⚠️ 1과 {max_q} 사이의 숫자를 입력해주세요.")
        except ValueError:
            print("⚠️ 유효한 숫자를 입력해주세요.")
            
    # 2. 퀴즈 실행
    # total은 퀴즈를 중단했을 때를 대비하여 총 문제수를 따로 저장
    score, total_answered, wrong_list, last_index = run_quiz_session(quiz_data_to_use, start_index=start_index)
    
    # 3. 결과 및 다시 풀기 기능
    
    # 중단 여부 체크 (마지막 인덱스가 총 문제수보다 작으면 중단된 것)
    is_interrupted = (last_index <= initial_total) 
    
    print("\n" + "="*60)
    if is_interrupted:
        print("⏸️ 퀴즈가 중단되었습니다.")
        
        # 중단 시에는 현재까지 푼 문제 수(total_answered)를 기준으로 계산
        total_q_solved = total_answered 
        
    else:
        print("🏁 Part 1 완료!")
        total_q_solved = initial_total # 전체 문제를 다 푼 경우
        
    # 최종 결과 출력
    print(f"✅ 최종 점수: {score} / {total_q_solved}")
    if total_q_solved > 0:
        print(f"📊 정답률: {(score/total_q_solved)*100:.1f}%")
    
    if wrong_list:
        # 틀린 문제 번호만 추출해서 출력
        wrong_idx_list = [item['original_idx'] for item in wrong_list]
        print(f"📝 틀린 문제 번호: {wrong_idx_list}")
        
        # 4. 다시 풀기 기능
        while True:
            retry_input = input("\n🤔 틀린 문제만 다시 풀어보시겠습니까? (y/n) > ").lower().strip()
            if retry_input == 'y':
                # 틀린 문제만 모은 리스트(wrong_list)를 재풀이 함수에 전달
                # 재풀이 시에는 랜덤이 아닌, 틀린 문제 리스트의 순서대로 진행됩니다.
                run_quiz_session(wrong_list, is_review=True)
                break
            elif retry_input == 'n':
                break
            else:
                print("⚠️ y 또는 n 을 입력해주세요.")

    print("="*60)
    print("👋 퀴즈를 종료합니다.")
    print("="*60)


if __name__ == "__main__":
    quiz_data = load_quiz_data()
    if quiz_data:
        run_quiz(quiz_data)