from flask import Flask, request, jsonify, render_template
import ollama

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

    if sentiment == 'positive':
        bot_message = "너무 잘하고 있어요! 계속 힘내세요! 😊"
    elif sentiment == 'negative':
        bot_message = "힘든 일이 있으면 언제든 이야기해 주세요. 함께할게요. 😢"
    else:
        bot_message = "무슨 일이든 잘 해결될 거예요. 당신은 할 수 있어요! ✨"

    # 챗봇 응답을 히스토리에 추가
    chat_history.append({'role': 'assistant', 'content': bot_message})
    
    return jsonify({'message': bot_message})

if __name__ == '__main__':
    app.run(debug=True)
