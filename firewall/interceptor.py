from datetime import datetime
import os

class ActionInterceptor:

    def __init__(self):
        self.log_file = "logs/action.log"

        os.makedirs("logs", exist_ok=True)


    def intercept(self, tool_name, user_intent):

        current_time = datetime.now()

        print("\n==============================")
        print("ACTION INTERCEPTED")
        print("==============================")

        print(f"Time           : {current_time}")
        print(f"Tool Requested : {tool_name}")
        print(f"User Intent    : {user_intent}")

        log_entry = (
            f"{current_time} | "
            f"Tool={tool_name} | "
            f"Intent={user_intent}\n" 
        )

        with open(self.log_file, "a") as file:
            file.write(log_entry)
        
        return True