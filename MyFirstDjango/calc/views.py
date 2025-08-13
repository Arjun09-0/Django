from django.shortcuts import render
from datetime import datetime
from collections import Counter

# Home view remains the same
def home(request):
    return render(request, 'home.html')

# Updated to save calculations in the session
def calculate(request):
    try:
        val1 = float(request.POST['num1'])
        val2 = float(request.POST['num2'])
        operation = request.POST.get('operation')

        result = 0
        op_symbol = ''

        if operation == 'add':
            result = val1 + val2
            op_symbol = '+'
        elif operation == 'subtract':
            result = val1 - val2
            op_symbol = '−'
        elif operation == 'multiply':
            result = val1 * val2
            op_symbol = '×'
        elif operation == 'divide':
            if val2 == 0:
                return render(request, 'result.html', {'error': 'Error: Cannot divide by zero.'})
            result = val1 / val2
            op_symbol = '÷'

        # Get existing history from session, or create an empty list
        history = request.session.get('history', [])

        # Add the new calculation to the history list
        history.insert(0, {
            'num1': val1,
            'num2': val2,
            'op_symbol': op_symbol,
            'operation': operation,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        # Save the updated history back to the session
        request.session['history'] = history

        context = {
            'val1': val1,
            'val2': val2,
            'op_symbol': op_symbol,
            'result': result
        }
        return render(request, 'result.html', context)

    except (ValueError, KeyError):
        return render(request, 'result.html', {'error': 'Invalid input. Please enter both numbers.'})

# Updated to read data from the session
def dashboard(request):
    # Get history from session, or an empty list if none exists
    history = request.session.get('history', [])
    
    # Calculate stats from the history list
    total_calculations = len(history)
    op_counts = Counter(item['operation'] for item in history)

    context = {
        'history': history,
        'total_calculations': total_calculations,
        'operation_counts': op_counts.items(),
    }
    return render(request, 'dashboard.html', context)