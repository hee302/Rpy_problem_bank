import time
import random 
import copy 
import json

# ==========================================================
# [데이터 로드 함수]
# ==========================================================
def load_quiz_data(file_path="quiz_data.json"):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ {file_path}에서 {len(data)}개의 퀴즈 데이터를 성공적으로 불러왔습니다.")
        return data
    except FileNotFoundError:
        print(f"❌ 오류: {file_path} 파일을 찾을 수 없습니다.")
        return []
    except json.JSONDecodeError:
        print(f"❌ 오류: {file_path} 파일의 JSON 형식이 올바르지 않습니다.")
        return []

# ==========================================
# [퀴즈 세션 실행 (문제 풀이 루프)]
# ==========================================
def run_quiz_session(data, start_display_index=1, is_review=False):
    total = len(data)
    score = 0
    wrong_answers = []

    # 문제 리스트는 0부터 시작하므로 반복문은 0부터 total까지
    for i in range(total):
        item = data[i]
        
        # 순차 모드일 경우: 사용자가 입력한 시작 번호부터 카운트 (예: 100번부터 시작이면 100, 101...)
        # 랜덤/오답 모드일 경우: 그냥 1번부터 카운트하거나 원본 번호 표시
        if is_review:
            current_display_num = i + 1 
        else:
            current_display_num = start_display_index + i

        # 원본 데이터에 있는 번호(original_idx)가 있으면 그걸 보여주고, 없으면 계산된 번호 사용
        original_idx = item.get('original_idx', current_display_num)
        
        print(f"\n[문제 {original_idx}] (진행률: {i+1}/{total}) {item['q']}")
        
        for option in item['options']:
            print(f"  {option}")

        while True:
            user_input = input("\n정답 입력 (a/b/c/d) 또는 [q, exit, s] > ").lower().strip()
            
            if user_input in ['exit', 'q']:
                print("\n[퀴즈를 중단합니다]")
                return score, total, wrong_answers, i # 중단 시점 반환
            
            if user_input in ['s', 'score']:
                print(f"⭐ 현재 점수: {score} / {i}")
                continue 

            if user_input in ['a', 'b', 'c', 'd']:
                break
            else:
                print("⚠️ a, b, c, d 중 하나만 입력하세요.")
        
        if user_input == item['a']:
            print("✅ 정답입니다!")
            score += 1
        else:
            print(f"❌ 틀렸습니다. 정답: '{item['a']}'")
            if not is_review:
                wrong_item = copy.deepcopy(item)
                wrong_item['original_idx'] = original_idx
                wrong_answers.append(wrong_item)
            
        time.sleep(0.3)

    return score, total, wrong_answers, total # 끝까지 다 풂

# ==========================================
# [메인 설정 및 분기 로직]
# ==========================================
def run_quiz(quiz_data):
    full_quiz_data = quiz_data
    max_q = len(full_quiz_data)
    
    print("="*60)
    print(f"🚀 [파이썬 퀴즈] 총 {max_q}문항 로드됨")
    print("="*60)
    time.sleep(0.5)

    quiz_data_to_use = []
    start_display_index = 1 # 문제 번호 보여줄 때 시작값

    # -------------------------------------------------
    # 1. 모드 선택 (랜덤 vs 순차)
    # -------------------------------------------------
    while True:
        mode = input("\n❓ 랜덤으로 푸시겠습니까?\n   [y] 랜덤 풀이 (무작위 뽑기)\n   [n] 순차 풀이 (번호 지정)\n   선택 > ").lower().strip()
        if mode in ['y', 'n']:
            break
        print("⚠️ y 또는 n 만 입력해주세요.")

    # -------------------------------------------------
    # 2. 랜덤 모드 로직
    # -------------------------------------------------
    if mode == 'y':
        print("\n🎲 [랜덤 모드]를 선택하셨습니다.")
        while True:
            try:
                cnt_input = input(f"❓ 총 몇 문제를 푸시겠습니까? (최대 {max_q}) > ").strip()
                if not cnt_input: continue # 엔터치면 다시 물어봄
                
                count = int(cnt_input)
                if 1 <= count <= max_q:
                    quiz_data_to_use = random.sample(full_quiz_data, count)
                    start_display_index = 1 # 랜덤은 그냥 1번부터 진행하는 느낌으로 표시
                    break
                else:
                    print(f"⚠️ 1 ~ {max_q} 사이 숫자를 입력하세요.")
            except ValueError:
                print("⚠️ 숫자만 입력해주세요.")

    # -------------------------------------------------
    # 3. 순차 모드 로직
    # -------------------------------------------------
    else:
        print("\n📝 [순차 모드]를 선택하셨습니다.")
        
        # 3-1. 시작 번호 입력
        start_idx = 1
        while True:
            try:
                s_input = input(f"❓ 몇 번 문제부터 시작하시겠습니까? (1 ~ {max_q}) > ").strip()
                if not s_input: continue
                
                start_idx = int(s_input)
                if 1 <= start_idx <= max_q:
                    break
                else:
                    print(f"⚠️ 1 ~ {max_q} 사이 범위를 입력하세요.")
            except ValueError:
                print("⚠️ 숫자만 입력해주세요.")

        # 3-2. 풀이 개수 입력
        count = 0
        while True:
            try:
                # 남은 문제 수 계산 (예: 100개 중 98번 시작이면 최대 3개 가능)
                remain_q = max_q - start_idx + 1
                c_input = input(f"❓ {start_idx}번부터 몇 개의 문제를 푸시겠습니까? (최대 {remain_q}개) > ").strip()
                if not c_input: continue

                count = int(c_input)
                if 1 <= count <= remain_q:
                    # 슬라이싱: (시작번호-1) 부터 (시작번호-1 + 개수) 까지
                    start_list_idx = start_idx - 1
                    end_list_idx = start_list_idx + count
                    
                    quiz_data_to_use = full_quiz_data[start_list_idx : end_list_idx]
                    start_display_index = start_idx # 퀴즈 풀 때 이 번호부터 보여줌
                    break
                else:
                    print(f"⚠️ 1 ~ {remain_q} 사이 숫자를 입력하세요. (범위 초과)")
            except ValueError:
                print("⚠️ 숫자만 입력해주세요.")

    # -------------------------------------------------
    # 4. 퀴즈 실행
    # -------------------------------------------------
    print(f"\n🚀 문제를 생성했습니다! ({len(quiz_data_to_use)}문항)")
    time.sleep(1)
    
    score, total_len, wrong_list, last_idx = run_quiz_session(quiz_data_to_use, start_display_index=start_display_index)

    # -------------------------------------------------
    # 5. 결과 처리
    # -------------------------------------------------
    print("\n" + "="*60)
    print("🏁 퀴즈 종료")
    
    # 중단 여부에 따라 분모 결정 (다 풀었으면 전체 개수, 중간에 껐으면 푼 개수)
    actual_solved = last_idx # run_quiz_session에서 푼 개수 반환
    if actual_solved == 0: actual_solved = 1 # 0으로 나누기 방지

    print(f"✅ 최종 점수: {score} / {total_len}")
    print(f"📊 정답률: {(score/total_len)*100:.1f}%" if total_len > 0 else "0%")

    if wrong_list:
        print(f"📝 틀린 문제 개수: {len(wrong_list)}")
        retry = input("\n🤔 틀린 문제만 다시 풀어보시겠습니까? (y/n) > ").lower().strip()
        if retry == 'y':
            run_quiz_session(wrong_list, is_review=True)

    print("="*60)

if __name__ == "__main__":
    quiz_data = load_quiz_data()
    if quiz_data:
        run_quiz(quiz_data)