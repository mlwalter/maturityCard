#'/home/marcelo/MaturityCard/JSON/list_roomsFinal.json'
import pandas as pd
import json

# Caminhos dos arquivos
json_file_path = '/home/marcelo/MaturityCard/JSON/list_roomsFinal.json'
output_excel_path = '/home/marcelo/MaturityCard/JSON/extracao_completa_corrigida.xlsx'

# Ler o arquivo JSON
with open(json_file_path, 'r') as file:
    rooms = json.load(file)

# Função para extrair informações gerais das salas
def extract_general_info(rooms):
    rows = []
    for room in rooms:
        row = {
            "ID": room.get("id"),
            "Name": room.get("name"),
            "Description": room.get("description"),
            "Active": room.get("active"),
            "Token": room.get("token"),
            "Language": room.get("lang"),
            "Owner Email": room.get("owner", {}).get("email"),
            "Start Date": room.get("startDate"),
            "End Date": room.get("endDate"),
            "Expiration Date": room.get("expirationDate"),
            "Company": room.get("company"),
            "Created At": room.get("createdAt"),
            "Game Type": room.get("gameType"),
            "Is Trial": room.get("isTrial")
        }
        rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos estágios das salas
def extract_stage_info(rooms):
    rows = []
    for room in rooms:
        if 'stage' in room:
            stage = room['stage']
            row = {
                "Room ID": room.get("id"),
                "Share Card ID": stage.get("shareCardId"),
                "Round Count": stage.get("roundCount"),
                "Round Stage": stage.get("roundStage"),
                "Suit Current": stage.get("suitCurrent")
            }
            rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos decks das salas
def extract_deck_info(rooms):
    rows = []
    for room in rooms:
        if 'stage' in room and 'deck' in room['stage']:
            for card in room['stage']['deck']:
                row = {
                    "Room ID": room.get("id"),
                    "Card ID": card.get("id"),
                    "Rank": card.get("rank"),
                    "Suit": card.get("suit"),
                    "Score": card.get("score"),
                    "Scenery": card.get("scenery"),
                    "Action": card.get("action"),
                    "Level": card.get("level"),
                    "Level Description": card.get("levelDescription"),
                    "Image": card.get("image"),
                    "Reference": card.get("reference")
                }
                rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos problemCards
def extract_problem_cards_info(rooms):
    rows = []
    for room in rooms:
        if 'stage' in room and 'problemsCards' in room['stage']:
            for card in room['stage']['problemsCards']:
                row = {
                    "Room ID": room.get("id"),
                    "Problem Card ID": card.get("id"),
                    "Card ID": card.get("card", {}).get("id"),
                    "Rank": card.get("card", {}).get("rank"),
                    "Suit": card.get("card", {}).get("suit"),
                    "Score": card.get("card", {}).get("score"),
                    "Scenery": card.get("card", {}).get("scenery"),
                    "Action": card.get("card", {}).get("action"),
                    "Level": card.get("card", {}).get("level"),
                    "Level Description": card.get("card", {}).get("levelDescription"),
                    "Image": card.get("card", {}).get("image"),
                    "Reference": card.get("card", {}).get("reference"),
                    "Owner Email": card.get("owner", {}).get("email"),
                    "Owner Nickname": card.get("owner", {}).get("nickname"),
                    "Owner Role": card.get("owner", {}).get("role"),
                    "Owner Score": card.get("owner", {}).get("score"),
                    "Vote Count": card.get("voteCount"),
                    "Is Unanimous": card.get("isUnanimous"),
                    "Flipped Front": card.get("flippedFront"),
                    "Status": card.get("status")
                }
                rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos votos
def extract_votes_info(rooms):
    rows = []
    for room in rooms:
        if 'stage' in room and 'problemsCards' in room['stage']:
            for card in room['stage']['problemsCards']:
                if 'votes' in card:
                    for vote in card['votes']:
                        row = {
                            "Room ID": room.get("id"),
                            "Problem Card ID": card.get("id"),
                            "Voter Email": vote.get("email"),
                            "Voter Nickname": vote.get("nickname"),
                            "Voter Role": vote.get("role"),
                            "Voter Score": vote.get("score")
                        }
                        rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos notProblemsCards
def extract_not_problem_cards_info(rooms):
    rows = []
    for room in rooms:
        if 'stage' in room and 'notProblemsCards' in room['stage']:
            for card in room['stage']['notProblemsCards']:
                row = {
                    "Room ID": room.get("id"),
                    "Card ID": card.get("id"),
                    "Rank": card.get("rank"),
                    "Suit": card.get("suit"),
                    "Score": card.get("score"),
                    "Scenery": card.get("scenery"),
                    "Action": card.get("action"),
                    "Level": card.get("level"),
                    "Level Description": card.get("levelDescription"),
                    "Image": card.get("image"),
                    "Reference": card.get("reference")
                }
                rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos notApplicableCards
