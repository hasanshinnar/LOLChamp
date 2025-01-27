League of Legends Champion Recommender
----------------------------------------------
This Python project uses Riot Games' API to analyze a player's performance history and recommend champions to play based on their win rates and roles.
Designed for League of Legends enthusiasts, the tool simplifies decision-making by suggesting champions that align with the player's strengths.
----------------------------------------------
# Features : 
1- Match Data Retrieval: Fetch recent match data using the Riot API.
2- Player-Centric Analysis: Focus on a specific player's history to calculate win rates for each champion they've played.
3- Champion Recommendation: Suggest top-performing champions based on win rate and frequency.
4= Customizable: Adaptable for different regions and game modes.
----------------------------------------------
# How It Works:
* Input: Provide your Riot ID, tag, and region.
* Data Processing: The script retrieves recent match data, filters it for the given player, and analyzes performance metrics.
* Output: Displays the top 3 champion recommendations with their respective win rates.
----------------------------------------------
# Tech Stack
* Python: Core programming language.
* Pandas: Data manipulation and analysis.
* Requests: API interaction.
* Riot Games API: Source of match data.
* MS SQL Server: Database for storing and managing match and player data.
----------------------------------------------
# Usage :
* To use this project, you must set up your own MS SQL Server to store match data. Unfortunately, I cannot host the server continuously, so you will need to:
* Install MS SQL Server and configure a database.
* Modify the connection settings in the script to point to your SQL Server instance.
* Ensure the database has the appropriate schema (instructions provided in the repository).
* Clone the repository.
* Install dependencies: pip install -r requirements.txt.
* Add your Riot API key to the script.
* Run the script and input your Riot ID, tag, and region.
----------------------------------------------
# Future Enhancements : 
* Implement role-specific recommendations.
* Add visualizations for performance metrics.
* Support for more advanced analytics (e.g., item builds, team composition).
----------------------------------------------
If you liked my project or have some advice you can chat with me on my LinkedIn: https://www.linkedin.com/in/hasan-shinnar/
