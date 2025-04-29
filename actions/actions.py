from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector
from rasa_sdk.events import SlotSet

# Helper function for MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Kmjd7432@@",
        database="travel_guide"
    )

# Action: Provide information about a city
class ActionProvideCityInfo(Action):
    def name(self) -> Text:
        return "action_provide_city_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = next(tracker.get_latest_entity_values("city"), None)

        if not city:
            dispatcher.utter_message(text="🌍 Which city are you interested in?")
            return []

        try:
            conn = get_mysql_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT city_name, description, best_time FROM city_info WHERE LOWER(city_name) = %s", (city.lower(),))
            result = cursor.fetchone()
            conn.close()

            if result:
                response = (
                    f"🌍 {result['city_name']}\n\n"
                    f"{result['description']}\n\n"
                    f"🕒 Best time to visit: {result['best_time']}"
                )
            else:
                response = f"Sorry, I'm still learning about {city.title()}! 🧭"

        except mysql.connector.Error:
            response = "⚠️ Oops! Couldn't access travel info right now. Please try again later."

        dispatcher.utter_message(text=response)
        return []

# Action: List places to visit in a city
class ActionProvidePlaces(Action):
    def name(self) -> Text:
        return "action_provide_places"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = next(tracker.get_latest_entity_values("city"), None)

        if not city:
            dispatcher.utter_message(text="🌍 Please tell me the city you want to explore.")
            return []

        try:
            conn = get_mysql_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.name
                FROM places_info p
                JOIN city_info c ON p.city_id = c.city_id
                WHERE LOWER(c.city_name) = %s
            """, (city.lower(),))
            results = cursor.fetchall()
            conn.close()

            if results:
                places = ", ".join([row[0] for row in results[:5]])
                dispatcher.utter_message(text=f"🌆 Top places to visit in {city.title()}: {places}")
            else:
                dispatcher.utter_message(text=f"🔎 Couldn't find places for {city.title()}.")

        except mysql.connector.Error:
            dispatcher.utter_message(text="⚠️ Database error! Please try again later.")

        return []

# Action: Generate a trip plan based on user preferences
class ActionGenerateTripPlan(Action):

    def name(self) -> Text:
        return "action_generate_trip_plan"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        duration = tracker.get_slot("duration")
        budget = tracker.get_slot("budget")

        if not city:
            dispatcher.utter_message(text="🏙️ Which city are you planning to visit?")
            return []
        if not duration:
            dispatcher.utter_message(text="🕒 How many days would you like your trip to be?")
            return []
        if not budget:
            dispatcher.utter_message(text="💸 What's your total budget for the trip?")
            return []

        try:
            # Establish database connection
            connection = get_mysql_connection()
            cursor = connection.cursor(dictionary=True)

            # Get city information
            cursor.execute("SELECT city_id, description, best_time FROM city_info WHERE city_name = %s", (city,))
            city_info = cursor.fetchone()

            if not city_info:
                dispatcher.utter_message(text=f"❌ Hmm... I couldn't find {city} in my travel guide. Can you choose another city?")
                return []

            city_id = city_info['city_id']
            description = city_info['description']
            best_time = city_info['best_time']

            # Stay details
            days = int(duration.split()[0])  # assume "2 days"
            budget_per_night = int(budget) / days

            cursor.execute("""
                SELECT name, price_per_night, description 
                FROM stays 
                WHERE city_id = %s
                ORDER BY price_per_night ASC
            """, (city_id,))
            stays = cursor.fetchall()

            recommended_stay = None
            for stay in stays:
                if stay['price_per_night'] <= budget_per_night:
                    recommended_stay = stay
                    break

            # Places to visit
            cursor.execute("""
                SELECT name, description 
                FROM places_info 
                WHERE city_id = %s
            """, (city_id,))
            places = cursor.fetchall()

            # ✨ Build smarter, richer response
            response = f"🌍 *Exciting {days}-Day Trip Plan to {city}* 🌴\n\n"
            response += f"{description}\n\n"
            response += f"🕒 *Ideal Time to Visit:* {best_time}\n\n"

            if recommended_stay:
                total_stay_cost = recommended_stay['price_per_night'] * days
                remaining_budget = int(budget) - total_stay_cost

                response += f"🏨 *Where to Stay:* {recommended_stay['name']}\n"
                response += f"💵 *Price per Night:* {recommended_stay['price_per_night']} LKR\n"
                response += f"🛏️ *Total Stay Cost for {days} nights:* {total_stay_cost} LKR\n"
                response += f"ℹ️ {recommended_stay['description']}\n\n"
                response += f"💰 *Remaining Budget after Stay:* {remaining_budget} LKR\n"
                response += f"🚗 You can use the remaining budget for food, local transport, entry tickets, and fun shopping! 🎉\n\n"
            else:
                response += "🚫 Unfortunately, I couldn't find a stay that fits your budget. You may want to consider increasing it slightly.\n\n"

            if places:
                response += "📍 *Top Places You Must Visit:*\n"
                for idx, place in enumerate(places[:5], start=1):
                    response += f"{idx}. {place['name']} - {place['description']}\n"
            else:
                response += "😔 Sorry, I couldn't find must-visit places for this city.\n"

            response += "\n✨ *Pro Tip:* Keep some cash handy for local food and tuk-tuk rides! 📸🍛"

            dispatcher.utter_message(text=response)

            # Friendly ending
            dispatcher.utter_message(text="Would you like me to plan another adventure? Just tell me where you'd love to go next! 🚀")

            # Reset slots to allow new planning
            return [SlotSet("city", None), SlotSet("duration", None), SlotSet("budget", None)]

        except mysql.connector.Error as error:
            print(f"Database error: {error}")
            dispatcher.utter_message(text="⚠️ Oops, something went wrong with my database. Please try again later.")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        return []