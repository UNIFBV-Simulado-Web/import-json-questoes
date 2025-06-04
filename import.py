import psycopg2
import json
    
connection = psycopg2.connect(database="postgres", user="postgres", password="docker", host="localhost", port="5432")
cursor = connection.cursor()

with open('C:/Users/diego/Desktop/www/import-json-questoes/questoes.json','r', encoding='utf-8') as json_file:
    file_contents = json_file.read()
    data = json.loads(file_contents)
    count = 1
    print(data[0]['alternatives'][0])
    for item in data:
        
        cursor.execute(
                "INSERT INTO questions (id, title, discipline, language, year, context, correct_alternative) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (count,item['title'], item['discipline'], item['language'], item['year'],item['context'], item['correctAlternative'])
            )

        for alternative in item['alternatives']:
                if(alternative['file']):
                      cursor.execute(
                    "INSERT INTO alternatives (question_id, letter, text, is_correct, image) VALUES (%s, %s, %s, %s, %s)",
                    (count, alternative['letter'], alternative['text'], alternative['isCorrect'],alternative['file'])
                )
        for file in item['files']:
                cursor.execute(
                    "INSERT INTO files (question_id, link) VALUES (%s, %s)",
                    (count, file)
                )
    
        count += 1
        print(f"Inserted question {count} into the database.")
    connection.commit()
    cursor.close()
    connection.close()
