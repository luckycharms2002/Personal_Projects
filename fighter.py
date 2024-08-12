import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine

NAMES = {"islam-makhachev", "charles-oliveira", "chan-sung-jung", "jose-aldo", "kamaru-usman", "cain-velasquez", "leon-edwards", "jon-jones", "anderson-silva", "conor-mcgregor", "khabib-nurmagomedov"}

# Function to scrape UFC fighter specific stats
def scrape_ufc_fighter_stats(fighter_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(fighter_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extracting the stats
    stats = {}
    
    # Example: Scraping
    try:
        streak = soup.find('p', string='Fight Win Streak').find_previous_sibling('p').text.strip()
    except AttributeError:
        streak = "1"
    
    try:
        dec_wins = None
        for label in soup.find_all('div', class_='c-stat-3bar__label'):
            if label.text.strip() == 'DEC':
                dec_wins = label.find_next_sibling('div', class_='c-stat-3bar__value').text.strip().split(' ')[0]
                break
        if not dec_wins:
            dec_wins = "X"
    except AttributeError:
        dec_wins = "X"    
    
    try:
        sig_strikes_absorbed = None
        for label in soup.find_all('div', class_='c-stat-compare__label'):
            if label.text.strip() == 'Sig. Str. Absorbed':
                sig_strikes_absorbed = label.find_previous_sibling('div', class_='c-stat-compare__number').text.strip().split(' ')[0]
                break
        if not sig_strikes_absorbed:
            sig_strikes_absorbed = "X"
    except AttributeError:
        sig_strikes_absorbed = "X" 

    try:
        KO_wins = soup.find('p', string='Wins by Knockout').find_previous_sibling('p').text.strip()
    except AttributeError:
        KO_wins = "X"
    
    try:
        Sub_Wins = soup.find('p', string='Wins by Submission').find_previous_sibling('p').text.strip()
    except AttributeError:
        Sub_Wins = "X"
    
    try:
        sig_strikes_landed = soup.find('dt', string='Sig. Strikes Landed').find_next('dd').text.strip()
    except AttributeError:
        sig_strikes_landed = "X"
    
    try:
        sig_strikes_attempted = soup.find('dt', string='Sig. Strikes Attempted').find_next('dd').text.strip()
    except AttributeError:
        sig_strikes_attempted = "X"

    try:
        # Scraping Standing strikes
        sig_strikes_stand = None
        for label in soup.find_all('div', class_='c-stat-3bar__label'):
            if label.text.strip() == 'Standing':
                sig_strikes_stand = label.find_next_sibling('div', class_='c-stat-3bar__value').text.strip().split(' ')[0]
                break
        if not sig_strikes_stand:
            sig_strikes_stand = "X"
    except AttributeError:
        sig_strikes_stand = "X"

    try:
        # Scraping Clinch strikes
        sig_strikes_clinch = None
        for label in soup.find_all('div', class_='c-stat-3bar__label'):
            if label.text.strip() == 'Clinch':
                sig_strikes_clinch = label.find_next_sibling('div', class_='c-stat-3bar__value').text.strip().split(' ')[0]
                break
        if not sig_strikes_clinch:
            sig_strikes_clinch = "X"
    except AttributeError:
        sig_strikes_clinch = "X"

    try:
        # Scraping Ground strikes
        sig_strikes_ground = None
        for label in soup.find_all('div', class_='c-stat-3bar__label'):
            if label.text.strip() == 'Ground':
                sig_strikes_ground = label.find_next_sibling('div', class_='c-stat-3bar__value').text.strip().split(' ')[0]
                break
        if not sig_strikes_ground:
            sig_strikes_ground = "X"
    except AttributeError:
        sig_strikes_ground = "X"
    
    try:
        takedowns_landed = soup.find('dt', string='Takedowns Landed').find_next('dd').text.strip()
    except AttributeError:
        takedowns_landed = "X"
    
    try:
        takedowns_attempted = soup.find('dt', string='Takedowns Attempted').find_next('dd').text.strip()
    except AttributeError:
        takedowns_attempted = "X"

    try:
        # Locate the 'Sig. Str. Defense' label
        sig_str_defense_label = soup.find('div', class_='c-stat-compare__label', string='Sig. Str. Defense')
        
        # Navigate to the corresponding number and extract it (before the % sign)
        sig_str_defense_percent = sig_str_defense_label.find_previous('div', class_='c-stat-compare__number').text.strip()
        sig_strikes_defended = sig_str_defense_percent.split('%')[0].strip()
    except AttributeError:
        sig_strikes_defended = "X"

    try:
        # Locate the 'Takedown Defense' label
        takedown_defense_label = soup.find('div', class_='c-stat-compare__label', string='Takedown Defense')
        
        # Navigate to the corresponding number and extract it (before the % sign)
        takedown_defense_percent = takedown_defense_label.find_previous('div', class_='c-stat-compare__number').text.strip()
        takedowns_defended = takedown_defense_percent.split('%')[0].strip()
    except AttributeError:
        takedowns_defended = "X"
    
    stats['Streak'] = streak
    stats['Dec_Wins'] = dec_wins
    stats['KO_Wins'] = KO_wins
    stats['Sub_Wins'] = Sub_Wins
    stats['Sig_Strikes_Landed'] = sig_strikes_landed
    stats['Sig_Strikes_Attempted'] = sig_strikes_attempted
    stats['Sig_Strikes_Absorbed'] = sig_strikes_absorbed
    stats['Sig_Strikes_from_Standing'] = sig_strikes_stand
    stats['Sig_Strikes_from_Clinch'] = sig_strikes_clinch
    stats['Sig_Strikes_from_Ground'] = sig_strikes_ground
    stats['Strike_Defense'] = sig_strikes_defended
    stats['Takedowns_Landed'] = takedowns_landed
    stats['Takedowns_Attempted'] = takedowns_attempted
    stats['Takedown_Defense'] = takedowns_defended

    try:
        fighter_name = soup.find('h1', class_='hero-profile__name').text.strip() 
    except AttributeError:
        fighter_name = "Unknown Fighter"
    try:
        nickname = soup.find('p', class_='hero-profile__nickname').text.strip()
        fighter_name = f"{fighter_name} {nickname}"
    except AttributeError:
        # If nickname is missing, just keep the fighter's name without a nickname
        pass

    stats_df = pd.DataFrame([stats], index=[fighter_name])
    return stats_df

# Function to save the stats to a SQL database
def save_to_sql(df, db_name='ufc_stats.db', table_name='fighter_stats'):
    engine = create_engine(f'sqlite:///{db_name}', echo=False)
    df.to_sql(table_name, con=engine, if_exists='append', index_label='fighter_name')

# Main function to execute the scraping and saving process
def main(fighter_url):
    # Scrape the fighter stats
    stats_df = scrape_ufc_fighter_stats(fighter_url)
    
    # Display the DataFrame
    print(stats_df)
    
    # Save the stats to SQL
    save_to_sql(stats_df, db_name='ufc_stats.db', table_name='fighter_stats')

# Example usage
for name in NAMES:
    fighter_url = 'https://www.ufc.com/athlete/' + name
    main(fighter_url)
