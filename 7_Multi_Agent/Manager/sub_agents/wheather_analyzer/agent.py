from google.adk.agents import Agent
import random

def today_weekday():
    """
    tell the week day of today in the form of, {sunday, monday, tuesday..}
    """
    
    weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    return  random.choice(weekdays) 

def fill_predictions():
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weather_conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Thunderstorms", "Foggy", "Drizzly"]

    weather_forecast = []

    for day in weekdays:
        temperature_c = round(random.uniform(20.0, 35.0), 1)
        temperature_f = round((temperature_c * 9/5) + 32, 1)
        humidity = random.randint(50, 95)
        wind_speed_kmh = random.randint(5, 30) 
        wind_speed_mph = round(wind_speed_kmh * 0.621371, 1)
        condition = random.choice(weather_conditions)
        
        day_weather = {
            "day": day,
            "temperature": {
                "celsius": temperature_c,
                "fahrenheit": temperature_f
            },
            "humidity": f"{humidity}%",
            "wind_speed": {
                "km/h": wind_speed_kmh,
                "mph": wind_speed_mph
            },
            "condition": condition
        }
        weather_forecast.append(day_weather)
    
    return weather_forecast

def wheather_predict(day:int) -> dict:
    """
    gives the predicted whether about the day of the week based on the input date
    input is an integer and its the index for relevent day
    1 : sunday, 2: monday like 1 based indexing 
    """  
    
    wheather_forcast = fill_predictions()
    
    return wheather_forcast[day-1]
    
    


wheather_analyzer = Agent(
    name="wheather_analyzer",
    model="gemini-2.0-flash",
    description="Whether analyzer",
    instruction="""
    your are whether analyzer and you can tell about the whether prediction up to one week and
    can give any other related information related to whether based on your knowladge.
    
    you have the whether details about a current week only.. so when user asking about monday when its tuesday give the past tuesday and mention about it clearly
    only the predictions are updated week by week.
    
    if today is staurday and user asked for tommorow prediction tell its not availble ok.. this also applicable for every cases user asking for out of range of current week
    
    you can use following tools to:
    wheather_predict : to get the predicted whether withing week, if user asked for whether out of the range simply tell cant give them, 
    input should be the day of the week inthe form 0 for sunday, 1 : monday, 2: like upto 6 : saturday
    
    today_weekday: give the today week day, like sunday, monday..
    
    if user aske anything out of the scope just delegate it back to the manager.
    """,
    tools=[today_weekday, wheather_predict],
)