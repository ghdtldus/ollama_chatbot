from flask import Flask, request, jsonify, render_template
import ollama
import random  # random 모듈을 추가하여 무작위 메시지를 선택

app = Flask(__name__)

# 대화 히스토리 저장
chat_history = []
keytopic = ''

# 사전 정보 로드 함수
def load_txt_data_to_history(file_path='./myfile.txt'):
    global keytopic
    history = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.split(":")[0] == '대표키워드':
                    keytopic = line.split(":")[1].strip()
                else:
                    history.append({'role': 'system', 'content': line})
    except FileNotFoundError:
        print(f"Error: {file_path} 파일을 찾을 수 없습니다.")
    return history

# 사용자 메시지의 감정을 분석하는 함수
def analyze_sentiment(message):
    positive_words = ['행복', '기쁨', '좋아요', '멋져요', '잘했어요', '잘된다']
    negative_words = ['슬픔', '화남', '우울', '힘들다', '짜증', '불안']
    
    positive_count = sum(word in message for word in positive_words)
    negative_count = sum(word in message for word in negative_words)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

# myfile.txt 내용을 히스토리에 추가
chat_history.extend(load_txt_data_to_history())

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/keytopic', methods=['GET'])
def get_keytopic():
    return jsonify({'keytopic': keytopic})

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    user_message = request.json.get('message').strip()

    # 감정 분석
    sentiment = analyze_sentiment(user_message)

    # 감정별 응답 메시지 설정
    if sentiment == 'positive':
        bot_message = [
            "너무 잘하고 있어요! 계속 힘내세요! 😊",
            "정말 멋지네요! 지금처럼 계속 나아가세요! 🌟",
            "당신의 긍정적인 에너지가 정말 멋져요! 👍",
            "이 순간을 즐기세요! 당신은 훌륭해요! 💖"
        ]
    elif sentiment == 'negative':
        bot_message = [
            "힘든 일이 있으면 언제든 이야기해 주세요. 함께할게요. 😢",
            "괜찮아요. 어려운 시간도 지나갈 거예요. 힘내세요. 💪",
            "지금 힘들다면 잠시 쉬어가도 괜찮아요. 언제든지 돕겠어요. 💙",
            "힘든 일이 있을 때는 이야기하는 것만으로도 큰 도움이 될 수 있어요. 함께해요. 🤝"
        ]
    else:
        bot_message = [
            "무슨 일이든 잘 해결될 거예요. 당신은 할 수 있어요! ✨",
            "모든 문제는 해결 방법이 있어요. 차분하게 해나가면 됩니다. 😊",
            "지금은 조금 불안할 수 있지만, 결국 좋은 결과가 있을 거예요. 힘내세요! 🌈",
            "모든 게 잘 풀릴 거예요. 조금만 더 기다려 보세요. 😌"
        ]
    
    # 감정에 맞는 응답 메시지 랜덤 선택
    selected_message = random.choice(bot_message)

    # 챗봇 응답을 히스토리에 추가
    chat_history.append({'role': 'assistant', 'content': selected_message})
    
    return jsonify({'message': selected_message})

if __name__ == '__main__':
    app.run(debug=True)
