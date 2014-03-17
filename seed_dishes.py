import model
import csv

def seed_dishes():
    with open('seeds/wikipedia_dishes.txt', 'rb') as f:
        reader = csv.reader(f, delimiter='|')
        for row in reader:
            for i in range(len(row)):
                row[i] = row[i].decode('utf-8')
                row[i] = row[i].strip()

            chin_name = row[0]
            eng_name = row[1].lower()

            print chin_name, eng_name
            dish = model.Dish(chin_name=chin_name, eng_name=eng_name)
            model.session.add(dish)

        try: 
            model.session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            model.session.rollback()

def main():
    seed_dishes()

if __name__ == "__main__":
    main()


