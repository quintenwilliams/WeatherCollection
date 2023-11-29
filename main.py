import sqlite3
import requests

AWC_API_URL = 'https://aviationweather.gov/cgi-bin/data/isigmet.php?format=json'

database_file = 'sigmets.db'

def fetch_sigmets():
  print('Starting "fetch_sigmets".')
  response = requests.get(AWC_API_URL)
  if response.status_code == 200:
    sigmets = response.json()
    return sigmets
  else:
    print(f'Failed to fetch sigmets. Status code: {response.status_code}')
    return None

def create_database():
  print('Starting "create_database".')
  conn = sqlite3.connect(database_file)
  cursor = conn.cursor()

  # Create SIGMETs table if it doesn't exist
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS sigmets (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      isigmetId INTEGER,
      icaoId TEXT,
      firId TEXT,
      firName TEXT,
      receiptTime TEXT,
      validTimeFrom INTEGER,
      validTimeTo INTEGER,
      seriesId TEXT,
      hazard TEXT,
      qualifier TEXT,
      base INTEGER,
      top INTEGER,
      geom TEXT,
      coords TEXT,
      dir TEXT,
      spd INTEGER,
      chng TEXT,
      rawSigmet TEXT
    )
  ''')

  conn.commit()
  conn.close()

def insert_sigmets(sigmets):
  print('Starting "insert_sigmets".')
  conn = sqlite3.connect(database_file)
  cursor = conn.cursor()

  for sigmet in sigmets:
    #print(type(sigmet['coords']))
    cursor.execute('''
    INSERT INTO sigmets (
      isigmetId, icaoId, firId, firName, receiptTime, 
      validTimeFrom, validTimeTo, seriesId, hazard, qualifier, 
      base, top, geom, coords, dir, spd, chng, rawSigmet
    ) VALUES (
      ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''',(
      sigmet['isigmetId'], sigmet['icaoId'], sigmet['firId'], 
      sigmet['firName'], sigmet['receiptTime'], sigmet['validTimeFrom'], 
      sigmet['validTimeTo'], sigmet['seriesId'], sigmet['hazard'], sigmet['qualifier'], 
      sigmet['base'], sigmet['top'], sigmet['geom'], str(sigmet['coords']), sigmet['dir'], 
      sigmet['spd'], sigmet['chng'], sigmet['rawSigmet']
    ))
    #print('test')
    conn.commit()
  conn.close()

def main():
  # Fetch SIGMETs from AWC API
  sigmets_json = fetch_sigmets()

  if sigmets_json:
    # Extract relevant information from the JSON response
    sigmets = []
    for sigmet in sigmets_json:
      sigmets.append({
        'isigmetId': sigmet.get('isigmetId', ''),
        'icaoId': sigmet.get('icaoId'),
        'firId': sigmet.get('firId'),
        'firName': sigmet.get('firName'),
        'receiptTime': sigmet.get('receiptTime'),
        'validTimeFrom': sigmet.get('validTimeFrom'),
        'validTimeTo': sigmet.get('validTimeTo'),
        'seriesId': sigmet.get('seriesId'),
        'hazard': sigmet.get('hazard'),
        'qualifier': sigmet.get('qualifier'),
        'base': sigmet.get('base'),
        'top': sigmet.get('top'),
        'geom': str(sigmet.get('geom')),
        'coords': sigmet.get('coords'),
        'dir': sigmet.get('dir'),
        'spd': sigmet.get('spd'),
        'chng': sigmet.get('chng'),
        'rawSigmet': sigmet.get('rawSigmet')
      })

    create_database()
    insert_sigmets(sigmets)
    #print(sigmets)
    print('SIGMETs successfully fetches and stored in database.')

  '''
  if sigmets_json:
    # Extract relevant information from the JSON response
    sigmets = []
    for sigmet in sigmets_json:
      sigmet = sigmet.get('sigmet', {})
      sigmets.append({
        'isigmetId': sigmet.get('isigmetId', ''),
        'icaoId': sigmet.get('icaoId'),
        'firId': sigmet.get('firId'),
        'firName': sigmet.get('firName'),
        'receiptTime': sigmet.get('receiptTime'),
        'validTimeFrom': sigmet.get('validTimeFrom'),
        'validTimeTo': sigmet.get('validTimeTo'),
        'seriesId': sigmet.get('seriesId'),
        'hazard': sigmet.get('hazard'),
        'qualifier': sigmet.get('qualifier'),
        'base': sigmet.get('base'),
        'top': sigmet.get('top'),
        'geom': sigmet.get('geom'),
        'coords': sigmet.get('coords'),
        'dir': sigmet.get('dir'),
        'spd': sigmet.get('spd'),
        'chng': sigmet.get('chng'),
        'rawSigmet': sigmet.get('rawSigmet')
      })

    create_database()
    insert_sigmets(sigmets)
    #print(sigmets)
    print('SIGMETs successfully fetches and stored in database.')
    '''

if __name__ == '__main__':
  print('Starting main.')
  main()
  print('Finishing main.')
