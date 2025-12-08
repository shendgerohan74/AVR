import json
from django.http import JsonResponse
from django.shortcuts import render


def voice_api(request):
    data = json.loads(request.body)
    user_message = data.get("message", "")

    # Generate AI response
    ai_reply = generate_ai_reply(user_message)

    return JsonResponse({"reply": ai_reply})


def generate_ai_reply(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant."},
                {"role": "user", "content": user_message},
            ]
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        return f"Error: {str(e)}"


from django.shortcuts import render

def voice_chat_page(request):
    return render(request, "voice_chat.html")