def extract_not_applicable_cards_info(rooms):
    rows = []
    for room in rooms:
        if 'stage' in room and 'notApplicableCards' in room['stage']:
            for card in room['stage']['notApplicableCards']:
                row = {
                    "Room ID": room.get("id"),
                    "Card ID": card.get("id"),
                    "Rank": card.get("rank"),
                    "Suit": card.get("suit"),
                    "Score": card.get("score"),
                    "Scenery": card.get("scenery"),
                    "Action": card.get("action"),
                    "Level": card.get("level"),
                    "Level Description": card.get("levelDescription"),
                    "Image": card.get("image"),
                    "Reference": card.get("reference")
                }
                rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos cardsTable
def extract_cards_table_info(rooms):
    rows = []
    for room in rooms:
        if 'stage' in room and 'cardsTable' in room['stage']:
            for card in room['stage']['cardsTable']:
                row = {
                    "Room ID": room.get("id"),
                    "Card ID": card.get("id"),
                    "Rank": card.get("rank"),
                    "Suit": card.get("suit"),
                    "Score": card.get("score"),
                    "Scenery": card.get("scenery"),
                    "Action": card.get("action"),
                    "Level": card.get("level"),
                    "Level Description": card.get("levelDescription"),
                    "Image": card.get("image"),
                    "Reference": card.get("reference")
                }
                rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos jogadores
def extract_players_info(rooms):
    rows = []
    for room in rooms:
        if 'stage' in room and 'players' in room['stage']:
            for player in room['stage']['players']:
                row = {
                    "Room ID": room.get("id"),
                    "Player Email": player.get("email"),
                    "Player Nickname": player.get("nickname"),
                    "Player Role": player.get("role"),
                    "Player Score": player.get("score"),
                    "Player Connected": player.get("connected"),
                    "Player Card Count": player.get("cardCount"),
                    "Player Has Played": player.get("hasPlayed")
                }
                rows.append(row)
    return pd.DataFrame(rows)

# Função para extrair informações dos decks das salas
def extract_physicalGame(rooms):
    rows = []
    for room in rooms:
        if 'physicalGame' in room and 'cards' in room['physicalGame']:
            for card in room['physicalGame']['cards']:
                row = {
                    "Room ID": room.get("id"),
                    "situation": card.get("situation"),
                    "playerIndex": card.get("playerIndex"),
                    "unanimous": card.get("unanimous"),
                    "suitId": card.get("suitId"),
                    "cardRank": card.get("cardRank")
                    }
                rows.append(row)
    return pd.DataFrame(rows)

def extract_playerPhysicalGame(rooms):
    rows = []
    for room in rooms:
        if 'physicalGame' in room and 'players' in room['physicalGame']:
            for card in room['physicalGame']['players']:
                row = {
                    "Room ID": room.get("id"),
                    "name": card.get("name"),
                    "email": card.get("email"),
                    "score": card.get("score")
                     }
                rows.append(row)
    return pd.DataFrame(rows)


# Extrair as informações gerais, dos estágios, dos decks, dos problemCards, dos votos, dos notProblemsCards, dos notApplicableCards, dos cardsTable e dos jogadores
general_info_df = extract_general_info(rooms)
stage_info_df = extract_stage_info(rooms)
deck_info_df = extract_deck_info(rooms)
problem_cards_df = extract_problem_cards_info(rooms)
votes_df = extract_votes_info(rooms)
not_problem_cards_df = extract_not_problem_cards_info(rooms)
not_applicable_cards_df = extract_not_applicable_cards_info(rooms)
cards_table_df = extract_cards_table_info(rooms)
players_df = extract_players_info(rooms)
physicalGame_df = extract_physicalGame(rooms)
playerPhysicalGame_df = extract_playerPhysicalGame(rooms)


# Salvar os DataFrames em um arquivo Excel com múltiplas abas
with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
    general_info_df.to_excel(writer, sheet_name='General Info', index=False)
    stage_info_df.to_excel(writer, sheet_name='Stage Info', index=False)
    deck_info_df.to_excel(writer, sheet_name='Deck Info', index=False)
    problem_cards_df.to_excel(writer, sheet_name='Problem Cards', index=False)
    votes_df.to_excel(writer, sheet_name='Votes', index=False)
    not_problem_cards_df.to_excel(writer, sheet_name='Not Problem Cards', index=False)
    not_applicable_cards_df.to_excel(writer, sheet_name='Not Applicable Cards', index=False)
    cards_table_df.to_excel(writer, sheet_name='Cards Table', index=False)
    players_df.to_excel(writer, sheet_name='Players', index=False)
    physicalGame_df.to_excel(writer, sheet_name='Physical Game', index=False)
    playerPhysicalGame_df.to_excel(writer, sheet_name='Player Physical Game', index=False)


