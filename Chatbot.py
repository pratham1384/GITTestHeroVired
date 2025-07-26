import re
import random
import math

class ChatBot:
    def __init__(self):
        self.name = "ChatBot"
        self.responses = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What's on your mind?",
                "Hey! Nice to meet you!",
                "Hello! I'm here to chat and help with calculations."
            ],
            'how_are_you': [
                "I'm doing great, thank you for asking!",
                "I'm functioning perfectly! How are you?",
                "All systems running smoothly! How about you?",
                "I'm here and ready to help!"
            ],
            'goodbye': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! It was nice chatting with you!",
                "Farewell! Come back anytime!"
            ],
            'thanks': [
                "You're welcome!",
                "Happy to help!",
                "No problem at all!",
                "Glad I could assist you!"
            ],
            'default': [
                "That's interesting! Tell me more.",
                "I see. What else would you like to talk about?",
                "Hmm, that's something to think about!",
                "I'm here to listen. What's on your mind?",
                "That's cool! Anything else you'd like to share?"
            ],
            'calculator_help': [
                "I can help you with calculations! Try asking me things like:",
                "- What is 5 + 3?",
                "- Calculate 15 * 7",
                "- What's the square root of 64?",
                "- Find 2 to the power of 8",
                "- What is sin(30)?",
                "Just type 'calc' followed by your expression or ask naturally!"
            ]
        }
        
        self.math_patterns = [
            r'what\s+is\s+(.+)',
            r'calculate\s+(.+)',
            r'solve\s+(.+)',
            r'find\s+(.+)',
            r'calc\s+(.+)',
            r'^(.+\s*[\+\-\*\/\^\%]\s*.+)$'
        ]

    def greet(self):
        print(f"\n🤖 {self.name}: {random.choice(self.responses['greeting'])}")
        print("💡 Tip: I can chat with you and solve math problems!")
        print("📱 Type 'help calc' for calculator instructions or 'quit' to exit.\n")

    def detect_intent(self, user_input):
        user_input = user_input.lower().strip()
        
        # Check for greetings
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return 'greeting'
        
        # Check for how are you
        if any(phrase in user_input for phrase in ['how are you', 'how do you do', 'how are things']):
            return 'how_are_you'
        
        # Check for goodbye
        if any(word in user_input for word in ['bye', 'goodbye', 'see you', 'quit', 'exit']):
            return 'goodbye'
        
        # Check for thanks
        if any(word in user_input for word in ['thank', 'thanks', 'appreciate']):
            return 'thanks'
        
        # Check for calculator help
        if 'help calc' in user_input or 'calculator help' in user_input:
            return 'calculator_help'
        
        # Check for math expressions
        for pattern in self.math_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                return 'math'
        
        return 'default'

    def evaluate_math(self, expression):
        try:
            # Clean the expression
            expression = expression.lower().strip()
            
            # Handle natural language math
            expression = self.process_natural_language_math(expression)
            
            # Replace common math functions
            replacements = {
                'sqrt': 'math.sqrt',
                'sin': 'math.sin',
                'cos': 'math.cos',
                'tan': 'math.tan',
                'log': 'math.log',
                'ln': 'math.log',
                'pi': 'math.pi',
                'e': 'math.e',
                '^': '**',
                'power': '**'
            }
            
            for old, new in replacements.items():
                expression = expression.replace(old, new)
            
            # Handle degrees to radians for trig functions
            if any(func in expression for func in ['math.sin', 'math.cos', 'math.tan']):
                # Convert degrees to radians if it looks like degrees
                expression = re.sub(r'math\.(sin|cos|tan)\((\d+)\)', 
                                  r'math.\1(math.radians(\2))', expression)
            
            # Evaluate the expression
            result = eval(expression, {"math": math, "__builtins__": {}})
            return f"The answer is: {result}"
            
        except Exception as e:
            return f"Sorry, I couldn't calculate that. Please check your expression. Error: {str(e)}"

    def process_natural_language_math(self, text):
        # Handle natural language patterns
        patterns = [
            (r'what\s+is\s+(.+)', r'\1'),
            (r'calculate\s+(.+)', r'\1'),
            (r'solve\s+(.+)', r'\1'),
            (r'find\s+(.+)', r'\1'),
            (r'calc\s+(.+)', r'\1'),
            (r'(\d+)\s+plus\s+(\d+)', r'\1 + \2'),
            (r'(\d+)\s+minus\s+(\d+)', r'\1 - \2'),
            (r'(\d+)\s+times\s+(\d+)', r'\1 * \2'),
            (r'(\d+)\s+divided\s+by\s+(\d+)', r'\1 / \2'),
            (r'(\d+)\s+to\s+the\s+power\s+of\s+(\d+)', r'\1 ** \2'),
            (r'square\s+root\s+of\s+(\d+)', r'sqrt(\1)'),
            (r'(\d+)\s+squared', r'\1 ** 2'),
            (r'(\d+)\s+cubed', r'\1 ** 3'),
        ]
        
        for pattern, replacement in patterns:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text

    def respond(self, user_input):
        intent = self.detect_intent(user_input)
        
        if intent == 'math':
            # Extract math expression
            for pattern in self.math_patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    expression = match.group(1) if match.lastindex else user_input
                    return self.evaluate_math(expression)
        
        elif intent in self.responses:
            return random.choice(self.responses[intent])
        
        return random.choice(self.responses['default'])

    def chat(self):
        self.greet()
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print(f"🤖 {self.name}: {random.choice(self.responses['goodbye'])}")
                    break
                
                response = self.respond(user_input)
                print(f"🤖 {self.name}: {response}\n")
                
            except KeyboardInterrupt:
                print(f"\n🤖 {self.name}: {random.choice(self.responses['goodbye'])}")
                break
            except Exception as e:
                print(f"🤖 {self.name}: Sorry, something went wrong. Let's try again!")

def main():
    print("=" * 50)
    print("🤖 CHATBOT WITH CALCULATOR")
    print("=" * 50)
    
    bot = ChatBot()
    bot.chat()

if __name__ == "__main__":
    main()
