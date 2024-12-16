from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.static import players
import json

def get_player_name(player_id):
    # Use get_players to get player information
    player_info = players.get_players()

    # Iterate through the player information to find the player with the given ID
    for player in player_info:
        if player['id'] == player_id:
            # Extract the player name
            return player['full_name']
    
    # Return None if the player ID is not found
    return None

def get_player_id(player_name):
    player_info = players.find_players_by_full_name(player_name)
    if player_info:
        return player_info[0]['id']
    else:
        return None

def get_player_game_data(player_name, player_id):
    player_database = []
    try:
        # Get the player's game log data
        player_log = playergamelog.PlayerGameLog(player_id=player_id)
        player_log_data = player_log.get_data_frames()[0]

        if not player_log_data.empty:
            # Display game data for the player
            print(f"Game data for {player_name} (Player ID: {player_id}):")
            for _, game_data in player_log_data.iterrows():
                
                curr_game = {}
                
                for category, value in game_data.items():
                    curr_game[category] = value
                    
                curr_game["Player_Name"] = player_name
                curr_game["player_last_ftsy_pts"] = 0
                
                player_database.append(curr_game)
                
                
        else:
            print(f"No game data available for {player_name} (Player ID: {player_id}).")

    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("player game data submitted")
    print("-----------------------------")
    return player_database







def get_active_players():
    # Use commonallplayers endpoint to get information about players in the current season
    players_info = commonallplayers.CommonAllPlayers(is_only_current_season=1).get_data_frames()[0]

    # Get names of players in the current season
    current_season_players_names = players_info['DISPLAY_FIRST_LAST'].tolist()

    return current_season_players_names

if __name__ == "__main__":
    while True:
        try:
            # Example usage
            all_data = []
            player_names = get_active_players()
            for name in player_names:
                player_name_input = name
                player_id_input = get_player_id(player_name_input)
                # Call the function to get game data for the player
                all_data.append(get_player_game_data(player_name_input, player_id_input))
            
            # Specify the file path
            file_path = "player_database.json"
        
            # Save data to JSON file
            with open(file_path, 'w') as json_file:
                json.dump(all_data, json_file, indent=2)
        
            print(f"Data has been saved to {file_path}")
            break  # Exit loop if successful
        
        except Exception as e:
            print(f"Error: {e}. Retrying...")  
