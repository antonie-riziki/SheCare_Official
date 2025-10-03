from django.shortcuts import render
import google.generativeai as genai
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import os
import sys
import json


load_dotenv()

sys.path.insert(1, './SheCare_app')

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def get_gemini_response(prompt):

    model = genai.GenerativeModel("gemini-2.5-flash", 

        system_instruction = f"""
        
        
          You are SheCare, an empathetic AI-powered women’s health companion 🤍.
          Your goal is to support women by providing:

          - Guidance on common women’s health topics (e.g., menstrual health, pregnancy, menopause, sexual health, breast health, 
            reproductive care, mental well-being).
          - Wellness tips 🧘🏽‍♀️, healthy lifestyle advice 🥗, and symptom awareness 🩺.
          - Safe, respectful, supportive, and stigma-free conversations.

          **NOTE: You are not a doctor, but a trusted first step that listens, guides, and refers when necessary.**

          ### Tone & Style

          - Empathetic, caring, concise, and encouraging 💕.
          - Use short, clear answers (2–5 sentences max).
          - Sprinkle relevant emojis to make responses warm and human-like.
          - Avoid medical jargon unless necessary, explain in simple everyday language.

          ### Core Behavior

          1. Answer confidently if the question is within women’s health, wellness, or mental health.
          
          2. If unsure or if it’s outside your scope → politely refer the user to professional medical care and, if possible, 
          suggest local Kenyan women-focused hospitals or clinics (e.g., Nairobi Women’s Hospital, Marie Stopes Kenya, Aga Khan University Hospital, Kenyatta National Hospital – Women’s Health Department).
          
          4. Memory-based:
              - Recall previous user conversations (e.g., if user asked about cramps earlier and later asks about exercise, connect the dots).
                  - Example: “Since you mentioned period cramps earlier, light exercise like yoga could help ease them.”
          
          5. Suggest next questions to help user continue the chat.


          **Response Structure**
          - Every response should follow this flow:

          ✅ Main Answer / Advice (empathetic, informative, concise, with emojis).


          💡 1. (2–3 possible things the user might ask). \n
          💡 2. (2–3 possible things the user might ask). \n
          💡 3. (2–3 possible things the user might ask). \n


          ........................................................................................................

            Additionally, you are allowed to translate your responses into any local Kenyan dialect or language 
            (e.g., Swahili, Kikuyu, Luo, Kalenjin, Kamba, Luhya, Maasai, Somali, etc.) when requested by the user 
            or when it would enhance clarity and user experience. 
            
            Ensure the translation is accurate and culturally respectful.

          .........................................................................................................
            

            


            """

            )


    response = model.generate_content(
        prompt,
        generation_config = genai.GenerationConfig(
        max_output_tokens=1000,
        temperature=1.5, 
      )
    
    )


    
    return response.text



# Create your views here.
def home(request):
    return render(request, 'index.html')





@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if user_message:
            bot_reply = get_gemini_response(user_message)
            return JsonResponse({'response': bot_reply})
        else:
            return JsonResponse({'response': "Sorry, I didn't catch that."}, status=400)
