import math
try:
    from flask import Flask, render_template, request, jsonify
except Exception:
    print('Missing dependency: Flask is required to run this app.')
    print('Install it with: python -m pip install flask')
    raise SystemExit(1)

app = Flask(__name__)

class CalculatorLogic:
    """Same calculation logic as your Tkinter app"""
    
    @staticmethod
    def calculate_expression(expression):
        """Evaluate expression with error handling"""
        try:
            # Replace display symbols with Python operators
            expression = expression.replace('×', '*').replace('÷', '/').replace('−', '-')
            
            # Check for empty expression
            if not expression:
                return "0"
            
            # Advanced calculation with math functions
            # Allow basic math operations and common functions
            allowed_names = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'sqrt': math.sqrt,
                'log': math.log10,
                'ln': math.log,
                'pi': math.pi,
                'e': math.e,
                'rad': math.radians,
                'deg': math.degrees,
                'abs': abs,
                'round': round,
                'floor': math.floor,
                'ceil': math.ceil
            }
            
            # Compile and evaluate safely
            code = compile(expression, '<string>', 'eval')
            
            # Check for allowed names
            for name in code.co_names:
                if name not in allowed_names:
                    raise NameError(f"Use of {name} not allowed")
            
            result = eval(code, {"__builtins__": {}}, allowed_names)
            
            # Handle special cases
            if result == float('inf') or result == float('-inf'):
                return "Infinity"
            
            # Format result
            if isinstance(result, float):
                # Remove unnecessary trailing zeros
                result_str = ('%.10f' % result).rstrip('0').rstrip('.')
                if len(result_str) > 15:
                    return str(round(result, 10))
                return result_str
            
            return str(result)
            
        except ZeroDivisionError:
            return "Cannot divide by zero"
        except SyntaxError:
            return "Syntax Error"
        except NameError as e:
            return str(e)
        except Exception:
            return "Error"
    
    @staticmethod
    def percentage(value):
        """Convert to percentage"""
        try:
            num = float(value)
            return str(num / 100)
        except:
            return "Error"
    
    @staticmethod
    def toggle_sign(value):
        """Toggle positive/negative"""
        try:
            if value.startswith('-'):
                return value[1:]
            else:
                return '-' + value
        except:
            return "Error"

# Initialize calculator
calculator = CalculatorLogic()

@app.route('/')
def home():
    """Serve the calculator page"""
    return render_template('calculator.html')

@app.route('/api/calculate', methods=['POST'])
def api_calculate():
    """API endpoint for calculations"""
    data = request.json
    action = data.get('action')
    expression = data.get('expression', '')
    current_value = data.get('current_value', '')
    
    response = {
        'success': True,
        'result': '',
        'display': ''
    }
    
    try:
        if action == 'calculate':
            result = calculator.calculate_expression(expression)
            response['result'] = result
            response['display'] = result
            
        elif action == 'percentage':
            result = calculator.percentage(current_value)
            response['result'] = result
            response['display'] = result
            
        elif action == 'toggle_sign':
            result = calculator.toggle_sign(current_value)
            response['result'] = result
            response['display'] = result
            
        elif action == 'clear':
            response['result'] = '0'
            response['display'] = '0'
            
        else:
            response['success'] = False
            response['result'] = 'Invalid action'
            
    except Exception as e:
        response['success'] = False
        response['result'] = str(e)
    
    return jsonify(response)

@app.route('/api/evaluate', methods=['POST'])
def api_evaluate():
    """Simple evaluation endpoint for direct calculation"""
    data = request.json
    expression = data.get('expression', '')
    
    result = calculator.calculate_expression(expression)
    
    return jsonify({
        'success': True if result not in ['Error', 'Syntax Error', 'Cannot divide by zero'] else False,
        'result': result
    })

if __name__ == '__main__':
    print("🚀 Starting Modern Calculator Web Edition...")
    print("🌐 Open: http://localhost:5000")
    app.run(debug=True)