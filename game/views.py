import random
from django.shortcuts import render

def guess_number(request):
    # Inicializa o número a ser adivinhado se ele não existir na sessão
    if 'number_to_guess' not in request.session:
        request.session['number_to_guess'] = random.randint(1, 100)
        request.session['attempts'] = 0  # Número de tentativas
        request.session['hint_used'] = False  # Controla se a dica foi usada

    # Garante que a chave 'hint_used' existe
    request.session.setdefault('hint_used', False)

    number_to_guess = request.session['number_to_guess']
    message = ''
    hint_message = ''

    if request.method == 'POST':
        # Restart
        if 'reset' in request.POST:
            request.session.flush()  # clean 
            return render(request, 'game/guess.html', {'message': 'Game restarted!'})

        # give a hint
        elif 'hint' in request.POST:
            if not request.session['hint_used']:
                if number_to_guess % 2 == 0:
                    hint_message = "Hint: The number is even."
                else:
                    hint_message = "Hint: The number is odd."

                if number_to_guess > 50:
                    hint_message += " Also, the number is above 50."
                else:
                    hint_message += " Also, the number is below or equal to 50."

                request.session['hint_used'] = True  # Marca a dica como usada
            else:
                hint_message = "You have already used your hint!"

        # Lógica de adivinhação (somente se o campo guess estiver no POST)
        elif 'guess' in request.POST and 'guess' in request.POST:
            try:
                guess = int(request.POST['guess'])
                request.session['attempts'] += 1  # Incrementa o número de tentativas

                difference = abs(number_to_guess - guess)  # Calcula a proximidade

                if guess < number_to_guess:
                    message = "Too low! "
                elif guess > number_to_guess:
                    message = "Too high! "
                else:
                    message = f"🎉 Congratulations! You guessed the number in {request.session['attempts']} attempts."
                    request.session.flush()  # Reinicia o jogo após acerto
                    return render(request, 'game/guess.html', {'message': message})

                # Adiciona a lógica de proximidade
                if difference <= 5:
                    message += "You're almost there! 🔥"
                else:
                    message += "You're still far away. ❄️"

            except ValueError:
                message = "Please enter a valid number!"

    return render(request, 'game/guess.html', {
        'message': message,
        'hint_message': hint_message,
    })



  
  


